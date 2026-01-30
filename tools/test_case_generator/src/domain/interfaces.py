"""
Interfaces del dominio siguiendo el Principio de Inversión de Dependencias (DIP).
Define contratos para las implementaciones de infraestructura.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from .models import TestCase, TestSuite, SwaggerEndpointData, ISTQBTechnique


class ISwaggerAnalysisReader(ABC):
    """Interfaz para leer el análisis de Swagger generado por otra herramienta."""
    
    @abstractmethod
    def read_analysis(self, file_path: str) -> Dict[str, Any]:
        """
        Lee el archivo JSON de análisis de Swagger.
        
        Args:
            file_path: Ruta al archivo JSON de análisis
            
        Returns:
            Diccionario con el análisis completo
        """
        pass
    
    @abstractmethod
    def extract_endpoints(self, analysis: Dict[str, Any]) -> List[SwaggerEndpointData]:
        """
        Extrae los datos de endpoints del análisis.
        
        Args:
            analysis: Análisis completo de Swagger
            
        Returns:
            Lista de datos de endpoints
        """
        pass


class ITestCaseGenerator(ABC):
    """Interfaz base para generadores de casos de prueba por técnica ISTQB."""
    
    @abstractmethod
    def generate(self, endpoint_data: SwaggerEndpointData) -> List[TestCase]:
        """
        Genera casos de prueba para un endpoint específico.
        
        Args:
            endpoint_data: Datos del endpoint de Swagger
            
        Returns:
            Lista de casos de prueba generados
        """
        pass
    
    @abstractmethod
    def get_technique(self) -> ISTQBTechnique:
        """Retorna la técnica ISTQB que implementa este generador."""
        pass


class ISyntheticDataGenerator(ABC):
    """Interfaz para generar datos sintéticos basados en schemas."""
    
    @abstractmethod
    def generate_valid_value(self, param: Dict[str, Any]) -> Any:
        """
        Genera un valor válido basado en el esquema del parámetro.
        
        Args:
            param: Definición del parámetro (type, format, constraints)
            
        Returns:
            Valor sintético válido
        """
        pass
    
    @abstractmethod
    def generate_invalid_value(self, param: Dict[str, Any], violation_type: str) -> Any:
        """
        Genera un valor inválido según el tipo de violación.
        
        Args:
            param: Definición del parámetro
            violation_type: Tipo de violación (null, empty, invalid_format, etc.)
            
        Returns:
            Valor sintético inválido
        """
        pass
    
    @abstractmethod
    def generate_boundary_values(self, param: Dict[str, Any]) -> List[Any]:
        """
        Genera valores límite para un parámetro.
        
        Args:
            param: Definición del parámetro con constraints (min, max, length)
            
        Returns:
            Lista de valores en los límites
        """
        pass


class ITestSuiteBuilder(ABC):
    """Interfaz para construir suites de casos de prueba."""
    
    @abstractmethod
    def build(
        self, 
        endpoints: List[SwaggerEndpointData],
        techniques: Optional[List[ISTQBTechnique]] = None,
        include_positive: bool = True,
        include_negative: bool = True
    ) -> TestSuite:
        """
        Construye una suite completa de casos de prueba.
        
        Args:
            endpoints: Lista de endpoints a probar
            techniques: Técnicas ISTQB a aplicar (None = todas)
            include_positive: Incluir casos positivos
            include_negative: Incluir casos negativos
            
        Returns:
            Suite de casos de prueba
        """
        pass
