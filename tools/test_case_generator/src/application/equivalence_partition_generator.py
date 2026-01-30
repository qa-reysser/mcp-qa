"""
Generador de casos de prueba usando Partición de Equivalencia.
Divide los datos de entrada en clases de equivalencia válidas e inválidas.
"""
from typing import List, Dict, Any
from ..domain.models import (
    TestCase, SwaggerEndpointData, ISTQBTechnique, 
    TestType, Priority, TestData, ExpectedResult
)
from ..domain.interfaces import ITestCaseGenerator, ISyntheticDataGenerator


class EquivalencePartitioningGenerator(ITestCaseGenerator):
    """Genera casos de prueba basados en Partición de Equivalencia de forma completamente dinámica."""
    
    def __init__(self, data_generator: ISyntheticDataGenerator):
        self.data_generator = data_generator
        self._test_counter = 0
    
    def get_technique(self) -> ISTQBTechnique:
        return ISTQBTechnique.EQUIVALENCE_PARTITIONING
    
    def generate(self, endpoint_data: SwaggerEndpointData) -> List[TestCase]:
        """Genera casos de prueba de partición de equivalencia."""
        test_cases = []
        
        # Caso positivo: todos los valores válidos
        test_cases.append(self._generate_all_valid_case(endpoint_data))
        
        # Casos negativos: headers faltantes
        for header in endpoint_data.get_required_headers():
            test_cases.append(self._generate_missing_param_case(endpoint_data, header, 'header'))
        
        # Casos negativos: headers con formato inválido
        for header in endpoint_data.get_required_headers():
            if header.get('format'):  # Solo si tiene formato específico
                test_cases.append(self._generate_invalid_format_case(endpoint_data, header, 'header'))
        
        # Casos negativos: body vacío si es requerido
        if endpoint_data.request_body and endpoint_data.request_body.get('required'):
            test_cases.append(self._generate_empty_body_case(endpoint_data))
        
        return test_cases
    
    def _generate_all_valid_case(self, endpoint_data: SwaggerEndpointData) -> TestCase:
        """Genera un caso con todos los valores válidos."""
        self._test_counter += 1
        test_data = self._populate_valid_test_data(endpoint_data)
        success_code = self._get_first_success_code(endpoint_data)
        
        return TestCase(
            id=f"EP-{self._test_counter:03d}",
            name=f"Partición válida - {endpoint_data.method} {endpoint_data.path}",
            description=f"Verifica que el endpoint responda correctamente con todos los valores en particiones válidas",
            technique=self.get_technique(),
            test_type=TestType.POSITIVE,
            priority=Priority.HIGH,
            endpoint=endpoint_data.path,
            http_method=endpoint_data.method,
            preconditions=["API disponible y accesible"],
            postconditions=[f"El endpoint retorna código {success_code}"],
            test_data=test_data,
            expected_result=ExpectedResult(
                status_code=success_code,
                description=f"Respuesta exitosa con código {success_code}"
            ),
            tags=endpoint_data.tags + ["equivalence_partitioning", "positive"]
        )
    
    def _generate_missing_param_case(
        self, 
        endpoint_data: SwaggerEndpointData, 
        param: Dict, 
        param_location: str
    ) -> TestCase:
        """Genera caso con un parámetro faltante."""
        self._test_counter += 1
        test_data = self._populate_valid_test_data(endpoint_data, exclude_param={
            'name': param['name'],
            'location': param_location
        })
        error_code = self._get_first_error_code(endpoint_data)
        
        return TestCase(
            id=f"EP-{self._test_counter:03d}",
            name=f"Partición inválida - {param['name']} faltante",
            description=f"Verifica que el endpoint rechace la solicitud cuando falta el parámetro '{param['name']}'",
            technique=self.get_technique(),
            test_type=TestType.NEGATIVE,
            priority=Priority.HIGH,
            endpoint=endpoint_data.path,
            http_method=endpoint_data.method,
            preconditions=["API disponible"],
            postconditions=[f"El endpoint retorna error {error_code}"],
            test_data=test_data,
            expected_result=ExpectedResult(
                status_code=error_code,
                description=f"Error por parámetro '{param['name']}' faltante"
            ),
            tags=endpoint_data.tags + ["equivalence_partitioning", "negative", "missing_param"]
        )
    
    def _generate_invalid_format_case(
        self, 
        endpoint_data: SwaggerEndpointData, 
        param: Dict, 
        param_location: str
    ) -> TestCase:
        """Genera caso con formato inválido."""
        self._test_counter += 1
        test_data = self._populate_valid_test_data(endpoint_data, invalid_param={
            'name': param['name'],
            'location': param_location,
            'data': param
        })
        error_code = self._get_first_error_code(endpoint_data)
        
        return TestCase(
            id=f"EP-{self._test_counter:03d}",
            name=f"Partición inválida - {param['name']} con formato inválido",
            description=f"Verifica que el endpoint rechace cuando '{param['name']}' tiene formato inválido",
            technique=self.get_technique(),
            test_type=TestType.NEGATIVE,
            priority=Priority.MEDIUM,
            endpoint=endpoint_data.path,
            http_method=endpoint_data.method,
            preconditions=["API disponible"],
            postconditions=[f"El endpoint retorna error {error_code}"],
            test_data=test_data,
            expected_result=ExpectedResult(
                status_code=error_code,
                description=f"Error por formato inválido en '{param['name']}'"
            ),
            tags=endpoint_data.tags + ["equivalence_partitioning", "negative", "invalid_format"]
        )
    
    def _generate_empty_body_case(self, endpoint_data: SwaggerEndpointData) -> TestCase:
        """Genera caso con body vacío."""
        self._test_counter += 1
        test_data = self._populate_valid_test_data(endpoint_data)
        test_data.body = {}
        error_code = self._get_first_error_code(endpoint_data)
        
        return TestCase(
            id=f"EP-{self._test_counter:03d}",
            name="Partición inválida - Body vacío",
            description="Verifica que el endpoint rechace la solicitud con body vacío",
            technique=self.get_technique(),
            test_type=TestType.NEGATIVE,
            priority=Priority.HIGH,
            endpoint=endpoint_data.path,
            http_method=endpoint_data.method,
            preconditions=["API disponible"],
            postconditions=[f"El endpoint retorna error {error_code}"],
            test_data=test_data,
            expected_result=ExpectedResult(
                status_code=error_code,
                description="Error por body vacío o campos requeridos faltantes"
            ),
            tags=endpoint_data.tags + ["equivalence_partitioning", "negative", "empty_body"]
        )
    
    def _populate_valid_test_data(
        self, 
        endpoint_data: SwaggerEndpointData,
        exclude_param: Dict[str, str] = None,
        invalid_param: Dict[str, Any] = None
    ) -> TestData:
        """Genera test data completo, permitiendo exclusiones o invalidaciones."""
        test_data = TestData()
        
        # Headers
        for header in endpoint_data.get_required_headers():
            if exclude_param and header['name'] == exclude_param.get('name') and exclude_param.get('location') == 'header':
                continue
            if invalid_param and header['name'] == invalid_param.get('name') and invalid_param.get('location') == 'header':
                test_data.headers[header['name']] = self.data_generator.generate_invalid_value(
                    invalid_param['data'], 
                    "invalid_format"
                )
            else:
                test_data.headers[header['name']] = self.data_generator.generate_valid_value(header)
        
        # Path params
        for param in endpoint_data.get_path_params():
            if exclude_param and param['name'] == exclude_param.get('name') and exclude_param.get('location') == 'path':
                continue
            test_data.path_params[param['name']] = self.data_generator.generate_valid_value(param)
        
        # Query params
        for param in endpoint_data.get_query_params():
            if param.get('required', False):
                if exclude_param and param['name'] == exclude_param.get('name') and exclude_param.get('location') == 'query':
                    continue
                test_data.query_params[param['name']] = self.data_generator.generate_valid_value(param)
        
        # Body
        if endpoint_data.request_body and endpoint_data.request_body.get('required'):
            schema = endpoint_data.request_body.get('schema', {})
            test_data.body = self.data_generator.generate_valid_value({'schema': schema})
        
        return test_data
    
    def _get_first_success_code(self, endpoint_data: SwaggerEndpointData) -> int:
        """Obtiene el primer código de éxito dinámicamente."""
        success_responses = endpoint_data.get_success_responses()
        if success_responses:
            return int(list(success_responses.keys())[0])
        return 200
    
    def _get_first_error_code(self, endpoint_data: SwaggerEndpointData) -> int:
        """Obtiene el primer código de error dinámicamente."""
        error_responses = endpoint_data.get_error_responses()
        if error_responses:
            return int(list(error_responses.keys())[0])
        return 400

