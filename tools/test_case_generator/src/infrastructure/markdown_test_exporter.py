"""
Exportador de casos de prueba a formato Markdown (README).
Genera documentación legible de los casos de prueba.
"""
import os
from ..domain.models import TestSuite, TestCase, TestType, Priority
from ..domain.exporters import ITestExporter


class MarkdownTestExporter(ITestExporter):
    """Exporta casos de prueba a formato Markdown."""
    
    def export(self, test_suite: TestSuite, output_path: str) -> str:
        """Exporta la suite de casos de prueba a Markdown."""
        # Asegurar que el directorio existe
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Generar contenido markdown
        content = self._generate_markdown(test_suite)
        
        # Guardar archivo
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return output_path
    
    def get_format_name(self) -> str:
        return "Markdown"
    
    def _generate_markdown(self, test_suite: TestSuite) -> str:
        """Genera el contenido Markdown completo."""
        lines = []
        
        # Título y descripción
        lines.append(f"# {test_suite.name}\n")
        lines.append(f"{test_suite.description}\n")
        
        # Metadata
        lines.append("## 📊 Información General\n")
        lines.append(f"- **API Source**: {test_suite.metadata.get('source_api', 'N/A')}")
        lines.append(f"- **API Version**: {test_suite.metadata.get('api_version', 'N/A')}")
        lines.append(f"- **OpenAPI Version**: {test_suite.metadata.get('openapi_version', 'N/A')}")
        lines.append(f"- **Total Test Cases**: {len(test_suite.test_cases)}")
        lines.append(f"- **Techniques Applied**: {', '.join(test_suite.metadata.get('techniques_applied', []))}\n")
        
        # Resumen
        summary = test_suite.to_dict()['summary']
        
        lines.append("## 📈 Resumen de Casos de Prueba\n")
        lines.append("### Por Técnica ISTQB\n")
        for technique, count in summary['by_technique'].items():
            lines.append(f"- **{technique}**: {count} casos")
        
        lines.append("\n### Por Tipo\n")
        for test_type, count in summary['by_type'].items():
            icon = "✅" if test_type == "positive" else "❌"
            lines.append(f"- {icon} **{test_type.upper()}**: {count} casos")
        
        lines.append("\n### Por Prioridad\n")
        for priority, count in summary['by_priority'].items():
            icon = "🔴" if priority == "high" else "🟡" if priority == "medium" else "🟢"
            lines.append(f"- {icon} **{priority.upper()}**: {count} casos")
        
        # Casos de prueba agrupados por endpoint
        lines.append("\n## 🧪 Casos de Prueba Detallados\n")
        
        endpoints = self._group_by_endpoint(test_suite.test_cases)
        
        for idx, (endpoint, cases) in enumerate(endpoints.items(), 1):
            lines.append(f"### {idx}. Endpoint: `{endpoint}`\n")
            lines.append(f"**Total de casos**: {len(cases)}\n")
            
            for case in cases:
                lines.append(self._format_test_case(case))
        
        return "\n".join(lines)
    
    def _group_by_endpoint(self, test_cases: list) -> dict:
        """Agrupa los casos de prueba por endpoint."""
        grouped = {}
        
        for test_case in test_cases:
            key = f"{test_case.http_method} {test_case.endpoint}"
            if key not in grouped:
                grouped[key] = []
            grouped[key].append(test_case)
        
        return grouped
    
    def _format_test_case(self, test_case: TestCase) -> str:
        """Formatea un caso de prueba individual."""
        lines = []
        
        # Encabezado del caso
        type_icon = "✅" if test_case.test_type == TestType.POSITIVE else "❌"
        priority_icon = "🔴" if test_case.priority == Priority.HIGH else "🟡" if test_case.priority == Priority.MEDIUM else "🟢"
        
        lines.append(f"#### {type_icon} {test_case.id} - {test_case.name}")
        lines.append(f"**Prioridad**: {priority_icon} {test_case.priority.value.upper()}  ")
        lines.append(f"**Técnica**: {test_case.technique.value}  ")
        lines.append(f"**Tipo**: {test_case.test_type.value.upper()}\n")
        
        # Descripción
        lines.append(f"**Descripción**: {test_case.description}\n")
        
        # Precondiciones
        if test_case.preconditions:
            lines.append("**Precondiciones**:")
            for precond in test_case.preconditions:
                lines.append(f"- {precond}")
            lines.append("")
        
        # Datos de prueba
        lines.append("**Datos de Prueba**:")
        
        if test_case.test_data.headers:
            lines.append("- **Headers**:")
            for key, value in test_case.test_data.headers.items():
                lines.append(f"  - `{key}`: `{value}`")
        
        if test_case.test_data.path_params:
            lines.append("- **Path Parameters**:")
            for key, value in test_case.test_data.path_params.items():
                lines.append(f"  - `{key}`: `{value}`")
        
        if test_case.test_data.query_params:
            lines.append("- **Query Parameters**:")
            for key, value in test_case.test_data.query_params.items():
                lines.append(f"  - `{key}`: `{value}`")
        
        if test_case.test_data.body:
            lines.append("- **Request Body**:")
            lines.append(f"  ```json")
            import json
            lines.append(f"  {json.dumps(test_case.test_data.body, indent=2)}")
            lines.append(f"  ```")
        
        lines.append("")
        
        # Resultado esperado
        lines.append("**Resultado Esperado**:")
        lines.append(f"- **Código HTTP**: `{test_case.expected_result.status_code}`")
        if test_case.expected_result.description:
            lines.append(f"- **Descripción**: {test_case.expected_result.description}")
        if test_case.expected_result.error_codes:
            lines.append(f"- **Códigos de Error**: {', '.join([f'`{code}`' for code in test_case.expected_result.error_codes])}")
        
        lines.append("")
        
        # Postcondiciones
        if test_case.postconditions:
            lines.append("**Postcondiciones**:")
            for postcond in test_case.postconditions:
                lines.append(f"- {postcond}")
            lines.append("")
        
        lines.append("---\n")
        
        return "\n".join(lines)
