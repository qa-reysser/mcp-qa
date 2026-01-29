"""
Implementaciones de infraestructura - Parser de contratos
Responsable de parsear contenido YAML/JSON
"""
import json
import yaml
from typing import Dict, Any
from src.domain.interfaces import IContractParser


class YamlJsonContractParser(IContractParser):
    """Parser que soporta tanto YAML como JSON"""
    
    def parse(self, content: str) -> Dict[str, Any]:
        """
        Parsea el contenido del contrato a un diccionario
        Intenta primero JSON, luego YAML
        
        Args:
            content: Contenido del contrato en formato YAML o JSON
            
        Returns:
            Diccionario con la estructura del contrato
            
        Raises:
            ValueError: Si el contenido no es válido o está vacío
            Exception: Si no se puede parsear como JSON ni YAML
        """
        if not content or not isinstance(content, str):
            raise ValueError("El contenido debe ser una cadena de texto no vacía")
        
        content = content.strip()
        if not content:
            raise ValueError("El contenido está vacío")
        
        # Intentar parsear como JSON primero
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            pass  # No es JSON, intentar YAML
        
        # Intentar parsear como YAML
        try:
            parsed = yaml.safe_load(content)
            if not isinstance(parsed, dict):
                raise ValueError("El contenido parseado no es un objeto válido")
            return parsed
        except yaml.YAMLError as e:
            raise Exception(f"Error al parsear el contrato (ni JSON ni YAML válido): {str(e)}")
        except Exception as e:
            raise Exception(f"Error inesperado al parsear el contrato: {str(e)}")
