"""
Generador de documentación Markdown - Genera README con estilo Swagger UI
"""
from pathlib import Path
from src.domain.exporters import IDocumentationGenerator
from src.domain.models import AnalysisResult, Endpoint, Schema


class MarkdownDocumentationGenerator(IDocumentationGenerator):
    """Genera documentación en formato Markdown estilo Swagger UI"""
    
    def generate(self, result: AnalysisResult, output_path: str, swagger_ui_url: str = None) -> str:
        """
        Genera un README.md con la documentación de la API
        
        Args:
            result: Resultado del análisis
            output_path: Ruta donde guardar el README
            swagger_ui_url: URL opcional de Swagger UI
            
        Returns:
            Ruta del archivo generado
        """
        content = self._generate_markdown(result, swagger_ui_url)
        
        # Crear directorio si no existe
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Escribir archivo
        with output_file.open('w', encoding='utf-8') as f:
            f.write(content)
        
        return str(output_file.absolute())
    
    def _generate_markdown(self, result: AnalysisResult, swagger_ui_url: str = None) -> str:
        """Genera el contenido Markdown"""
        lines = []
        contract = result.contract
        
        # Título y descripción
        lines.append(f"# {contract.title}")
        lines.append("")
        lines.append(f"**Versión**: {contract.version}")
        if contract.openapi_version:
            lines.append(f"**OpenAPI**: {contract.openapi_version}")
        if contract.swagger_version:
            lines.append(f"**Swagger**: {contract.swagger_version}")
        lines.append("")
        
        if contract.description:
            lines.append("## 📋 Descripción")
            lines.append("")
            lines.append(contract.description)
            lines.append("")
        
        # Link a Swagger UI
        if swagger_ui_url:
            lines.append("## 🔗 Swagger UI")
            lines.append("")
            lines.append(f"[Abrir Swagger UI]({swagger_ui_url})")
            lines.append("")
        
        # Tabla de contenidos
        lines.append("## 📑 Tabla de Contenidos")
        lines.append("")
        lines.append("- [Servidores](#servidores)")
        lines.append("- [Autenticación](#autenticación)")
        lines.append("- [Endpoints](#endpoints)")
        for endpoint in contract.endpoints:
            anchor = f"{endpoint.method.value.lower()}-{endpoint.path.replace('/', '').replace('{', '').replace('}', '')}"
            lines.append(f"  - [{endpoint.method.value} {endpoint.path}](#{anchor})")
        lines.append("- [Schemas](#schemas)")
        lines.append("- [Códigos de Estado](#códigos-de-estado)")
        lines.append("")
        
        # Estadísticas
        lines.append("## 📊 Resumen")
        lines.append("")
        lines.append(f"- **Total de Endpoints**: {result.total_endpoints}")
        lines.append(f"- **Total de Schemas**: {result.total_schemas}")
        lines.append(f"- **Autenticación**: {'✅ Sí' if result.has_security else '❌ No'}")
        lines.append("")
        
        if result.methods_summary:
            lines.append("### Métodos HTTP")
            lines.append("")
            for method, count in sorted(result.methods_summary.items()):
                lines.append(f"- `{method}`: {count} endpoint(s)")
            lines.append("")
        
        # Servidores
        if contract.servers:
            lines.append("## 🌐 Servidores")
            lines.append("")
            for server in contract.servers:
                lines.append(f"### {server.url}")
                if server.description:
                    lines.append(f"> {server.description}")
                lines.append("")
        
        # Autenticación
        if result.has_security:
            lines.append("## 🔒 Autenticación")
            lines.append("")
            for scheme_name, scheme_data in contract.security_schemes.items():
                scheme_type = scheme_data.get('type', 'unknown')
                lines.append(f"### {scheme_name}")
                lines.append(f"- **Tipo**: `{scheme_type}`")
                if scheme_data.get('description'):
                    lines.append(f"- **Descripción**: {scheme_data['description']}")
                lines.append("")
        
        # Endpoints
        lines.append("## 🔗 Endpoints")
        lines.append("")
        
        for endpoint in contract.endpoints:
            self._add_endpoint_section(lines, endpoint)
        
        # Schemas
        if contract.schemas:
            lines.append("## 📦 Schemas")
            lines.append("")
            for schema in contract.schemas:
                self._add_schema_section(lines, schema)
        
        # Códigos de estado
        if result.status_codes_summary:
            lines.append("## 📈 Códigos de Estado")
            lines.append("")
            lines.append("| Código | Descripción | Endpoints |")
            lines.append("|--------|-------------|-----------|")
            
            status_descriptions = {
                "200": "OK - Solicitud exitosa",
                "201": "Created - Recurso creado exitosamente",
                "204": "No Content - Operación exitosa sin contenido",
                "400": "Bad Request - Solicitud inválida",
                "401": "Unauthorized - No autenticado",
                "403": "Forbidden - No autorizado",
                "404": "Not Found - Recurso no encontrado",
                "409": "Conflict - Conflicto con el estado actual",
                "500": "Internal Server Error - Error del servidor"
            }
            
            for code, count in sorted(result.status_codes_summary.items()):
                description = status_descriptions.get(code, "")
                lines.append(f"| `{code}` | {description} | {count} |")
            lines.append("")
        
        # Content Types
        if result.content_types:
            lines.append("## 📄 Content Types Soportados")
            lines.append("")
            for ct in result.content_types:
                lines.append(f"- `{ct}`")
            lines.append("")
        
        # Tags
        if contract.tags:
            lines.append("## 🏷️ Tags")
            lines.append("")
            for tag in contract.tags:
                tag_name = tag.get('name', 'Sin nombre')
                tag_desc = tag.get('description', '')
                lines.append(f"### {tag_name}")
                if tag_desc:
                    lines.append(tag_desc)
                lines.append("")
        
        # Footer
        lines.append("---")
        lines.append("")
        lines.append("*Documentación generada automáticamente por MCP-QA*")
        lines.append("")
        
        return "\n".join(lines)
    
    def _add_endpoint_section(self, lines: list, endpoint: Endpoint):
        """Agrega la sección de un endpoint"""
        anchor = f"{endpoint.method.value.lower()}-{endpoint.path.replace('/', '').replace('{', '').replace('}', '')}"
        
        # Título del endpoint
        lines.append(f"### `{endpoint.method.value}` {endpoint.path}")
        lines.append("")
        
        if endpoint.summary:
            lines.append(f"**{endpoint.summary}**")
            lines.append("")
        
        if endpoint.description:
            lines.append(endpoint.description)
            lines.append("")
        
        if endpoint.deprecated:
            lines.append("> ⚠️ **DEPRECATED** - Este endpoint está obsoleto")
            lines.append("")
        
        if endpoint.tags:
            lines.append(f"**Tags**: {', '.join([f'`{tag}`' for tag in endpoint.tags])}")
            lines.append("")
        
        if endpoint.operation_id:
            lines.append(f"**Operation ID**: `{endpoint.operation_id}`")
            lines.append("")
        
        # Parámetros
        if endpoint.parameters:
            lines.append("#### Parámetros")
            lines.append("")
            lines.append("| Nombre | Ubicación | Tipo | Requerido | Descripción |")
            lines.append("|--------|-----------|------|-----------|-------------|")
            
            for param in endpoint.parameters:
                required = "✅" if param.required else "❌"
                param_type = param.type or "any"
                if param.format:
                    param_type += f" ({param.format})"
                description = param.description or ""
                lines.append(f"| `{param.name}` | {param.location} | `{param_type}` | {required} | {description} |")
            
            lines.append("")
        
        # Request Body
        if endpoint.request_body:
            lines.append("#### Request Body")
            lines.append("")
            required = "✅ Obligatorio" if endpoint.request_body.required else "❌ Opcional"
            lines.append(f"**{required}**")
            lines.append("")
            
            if endpoint.request_body.content_types:
                lines.append(f"**Content-Type**: {', '.join([f'`{ct}`' for ct in endpoint.request_body.content_types])}")
                lines.append("")
            
            if endpoint.request_body.schema:
                lines.append(f"**Schema**: [`{endpoint.request_body.schema.name}`](#{endpoint.request_body.schema.name.lower()})")
                lines.append("")
        
        # Responses
        if endpoint.responses:
            lines.append("#### Respuestas")
            lines.append("")
            
            for response in endpoint.responses:
                lines.append(f"##### {response.status_code}")
                if response.description:
                    lines.append(response.description)
                lines.append("")
                
                if response.content_types:
                    lines.append(f"**Content-Type**: {', '.join([f'`{ct}`' for ct in response.content_types])}")
                    lines.append("")
                
                if response.schema:
                    lines.append(f"**Schema**: [`{response.schema.name}`](#{response.schema.name.lower()})")
                    lines.append("")
                
                if response.headers:
                    lines.append("**Headers**:")
                    for header in response.headers:
                        lines.append(f"- `{header.name}`: {header.type or 'string'}")
                    lines.append("")
        
        lines.append("---")
        lines.append("")
    
    def _add_schema_section(self, lines: list, schema: Schema):
        """Agrega la sección de un schema"""
        lines.append(f"### {schema.name}")
        lines.append("")
        
        if schema.description:
            lines.append(schema.description)
            lines.append("")
        
        if schema.type:
            lines.append(f"**Tipo**: `{schema.type}`")
            lines.append("")
        
        if schema.properties:
            lines.append("#### Propiedades")
            lines.append("")
            lines.append("| Nombre | Tipo | Requerido | Descripción | Validaciones |")
            lines.append("|--------|------|-----------|-------------|--------------|")
            
            for prop in schema.properties:
                required = "✅" if prop.required else "❌"
                prop_type = prop.type or "any"
                if prop.format:
                    prop_type += f" ({prop.format})"
                description = prop.description or ""
                
                # Validaciones
                validations = []
                if prop.min_length is not None:
                    validations.append(f"min: {prop.min_length}")
                if prop.max_length is not None:
                    validations.append(f"max: {prop.max_length}")
                if prop.minimum is not None:
                    validations.append(f"≥ {prop.minimum}")
                if prop.maximum is not None:
                    validations.append(f"≤ {prop.maximum}")
                if prop.pattern:
                    validations.append(f"pattern: `{prop.pattern}`")
                if prop.enum:
                    validations.append(f"enum: {', '.join(map(str, prop.enum))}")
                
                validation_str = ", ".join(validations) if validations else "-"
                
                lines.append(f"| `{prop.name}` | `{prop_type}` | {required} | {description} | {validation_str} |")
            
            lines.append("")
        
        lines.append("")
