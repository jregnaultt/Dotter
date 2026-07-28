import io
import os
from typing import List, Tuple
from PIL import Image, ImageChops
from app.models.sprite import SpriteState, GeneratedFrameInfo

class SpriteProcessor:
    """
    Procesador visual de Sprites:
    - Remoción de fondos y transparencia RGBA.
    - Recorte automático de bounding box a dimensiones variables.
    - Generación de tira/hoja vertical PNG (`vertical_spritesheet.png`).
    - Almacenamiento organizado en carpetas por personaje y estado.
    """

    @staticmethod
    def process_and_save_frame(
        raw_bytes: bytes,
        output_dir: str,
        character_name: str,
        state: SpriteState
    ) -> GeneratedFrameInfo:
        # Cargar imagen con PIL
        img = Image.open(io.BytesIO(raw_bytes)).convert("RGBA")
        
        # Garantizar canal alfa (transparencia) si el fondo es blanco
        datas = img.getdata()
        new_data = []
        for item in datas:
            # Si el píxel es blanco o casi blanco, hacerlo transparente
            if item[0] > 240 and item[1] > 240 and item[2] > 240:
                new_data.append((255, 255, 255, 0))
            else:
                new_data.append(item)
        img.putdata(new_data)
        
        # Recorte adaptativo (bounding box) para dimensiones variables
        bbox = img.getbbox()
        if bbox:
            # Añadir pequeño padding de 10px alrededor del sprite
            pad = 10
            left = max(0, bbox[0] - pad)
            top = max(0, bbox[1] - pad)
            right = min(img.width, bbox[2] + pad)
            bottom = min(img.height, bbox[3] + pad)
            img_cropped = img.crop((left, top, right, bottom))
        else:
            img_cropped = img
            
        # Crear estructura de carpeta de salida
        state_folder = os.path.join(output_dir, character_name, state.value)
        os.makedirs(state_folder, exist_ok=True)
        
        file_name = f"{character_name}_{state.value}.png"
        full_path = os.path.join(state_folder, file_name)
        img_cropped.save(full_path, "PNG")
        
        return GeneratedFrameInfo(
            state=state,
            file_name=file_name,
            file_path=full_path,
            width=img_cropped.width,
            height=img_cropped.height
        )

    @staticmethod
    def create_vertical_spritesheet(
        frames: List[GeneratedFrameInfo],
        output_dir: str,
        character_name: str
    ) -> str:
        """
        Ensambla todos los PNGs generados en una única hoja vertical (vertical strip)
        con dimensiones adaptativas según el ancho máximo y alto acumulado.
        """
        if not frames:
            return ""
            
        images = []
        max_width = 0
        total_height = 0
        spacing = 20 # Espaciado vertical entre sprites
        
        for frame in frames:
            img = Image.open(frame.file_path).convert("RGBA")
            images.append(img)
            if img.width > max_width:
                max_width = img.width
            total_height += img.height + spacing

        # Crear canvas transparente vertical
        sheet = Image.new("RGBA", (max_width, total_height), (0, 0, 0, 0))
        
        current_y = 0
        for img in images:
            # Centrar horizontalmente cada sprite de dimensión variable
            offset_x = (max_width - img.width) // 2
            sheet.paste(img, (offset_x, current_y), img)
            current_y += img.height + spacing

        character_dir = os.path.join(output_dir, character_name)
        sheet_path = os.path.join(character_dir, f"{character_name}_vertical_spritesheet.png")
        sheet.save(sheet_path, "PNG")
        return sheet_path
