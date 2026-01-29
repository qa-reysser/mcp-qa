# MCP-QA: Analizador de Contratos Swagger/OpenAPI

MCP Server para análisis completo de contratos Swagger/OpenAPI con exportación a JSON y generación automática de documentación.

## 🎯 Características

- ✅ Soporta Swagger 2.0 y OpenAPI 3.x
- ✅ Análisis completo de endpoints (paths, métodos HTTP)
- ✅ Extracción de parámetros (path, query, header, cookie)
- ✅ Análisis de request bodies con schemas
- ✅ Análisis de responses (códigos HTTP, schemas, headers)
- ✅ Extracción de schemas con propiedades, tipos y formatos
- ✅ Validaciones (obligatoriedad, tipos, formatos UUID/fecha/etc)
- ✅ Información de servidores y seguridad
- ✅ Tags y documentación
- ✅ **Exportación a JSON** con toda la información estructurada
- ✅ **Generación de README** con documentación estilo Swagger UI

## 🏗️ Arquitectura

El proyecto sigue **arquitectura limpia** y **principios SOLID**:

```
mcp-qa/
├── src/
│   ├── domain/           # Capa de dominio (entidades e interfaces)
│   │   ├── models.py     # Modelos de dominio
│   │   └── interfaces.py # Abstracciones (IContractFetcher, IContractParser, IContractAnalyzer)
│   ├── application/      # Capa de aplicación (casos de uso)
│   │   ├── swagger_analyzer.py  # Analizador de contratos
│   │   └── use_cases.py         # Orquestación del flujo
│   └── infrastructure/   # Capa de infraestructura (implementaciones)
│       ├── http_fetcher.py      # Obtención de contratos HTTP
│       └── contract_parser.py   # Parser YAML/JSON
└── main.py              # Punto de entrada MCP
```

### Principios SOLID aplicados:

- **S (Single Responsibility)**: Cada clase tiene una única responsabilidad
- **O (Open/Closed)**: Extensible sin modificar código existente
- **L (Liskov Substitution)**: Las implementaciones son intercambiables
- **I (Interface Segregation)**: Interfaces específicas y focalizadas
- **D (Dependency Inversion)**: Dependencias de abstracciones, no de concreciones

## 📦 Instalación

```bash
# Instalar dependencias
pip install -e .
```

## 🚀 Uso

```bash
# Ejecutar el servidor MCP
python main.py
```

### Herramientas disponibles:

#### 1. Analizar contrato (salida de texto)

```python
# Analizar el contrato de Petstore
analizar_contrato_swagger("https://petstore.swagger.io/v2/swagger.json")
```

#### 2. Exportar análisis a JSON

```python
# Generar archivo JSON con toda la información
generar_json_analisis("http://localhost:8080/v3/api-docs", "mi-api-analysis.json")
```

Esto genera un archivo JSON estructurado con:
- Metadata del análisis (totales, resúmenes)
- Información completa del contrato
- Todos los endpoints con detalles
- Schemas completos
- Esquemas de seguridad

#### 3. Generar README con documentación

```python
# Generar README estilo Swagger UI
generar_readme_api(
    "http://localhost:8080/v3/api-docs",
    "API-DOCS.md",
    "http://localhost:8080/swagger-ui/index.html"
)
```

Esto genera un README.md profesional con:
- Tabla de contenidos
- Resumen y estadísticas
- Links a Swagger UI
- Documentación completa de endpoints
- Tablas de schemas y propiedades
- Códigos de estado HTTP

## 🔍 Información extraída

El analizador extrae:

- **Información general**: título, versión, descripción
- **Servidores**: URLs y configuraciones
- **Endpoints**: 
  - Path y método HTTP
  - Parámetros (ubicación, tipo, obligatoriedad)
  - Request body (content types, schemas)
  - Responses (códigos, schemas, headers)
- **Schemas**:
  - Propiedades con tipos y formatos
  - Validaciones (min/max length, pattern, enum)
  - Obligatoriedad de campos
  - Formatos especiales (UUID, date, email, etc)
- **Seguridad**: esquemas de autenticación
- **Estadísticas**: resumen de métodos, códigos HTTP, content types

## 📄 Licencia

MIT
