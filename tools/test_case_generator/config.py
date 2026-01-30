"""
Configuración del generador de casos de prueba.
"""
import os

# Rutas de salida
OUTPUT_DIR = os.path.join(os.getcwd(), "output", "test_case_generator")
DEFAULT_JSON_OUTPUT = os.path.join(OUTPUT_DIR, "test-cases.json")
DEFAULT_README_OUTPUT = os.path.join(OUTPUT_DIR, "TEST-CASES-README.md")

# Configuración por defecto
DEFAULT_TECHNIQUES = None  # None = todas las técnicas
DEFAULT_INCLUDE_POSITIVE = True
DEFAULT_INCLUDE_NEGATIVE = True
