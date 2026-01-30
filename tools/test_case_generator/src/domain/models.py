"""
Modelos de dominio para la generación de casos de prueba.
Siguiendo principios de Clean Architecture y SOLID.
"""
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from enum import Enum


class ISTQBTechnique(Enum):
    """Técnicas de prueba según ISTQB."""
    EQUIVALENCE_PARTITIONING = "equivalence_partitioning"
    BOUNDARY_VALUE_ANALYSIS = "boundary_value_analysis"
    DECISION_TABLE = "decision_table"
    STATE_TRANSITION = "state_transition"
    USE_CASE_TESTING = "use_case_testing"
    SYNTAX_TESTING = "syntax_testing"


class TestType(Enum):
    """Tipo de caso de prueba."""
    POSITIVE = "positive"
    NEGATIVE = "negative"


class Priority(Enum):
    """Prioridad del caso de prueba."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class TestData:
    """Datos de entrada para un caso de prueba."""
    headers: Dict[str, Any] = field(default_factory=dict)
    path_params: Dict[str, Any] = field(default_factory=dict)
    query_params: Dict[str, Any] = field(default_factory=dict)
    body: Optional[Dict[str, Any]] = None


@dataclass
class ExpectedResult:
    """Resultado esperado de un caso de prueba."""
    status_code: int
    response_schema: Optional[str] = None
    error_codes: List[str] = field(default_factory=list)
    description: str = ""


@dataclass
class TestCase:
    """Caso de prueba individual."""
    id: str
    name: str
    description: str
    technique: ISTQBTechnique
    test_type: TestType
    priority: Priority
    endpoint: str
    http_method: str
    preconditions: List[str] = field(default_factory=list)
    postconditions: List[str] = field(default_factory=list)
    test_data: TestData = field(default_factory=TestData)
    expected_result: ExpectedResult = field(default_factory=ExpectedResult)
    tags: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el caso de prueba a diccionario."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "technique": self.technique.value,
            "test_type": self.test_type.value,
            "priority": self.priority.value,
            "endpoint": self.endpoint,
            "http_method": self.http_method,
            "preconditions": self.preconditions,
            "postconditions": self.postconditions,
            "test_data": {
                "headers": self.test_data.headers,
                "path_params": self.test_data.path_params,
                "query_params": self.test_data.query_params,
                "body": self.test_data.body
            },
            "expected_result": {
                "status_code": self.expected_result.status_code,
                "response_schema": self.expected_result.response_schema,
                "error_codes": self.expected_result.error_codes,
                "description": self.expected_result.description
            },
            "tags": self.tags
        }


@dataclass
class TestSuite:
    """Suite de casos de prueba agrupados."""
    name: str
    description: str
    test_cases: List[TestCase] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def add_test_case(self, test_case: TestCase):
        """Agrega un caso de prueba a la suite."""
        self.test_cases.append(test_case)
    
    def get_by_technique(self, technique: ISTQBTechnique) -> List[TestCase]:
        """Obtiene casos de prueba por técnica."""
        return [tc for tc in self.test_cases if tc.technique == technique]
    
    def get_by_type(self, test_type: TestType) -> List[TestCase]:
        """Obtiene casos de prueba por tipo."""
        return [tc for tc in self.test_cases if tc.test_type == test_type]
    
    def get_by_priority(self, priority: Priority) -> List[TestCase]:
        """Obtiene casos de prueba por prioridad."""
        return [tc for tc in self.test_cases if tc.priority == priority]
    
    def get_by_endpoint(self, endpoint: str) -> List[TestCase]:
        """Obtiene casos de prueba por endpoint."""
        return [tc for tc in self.test_cases if tc.endpoint == endpoint]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte la suite a diccionario."""
        return {
            "name": self.name,
            "description": self.description,
            "metadata": self.metadata,
            "test_cases": [tc.to_dict() for tc in self.test_cases],
            "summary": {
                "total_test_cases": len(self.test_cases),
                "by_technique": self._count_by_technique(),
                "by_type": self._count_by_type(),
                "by_priority": self._count_by_priority()
            }
        }
    
    def _count_by_technique(self) -> Dict[str, int]:
        """Cuenta casos por técnica."""
        counts = {}
        for technique in ISTQBTechnique:
            count = len(self.get_by_technique(technique))
            if count > 0:
                counts[technique.value] = count
        return counts
    
    def _count_by_type(self) -> Dict[str, int]:
        """Cuenta casos por tipo."""
        return {
            TestType.POSITIVE.value: len(self.get_by_type(TestType.POSITIVE)),
            TestType.NEGATIVE.value: len(self.get_by_type(TestType.NEGATIVE))
        }
    
    def _count_by_priority(self) -> Dict[str, int]:
        """Cuenta casos por prioridad."""
        counts = {}
        for priority in Priority:
            count = len(self.get_by_priority(priority))
            if count > 0:
                counts[priority.value] = count
        return counts


@dataclass
class SwaggerEndpointData:
    """Datos extraídos de un endpoint de Swagger para generar casos de prueba."""
    path: str
    method: str
    operation_id: Optional[str]
    summary: Optional[str]
    description: Optional[str]
    tags: List[str]
    parameters: List[Dict[str, Any]]
    request_body: Optional[Dict[str, Any]]
    responses: Dict[str, Dict[str, Any]]
    
    def get_required_headers(self) -> List[Dict[str, Any]]:
        """Obtiene los headers requeridos."""
        return [p for p in self.parameters if p.get('in') == 'header' and p.get('required', False)]
    
    def get_path_params(self) -> List[Dict[str, Any]]:
        """Obtiene los parámetros de path."""
        return [p for p in self.parameters if p.get('in') == 'path']
    
    def get_query_params(self) -> List[Dict[str, Any]]:
        """Obtiene los parámetros de query."""
        return [p for p in self.parameters if p.get('in') == 'query']
    
    def get_success_responses(self) -> Dict[str, Dict[str, Any]]:
        """Obtiene las respuestas exitosas (2xx)."""
        return {code: resp for code, resp in self.responses.items() if code.startswith('2')}
    
    def get_error_responses(self) -> Dict[str, Dict[str, Any]]:
        """Obtiene las respuestas de error (4xx, 5xx)."""
        return {code: resp for code, resp in self.responses.items() if code.startswith('4') or code.startswith('5')}
