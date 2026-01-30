"""
Generador de datos sintéticos basado en schemas de Swagger/OpenAPI.
Genera datos válidos e inválidos de forma completamente dinámica.
"""
import uuid
import random
import string
from typing import Any, List, Dict, Optional
from datetime import datetime, date
from ..domain.interfaces import ISyntheticDataGenerator


class SyntheticDataGenerator(ISyntheticDataGenerator):
    """Genera datos sintéticos basados en el tipo, formato y constraints del schema."""
    
    def generate_valid_value(self, param: Dict[str, Any]) -> Any:
        """Genera un valor válido basado en el esquema del parámetro."""
        schema = param.get('schema', {})
        param_type = schema.get('type', param.get('type', 'string'))
        param_format = schema.get('format', param.get('format'))
        example = schema.get('example', param.get('example'))
        
        # Si hay ejemplo, usarlo
        if example is not None:
            return example
        
        # Generar según tipo y formato
        if param_type == 'string':
            return self._generate_valid_string(schema, param_format)
        elif param_type == 'integer':
            return self._generate_valid_integer(schema)
        elif param_type == 'number':
            return self._generate_valid_number(schema)
        elif param_type == 'boolean':
            return random.choice([True, False])
        elif param_type == 'array':
            return self._generate_valid_array(schema)
        elif param_type == 'object':
            return self._generate_valid_object(schema)
        
        # Fallback: generar string genérico
        return self._random_string(10)
    
    def generate_invalid_value(self, param: Dict[str, Any], violation_type: str) -> Any:
        """Genera un valor inválido según el tipo de violación."""
        schema = param.get('schema', {})
        param_type = schema.get('type', param.get('type', 'string'))
        
        if violation_type == 'null':
            return None
        elif violation_type == 'empty':
            if param_type == 'string':
                return ""
            elif param_type == 'array':
                return []
            elif param_type == 'object':
                return {}
        elif violation_type == 'invalid_format':
            return self._generate_invalid_format(param_type, schema.get('format'))
        elif violation_type == 'wrong_type':
            return self._generate_wrong_type(param_type)
        
        # Fallback: generar valor obviamente inválido
        return f"INVALID_{self._random_string(5)}"
    
    def generate_boundary_values(self, param: Dict[str, Any]) -> List[Any]:
        """Genera valores límite para un parámetro."""
        schema = param.get('schema', {})
        param_type = schema.get('type', param.get('type', 'string'))
        boundary_values = []
        
        if param_type == 'string':
            boundary_values.extend(self._generate_string_boundaries(schema))
        elif param_type in ['integer', 'number']:
            boundary_values.extend(self._generate_numeric_boundaries(schema))
        elif param_type == 'array':
            boundary_values.extend(self._generate_array_boundaries(schema))
        
        return boundary_values
    
    # ============================================================================
    # GENERACIÓN DE STRINGS VÁLIDOS
    # ============================================================================
    
    def _generate_valid_string(self, schema: Dict, format_type: Optional[str]) -> str:
        """Genera un string válido según formato y constraints."""
        
        # Formatos específicos
        if format_type == 'uuid':
            return str(uuid.uuid4())
        elif format_type == 'email':
            return f"test{random.randint(1000, 9999)}@example.com"
        elif format_type == 'date':
            return date.today().isoformat()
        elif format_type == 'date-time':
            return datetime.now().isoformat()
        elif format_type == 'uri':
            return f"https://example.com/resource/{random.randint(1, 100)}"
        
        # String genérico respetando longitud
        min_length = schema.get('min_length', schema.get('minLength', 1))
        max_length = schema.get('max_length', schema.get('maxLength', 50))
        
        # Generar longitud válida (punto medio del rango)
        target_length = max(min_length, min((min_length + max_length) // 2, max_length))
        
        # Si hay enum, retornar un valor aleatorio
        enum_values = schema.get('enum')
        if enum_values:
            return random.choice(enum_values)
        
        # Si hay pattern, generar string que lo cumpla (simplificado)
        pattern = schema.get('pattern')
        if pattern:
            return self._generate_from_pattern(pattern, target_length)
        
        # String genérico
        return self._random_string(target_length)
    
    def _generate_string_boundaries(self, schema: Dict) -> List[str]:
        """Genera valores límite para strings."""
        boundaries = []
        min_length = schema.get('min_length', schema.get('minLength'))
        max_length = schema.get('max_length', schema.get('maxLength'))
        
        if min_length is not None:
            # Justo debajo del mínimo
            if min_length > 0:
                boundaries.append(self._random_string(min_length - 1))
            # En el mínimo
            boundaries.append(self._random_string(min_length))
            # Justo encima del mínimo
            boundaries.append(self._random_string(min_length + 1))
        
        if max_length is not None:
            # Justo debajo del máximo
            if max_length > 1:
                boundaries.append(self._random_string(max_length - 1))
            # En el máximo
            boundaries.append(self._random_string(max_length))
            # Justo encima del máximo
            boundaries.append(self._random_string(max_length + 1))
        
        return boundaries
    
    # ============================================================================
    # GENERACIÓN DE NÚMEROS VÁLIDOS
    # ============================================================================
    
    def _generate_valid_integer(self, schema: Dict) -> int:
        """Genera un integer válido."""
        minimum = schema.get('minimum', 1)
        maximum = schema.get('maximum', 1000)
        
        # Generar valor en el punto medio
        return (minimum + maximum) // 2
    
    def _generate_valid_number(self, schema: Dict) -> float:
        """Genera un number (float) válido."""
        minimum = schema.get('minimum', 0.0)
        maximum = schema.get('maximum', 1000.0)
        
        return (minimum + maximum) / 2
    
    def _generate_numeric_boundaries(self, schema: Dict) -> List[Any]:
        """Genera valores límite para números."""
        boundaries = []
        minimum = schema.get('minimum')
        maximum = schema.get('maximum')
        param_type = schema.get('type', 'integer')
        
        if minimum is not None:
            boundaries.append(minimum - 1)  # Debajo del mínimo
            boundaries.append(minimum)  # En el mínimo
            if param_type == 'integer':
                boundaries.append(minimum + 1)  # Encima del mínimo
            else:
                boundaries.append(minimum + 0.1)
        
        if maximum is not None:
            if param_type == 'integer':
                boundaries.append(maximum - 1)  # Debajo del máximo
            else:
                boundaries.append(maximum - 0.1)
            boundaries.append(maximum)  # En el máximo
            boundaries.append(maximum + 1)  # Encima del máximo
        
        return boundaries
    
    # ============================================================================
    # GENERACIÓN DE ARRAYS Y OBJECTS
    # ============================================================================
    
    def _generate_valid_array(self, schema: Dict) -> List[Any]:
        """Genera un array válido."""
        min_items = schema.get('minItems', 1)
        max_items = schema.get('maxItems', 5)
        items_schema = schema.get('items', {})
        
        count = (min_items + max_items) // 2
        
        return [self._generate_value_from_schema(items_schema) for _ in range(count)]
    
    def _generate_array_boundaries(self, schema: Dict) -> List[List]:
        """Genera valores límite para arrays."""
        boundaries = []
        min_items = schema.get('minItems')
        max_items = schema.get('maxItems')
        items_schema = schema.get('items', {})
        
        if min_items is not None:
            if min_items > 0:
                boundaries.append([self._generate_value_from_schema(items_schema) for _ in range(min_items - 1)])
            boundaries.append([self._generate_value_from_schema(items_schema) for _ in range(min_items)])
            boundaries.append([self._generate_value_from_schema(items_schema) for _ in range(min_items + 1)])
        
        if max_items is not None:
            boundaries.append([self._generate_value_from_schema(items_schema) for _ in range(max_items - 1)])
            boundaries.append([self._generate_value_from_schema(items_schema) for _ in range(max_items)])
            boundaries.append([self._generate_value_from_schema(items_schema) for _ in range(max_items + 1)])
        
        return boundaries
    
    def _generate_valid_object(self, schema: Dict) -> Dict[str, Any]:
        """Genera un object válido basado en sus properties."""
        obj = {}
        properties = schema.get('properties', [])
        required = schema.get('required', [])
        
        for prop in properties:
            prop_name = prop.get('name', '')
            is_required = prop_name in required or prop.get('required', False)
            
            # Solo generar campos requeridos
            if is_required:
                obj[prop_name] = self._generate_value_from_property(prop)
        
        return obj
    
    def _generate_value_from_property(self, prop: Dict) -> Any:
        """Genera un valor para una propiedad de un objeto."""
        prop_type = prop.get('type', 'string')
        prop_format = prop.get('format')
        
        if prop.get('example') is not None:
            return prop['example']
        
        if prop_type == 'string':
            return self._generate_valid_string(prop, prop_format)
        elif prop_type == 'integer':
            return self._generate_valid_integer(prop)
        elif prop_type == 'number':
            return self._generate_valid_number(prop)
        elif prop_type == 'boolean':
            return True
        elif prop_type == 'array':
            return self._generate_valid_array(prop)
        
        # Fallback: generar string genérico
        return self._random_string(8)
    
    def _generate_value_from_schema(self, schema: Dict) -> Any:
        """Genera un valor desde un schema genérico."""
        if not schema:
            return self._random_string(10)
        
        schema_type = schema.get('type', 'string')
        
        if schema_type == 'string':
            return self._generate_valid_string(schema, schema.get('format'))
        elif schema_type == 'integer':
            return self._generate_valid_integer(schema)
        elif schema_type == 'number':
            return self._generate_valid_number(schema)
        elif schema_type == 'boolean':
            return True
        
        # Fallback: generar string genérico
        return self._random_string(8)
    
    # ============================================================================
    # GENERACIÓN DE VALORES INVÁLIDOS
    # ============================================================================
    
    def _generate_invalid_format(self, param_type: str, format_type: Optional[str]) -> Any:
        """Genera un valor con formato inválido."""
        if format_type == 'uuid':
            return "invalid-uuid-format"
        elif format_type == 'email':
            return "not-an-email"
        elif format_type == 'date':
            return "not-a-date"
        elif format_type == 'date-time':
            return "not-a-datetime"
        elif format_type == 'uri':
            return "not a uri"
        elif param_type == 'integer':
            return "not_an_integer"
        elif param_type == 'number':
            return "not_a_number"
        
        # Fallback: generar valor claramente inválido
        return f"INVALID_FORMAT_{self._random_string(5)}"
    
    def _generate_wrong_type(self, expected_type: str) -> Any:
        """Genera un valor de tipo incorrecto."""
        if expected_type == 'string':
            return 12345
        elif expected_type in ['integer', 'number']:
            return "this_is_not_a_number"
        elif expected_type == 'boolean':
            return "not_a_boolean"
        elif expected_type == 'array':
            return "not_an_array"
        elif expected_type == 'object':
            return "not_an_object"
        
        return None
    
    # ============================================================================
    # UTILIDADES
    # ============================================================================
    
    def _random_string(self, length: int) -> str:
        """Genera un string aleatorio de longitud específica."""
        if length <= 0:
            return ""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    def _generate_from_pattern(self, pattern: str, length: int) -> str:
        """Genera un string que cumpla con un patrón (simplificado)."""
        # Implementación simplificada - en producción usar biblioteca de regex
        return self._random_string(length)
