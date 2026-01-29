"""
Exportador JSON - Exporta el resultado del análisis a formato JSON
"""
import json
from pathlib import Path
from typing import Any, Dict, List
from src.domain.exporters import IResultExporter
from src.domain.models import AnalysisResult, Endpoint, Schema, Response, Parameter, Property


class JsonResultExporter(IResultExporter):
    """Exporta resultados de análisis a formato JSON estructurado"""
    
    def export(self, result: AnalysisResult, output_path: str) -> str:
        """
        Exporta el resultado del análisis a un archivo JSON
        
        Args:
            result: Resultado del análisis a exportar
            output_path: Ruta donde guardar el archivo JSON
            
        Returns:
            Ruta del archivo generado
        """
        # Convertir el resultado a un diccionario serializable
        data = self._result_to_dict(result)
        
        # Crear directorio si no existe
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Escribir JSON con formato legible
        with output_file.open('w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return str(output_file.absolute())
    
    def _result_to_dict(self, result: AnalysisResult) -> Dict[str, Any]:
        """Convierte el resultado a un diccionario serializable"""
        contract = result.contract
        
        return {
            "analysis_metadata": {
                "total_endpoints": result.total_endpoints,
                "total_schemas": result.total_schemas,
                "has_security": result.has_security,
                "methods_summary": result.methods_summary,
                "status_codes_summary": result.status_codes_summary,
                "content_types": result.content_types,
                "warnings": result.warnings,
                "errors": result.errors
            },
            "contract_info": {
                "title": contract.title,
                "version": contract.version,
                "openapi_version": contract.openapi_version,
                "swagger_version": contract.swagger_version,
                "description": contract.description,
                "tags": contract.tags,
                "external_docs": contract.external_docs
            },
            "servers": [
                {
                    "url": server.url,
                    "description": server.description,
                    "variables": server.variables
                }
                for server in contract.servers
            ],
            "endpoints": [
                self._endpoint_to_dict(endpoint)
                for endpoint in contract.endpoints
            ],
            "schemas": [
                self._schema_to_dict(schema)
                for schema in contract.schemas
            ],
            "security_schemes": contract.security_schemes
        }
    
    def _endpoint_to_dict(self, endpoint: Endpoint) -> Dict[str, Any]:
        """Convierte un endpoint a diccionario"""
        return {
            "path": endpoint.path,
            "method": endpoint.method.value,
            "operation_id": endpoint.operation_id,
            "summary": endpoint.summary,
            "description": endpoint.description,
            "tags": endpoint.tags,
            "deprecated": endpoint.deprecated,
            "parameters": [
                self._parameter_to_dict(param)
                for param in endpoint.parameters
            ],
            "request_body": self._request_body_to_dict(endpoint.request_body) if endpoint.request_body else None,
            "responses": [
                self._response_to_dict(response)
                for response in endpoint.responses
            ],
            "security": endpoint.security
        }
    
    def _parameter_to_dict(self, param: Parameter) -> Dict[str, Any]:
        """Convierte un parámetro a diccionario"""
        return {
            "name": param.name,
            "location": param.location,
            "required": param.required,
            "type": param.type,
            "format": param.format,
            "description": param.description,
            "schema": param.schema,
            "example": param.example
        }
    
    def _request_body_to_dict(self, request_body) -> Dict[str, Any]:
        """Convierte un request body a diccionario"""
        return {
            "required": request_body.required,
            "description": request_body.description,
            "content_types": request_body.content_types,
            "schema": self._schema_to_dict(request_body.schema) if request_body.schema else None,
            "example": request_body.example
        }
    
    def _response_to_dict(self, response: Response) -> Dict[str, Any]:
        """Convierte una respuesta a diccionario"""
        return {
            "status_code": response.status_code,
            "description": response.description,
            "content_types": response.content_types,
            "schema": self._schema_to_dict(response.schema) if response.schema else None,
            "headers": [
                {
                    "name": header.name,
                    "type": header.type,
                    "required": header.required,
                    "description": header.description,
                    "format": header.format
                }
                for header in response.headers
            ],
            "example": response.example
        }
    
    def _schema_to_dict(self, schema: Schema) -> Dict[str, Any]:
        """Convierte un schema a diccionario"""
        return {
            "name": schema.name,
            "type": schema.type,
            "description": schema.description,
            "required": schema.required,
            "properties": [
                self._property_to_dict(prop)
                for prop in schema.properties
            ],
            "example": schema.example,
            "all_of": schema.all_of,
            "one_of": schema.one_of,
            "any_of": schema.any_of
        }
    
    def _property_to_dict(self, prop: Property) -> Dict[str, Any]:
        """Convierte una propiedad a diccionario"""
        return {
            "name": prop.name,
            "type": prop.type,
            "format": prop.format,
            "required": prop.required,
            "description": prop.description,
            "enum": prop.enum,
            "pattern": prop.pattern,
            "min_length": prop.min_length,
            "max_length": prop.max_length,
            "minimum": prop.minimum,
            "maximum": prop.maximum,
            "nullable": prop.nullable,
            "example": prop.example
        }
