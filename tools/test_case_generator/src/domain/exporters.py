"""
Interfaces para exportar casos de prueba a diferentes formatos.
Siguiendo el Principio Abierto/Cerrado (OCP).
"""
from abc import ABC, abstractmethod
from .models import TestSuite


class ITestExporter(ABC):
    """Interfaz base para exportadores de casos de prueba."""
    
    @abstractmethod
    def export(self, test_suite: TestSuite, output_path: str) -> str:
        """
        Exporta la suite de casos de prueba al formato específico.
        
        Args:
            test_suite: Suite de casos de prueba a exportar
            output_path: Ruta donde guardar el archivo
            
        Returns:
            Ruta del archivo generado
        """
        pass
    
    @abstractmethod
    def get_format_name(self) -> str:
        """Retorna el nombre del formato de exportación."""
        pass
