"""
Configuración de la herramienta Swagger Analyzer
Define parámetros y rutas específicas de la herramienta
"""
from pathlib import Path

# Configuración de la herramienta
TOOL_NAME = "swagger_analyzer"
TOOL_DESCRIPTION = "Analizador completo de contratos Swagger/OpenAPI"

# Directorios
BASE_DIR = Path(__file__).parent.parent.parent
OUTPUT_DIR = BASE_DIR / "output" / TOOL_NAME

# Nombres de archivos de salida
JSON_OUTPUT_FILENAME = "swagger-analysis.json"
README_OUTPUT_FILENAME = "API-README.md"

# Configuración de fetch
DEFAULT_TIMEOUT = 30
DEFAULT_VERIFY_SSL = True
