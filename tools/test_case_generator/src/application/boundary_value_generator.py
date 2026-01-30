"""
Generador de casos de prueba usando Análisis de Valores Límite.
Prueba los valores en los límites de las particiones de equivalencia.
"""
from typing import List, Any, Dict
from ..domain.models import (
    TestCase, SwaggerEndpointData, ISTQBTechnique,
    TestType, Priority, TestData, ExpectedResult
)
from ..domain.interfaces import ITestCaseGenerator, ISyntheticDataGenerator


class BoundaryValueGenerator(ITestCaseGenerator):
    """Genera casos de prueba basados en Análisis de Valores Límite de forma completamente dinámica."""
    
    def __init__(self, data_generator: ISyntheticDataGenerator):
        self.data_generator = data_generator
        self._test_counter = 0
    
    def get_technique(self) -> ISTQBTechnique:
        return ISTQBTechnique.BOUNDARY_VALUE_ANALYSIS
    
    def generate(self, endpoint_data: SwaggerEndpointData) -> List[TestCase]:
        """Genera casos de prueba de valores límite."""
        test_cases = []
        
        # Generar casos para cada parámetro con límites
        for param in endpoint_data.parameters:
            if self._has_boundaries(param):
                test_cases.extend(self._generate_param_boundary_cases(endpoint_data, param))
        
        # Casos para request body (si tiene constraints)
        if endpoint_data.request_body:
            schema = endpoint_data.request_body.get('schema', {})
            properties = schema.get('properties', [])
            for prop in properties:
                if self._property_has_boundaries(prop):
                    test_cases.extend(self._generate_property_boundary_cases(endpoint_data, schema, prop))
        
        return test_cases
    
    def _has_boundaries(self, param: Dict[str, Any]) -> bool:
        """Verifica si un parámetro tiene límites definidos."""
        schema = param.get('schema', {})
        return (
            'minLength' in schema or 'maxLength' in schema or
            'minimum' in schema or 'maximum' in schema or
            'minItems' in schema or 'maxItems' in schema
        )
    
    def _property_has_boundaries(self, prop: Dict[str, Any]) -> bool:
        """Verifica si una propiedad tiene límites definidos."""
        return (
            prop.get('min_length') is not None or 
            prop.get('minLength') is not None or
            prop.get('max_length') is not None or 
            prop.get('maxLength') is not None or
            prop.get('minimum') is not None or
            prop.get('maximum') is not None
        )
    
    def _generate_param_boundary_cases(
        self, 
        endpoint_data: SwaggerEndpointData, 
        param: Dict
    ) -> List[TestCase]:
        """Genera casos de prueba para los límites de un parámetro."""
        cases = []
        boundary_values = self.data_generator.generate_boundary_values(param)
        
        for boundary_value in boundary_values:
            is_valid = self._is_valid_boundary_value(param, boundary_value)
            cases.append(self._create_param_boundary_case(
                endpoint_data, 
                param, 
                boundary_value, 
                is_valid
            ))
        
        return cases
    
    def _generate_property_boundary_cases(
        self,
        endpoint_data: SwaggerEndpointData,
        schema: Dict,
        prop: Dict
    ) -> List[TestCase]:
        """Genera casos de valores límite para una propiedad del body."""
        cases = []
        prop_name = prop.get('name', '')
        min_length = prop.get('min_length', prop.get('minLength'))
        max_length = prop.get('max_length', prop.get('maxLength'))
        minimum = prop.get('minimum')
        maximum = prop.get('maximum')
        
        # Generar casos para límites de longitud (strings)
        if min_length is not None:
            # Valor en el mínimo (válido)
            cases.append(self._create_property_boundary_case(
                endpoint_data, schema, prop_name, min_length, True, "min_length"
            ))
            # Valor debajo del mínimo (inválido)
            if min_length > 0:
                cases.append(self._create_property_boundary_case(
                    endpoint_data, schema, prop_name, min_length - 1, False, "below_min"
                ))
        
        if max_length is not None:
            # Valor en el máximo (válido)
            cases.append(self._create_property_boundary_case(
                endpoint_data, schema, prop_name, max_length, True, "max_length"
            ))
            # Valor encima del máximo (inválido)
            cases.append(self._create_property_boundary_case(
                endpoint_data, schema, prop_name, max_length + 1, False, "above_max"
            ))
        
        # Generar casos para límites numéricos
        if minimum is not None:
            cases.append(self._create_numeric_property_case(
                endpoint_data, schema, prop_name, minimum, True, "minimum"
            ))
            cases.append(self._create_numeric_property_case(
                endpoint_data, schema, prop_name, minimum - 1, False, "below_min"
            ))
        
        if maximum is not None:
            cases.append(self._create_numeric_property_case(
                endpoint_data, schema, prop_name, maximum, True, "maximum"
            ))
            cases.append(self._create_numeric_property_case(
                endpoint_data, schema, prop_name, maximum + 1, False, "above_max"
            ))
        
        return cases
    
    def _create_param_boundary_case(
        self, 
        endpoint_data: SwaggerEndpointData, 
        param: Dict, 
        boundary_value: Any,
        is_valid: bool
    ) -> TestCase:
        """Crea un caso de prueba para un valor límite de parámetro."""
        self._test_counter += 1
        test_data = self._create_valid_test_data(endpoint_data, {param['name']: boundary_value}, param.get('in'))
        
        success_code = self._get_first_success_code(endpoint_data)
        error_code = self._get_first_error_code(endpoint_data)
        expected_status = success_code if is_valid else error_code
        test_type = TestType.POSITIVE if is_valid else TestType.NEGATIVE
        
        return TestCase(
            id=f"BVA-{self._test_counter:03d}",
            name=f"Valor límite - {param['name']} = {self._format_value(boundary_value)}",
            description=f"Verifica el comportamiento cuando '{param['name']}' tiene el valor límite {self._format_value(boundary_value)}",
            technique=self.get_technique(),
            test_type=test_type,
            priority=Priority.HIGH,
            endpoint=endpoint_data.path,
            http_method=endpoint_data.method,
            preconditions=["API disponible"],
            postconditions=[f"El endpoint retorna código {expected_status}"],
            test_data=test_data,
            expected_result=ExpectedResult(
                status_code=expected_status,
                description=f"{'Respuesta exitosa' if is_valid else 'Error de validación'} para valor límite"
            ),
            tags=endpoint_data.tags + ["boundary_value", test_type.value]
        )
    
    def _create_property_boundary_case(
        self,
        endpoint_data: SwaggerEndpointData,
        schema: Dict,
        prop_name: str,
        length: int,
        is_valid: bool,
        boundary_type: str
    ) -> TestCase:
        """Crea un caso de prueba para valor límite de longitud de propiedad."""
        self._test_counter += 1
        
        # Generar string de la longitud especificada
        value = self.data_generator._random_string(length) if length >= 0 else ""
        
        test_data = self._create_valid_test_data(endpoint_data)
        test_data.body = self._create_body_with_property_value(schema, prop_name, value)
        
        success_code = self._get_first_success_code(endpoint_data)
        error_code = self._get_first_error_code(endpoint_data)
        expected_status = success_code if is_valid else error_code
        test_type = TestType.POSITIVE if is_valid else TestType.NEGATIVE
        
        return TestCase(
            id=f"BVA-{self._test_counter:03d}",
            name=f"Valor límite - {prop_name} longitud {length} ({boundary_type})",
            description=f"Verifica que el endpoint {'acepte' if is_valid else 'rechace'} {prop_name} con longitud {length}",
            technique=self.get_technique(),
            test_type=test_type,
            priority=Priority.HIGH,
            endpoint=endpoint_data.path,
            http_method=endpoint_data.method,
            preconditions=["API disponible"],
            postconditions=[f"El endpoint retorna código {expected_status}"],
            test_data=test_data,
            expected_result=ExpectedResult(
                status_code=expected_status,
                description=f"{'Acepta' if is_valid else 'Rechaza'} {prop_name} con longitud {length}"
            ),
            tags=endpoint_data.tags + ["boundary_value", test_type.value, boundary_type]
        )
    
    def _create_numeric_property_case(
        self,
        endpoint_data: SwaggerEndpointData,
        schema: Dict,
        prop_name: str,
        value: Any,
        is_valid: bool,
        boundary_type: str
    ) -> TestCase:
        """Crea un caso de prueba para valor límite numérico de propiedad."""
        self._test_counter += 1
        
        test_data = self._create_valid_test_data(endpoint_data)
        test_data.body = self._create_body_with_property_value(schema, prop_name, value)
        
        success_code = self._get_first_success_code(endpoint_data)
        error_code = self._get_first_error_code(endpoint_data)
        expected_status = success_code if is_valid else error_code
        test_type = TestType.POSITIVE if is_valid else TestType.NEGATIVE
        
        return TestCase(
            id=f"BVA-{self._test_counter:03d}",
            name=f"Valor límite - {prop_name} = {value} ({boundary_type})",
            description=f"Verifica que el endpoint {'acepte' if is_valid else 'rechace'} {prop_name} con valor {value}",
            technique=self.get_technique(),
            test_type=test_type,
            priority=Priority.HIGH,
            endpoint=endpoint_data.path,
            http_method=endpoint_data.method,
            preconditions=["API disponible"],
            postconditions=[f"El endpoint retorna código {expected_status}"],
            test_data=test_data,
            expected_result=ExpectedResult(
                status_code=expected_status,
                description=f"{'Acepta' if is_valid else 'Rechaza'} {prop_name} = {value}"
            ),
            tags=endpoint_data.tags + ["boundary_value", test_type.value, boundary_type]
        )
    
    def _is_valid_boundary_value(self, param: Dict, value: Any) -> bool:
        """Determina si un valor límite es válido según el schema."""
        schema = param.get('schema', {})
        
        if isinstance(value, str):
            min_len = schema.get('minLength', 0)
            max_len = schema.get('maxLength', float('inf'))
            return min_len <= len(value) <= max_len
        
        if isinstance(value, (int, float)):
            minimum = schema.get('minimum', float('-inf'))
            maximum = schema.get('maximum', float('inf'))
            return minimum <= value <= maximum
        
        return True
    
    def _create_valid_test_data(
        self, 
        endpoint_data: SwaggerEndpointData,
        override_values: Dict[str, Any] = None,
        param_location: str = None
    ) -> TestData:
        """Crea test data con valores válidos, permitiendo override de valores específicos."""
        test_data = TestData()
        override_values = override_values or {}
        
        # Headers
        for header in endpoint_data.get_required_headers():
            if param_location == 'header' and header['name'] in override_values:
                test_data.headers[header['name']] = override_values[header['name']]
            else:
                test_data.headers[header['name']] = self.data_generator.generate_valid_value(header)
        
        # Path params
        for param in endpoint_data.get_path_params():
            if param_location == 'path' and param['name'] in override_values:
                test_data.path_params[param['name']] = override_values[param['name']]
            else:
                test_data.path_params[param['name']] = self.data_generator.generate_valid_value(param)
        
        # Query params
        for param in endpoint_data.get_query_params():
            if param.get('required', False):
                if param_location == 'query' and param['name'] in override_values:
                    test_data.query_params[param['name']] = override_values[param['name']]
                else:
                    test_data.query_params[param['name']] = self.data_generator.generate_valid_value(param)
        
        return test_data
    
    def _create_body_with_property_value(
        self, 
        schema: Dict, 
        target_prop_name: str, 
        target_value: Any
    ) -> Dict:
        """Crea un body con una propiedad específica y el resto válidas."""
        body = {}
        properties = schema.get('properties', [])
        required = schema.get('required', [])
        
        for prop in properties:
            prop_name = prop.get('name', '')
            is_required = prop_name in required or prop.get('required', False)
            
            if is_required:
                if prop_name == target_prop_name:
                    body[prop_name] = target_value
                else:
                    body[prop_name] = self.data_generator._generate_value_from_property(prop)
        
        return body
    
    def _get_first_success_code(self, endpoint_data: SwaggerEndpointData) -> int:
        """Obtiene el primer código de éxito dinámicamente."""
        success_responses = endpoint_data.get_success_responses()
        return int(list(success_responses.keys())[0]) if success_responses else 200
    
    def _get_first_error_code(self, endpoint_data: SwaggerEndpointData) -> int:
        """Obtiene el primer código de error dinámicamente."""
        error_responses = endpoint_data.get_error_responses()
        return int(list(error_responses.keys())[0]) if error_responses else 400
    
    def _format_value(self, value: Any) -> str:
        """Formatea un valor para mostrar en la descripción."""
        if isinstance(value, str):
            return f"'{value}' (len={len(value)})"
        return str(value)

