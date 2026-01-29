"""
Interfaces para exportadores - Abstracciones para generar archivos de salida
"""
from abc import ABC, abstractmethod
from .models import AnalysisResult


class IResultExporter(ABC):
    """Interfaz para exportar resultados de análisis"""
    
    @abstractmethod
    def export(self, result: AnalysisResult, output_path: str) -> str:
        """
        Exporta el resultado del análisis a un archivo
        
        Args:
            result: Resultado del análisis a exportar
            output_path: Ruta donde guardar el archivo
            
        Returns:
            Ruta del archivo generado
            
        Raises:
            Exception: Si hay un error al exportar
        """
        pass


class IDocumentationGenerator(ABC):
    """Interfaz para generar documentación"""
    
    @abstractmethod
    def generate(self, result: AnalysisResult, output_path: str, swagger_ui_url: str = None) -> str:
        """
        Genera documentación a partir del resultado del análisis
        
        Args:
            result: Resultado del análisis
            output_path: Ruta donde guardar la documentación
            swagger_ui_url: URL opcional de Swagger UI
            
        Returns:
            Ruta del archivo generado
            
        Raises:
            Exception: Si hay un error al generar la documentación
        """
        pass
