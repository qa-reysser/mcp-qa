"""
Casos de uso para la generación de casos de prueba.
"""
from typing import Optional, List
from ..domain.models import TestSuite, ISTQBTechnique
from ..domain.interfaces import (
    ISwaggerAnalysisReader,
    ITestSuiteBuilder
)


class GenerateTestCasesUseCase:
    """Caso de uso para generar casos de prueba desde un análisis de Swagger."""
    
    def __init__(
        self,
        swagger_reader: ISwaggerAnalysisReader,
        suite_builder: ITestSuiteBuilder
    ):
        self.swagger_reader = swagger_reader
        self.suite_builder = suite_builder
    
    def execute(
        self,
        swagger_analysis_path: str,
        techniques: Optional[List[ISTQBTechnique]] = None,
        include_positive: bool = True,
        include_negative: bool = True
    ) -> TestSuite:
        """
        Ejecuta la generación de casos de prueba.
        
        Args:
            swagger_analysis_path: Ruta al archivo JSON de análisis de Swagger
            techniques: Técnicas ISTQB a aplicar (None = todas)
            include_positive: Incluir casos positivos
            include_negative: Incluir casos negativos
            
        Returns:
            Suite de casos de prueba generada
        """
        # Leer el análisis de Swagger
        analysis = self.swagger_reader.read_analysis(swagger_analysis_path)
        
        # Extraer endpoints
        endpoints = self.swagger_reader.extract_endpoints(analysis)
        
        # Construir la suite de casos de prueba
        test_suite = self.suite_builder.build(
            endpoints=endpoints,
            techniques=techniques,
            include_positive=include_positive,
            include_negative=include_negative
        )
        
        # Agregar metadata del contrato
        contract_info = analysis.get('contract_info', {})
        test_suite.metadata.update({
            'source_api': contract_info.get('title', 'Unknown'),
            'api_version': contract_info.get('version', 'Unknown'),
            'openapi_version': contract_info.get('openapi_version', 'Unknown')
        })
        
        return test_suite
