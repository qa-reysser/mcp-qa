"""
MCP Server para análisis de calidad de software
Punto de entrada centralizado para todas las herramientas de QA
"""
from fastmcp import FastMCP
from tools.swagger_analyzer import SwaggerAnalyzerTool

# Inicializar MCP
mcp = FastMCP('Calidad de Software MCP')

# Inicializar herramientas
swagger_tool = SwaggerAnalyzerTool()


@mcp.tool()
def analizar_contrato_swagger(
    url: str,
    swagger_ui_url: str = None,
    generar_json: bool = True,
    generar_readme: bool = True
) -> str:
    """
    Analiza un contrato Swagger/OpenAPI y genera análisis completo con exportaciones.
    
    Esta herramienta realiza un análisis exhaustivo del contrato y genera:
    - Análisis detallado en formato texto
    - Archivo JSON con toda la información estructurada (opcional)
    - README con documentación estilo Swagger UI (opcional)
    
    Extrae información completa incluyendo:
    - Endpoints (paths, métodos HTTP, parámetros)
    - Request bodies (schemas, content types, validaciones)
    - Responses (códigos HTTP, schemas, headers)
    - Schemas/Definiciones (propiedades, tipos, formatos)
    - Validaciones (obligatoriedad, min/max, patterns, enums)
    - Información de servidores y seguridad
    - Tags y documentación externa
    
    Los archivos se guardan en: output/swagger_analyzer/
    
    Args:
        url: URL del contrato Swagger/OpenAPI (JSON o YAML)
        swagger_ui_url: URL de Swagger UI para incluir en el README (opcional)
        generar_json: Generar archivo JSON con análisis completo (por defecto: True)
        generar_readme: Generar README con documentación (por defecto: True)
        
    Returns:
        Análisis detallado y rutas de archivos generados
        
    Examples:
        # Análisis completo (texto + JSON + README)
        analizar_contrato_swagger("http://localhost:8080/v3/api-docs")
        
        # Con URL de Swagger UI
        analizar_contrato_swagger(
            "http://localhost:8080/v3/api-docs",
            "http://localhost:8080/swagger-ui/index.html"
        )
        
        # Solo análisis de texto, sin generar archivos
        analizar_contrato_swagger(
            "https://petstore.swagger.io/v2/swagger.json",
            generar_json=False,
            generar_readme=False
        )
    """
    return swagger_tool.analyze_contract(
        url=url,
        swagger_ui_url=swagger_ui_url,
        generate_json=generar_json,
        generate_readme=generar_readme
    )


if __name__ == "__main__":
    mcp.run()

