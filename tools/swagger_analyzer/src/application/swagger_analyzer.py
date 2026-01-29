"""
Servicio de análisis de contratos Swagger/OpenAPI
Implementa la lógica de negocio para analizar contratos
"""
from typing import Dict, Any, List, Optional
from ..domain.interfaces import IContractAnalyzer
from ..domain.models import (
    AnalysisResult, SwaggerContract, Endpoint, Server, Schema, 
    RequestBody, Response, Parameter, Header, Property, HttpMethod
)


class SwaggerContractAnalyzer(IContractAnalyzer):
    """Analizador de contratos Swagger 2.0 y OpenAPI 3.x"""
    
    def analyze(self, contract_dict: Dict[str, Any]) -> AnalysisResult:
        """
        Analiza el contrato y extrae toda la información relevante
        
        Args:
            contract_dict: Diccionario con la estructura del contrato
            
        Returns:
            Resultado del análisis con toda la información extraída
        """
        warnings = []
        errors = []
        
        # Validar que sea un contrato válido
        if not self._is_valid_contract(contract_dict):
            errors.append("El contrato no tiene una estructura válida de Swagger/OpenAPI")
            return self._create_error_result(errors)
        
        # Determinar versión
        openapi_version = contract_dict.get('openapi')
        swagger_version = contract_dict.get('swagger')
        
        # Extraer información básica
        info = contract_dict.get('info', {})
        title = info.get('title', 'Sin título')
        version = info.get('version', 'Sin versión')
        description = info.get('description')
        
        # Extraer servers
        servers = self._extract_servers(contract_dict, openapi_version)
        
        # Extraer schemas
        schemas = self._extract_schemas(contract_dict, openapi_version)
        
        # Extraer endpoints
        endpoints = self._extract_endpoints(contract_dict, openapi_version, warnings)
        
        # Extraer security schemes
        security_schemes = self._extract_security_schemes(contract_dict, openapi_version)
        
        # Extraer tags
        tags = contract_dict.get('tags', [])
        
        # Extraer external docs
        external_docs = contract_dict.get('externalDocs')
        
        # Crear el contrato
        contract = SwaggerContract(
            title=title,
            version=version,
            openapi_version=openapi_version,
            swagger_version=swagger_version,
            description=description,
            servers=servers,
            endpoints=endpoints,
            schemas=schemas,
            security_schemes=security_schemes,
            tags=tags,
            external_docs=external_docs
        )
        
        # Calcular métricas
        total_endpoints = len(endpoints)
        methods_summary = self._calculate_methods_summary(endpoints)
        total_schemas = len(schemas)
        status_codes_summary = self._calculate_status_codes_summary(endpoints)
        has_security = len(security_schemes) > 0
        content_types = self._extract_content_types(endpoints)
        
        return AnalysisResult(
            contract=contract,
            total_endpoints=total_endpoints,
            methods_summary=methods_summary,
            total_schemas=total_schemas,
            status_codes_summary=status_codes_summary,
            has_security=has_security,
            content_types=content_types,
            warnings=warnings,
            errors=errors
        )
    
    def _is_valid_contract(self, contract_dict: Dict[str, Any]) -> bool:
        """Valida que el diccionario sea un contrato Swagger/OpenAPI válido"""
        has_openapi = 'openapi' in contract_dict
        has_swagger = 'swagger' in contract_dict
        has_info = 'info' in contract_dict
        has_paths = 'paths' in contract_dict
        
        return (has_openapi or has_swagger) and has_info and has_paths
    
    def _extract_servers(self, contract_dict: Dict[str, Any], openapi_version: Optional[str]) -> List[Server]:
        """Extrae la información de servidores"""
        servers = []
        
        if openapi_version:  # OpenAPI 3.x
            servers_list = contract_dict.get('servers', [])
            for server_dict in servers_list:
                servers.append(Server(
                    url=server_dict.get('url', ''),
                    description=server_dict.get('description'),
                    variables=server_dict.get('variables', {})
                ))
        else:  # Swagger 2.0
            schemes = contract_dict.get('schemes', ['http'])
            host = contract_dict.get('host', '')
            base_path = contract_dict.get('basePath', '')
            
            if host:
                for scheme in schemes:
                    url = f"{scheme}://{host}{base_path}"
                    servers.append(Server(url=url))
        
        return servers
    
    def _extract_schemas(self, contract_dict: Dict[str, Any], openapi_version: Optional[str]) -> List[Schema]:
        """Extrae los schemas/definiciones"""
        schemas = []
        
        if openapi_version:  # OpenAPI 3.x
            components = contract_dict.get('components', {})
            schemas_dict = components.get('schemas', {})
        else:  # Swagger 2.0
            schemas_dict = contract_dict.get('definitions', {})
        
        for schema_name, schema_data in schemas_dict.items():
            schema = self._parse_schema(schema_name, schema_data)
            schemas.append(schema)
        
        return schemas
    
    def _parse_schema(self, name: str, schema_data: Dict[str, Any]) -> Schema:
        """Parsea un schema individual"""
        properties = []
        required_fields = schema_data.get('required', [])
        
        props_dict = schema_data.get('properties', {})
        for prop_name, prop_data in props_dict.items():
            prop = Property(
                name=prop_name,
                type=prop_data.get('type'),
                format=prop_data.get('format'),
                required=prop_name in required_fields,
                description=prop_data.get('description'),
                enum=prop_data.get('enum'),
                pattern=prop_data.get('pattern'),
                min_length=prop_data.get('minLength'),
                max_length=prop_data.get('maxLength'),
                minimum=prop_data.get('minimum'),
                maximum=prop_data.get('maximum'),
                items=prop_data.get('items'),
                properties=prop_data.get('properties'),
                example=prop_data.get('example'),
                nullable=prop_data.get('nullable', False)
            )
            properties.append(prop)
        
        return Schema(
            name=name,
            type=schema_data.get('type'),
            properties=properties,
            required=required_fields,
            description=schema_data.get('description'),
            example=schema_data.get('example'),
            all_of=schema_data.get('allOf'),
            one_of=schema_data.get('oneOf'),
            any_of=schema_data.get('anyOf')
        )
    
    def _extract_endpoints(self, contract_dict: Dict[str, Any], 
                          openapi_version: Optional[str], warnings: List[str]) -> List[Endpoint]:
        """Extrae todos los endpoints de la API"""
        endpoints = []
        paths = contract_dict.get('paths', {})
        
        for path, path_item in paths.items():
            if not isinstance(path_item, dict):
                continue
            
            # Parámetros comunes a todos los métodos del path
            common_parameters = path_item.get('parameters', [])
            
            for method in ['get', 'post', 'put', 'delete', 'patch', 'options', 'head']:
                if method not in path_item:
                    continue
                
                operation = path_item[method]
                if not isinstance(operation, dict):
                    continue
                
                try:
                    http_method = HttpMethod[method.upper()]
                except KeyError:
                    warnings.append(f"Método HTTP no soportado: {method}")
                    continue
                
                # Extraer parámetros
                parameters = self._extract_parameters(
                    operation.get('parameters', []) + common_parameters
                )
                
                # Extraer request body
                request_body = self._extract_request_body(operation, openapi_version)
                
                # Extraer responses
                responses = self._extract_responses(operation.get('responses', {}), openapi_version)
                
                endpoint = Endpoint(
                    path=path,
                    method=http_method,
                    operation_id=operation.get('operationId'),
                    summary=operation.get('summary'),
                    description=operation.get('description'),
                    tags=operation.get('tags', []),
                    parameters=parameters,
                    request_body=request_body,
                    responses=responses,
                    deprecated=operation.get('deprecated', False),
                    security=operation.get('security', [])
                )
                endpoints.append(endpoint)
        
        return endpoints
    
    def _extract_parameters(self, params_list: List[Dict[str, Any]]) -> List[Parameter]:
        """Extrae parámetros de un endpoint"""
        parameters = []
        
        for param in params_list:
            if not isinstance(param, dict):
                continue
            
            # Manejar referencias
            if '$ref' in param:
                continue  # Por simplicidad, no resolvemos referencias aquí
            
            schema = param.get('schema', {})
            
            parameter = Parameter(
                name=param.get('name', ''),
                location=param.get('in', ''),
                required=param.get('required', False),
                type=param.get('type') or schema.get('type'),
                format=param.get('format') or schema.get('format'),
                description=param.get('description'),
                schema=schema if schema else None,
                example=param.get('example')
            )
            parameters.append(parameter)
        
        return parameters
    
    def _extract_request_body(self, operation: Dict[str, Any], 
                             openapi_version: Optional[str]) -> Optional[RequestBody]:
        """Extrae el request body de un endpoint"""
        if openapi_version:  # OpenAPI 3.x
            request_body_data = operation.get('requestBody')
            if not request_body_data:
                return None
            
            content = request_body_data.get('content', {})
            content_types = list(content.keys())
            
            # Tomar el primer content type para extraer el schema
            schema = None
            if content_types:
                first_content = content[content_types[0]]
                schema_data = first_content.get('schema', {})
                if schema_data:
                    schema = self._parse_schema('RequestBody', schema_data)
            
            return RequestBody(
                required=request_body_data.get('required', False),
                content_types=content_types,
                schema=schema,
                description=request_body_data.get('description'),
                example=request_body_data.get('example')
            )
        else:  # Swagger 2.0
            # En Swagger 2.0, el body está en parameters
            body_params = [p for p in operation.get('parameters', []) 
                          if p.get('in') == 'body']
            
            if not body_params:
                return None
            
            body_param = body_params[0]
            schema_data = body_param.get('schema', {})
            schema = None
            if schema_data:
                schema = self._parse_schema('RequestBody', schema_data)
            
            consumes = operation.get('consumes', [])
            
            return RequestBody(
                required=body_param.get('required', False),
                content_types=consumes,
                schema=schema,
                description=body_param.get('description')
            )
    
    def _extract_responses(self, responses_dict: Dict[str, Any], 
                          openapi_version: Optional[str]) -> List[Response]:
        """Extrae las respuestas de un endpoint"""
        responses = []
        
        for status_code, response_data in responses_dict.items():
            if not isinstance(response_data, dict):
                continue
            
            content_types = []
            schema = None
            headers = []
            
            if openapi_version:  # OpenAPI 3.x
                content = response_data.get('content', {})
                content_types = list(content.keys())
                
                # Extraer schema del primer content type
                if content_types:
                    first_content = content[content_types[0]]
                    schema_data = first_content.get('schema', {})
                    if schema_data:
                        schema = self._parse_schema(f'Response{status_code}', schema_data)
                
                # Extraer headers
                headers_dict = response_data.get('headers', {})
                for header_name, header_data in headers_dict.items():
                    header = Header(
                        name=header_name,
                        required=header_data.get('required', False),
                        type=header_data.get('schema', {}).get('type'),
                        description=header_data.get('description'),
                        format=header_data.get('schema', {}).get('format')
                    )
                    headers.append(header)
            else:  # Swagger 2.0
                schema_data = response_data.get('schema', {})
                if schema_data:
                    schema = self._parse_schema(f'Response{status_code}', schema_data)
                
                # Headers en Swagger 2.0
                headers_dict = response_data.get('headers', {})
                for header_name, header_data in headers_dict.items():
                    header = Header(
                        name=header_name,
                        type=header_data.get('type'),
                        description=header_data.get('description'),
                        format=header_data.get('format')
                    )
                    headers.append(header)
            
            response = Response(
                status_code=str(status_code),
                description=response_data.get('description'),
                content_types=content_types,
                schema=schema,
                headers=headers,
                example=response_data.get('example')
            )
            responses.append(response)
        
        return responses
    
    def _extract_security_schemes(self, contract_dict: Dict[str, Any], 
                                  openapi_version: Optional[str]) -> Dict[str, Any]:
        """Extrae los esquemas de seguridad"""
        if openapi_version:  # OpenAPI 3.x
            components = contract_dict.get('components', {})
            return components.get('securitySchemes', {})
        else:  # Swagger 2.0
            return contract_dict.get('securityDefinitions', {})
    
    def _calculate_methods_summary(self, endpoints: List[Endpoint]) -> Dict[str, int]:
        """Calcula un resumen de métodos HTTP utilizados"""
        summary = {}
        for endpoint in endpoints:
            method = endpoint.method.value
            summary[method] = summary.get(method, 0) + 1
        return summary
    
    def _calculate_status_codes_summary(self, endpoints: List[Endpoint]) -> Dict[str, int]:
        """Calcula un resumen de códigos de estado HTTP"""
        summary = {}
        for endpoint in endpoints:
            for response in endpoint.responses:
                code = response.status_code
                summary[code] = summary.get(code, 0) + 1
        return summary
    
    def _extract_content_types(self, endpoints: List[Endpoint]) -> List[str]:
        """Extrae todos los content types utilizados"""
        content_types = set()
        
        for endpoint in endpoints:
            if endpoint.request_body:
                content_types.update(endpoint.request_body.content_types)
            
            for response in endpoint.responses:
                content_types.update(response.content_types)
        
        return sorted(list(content_types))
    
    def _create_error_result(self, errors: List[str]) -> AnalysisResult:
        """Crea un resultado de análisis con errores"""
        empty_contract = SwaggerContract(
            title="Error",
            version="0.0.0"
        )
        
        return AnalysisResult(
            contract=empty_contract,
            total_endpoints=0,
            methods_summary={},
            total_schemas=0,
            status_codes_summary={},
            has_security=False,
            content_types=[],
            errors=errors
        )
