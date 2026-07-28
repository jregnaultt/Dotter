from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

class SpriteState(str, Enum):
    IDLE = "idle"
    PUNCH = "punch"
    KICK = "kick"
    DAMAGE = "damage"
    PROJECTILE = "projectile"
    CHARACTER_SELECT = "character_select"
    MEGA_EVOLUTION_1 = "mega_evolution_1"
    MEGA_EVOLUTION_2 = "mega_evolution_2"
    FATALITY = "fatality"

class SpriteDimension(BaseModel):
    width: int = Field(default=256, description="Ancho base del sprite en px")
    height: int = Field(default=384, description="Alto base del sprite en px")

class SpriteGenerationRequest(BaseModel):
    character_name: str = Field(..., example="Geyser")
    description: str = Field(
        default="Luchador de artes marciales en traje con corbata roja y anteojos",
        description="Descripción detallada del personaje"
    )
    style_preference: Optional[str] = Field(
        default="16-bit arcade pixel art 90s style",
        description="Estilo artístico (Ej: The Legend of Zelda Ocarina of Time, Anime 90s, Pixel Art)"
    )
    states: Optional[List[SpriteState]] = Field(
        default=[
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
    )
    dimensions: SpriteDimension = Field(default_factory=SpriteDimension)
    pollinations_model: str = Field(default="flux")
    api_key: Optional[str] = Field(default=None)

class RegenerateFrameRequest(BaseModel):
    character_name: str
    description: Optional[str] = "Luchador en traje"
    state: SpriteState
    custom_instruction: str = Field(..., example="Hacer patada voladora extendida con la pierna completamente horizontal hacia el frente")
    style_preference: Optional[str] = "16-bit arcade pixel art"
    pollinations_model: Optional[str] = "flux"
    groq_api_key: Optional[str] = None

class GeneratedFrameInfo(BaseModel):
    state: SpriteState
    file_name: str
    file_path: str
    width: int
    height: int

class SpriteGenerationResponse(BaseModel):
    character_name: str
    total_generated: int
    output_folder: str
    vertical_sheet_path: Optional[str] = None
    frames: List[GeneratedFrameInfo]

class RegenerateFrameResponse(BaseModel):
    character_name: str
    updated_frame: GeneratedFrameInfo
    vertical_sheet_path: str
