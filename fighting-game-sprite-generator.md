# Generador Modular de Sprites para Juego de Pelea

## Goal
Desarrollar una aplicación modular en Python con FastAPI y principios de Clean Code para estructurar, procesar y generar la hoja/archivos de sprites en PNG de un personaje de juego de pelea (idle, punch, kick, damage, projectile, character select, megaevoluciones y fatality) organizados verticalmente con dimensiones variables en carpetas.

## Groq AI Model Selection & Guidance
- **Visión (`Qwen 3.6 27B`)**: Ideal para analizar la imagen de referencia subida (`uploaded_media_1.png` - portrait/character pose) y extraer atributos visuales (estilo pixel art, vestimenta, colores de aura).
- **Texto y Razonamiento (`Llama 3.3 70B` / `GPT OSS 120B`)**: Excelentes para estructurar los prompts detallados de cada animación, generar esquemas JSON de los frames y manejar la lógica de estado del personaje.
- **Nota de Generación de Imagen**: Groq provee inferencia ultra rápida para LLMs/STT/Vision. Para la generación final de PNGs, FastAPI coordinará el procesamiento local de imágenes (usando **Pillow/PIL** para composición, recortado y layout vertical con dimensiones variables) y/o consumo de APIs externas de difusión (p. ej., Fal.ai / Replicate / FLUX) impulsadas por los prompts refinados con Groq.

## Applied Python & Architecture Skills
1. **`fastapi-pro` & `pydantic-models-py`**: Diseño de la API RESTful modular, inyección de dependencias, rutas asíncronas y validación de contratos con Pydantic v2.
2. **`python-pro` & `clean-code`**: Principios SOLID, Tipado estricto (`typing`), Factory Pattern para generadores, Dataclasses y modularidad limpia sin acoplamiento.
3. **`api-patterns`**: Manejo de errores estandarizado, estructura de respuesta limpia y arquitectura en capas (Routers -> Services -> Processors/Generators -> Storage).

## Tasks
- [ ] Task 1: Configurar la estructura de proyecto modular FastAPI (`app/core`, `app/models`, `app/services`, `app/processors`, `app/api`) y dependencias (`fastapi`, `uvicorn`, `pillow`, `pydantic`). → Verify: Executing `python3 -m app.main` or `pytest` initializes the server without import errors.
- [ ] Task 2: Definir esquemas Pydantic para el personaje, estados de sprites (`IDLE`, `PUNCH`, `KICK`, `DAMAGE`, `PROJECTILE`, `CHARACTER_SELECT`, `MEGA_EVOLUTION_1`, `MEGA_EVOLUTION_2`, `FATALITY`) y especificaciones de dimensiones variables/verticales. → Verify: Unit test validates Pydantic model serialization and state enum validation.
- [ ] Task 3: Implementar el motor de procesamiento visual/sprites (`SpriteProcessorService`) usando Pillow/PIL para la generación, recorte, formateo e hibridación vertical de imágenes PNG con dimensiones adaptativas. → Verify: Script processes sample images and generates vertical PNG strips with proper metadata in target folders.
- [ ] Task 4: Crear el servicio de IA de prompts y metadatos con el modelo Groq (`Qwen 3.6 27B` vision / `Llama 3.3 70B` text) para parametrizar efectos (auras, transformaciones mega, ejecuciones fatality). → Verify: Calling the prompt service returns structured frame prompt lists for all 9 required states.
- [ ] Task 5: Desarrollar los endpoints FastAPI (`POST /api/v1/sprites/generate`, `GET /api/v1/sprites/{character_id}`) inyectando los servicios de generación y exportación a carpetas. → Verify: `curl -X POST http://localhost:8000/api/v1/sprites/generate` successfully outputs PNG files into `/output_sprites/{character}/`.
- [ ] Task 6: Crear suite de pruebas de integración (`pytest`) verificando la creación de los 9 tipos de sprites, ordenamiento vertical y estructura de archivos PNG resultante. → Verify: Running `pytest` passes 100% of tests.

## Done When
- [ ] El API FastAPI está funcionando con arquitectura modular y Clean Code.
- [ ] Se generan y exportan los archivos PNG de todos los estados solicitados (Idle, Punch, Kick, Hit/Damage, Projectile, Character Select, Megaevolución 1 & 2, y Fatality).
- [ ] Los sprites se organizan verticalmente con dimensiones variables dentro de las carpetas de salida.
- [ ] Las skills de Python utilizadas están explicadas y documentadas en el proyecto.
