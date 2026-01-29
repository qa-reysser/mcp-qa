"""
Servicio de aplicación - Orquesta el flujo completo de análisis
Coordina el fetcher, parser y analyzer siguiendo el patrón de caso de uso
"""
from typing import Dict, Any
from ..domain.interfaces import IContractFetcher, IContractParser, IContractAnalyzer
from ..domain.models import AnalysisResult


class AnalyzeContractUseCase:
    """Caso de uso para analizar un contrato Swagger/OpenAPI desde una URL"""
    
    def __init__(
        self,
        fetcher: IContractFetcher,
        parser: IContractParser,
        analyzer: IContractAnalyzer
    ):
        """
        Inicializa el caso de uso con sus dependencias
        
        Args:
            fetcher: Servicio para obtener contratos desde URLs
            parser: Servicio para parsear YAML/JSON
            analyzer: Servicio para analizar contratos
        """
        self._fetcher = fetcher
        self._parser = parser
        self._analyzer = analyzer
    
    def execute(self, url: str) -> AnalysisResult:
        """
        Ejecuta el análisis completo de un contrato
        
        Args:
            url: URL del contrato Swagger/OpenAPI
            
        Returns:
            Resultado del análisis con toda la información extraída
            
        Raises:
            Exception: Si hay algún error en cualquier paso del proceso
        """
        # Paso 1: Obtener el contrato desde la URL
        content = self._fetcher.fetch(url)
        
        # Paso 2: Parsear el contenido
        contract_dict = self._parser.parse(content)
        
        # Paso 3: Analizar el contrato
        result = self._analyzer.analyze(contract_dict)
        
        return result


class FormatAnalysisResultUseCase:
    """Caso de uso para formatear el resultado del análisis en un formato legible"""
    
    def execute(self, result: AnalysisResult) -> str:
        """
        Formatea el resultado del análisis en texto estructurado
        
        Args:
            result: Resultado del análisis a formatear
            
        Returns:
            String con el análisis formateado
        """
        lines = []
        
        # Errores críticos
        if result.errors:
            lines.append("❌ ERRORES CRÍTICOS:")
            for error in result.errors:
                lines.append(f"  - {error}")
            return "\n".join(lines)
        
        contract = result.contract
        
        # Información general
        lines.append("=" * 80)
        lines.append("📋 ANÁLISIS DE CONTRATO SWAGGER/OPENAPI")
        lines.append("=" * 80)
        lines.append("")
        
        lines.append("📌 INFORMACIÓN GENERAL:")
        lines.append(f"  Título: {contract.title}")
        lines.append(f"  Versión: {contract.version}")
        if contract.openapi_version:
            lines.append(f"  OpenAPI Version: {contract.openapi_version}")
        if contract.swagger_version:
            lines.append(f"  Swagger Version: {contract.swagger_version}")
        if contract.description:
            lines.append(f"  Descripción: {contract.description}")
        lines.append("")
        
        # Servidores
        if contract.servers:
            lines.append("🌐 SERVIDORES:")
            for i, server in enumerate(contract.servers, 1):
                lines.append(f"  {i}. {server.url}")
                if server.description:
                    lines.append(f"     Descripción: {server.description}")
            lines.append("")
        
        # Resumen de endpoints
        lines.append("📊 RESUMEN DE ENDPOINTS:")
        lines.append(f"  Total de endpoints: {result.total_endpoints}")
        if result.methods_summary:
            lines.append("  Métodos HTTP:")
            for method, count in sorted(result.methods_summary.items()):
                lines.append(f"    - {method}: {count}")
        lines.append("")
        
        # Endpoints detallados
        if contract.endpoints:
            lines.append("🔗 ENDPOINTS DETALLADOS:")
            lines.append("")
            
            for i, endpoint in enumerate(contract.endpoints, 1):
                lines.append(f"  [{i}] {endpoint.method.value} {endpoint.path}")
                
                if endpoint.summary:
                    lines.append(f"      Resumen: {endpoint.summary}")
                
                if endpoint.description:
                    lines.append(f"      Descripción: {endpoint.description}")
                
                if endpoint.operation_id:
                    lines.append(f"      Operation ID: {endpoint.operation_id}")
                
                if endpoint.tags:
                    lines.append(f"      Tags: {', '.join(endpoint.tags)}")
                
                if endpoint.deprecated:
                    lines.append("      ⚠️  DEPRECATED")
                
                # Parámetros
                if endpoint.parameters:
                    lines.append("      Parámetros:")
                    for param in endpoint.parameters:
                        required = "✓ Obligatorio" if param.required else "Opcional"
                        type_info = f"{param.type}" if param.type else "any"
                        if param.format:
                            type_info += f" (formato: {param.format})"
                        lines.append(f"        - {param.name} [{param.location}] - {type_info} - {required}")
                        if param.description:
                            lines.append(f"          {param.description}")
                
                # Request Body
                if endpoint.request_body:
                    lines.append("      Request Body:")
                    required = "✓ Obligatorio" if endpoint.request_body.required else "Opcional"
                    lines.append(f"        {required}")
                    if endpoint.request_body.content_types:
                        lines.append(f"        Content-Types: {', '.join(endpoint.request_body.content_types)}")
                    if endpoint.request_body.schema:
                        lines.append("        Schema:")
                        self._format_schema(lines, endpoint.request_body.schema, indent="          ")
                
                # Responses
                if endpoint.responses:
                    lines.append("      Respuestas:")
                    for response in endpoint.responses:
                        lines.append(f"        [{response.status_code}] {response.description or 'Sin descripción'}")
                        if response.content_types:
                            lines.append(f"          Content-Types: {', '.join(response.content_types)}")
                        if response.headers:
                            lines.append("          Headers:")
                            for header in response.headers:
                                lines.append(f"            - {header.name}: {header.type or 'string'}")
                        if response.schema:
                            lines.append("          Schema:")
                            self._format_schema(lines, response.schema, indent="            ")
                
                lines.append("")
        
        # Schemas
        if contract.schemas:
            lines.append(f"📦 SCHEMAS ({result.total_schemas}):")
            lines.append("")
            for schema in contract.schemas:
                lines.append(f"  {schema.name}")
                if schema.description:
                    lines.append(f"    Descripción: {schema.description}")
                if schema.type:
                    lines.append(f"    Tipo: {schema.type}")
                if schema.properties:
                    lines.append("    Propiedades:")
                    for prop in schema.properties:
                        required = "✓" if prop.required else " "
                        type_info = prop.type or "any"
                        if prop.format:
                            type_info += f" (formato: {prop.format})"
                        lines.append(f"      [{required}] {prop.name}: {type_info}")
                        if prop.description:
                            lines.append(f"          {prop.description}")
                        if prop.enum:
                            lines.append(f"          Valores: {', '.join(map(str, prop.enum))}")
                        if prop.pattern:
                            lines.append(f"          Patrón: {prop.pattern}")
                        if prop.min_length is not None or prop.max_length is not None:
                            length = []
                            if prop.min_length is not None:
                                length.append(f"min: {prop.min_length}")
                            if prop.max_length is not None:
                                length.append(f"max: {prop.max_length}")
                            lines.append(f"          Longitud: {', '.join(length)}")
                        if prop.minimum is not None or prop.maximum is not None:
                            range_info = []
                            if prop.minimum is not None:
                                range_info.append(f"min: {prop.minimum}")
                            if prop.maximum is not None:
                                range_info.append(f"max: {prop.maximum}")
                            lines.append(f"          Rango: {', '.join(range_info)}")
                lines.append("")
        
        # Códigos de estado
        if result.status_codes_summary:
            lines.append("📈 CÓDIGOS DE ESTADO HTTP:")
            for code, count in sorted(result.status_codes_summary.items()):
                lines.append(f"  {code}: {count} endpoint(s)")
            lines.append("")
        
        # Content types
        if result.content_types:
            lines.append("📄 CONTENT TYPES:")
            for ct in result.content_types:
                lines.append(f"  - {ct}")
            lines.append("")
        
        # Seguridad
        if result.has_security:
            lines.append("🔒 SEGURIDAD:")
            lines.append(f"  Esquemas de seguridad definidos: {len(contract.security_schemes)}")
            for scheme_name, scheme_data in contract.security_schemes.items():
                scheme_type = scheme_data.get('type', 'unknown')
                lines.append(f"    - {scheme_name} ({scheme_type})")
            lines.append("")
        
        # Tags
        if contract.tags:
            lines.append("🏷️  TAGS:")
            for tag in contract.tags:
                tag_name = tag.get('name', 'Sin nombre')
                tag_desc = tag.get('description', '')
                if tag_desc:
                    lines.append(f"  - {tag_name}: {tag_desc}")
                else:
                    lines.append(f"  - {tag_name}")
            lines.append("")
        
        # Warnings
        if result.warnings:
            lines.append("⚠️  ADVERTENCIAS:")
            for warning in result.warnings:
                lines.append(f"  - {warning}")
            lines.append("")
        
        lines.append("=" * 80)
        
        return "\n".join(lines)
    
    def _format_schema(self, lines: list, schema, indent: str = ""):
        """Helper para formatear schemas de forma recursiva"""
        if schema.properties:
            for prop in schema.properties[:5]:  # Limitar a 5 propiedades para brevedad
                required = "✓" if prop.required else " "
                type_info = prop.type or "any"
                if prop.format:
                    type_info += f" ({prop.format})"
                lines.append(f"{indent}[{required}] {prop.name}: {type_info}")
            if len(schema.properties) > 5:
                lines.append(f"{indent}... y {len(schema.properties) - 5} propiedades más")
