"""
Interfaces del dominio - Abstracciones siguiendo el principio de Inversión de Dependencias
Estas interfaces definen los contratos sin depender de implementaciones concretas
"""
from abc import ABC, abstractmethod
from typing import Dict, Any
from .models import SwaggerContract, AnalysisResult


class IContractFetcher(ABC):
    """Interfaz para obtener contratos desde una URL"""
    
    @abstractmethod
    def fetch(self, url: str) -> str:
        """
        Obtiene el contenido del contrato desde una URL
        
        Args:
            url: URL del contrato Swagger/OpenAPI
            
        Returns:
            Contenido del contrato como string
            
        Raises:
            Exception: Si no se puede obtener el contrato
        """
        pass


class IContractParser(ABC):
    """Interfaz para parsear contratos YAML/JSON"""
    
    @abstractmethod
    def parse(self, content: str) -> Dict[str, Any]:
        """
        Parsea el contenido del contrato a un diccionario
        
        Args:
            content: Contenido del contrato en formato YAML o JSON
            
        Returns:
            Diccionario con la estructura del contrato
            
        Raises:
            Exception: Si el contenido no es válido
        """
        pass


class IContractAnalyzer(ABC):
    """Interfaz para analizar contratos Swagger/OpenAPI"""
    
    @abstractmethod
    def analyze(self, contract_dict: Dict[str, Any]) -> AnalysisResult:
        """
        Analiza el contrato y extrae toda la información relevante
        
        Args:
            contract_dict: Diccionario con la estructura del contrato
            
        Returns:
            Resultado del análisis con toda la información extraída
            
        Raises:
            Exception: Si el contrato no es válido o tiene errores
        """
        pass
