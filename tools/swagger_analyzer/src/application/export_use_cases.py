"""
Casos de uso para exportación - Orquesta la exportación de resultados
"""
from ..domain.models import AnalysisResult
from ..domain.exporters import IResultExporter, IDocumentationGenerator


class ExportToJsonUseCase:
    """Caso de uso para exportar resultados a JSON"""
    
    def __init__(self, exporter: IResultExporter):
        """
        Inicializa el caso de uso
        
        Args:
            exporter: Servicio para exportar a JSON
        """
        self._exporter = exporter
    
    def execute(self, result: AnalysisResult, output_path: str) -> str:
        """
        Exporta el resultado del análisis a un archivo JSON
        
        Args:
            result: Resultado del análisis
            output_path: Ruta donde guardar el archivo
            
        Returns:
            Ruta del archivo generado
        """
        return self._exporter.export(result, output_path)


class GenerateReadmeUseCase:
    """Caso de uso para generar documentación README"""
    
    def __init__(self, generator: IDocumentationGenerator):
        """
        Inicializa el caso de uso
        
        Args:
            generator: Servicio para generar documentación
        """
        self._generator = generator
    
    def execute(self, result: AnalysisResult, output_path: str, swagger_ui_url: str = None) -> str:
        """
        Genera un README con la documentación de la API
        
        Args:
            result: Resultado del análisis
            output_path: Ruta donde guardar el README
            swagger_ui_url: URL opcional de Swagger UI
            
        Returns:
            Ruta del archivo generado
        """
        return self._generator.generate(result, output_path, swagger_ui_url)
