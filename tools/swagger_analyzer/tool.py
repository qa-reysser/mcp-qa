"""
Punto de entrada de la herramienta Swagger Analyzer
Orquesta la inicialización y ejecución del análisis completo
"""
from .src.infrastructure.http_fetcher import HttpContractFetcher
from .src.infrastructure.contract_parser import YamlJsonContractParser
from .src.infrastructure.json_exporter import JsonResultExporter
from .src.infrastructure.markdown_generator import MarkdownDocumentationGenerator
from .src.application.swagger_analyzer import SwaggerContractAnalyzer
from .src.application.complete_analysis_use_case import AnalyzeContractCompleteUseCase
from .config import OUTPUT_DIR, DEFAULT_TIMEOUT, DEFAULT_VERIFY_SSL


class SwaggerAnalyzerTool:
    """
    Herramienta principal para análisis de contratos Swagger/OpenAPI.
    Implementa el patrón Facade para simplificar la interacción.
    """
    
    def __init__(self):
        """Inicializa la herramienta con todas sus dependencias."""
        # Inicializar servicios de infraestructura (capa más externa)
        self._fetcher = HttpContractFetcher(
            timeout=DEFAULT_TIMEOUT,
            verify_ssl=DEFAULT_VERIFY_SSL
        )
        self._parser = YamlJsonContractParser()
        self._json_exporter = JsonResultExporter()
        self._readme_generator = MarkdownDocumentationGenerator()
        
        # Inicializar servicio de dominio
        self._analyzer = SwaggerContractAnalyzer()
        
        # Inicializar caso de uso (capa de aplicación)
        self._complete_analysis_use_case = AnalyzeContractCompleteUseCase(
            fetcher=self._fetcher,
            parser=self._parser,
            analyzer=self._analyzer,
            json_exporter=self._json_exporter,
            readme_generator=self._readme_generator,
            output_dir=str(OUTPUT_DIR)
        )
    
    def analyze_contract(
        self,
        url: str,
        swagger_ui_url: str = None,
        generate_json: bool = True,
        generate_readme: bool = True
    ) -> str:
        """
        Ejecuta el análisis completo de un contrato Swagger/OpenAPI.
        
        Args:
            url: URL del contrato Swagger/OpenAPI (JSON o YAML)
            swagger_ui_url: URL opcional de Swagger UI para incluir en README
            generate_json: Si se debe generar el archivo JSON (por defecto: True)
            generate_readme: Si se debe generar el archivo README (por defecto: True)
            
        Returns:
            Mensaje con el resultado del análisis y rutas de archivos generados
            
        Raises:
            ValueError: Si la URL no es válida
            Exception: Si hay algún error en el análisis
        """
        try:
            # Ejecutar análisis completo
            output = self._complete_analysis_use_case.execute(
                url=url,
                swagger_ui_url=swagger_ui_url,
                generate_json=generate_json,
                generate_readme=generate_readme
            )
            
            # Construir mensaje de respuesta
            response_lines = [
                "✅ Análisis completado exitosamente",
                "",
                output.formatted_text,
                "",
                "📁 ARCHIVOS GENERADOS:"
            ]
            
            if output.json_file_path:
                response_lines.append(f"  📊 JSON: {output.json_file_path}")
            
            if output.readme_file_path:
                response_lines.append(f"  📄 README: {output.readme_file_path}")
            
            return "\n".join(response_lines)
        
        except ValueError as e:
            return f"❌ Error de validación: {str(e)}"
        except Exception as e:
            return f"❌ Error al analizar el contrato: {str(e)}"
