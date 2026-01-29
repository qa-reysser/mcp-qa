"""
MCP Server para análisis de calidad de software
Herramienta para analizar contratos Swagger/OpenAPI
"""
from fastmcp import FastMCP

# Importar componentes de infraestructura
from src.infrastructure.http_fetcher import HttpContractFetcher
from src.infrastructure.contract_parser import YamlJsonContractParser
from src.infrastructure.json_exporter import JsonResultExporter
from src.infrastructure.markdown_generator import MarkdownDocumentationGenerator

# Importar componentes de aplicación
from src.application.swagger_analyzer import SwaggerContractAnalyzer
from src.application.use_cases import AnalyzeContractUseCase, FormatAnalysisResultUseCase
from src.application.export_use_cases import ExportToJsonUseCase, GenerateReadmeUseCase

# Inicializar MCP
mcp = FastMCP('Calidad de Software MCP')

# Inicializar dependencias (Dependency Injection)
fetcher = HttpContractFetcher(timeout=30, verify_ssl=True)
parser = YamlJsonContractParser()
analyzer = SwaggerContractAnalyzer()
json_exporter = JsonResultExporter()
markdown_generator = MarkdownDocumentationGenerator()

# Inicializar casos de uso
analyze_use_case = AnalyzeContractUseCase(fetcher, parser, analyzer)
format_use_case = FormatAnalysisResultUseCase()
export_json_use_case = ExportToJsonUseCase(json_exporter)
generate_readme_use_case = GenerateReadmeUseCase(markdown_generator)


@mcp.tool()
def analizar_contrato_swagger(url: str) -> str:
    """
    Analiza un contrato Swagger/OpenAPI desde una URL.
    
    Extrae información detallada incluyendo:
    - Endpoints (paths, métodos HTTP)
    - Parámetros (path, query, header, cookie)
    - Request bodies (schemas, content types)
    - Responses (códigos HTTP, schemas, headers)
    - Schemas/Definiciones (propiedades, tipos, formatos, validaciones)
    - Servidores
    - Seguridad
    - Tags y documentación
    
    Args:
        url: URL del contrato Swagger/OpenAPI (JSON o YAML)
        
    Returns:
        Análisis detallado del contrato en formato texto estructurado
        
    Examples:
        analizar_contrato_swagger("https://petstore.swagger.io/v2/swagger.json")
        analizar_contrato_swagger("https://api.example.com/openapi.yaml")
    """
    try:
        # Ejecutar análisis
        result = analyze_use_case.execute(url)
        
        # Formatear resultado
        formatted_output = format_use_case.execute(result)
        
        return formatted_output
    
    except ValueError as e:
        return f"❌ Error de validación: {str(e)}"
    except Exception as e:
        return f"❌ Error al analizar el contrato: {str(e)}"


@mcp.tool()
def generar_json_analisis(url: str, output_path: str = "swagger-analysis.json") -> str:
    """
    Analiza un contrato Swagger/OpenAPI y exporta el resultado a JSON.
    
    Genera un archivo JSON estructurado con toda la información del análisis:
    - Metadata del análisis (totales, resúmenes)
    - Información del contrato
    - Servidores
    - Endpoints completos con parámetros, request/response
    - Schemas detallados
    - Esquemas de seguridad
    
    Args:
        url: URL del contrato Swagger/OpenAPI (JSON o YAML)
        output_path: Ruta donde guardar el archivo JSON (por defecto: swagger-analysis.json)
        
    Returns:
        Mensaje con la ruta del archivo generado
        
    Examples:
        generar_json_analisis("https://petstore.swagger.io/v2/swagger.json")
        generar_json_analisis("http://localhost:8080/v3/api-docs", "api-analysis.json")
    """
    try:
        # Ejecutar análisis
        result = analyze_use_case.execute(url)
        
        # Exportar a JSON
        file_path = export_json_use_case.execute(result, output_path)
        
        return f"✅ Archivo JSON generado exitosamente:\n📁 {file_path}"
    
    except ValueError as e:
        return f"❌ Error de validación: {str(e)}"
    except Exception as e:
        return f"❌ Error al generar el JSON: {str(e)}"


@mcp.tool()
def generar_readme_api(url: str, output_path: str = "API-README.md", swagger_ui_url: str = None) -> str:
    """
    Analiza un contrato Swagger/OpenAPI y genera un README con documentación estilo Swagger UI.
    
    Genera un archivo Markdown completo con:
    - Descripción general de la API
    - Link a Swagger UI (si se proporciona)
    - Tabla de contenidos
    - Estadísticas y resumen
    - Información de servidores
    - Documentación de autenticación
    - Endpoints detallados (parámetros, request/response)
    - Schemas con tablas de propiedades
    - Códigos de estado HTTP
    - Content types soportados
    
    Args:
        url: URL del contrato Swagger/OpenAPI (JSON o YAML)
        output_path: Ruta donde guardar el README (por defecto: API-README.md)
        swagger_ui_url: URL de Swagger UI para incluir en el README (opcional)
        
    Returns:
        Mensaje con la ruta del archivo generado
        
    Examples:
        generar_readme_api("https://petstore.swagger.io/v2/swagger.json")
        generar_readme_api("http://localhost:8080/v3/api-docs", "README.md", "http://localhost:8080/swagger-ui/index.html")
    """
    try:
        # Ejecutar análisis
        result = analyze_use_case.execute(url)
        
        # Generar README
        file_path = generate_readme_use_case.execute(result, output_path, swagger_ui_url)
        
        return f"✅ README generado exitosamente:\n📁 {file_path}"
    
    except ValueError as e:
        return f"❌ Error de validación: {str(e)}"
    except Exception as e:
        return f"❌ Error al generar el README: {str(e)}"


if __name__ == "__main__":
    mcp.run()
