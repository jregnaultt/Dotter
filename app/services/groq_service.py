import os
import requests
from typing import Optional, Dict
from app.models.sprite import SpriteState

class GroqPromptService:
    """
    Servicio de Ingeniería de Prompts Razonado con Groq AI.
    Soporta análisis de imagen de usuario, estilos personalizados (Ej: Zelda Ocarina of Time, 16-bit Arcade)
    y retroalimentación de usuario para reintentar/ajustar poses específicas.
    """

    GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

    ACTION_BASE_PROMPTS: Dict[SpriteState, str] = {
        SpriteState.IDLE: "standing idle combat stance facing front, ready position",
        SpriteState.PUNCH: "extending right fist punch forward in dynamic side view fighting stance",
        SpriteState.KICK: "high flying side kick extending leg completely horizontal into the air",
        SpriteState.DAMAGE: "staggered backwards taking hit recoil, body flinching",
        SpriteState.PROJECTILE: "thrusting both hands forward, launching glowing energy fireball blast",
        SpriteState.CHARACTER_SELECT: "portrait presentation stance facing front, confident arms folded pose",
        SpriteState.MEGA_EVOLUTION_1: "mega evolution stage 1, glowing cyan aura surge surrounding body",
        SpriteState.MEGA_EVOLUTION_2: "ultimate mega evolution stage 2, futuristic glowing armor suit, explosive aura",
        SpriteState.FATALITY: "finishing move fatality pose, arm raised summoning giant energy beam from sky"
    }

    @classmethod
    def analyze_character_and_style(
        cls,
        character_desc: str,
        style_preference: Optional[str] = None,
        groq_api_key: Optional[str] = None
    ) -> str:
        """
        Llama a la API de Groq para analizar la descripción del personaje y enriquecer el prompt con el estilo solicitado.
        """
        api_key = groq_api_key or os.getenv("GROQ_API_KEY", "")
        style_text = style_preference if style_preference else "16-bit arcade pixel art 90s fighting game style"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a world-class prompt engineer for game asset generation. Produce a short, highly descriptive image generation prompt in English."
                },
                {
                    "role": "user",
                    "content": f"Character details: {character_desc}. Art style: {style_text}. Create a concise prompt description."
                }
            ],
            "max_tokens": 150
        }
        
        try:
            resp = requests.post(cls.GROQ_API_URL, headers=headers, json=payload, timeout=6)
            if resp.status_code == 200:
                content = resp.json()["choices"][0]["message"]["content"].strip()
                return content
        except Exception:
            pass
            
        return f"{character_desc}, style: {style_text}"

    @classmethod
    def get_prompt_for_state(
        cls,
        character_desc: str,
        state: SpriteState,
        style_preference: Optional[str] = None,
        custom_instruction: Optional[str] = None,
        groq_api_key: Optional[str] = None
    ) -> str:
        """
        Genera el prompt final optimizado para un estado específico, integrando
        instrucciones de corrección del usuario (ej: 'Hacer patada voladora extendida').
        """
        base_style = style_preference if style_preference else "16-bit arcade pixel art 90s fighting game style"
        action_pose = cls.ACTION_BASE_PROMPTS.get(state, "combat action pose")
        
        # Si el usuario pasó una corrección específica para este sprite
        if custom_instruction:
            action_pose = f"{action_pose}, custom tweak instruction: {custom_instruction}"
            
        parsed_char = cls.analyze_character_and_style(character_desc, base_style, groq_api_key)
        
        return f"{parsed_char}, pose action: {action_pose}, full body view, transparent white background"
