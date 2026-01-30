"""
Exportador de casos de prueba a formato JSON.
"""
import json
import os
from ..domain.models import TestSuite
from ..domain.exporters import ITestExporter


class JsonTestExporter(ITestExporter):
    """Exporta casos de prueba a formato JSON estructurado."""
    
    def export(self, test_suite: TestSuite, output_path: str) -> str:
        """Exporta la suite de casos de prueba a JSON."""
        # Asegurar que el directorio existe
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Convertir a diccionario
        suite_dict = test_suite.to_dict()
        
        # Guardar como JSON
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(suite_dict, f, indent=2, ensure_ascii=False)
        
        return output_path
    
    def get_format_name(self) -> str:
        return "JSON"
