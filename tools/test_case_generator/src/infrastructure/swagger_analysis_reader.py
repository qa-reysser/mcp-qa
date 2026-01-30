"""
Lector del análisis de Swagger generado por la herramienta swagger_analyzer.
Lee y parsea el archivo JSON de forma dinámica sin asumir estructura específica.
"""
import json
from typing import Dict, Any, List, Optional
from ..domain.interfaces import ISwaggerAnalysisReader
from ..domain.models import SwaggerEndpointData


class SwaggerAnalysisJsonReader(ISwaggerAnalysisReader):
    """Lee el JSON de análisis de Swagger y extrae datos de endpoints."""
    
    def read_analysis(self, file_path: str) -> Dict[str, Any]:
        """Lee el archivo JSON de análisis."""
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def extract_endpoints(self, analysis: Dict[str, Any]) -> List[SwaggerEndpointData]:
        """Extrae los datos de endpoints del análisis."""
        endpoints_data = []
        
        endpoints = analysis.get('endpoints', [])
        schemas = analysis.get('schemas', [])
        
        for endpoint in endpoints:
            endpoint_data = SwaggerEndpointData(
                path=endpoint.get('path', ''),
                method=endpoint.get('method', ''),
                operation_id=endpoint.get('operation_id'),
                summary=endpoint.get('summary'),
                description=endpoint.get('description'),
                tags=endpoint.get('tags', []),
                parameters=self._extract_parameters(endpoint.get('parameters', [])),
                request_body=self._extract_request_body(endpoint.get('request_body'), schemas),
                responses=self._extract_responses(endpoint.get('responses', []))
            )
            endpoints_data.append(endpoint_data)
        
        return endpoints_data
    
    def _extract_parameters(self, parameters: List[Dict]) -> List[Dict[str, Any]]:
        """Extrae y normaliza los parámetros."""
        normalized_params = []
        
        for param in parameters:
            normalized = {
                'name': param.get('name', ''),
                'in': param.get('location', ''),  # header, path, query
                'required': param.get('required', False),
                'type': param.get('type', 'string'),
                'format': param.get('format'),
                'description': param.get('description', ''),
                'schema': param.get('schema', {}),
                'example': param.get('example')
            }
            
            # Agregar schema si no existe, usando datos del parámetro
            if not normalized['schema']:
                normalized['schema'] = {
                    'type': param.get('type', 'string'),
                    'format': param.get('format'),
                    'example': param.get('example')
                }
            
            normalized_params.append(normalized)
        
        return normalized_params
    
    def _extract_request_body(
        self, 
        request_body: Optional[Dict], 
        schemas: List[Dict]
    ) -> Optional[Dict[str, Any]]:
        """Extrae y enriquece el request body con información de schemas."""
        if not request_body:
            return None
        
        body_schema = request_body.get('schema', {})
        schema_name = body_schema.get('name')
        
        # Buscar el schema completo en la lista de schemas
        full_schema = None
        if schema_name:
            for schema in schemas:
                if schema.get('name') == schema_name:
                    full_schema = schema
                    break
        
        return {
            'required': request_body.get('required', False),
            'description': request_body.get('description', ''),
            'content_types': request_body.get('content_types', ['application/json']),
            'schema': full_schema if full_schema else body_schema,
            'example': request_body.get('example')
        }
    
    def _extract_responses(self, responses: List[Dict]) -> Dict[str, Dict[str, Any]]:
        """Extrae las respuestas y las organiza por código de estado."""
        responses_dict = {}
        
        for response in responses:
            status_code = str(response.get('status_code', '200'))
            responses_dict[status_code] = {
                'description': response.get('description', ''),
                'content_types': response.get('content_types', []),
                'schema': response.get('schema', {}),
                'headers': response.get('headers', []),
                'example': response.get('example')
            }
        
        return responses_dict
