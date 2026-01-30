"""
Generador de casos de prueba usando Tabla de Decisión.
Prueba combinaciones de condiciones para validar reglas de negocio.
"""
from typing import List, Dict, Any
from itertools import product
from ..domain.models import (
    TestCase, SwaggerEndpointData, ISTQBTechnique,
    TestType, Priority, TestData, ExpectedResult
)
from ..domain.interfaces import ITestCaseGenerator, ISyntheticDataGenerator


class DecisionTableGenerator(ITestCaseGenerator):
    """Genera casos de prueba basados en Tabla de Decisión."""
    
    def __init__(self, data_generator: ISyntheticDataGenerator):
        self.data_generator = data_generator
        self._test_counter = 0
    
    def get_technique(self) -> ISTQBTechnique:
        return ISTQBTechnique.DECISION_TABLE
    
    def generate(self, endpoint_data: SwaggerEndpointData) -> List[TestCase]:
        """Genera casos de prueba basados en tabla de decisión."""
        test_cases = []
        
        # Generar tabla de decisión para headers requeridos
        required_headers = endpoint_data.get_required_headers()
        if len(required_headers) >= 2:
            # Limitar combinaciones para evitar explosión combinatoria
            test_cases.extend(self._generate_header_decision_table(endpoint_data, required_headers[:3]))
        
        return test_cases
    
    def _generate_header_decision_table(
        self, 
        endpoint_data: SwaggerEndpointData, 
        headers: List[Dict]
    ) -> List[TestCase]:
        """Genera casos de prueba para combinaciones de headers."""
        cases = []
        
        # Generar combinaciones: presente/ausente para cada header
        # True = presente y válido, False = ausente
        combinations = list(product([True, False], repeat=len(headers)))
        
        for combination in combinations:
            test_case = self._create_decision_table_case(
                endpoint_data,
                headers,
                combination
            )
            cases.append(test_case)
        
        return cases
    
    def _create_decision_table_case(
        self,
        endpoint_data: SwaggerEndpointData,
        headers: List[Dict],
        combination: tuple
    ) -> TestCase:
        """Crea un caso de prueba para una combinación específica."""
        self._test_counter += 1
        test_id = f"DT-{self._test_counter:03d}"
        
        test_data = TestData()
        missing_headers = []
        
        # Configurar headers según la combinación
        for header, is_present in zip(headers, combination):
            if is_present:
                test_data.headers[header['name']] = self.data_generator.generate_valid_value(header)
            else:
                missing_headers.append(header['name'])
        
        # Agregar headers restantes que no están en la tabla de decisión
        all_required_headers = endpoint_data.get_required_headers()
        for header in all_required_headers:
            if header not in headers and header['name'] not in test_data.headers:
                test_data.headers[header['name']] = self.data_generator.generate_valid_value(header)
        
        # Configurar path params
        for param in endpoint_data.get_path_params():
            test_data.path_params[param['name']] = self.data_generator.generate_valid_value(param)
        
        # Determinar si es caso positivo o negativo
        is_valid = all(combination)
        test_type = TestType.POSITIVE if is_valid else TestType.NEGATIVE
        expected_status = self._determine_expected_status(endpoint_data, is_valid)
        
        # Crear descripción de la combinación
        combo_desc = ", ".join([
            f"{h['name']}={'✓' if p else '✗'}" 
            for h, p in zip(headers, combination)
        ])
        
        return TestCase(
            id=test_id,
            name=f"Tabla decisión - {combo_desc}",
            description=f"Verifica el comportamiento con la combinación: {combo_desc}" + 
                       (f". Headers faltantes: {', '.join(missing_headers)}" if missing_headers else ""),
            technique=self.get_technique(),
            test_type=test_type,
            priority=Priority.MEDIUM if is_valid else Priority.HIGH,
            endpoint=endpoint_data.path,
            http_method=endpoint_data.method,
            preconditions=["API disponible"],
            postconditions=[f"El endpoint retorna código {expected_status}"],
            test_data=test_data,
            expected_result=ExpectedResult(
                status_code=expected_status,
                description=f"{'Respuesta exitosa' if is_valid else 'Error por headers faltantes'}"
            ),
            tags=endpoint_data.tags + ["decision_table", test_type.value]
        )
    
    def _determine_expected_status(self, endpoint_data: SwaggerEndpointData, is_valid: bool) -> int:
        """Determina el código de estado esperado dinámicamente."""
        if is_valid:
            success_responses = endpoint_data.get_success_responses()
            return int(list(success_responses.keys())[0]) if success_responses else 200
        
        error_responses = endpoint_data.get_error_responses()
        return int(list(error_responses.keys())[0]) if error_responses else 400
