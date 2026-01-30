"""
Tool Facade para el generador de casos de prueba.
Punto de entrada principal siguiendo el patrón Facade.
"""
from typing import Optional, List
from .config import (
    DEFAULT_JSON_OUTPUT, 
    DEFAULT_README_OUTPUT,
    DEFAULT_TECHNIQUES,
    DEFAULT_INCLUDE_POSITIVE,
    DEFAULT_INCLUDE_NEGATIVE
)
from .src.domain.models import ISTQBTechnique
from .src.application.equivalence_partition_generator import EquivalencePartitioningGenerator
from .src.application.boundary_value_generator import BoundaryValueGenerator
from .src.application.decision_table_generator import DecisionTableGenerator
from .src.application.test_suite_builder import TestSuiteBuilder
from .src.application.use_cases import GenerateTestCasesUseCase
from .src.infrastructure.swagger_analysis_reader import SwaggerAnalysisJsonReader
from .src.infrastructure.synthetic_data_generator import SyntheticDataGenerator
from .src.infrastructure.json_test_exporter import JsonTestExporter
from .src.infrastructure.markdown_test_exporter import MarkdownTestExporter


class TestCaseGeneratorTool:
    """Facade para el generador de casos de prueba."""
    
    def __init__(self):
        # Inicializar infraestructura
        self.data_generator = SyntheticDataGenerator()
        self.swagger_reader = SwaggerAnalysisJsonReader()
        self.json_exporter = JsonTestExporter()
        self.markdown_exporter = MarkdownTestExporter()
        
        # Inicializar generadores por técnica
        self.generators = {
            ISTQBTechnique.EQUIVALENCE_PARTITIONING: EquivalencePartitioningGenerator(self.data_generator),
            ISTQBTechnique.BOUNDARY_VALUE_ANALYSIS: BoundaryValueGenerator(self.data_generator),
            ISTQBTechnique.DECISION_TABLE: DecisionTableGenerator(self.data_generator)
        }
        
        # Inicializar builder
        self.suite_builder = TestSuiteBuilder(self.generators)
        
        # Inicializar caso de uso
        self.generate_use_case = GenerateTestCasesUseCase(
            self.swagger_reader,
            self.suite_builder
        )
    
    def generate_test_cases(
        self,
        swagger_analysis_json_path: str,
        techniques: Optional[List[str]] = None,
        include_positive: bool = DEFAULT_INCLUDE_POSITIVE,
        include_negative: bool = DEFAULT_INCLUDE_NEGATIVE,
        generate_json: bool = True,
        generate_readme: bool = True,
        json_output_path: str = DEFAULT_JSON_OUTPUT,
        readme_output_path: str = DEFAULT_README_OUTPUT
    ) -> dict:
        """
        Genera casos de prueba desde un análisis de Swagger.
        
        Args:
            swagger_analysis_json_path: Ruta al JSON de análisis de Swagger
            techniques: Lista de técnicas a aplicar (None = todas)
            include_positive: Incluir casos positivos
            include_negative: Incluir casos negativos
            generate_json: Generar archivo JSON
            generate_readme: Generar archivo README
            json_output_path: Ruta de salida del JSON
            readme_output_path: Ruta de salida del README
            
        Returns:
            Diccionario con rutas de archivos generados y resumen
        """
        # Convertir técnicas de string a enum
        technique_enums = None
        if techniques:
            technique_enums = [
                ISTQBTechnique(t) for t in techniques 
                if t in [e.value for e in ISTQBTechnique]
            ]
        
        # Generar suite de casos de prueba
        test_suite = self.generate_use_case.execute(
            swagger_analysis_path=swagger_analysis_json_path,
            techniques=technique_enums,
            include_positive=include_positive,
            include_negative=include_negative
        )
        
        # Exportar a formatos solicitados
        result = {
            "total_test_cases": len(test_suite.test_cases),
            "summary": test_suite.to_dict()['summary'],
            "files_generated": []
        }
        
        if generate_json:
            json_path = self.json_exporter.export(test_suite, json_output_path)
            result["files_generated"].append({
                "type": "JSON",
                "path": json_path
            })
        
        if generate_readme:
            readme_path = self.markdown_exporter.export(test_suite, readme_output_path)
            result["files_generated"].append({
                "type": "README",
                "path": readme_path
            })
        
        return result
