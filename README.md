# Dotter
Generador de Sprite

Dotter es el motor principal y backend encargado de la generación y procesamiento automático de sprites, diseñado especialmente para videojuegos (incluyendo juegos de pelea). 

Esta aplicación expone una API REST construida con FastAPI, integra servicios de Inteligencia Artificial mediante Groq y cuenta con módulos de procesamiento gráfico e imágenes.



# Tecnologías y Librerías

- Lenguaje: Python 3.x
- Framework Web: [FastAPI](https://fastapi.tiangolo.com/) / Uvicorn.
- Procesamiento de Inteligencia Artificial: API de Groq (`groq_service.py`).
- Procesamiento de Imágenes: Módulos internos (`sprite_processor.py`, `image_generator.py`).
- Testing: `pytest`.

# Requisitos e Instalación
1. Clonar e ingresar al directorio
Bash
cd Dotter-main
2. Crear y activar un entorno virtual
Bash

 En Linux/macOS:
python3 -m venv venv
source venv/bin/activate

 En Windows:
python -m venv venv
venv\Scripts\activate

3. Instalar dependencias
Bash
pip install -r requirements.txt

5. Configurar variables de entorno
Crea un archivo .env basándote en la plantilla .env.example y asigna las llaves/API Keys necesarias (como la clave de Groq)[cite: 2]:

Bash
cp .env.example .env

# Ejecución de la API
Para levantar el servidor de desarrollo local con recarga automática:

Bash
      uvicorn app.main:app --reload
      
Una vez en marcha:

  API URL: http://127.0.0.1:8000

  Documentación interactiva Swagger/OpenAPI: http://127.0.0.1:8000/docs

  Documentación alternativa Redoc: http://127.0.0.1:8000/redoc

# Pruebas Unitarias
Para ejecutar el conjunto de pruebas del procesador y los servicios[cite: 2]:

Bash
pytest

# Licencia
Este proyecto se distribuye bajo los términos especificados en el archivo LICENSE

# Estructura del Proyecto

```text
Dotter-main/
├── app/
│   ├── core/
│   │   └── config.py              # Variables de entorno y configuración central[cite: 2]
│   ├── models/
│   │   └── sprite.py              # Esquemas de datos y modelos (Pydantic)[cite: 2]
│   ├── processors/
│   │   └── sprite_processor.py    # Algoritmos de tratamiento y procesamiento de sprites[cite: 2]
│   ├── services/
│   │   ├── groq_service.py        # Conector para la API de Groq[cite: 2]
│   │   └── image_generator.py     # Lógica de generación e intervención de imágenes[cite: 2]
│   └── main.py                    # Punto de entrada de la API FastAPI[cite: 2]
├── tests/
│   └── test_sprites.py            # Suite de pruebas unitarias[cite: 2]
├── .env.example                   # Plantilla para variables de entorno[cite: 2]
├── fighting-game-sprite-generator.md # Documentación adicional y prompts de referencia[cite: 2]
├── requirements.txt               # Dependencias de Python[cite: 2]
├── .gitignore
└── LICENSE
