"""
MCP Server para análisis de calidad de software
Herramienta para analizar contratos Swagger/OpenAPI
"""
from fastmcp import FastMCP

# Importar componentes de infraestructura
from src.infrastructure.http_fetcher import HttpContractFetcher
from src.infrastructure.contract_parser import YamlJsonContractParser

# Importar componentes de aplicación
from src.application.swagger_analyzer import SwaggerContractAnalyzer
from src.application.use_cases import AnalyzeContractUseCase, FormatAnalysisResultUseCase

# Inicializar MCP
mcp = FastMCP('Calidad de Software MCP')

# Inicializar dependencias (Dependency Injection)
fetcher = HttpContractFetcher(timeout=30, verify_ssl=True)
parser = YamlJsonContractParser()
analyzer = SwaggerContractAnalyzer()

# Inicializar casos de uso
analyze_use_case = AnalyzeContractUseCase(fetcher, parser, analyzer)
format_use_case = FormatAnalysisResultUseCase()


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


if __name__ == "__main__":
    mcp.run()
