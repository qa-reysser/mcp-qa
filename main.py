"""
MCP Server para análisis de calidad de software
Punto de entrada centralizado para todas las herramientas de QA
"""
from fastmcp import FastMCP
from tools.swagger_analyzer import SwaggerAnalyzerTool
from tools.test_case_generator import TestCaseGeneratorTool

# Inicializar MCP
mcp = FastMCP('Calidad de Software MCP')

# Inicializar herramientas
swagger_tool = SwaggerAnalyzerTool()
test_case_generator_tool = TestCaseGeneratorTool()


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


@mcp.tool()
def generar_casos_prueba(
    swagger_analysis_json_path: str,
    tecnicas: list[str] = None,
    incluir_positivos: bool = True,
    incluir_negativos: bool = True,
    generar_json: bool = True,
    generar_readme: bool = True
) -> str:
    """
    Genera casos de prueba automáticamente desde un análisis de Swagger usando técnicas ISTQB.
    
    Esta herramienta crea casos de prueba completos aplicando técnicas de testing reconocidas:
    - Partición de Equivalencia (equivalence_partitioning)
    - Análisis de Valores Límite (boundary_value_analysis)
    - Tabla de Decisión (decision_table)
    
    Genera casos detallados con:
    - ID único y nombre descriptivo
    - Técnica ISTQB aplicada (trazabilidad)
    - Tipo (positivo/negativo)
    - Prioridad (alta/media/baja)
    - Datos de entrada sintéticos realistas (headers, params, body)
    - Resultado esperado (código HTTP, errores específicos)
    - Pre y post condiciones
    
    Los archivos se guardan en: output/test_case_generator/
    
    Args:
        swagger_analysis_json_path: Ruta al JSON generado por analizar_contrato_swagger
        tecnicas: Lista de técnicas ISTQB a aplicar (default: todas)
                 Valores: ["equivalence_partitioning", "boundary_value_analysis", "decision_table"]
        incluir_positivos: Incluir casos de prueba positivos (default: True)
        incluir_negativos: Incluir casos de prueba negativos (default: True)
        generar_json: Generar archivo JSON con casos de prueba (default: True)
        generar_readme: Generar README con listado de casos (default: True)
        
    Returns:
        Resumen de casos generados y rutas de archivos
        
    Examples:
        # Generar todos los casos con todas las técnicas
        generar_casos_prueba("output/swagger_analyzer/swagger-analysis.json")
        
        # Solo casos de valores límite
        generar_casos_prueba(
            "output/swagger_analyzer/swagger-analysis.json",
            tecnicas=["boundary_value_analysis"]
        )
        
        # Solo casos negativos
        generar_casos_prueba(
            "output/swagger_analyzer/swagger-analysis.json",
            incluir_positivos=False,
            incluir_negativos=True
        )
    """
    result = test_case_generator_tool.generate_test_cases(
        swagger_analysis_json_path=swagger_analysis_json_path,
        techniques=tecnicas,
        include_positive=incluir_positivos,
        include_negative=incluir_negativos,
        generate_json=generar_json,
        generate_readme=generar_readme
    )
    
    # Formatear resultado
    output = []
    output.append("✅ Generación de casos de prueba completada\n")
    output.append(f"📊 Total de casos generados: {result['total_test_cases']}\n")
    
    summary = result['summary']
    
    output.append("🎯 Distribución por técnica:")
    for technique, count in summary['by_technique'].items():
        output.append(f"  - {technique}: {count} casos")
    
    output.append("\n📋 Distribución por tipo:")
    for test_type, count in summary['by_type'].items():
        icon = "✅" if test_type == "positive" else "❌"
        output.append(f"  {icon} {test_type}: {count} casos")
    
    output.append("\n⚡ Distribución por prioridad:")
    for priority, count in summary['by_priority'].items():
        icon = "🔴" if priority == "high" else "🟡" if priority == "medium" else "🟢"
        output.append(f"  {icon} {priority}: {count} casos")
    
    output.append("\n📁 Archivos generados:")
    for file_info in result['files_generated']:
        output.append(f"  {file_info['type']}: {file_info['path']}")
    
    return "\n".join(output)


if __name__ == "__main__":
    mcp.run()

