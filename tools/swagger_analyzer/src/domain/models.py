"""
Domain models - Entidades del dominio para representar contratos Swagger/OpenAPI
Estas clases representan la estructura de un contrato API sin depender de frameworks externos
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum


class HttpMethod(Enum):
    """Métodos HTTP soportados"""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    OPTIONS = "OPTIONS"
    HEAD = "HEAD"


class DataType(Enum):
    """Tipos de datos en OpenAPI"""
    STRING = "string"
    NUMBER = "number"
    INTEGER = "integer"
    BOOLEAN = "boolean"
    ARRAY = "array"
    OBJECT = "object"


@dataclass
class Server:
    """Representa un servidor definido en el contrato"""
    url: str
    description: Optional[str] = None
    variables: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Header:
    """Representa un header HTTP"""
    name: str
    required: bool = False
    type: Optional[str] = None
    description: Optional[str] = None
    format: Optional[str] = None
    example: Optional[Any] = None


@dataclass
class Parameter:
    """Representa un parámetro (path, query, header, cookie)"""
    name: str
    location: str  # path, query, header, cookie
    required: bool = False
    type: Optional[str] = None
    format: Optional[str] = None
    description: Optional[str] = None
    schema: Optional[Dict[str, Any]] = None
    example: Optional[Any] = None


@dataclass
class Property:
    """Representa una propiedad de un schema"""
    name: str
    type: Optional[str] = None
    format: Optional[str] = None
    required: bool = False
    description: Optional[str] = None
    enum: Optional[List[Any]] = None
    pattern: Optional[str] = None
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    minimum: Optional[float] = None
    maximum: Optional[float] = None
    items: Optional[Dict[str, Any]] = None
    properties: Optional[Dict[str, Any]] = None
    example: Optional[Any] = None
    nullable: bool = False


@dataclass
class Schema:
    """Representa un schema de datos"""
    name: str
    type: Optional[str] = None
    properties: List[Property] = field(default_factory=list)
    required: List[str] = field(default_factory=list)
    description: Optional[str] = None
    example: Optional[Any] = None
    all_of: Optional[List[Dict]] = None
    one_of: Optional[List[Dict]] = None
    any_of: Optional[List[Dict]] = None


@dataclass
class RequestBody:
    """Representa el cuerpo de una petición"""
    required: bool = False
    content_types: List[str] = field(default_factory=list)
    schema: Optional[Schema] = None
    description: Optional[str] = None
    example: Optional[Any] = None


@dataclass
class Response:
    """Representa una respuesta HTTP"""
    status_code: str
    description: Optional[str] = None
    content_types: List[str] = field(default_factory=list)
    schema: Optional[Schema] = None
    headers: List[Header] = field(default_factory=list)
    example: Optional[Any] = None


@dataclass
class Endpoint:
    """Representa un endpoint de la API"""
    path: str
    method: HttpMethod
    operation_id: Optional[str] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    parameters: List[Parameter] = field(default_factory=list)
    request_body: Optional[RequestBody] = None
    responses: List[Response] = field(default_factory=list)
    deprecated: bool = False
    security: List[Dict[str, List[str]]] = field(default_factory=list)


@dataclass
class SwaggerContract:
    """Representa el contrato completo de Swagger/OpenAPI"""
    title: str
    version: str
    openapi_version: Optional[str] = None
    swagger_version: Optional[str] = None
    description: Optional[str] = None
    servers: List[Server] = field(default_factory=list)
    endpoints: List[Endpoint] = field(default_factory=list)
    schemas: List[Schema] = field(default_factory=list)
    security_schemes: Dict[str, Any] = field(default_factory=dict)
    tags: List[Dict[str, str]] = field(default_factory=list)
    external_docs: Optional[Dict[str, str]] = None


@dataclass
class AnalysisResult:
    """Resultado del análisis del contrato"""
    contract: SwaggerContract
    total_endpoints: int
    methods_summary: Dict[str, int]
    total_schemas: int
    status_codes_summary: Dict[str, int]
    has_security: bool
    content_types: List[str]
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
