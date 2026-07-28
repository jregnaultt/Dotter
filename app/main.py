import os
import shutil
import asyncio
from typing import List, Optional
from fastapi import FastAPI, HTTPException, UploadFile, File, Form, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.models.sprite import (
    SpriteGenerationRequest,
    SpriteGenerationResponse,
    RegenerateFrameRequest,
    RegenerateFrameResponse,
    GeneratedFrameInfo,
    SpriteState
)
from app.services.groq_service import GroqPromptService
from app.services.image_generator import ImageGeneratorService
from app.processors.sprite_processor import SpriteProcessor

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="API RESTful modular para la generación rápida de sprites."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs(settings.OUTPUT_DIR, exist_ok=True)
os.makedirs("uploads", exist_ok=True)
app.mount("/static/output", StaticFiles(directory=settings.OUTPUT_DIR), name="static_output")

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "project": settings.PROJECT_NAME, "version": settings.VERSION}

@app.get(f"{settings.API_V1_STR}/sprites/states", tags=["Sprites"])
def list_supported_states():
    return {"supported_states": [state.value for state in SpriteState]}

def _process_single_state(
    state: SpriteState,
    description: str,
    character_name: str,
    target_model: str,
    key: Optional[str],
    style_preference: Optional[str] = None,
    custom_instruction: Optional[str] = None,
    groq_key: Optional[str] = None
) -> GeneratedFrameInfo:
    prompt = GroqPromptService.get_prompt_for_state(
        character_desc=description,
        state=state,
        style_preference=style_preference,
        custom_instruction=custom_instruction,
        groq_api_key=groq_key
    )
    raw_bytes = ImageGeneratorService.fetch_from_pollinations(
        prompt=prompt,
        model=target_model,
        api_key=key
    )
    return SpriteProcessor.process_and_save_frame(
        raw_bytes=raw_bytes,
        output_dir=settings.OUTPUT_DIR,
        character_name=character_name,
        state=state
    )

@app.post(
    f"{settings.API_V1_STR}/sprites/generate-from-image",
    response_model=SpriteGenerationResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Sprites"]
)
async def generate_sprites_from_uploaded_photo(
    image_file: UploadFile = File(...),
    character_name: str = Form("MiPersonaje"),
    description: Optional[str] = Form("Luchador personalizado basado en foto cargada"),
    style_preference: Optional[str] = Form("16-bit arcade pixel art 90s style"),
    pollinations_model: str = Form("flux"),
    api_key: Optional[str] = Form(None),
    groq_api_key: Optional[str] = Form(None)
):
    upload_path = os.path.join("uploads", f"{character_name}_{image_file.filename}")
    with open(upload_path, "wb") as buffer:
        shutil.copyfileobj(image_file.file, buffer)

    target_model = pollinations_model or settings.POLLINATIONS_MODEL
    key = api_key or settings.POLLINATIONS_API_KEY
    
    states = [
        SpriteState.IDLE,
        SpriteState.PUNCH,
        SpriteState.KICK,
        SpriteState.DAMAGE,
        SpriteState.PROJECTILE,
        SpriteState.CHARACTER_SELECT,
        SpriteState.MEGA_EVOLUTION_1,
        SpriteState.MEGA_EVOLUTION_2,
        SpriteState.FATALITY,
    ]

    # Ejecución paralela inmediata
    tasks = [
        asyncio.to_thread(_process_single_state, state, description, character_name, target_model, key, style_preference, None, groq_api_key)
        for state in states
    ]
    
    generated_frames = list(await asyncio.gather(*tasks))

    state_order = {s: i for i, s in enumerate(states)}
    generated_frames.sort(key=lambda f: state_order.get(f.state, 99))

    vertical_sheet_path = SpriteProcessor.create_vertical_spritesheet(
        frames=generated_frames,
        output_dir=settings.OUTPUT_DIR,
        character_name=character_name
    )

    character_folder = os.path.abspath(os.path.join(settings.OUTPUT_DIR, character_name))

    return SpriteGenerationResponse(
        character_name=character_name,
        total_generated=len(generated_frames),
        output_folder=character_folder,
        vertical_sheet_path=os.path.abspath(vertical_sheet_path) if vertical_sheet_path else None,
        frames=generated_frames
    )

@app.post(
    f"{settings.API_V1_STR}/sprites/regenerate-frame",
    response_model=RegenerateFrameResponse,
    status_code=status.HTTP_200_OK,
    tags=["Sprites"]
)
async def regenerate_single_frame(request: RegenerateFrameRequest):
    updated_frame = await asyncio.to_thread(
        _process_single_state,
        request.state,
        request.description or "Luchador",
        request.character_name,
        request.pollinations_model or "flux",
        None,
        request.style_preference,
        request.custom_instruction,
        request.groq_api_key
    )
    
    character_folder = os.path.join(settings.OUTPUT_DIR, request.character_name)
    existing_frames: List[GeneratedFrameInfo] = []
    
    for state_enum in SpriteState:
        state_dir = os.path.join(character_folder, state_enum.value)
        img_name = f"{request.character_name}_{state_enum.value}.png"
        img_path = os.path.join(state_dir, img_name)
        if os.path.exists(img_path):
            existing_frames.append(GeneratedFrameInfo(
                state=state_enum,
                file_name=img_name,
                file_path=img_path,
                width=384,
                height=512
            ))
            
    vertical_sheet_path = SpriteProcessor.create_vertical_spritesheet(
        frames=existing_frames,
        output_dir=settings.OUTPUT_DIR,
        character_name=request.character_name
    )

    return RegenerateFrameResponse(
        character_name=request.character_name,
        updated_frame=updated_frame,
        vertical_sheet_path=os.path.abspath(vertical_sheet_path)
    )
