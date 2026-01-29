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

El proyecto sigue **arquitectura limpia** y **principios SOLID** con estructura modular donde cada herramienta es completamente autónoma:

```
mcp-qa/
├── tools/                           # Herramientas de QA (una por subdirectorio)
│   └── swagger_analyzer/            # Analizador de contratos Swagger/OpenAPI
│       ├── src/                     # Código fuente de la herramienta
│       │   ├── domain/              # Capa de dominio
│       │   │   ├── models.py        # Entidades del dominio
│       │   │   ├── interfaces.py    # Abstracciones (Fetcher, Parser, Analyzer)
│       │   │   └── exporters.py     # Interfaces de exportación
│       │   ├── application/         # Capa de aplicación (casos de uso)
│       │   │   ├── swagger_analyzer.py            # Analizador de contratos
│       │   │   ├── complete_analysis_use_case.py  # Orquestador principal
│       │   │   └── export_use_cases.py            # Casos de uso de exportación
│       │   └── infrastructure/      # Capa de infraestructura
│       │       ├── http_fetcher.py           # Obtención HTTP
│       │       ├── contract_parser.py        # Parser YAML/JSON
│       │       ├── json_exporter.py          # Exportador JSON
│       │       └── markdown_generator.py     # Generador de Markdown
│       ├── __init__.py
│       ├── config.py                # Configuración de la herramienta
│       └── tool.py                  # Facade de la herramienta
├── output/                          # Salidas generadas (por herramienta)
│   └── swagger_analyzer/            # Salidas del analizador Swagger
│       ├── swagger-analysis.json
│       └── API-README.md
└── main.py                          # Punto de entrada MCP
```

### Principios SOLID aplicados:

- **S (Single Responsibility)**: Cada clase tiene una única responsabilidad bien definida
- **O (Open/Closed)**: Fácil agregar nuevas herramientas sin modificar las existentes
- **L (Liskov Substitution)**: Las implementaciones son intercambiables vía interfaces
- **I (Interface Segregation)**: Interfaces específicas y focalizadas
- **D (Dependency Inversion)**: Dependencias de abstracciones mediante inyección

### Estructura modular y escalable:

- **Cada herramienta es autónoma**: Tiene su propio `src/` con arquitectura limpia completa
- **Alta cohesión, bajo acoplamiento**: No hay dependencias entre herramientas
- **Estructura homóloga**: Todas las herramientas siguen el mismo patrón arquitectónico
- **Salidas organizadas**: Por herramienta en `output/`
- **Fácil de mantener**: Cambios en una herramienta NO afectan a otras
- **Fácil de escalar**: Agregar nuevas herramientas es simplemente duplicar la estructura

## 📦 Instalación

```bash
# Instalar dependencias
pip install -e .
```

## 🚀 Uso principal:

#### Análisis completo de contrato Swagger (una herramienta, todo incluido)

```python
# Análisis completo: texto + JSON + README
analizar_contrato_swagger("http://localhost:8080/v3/api-docs")

# Con URL de Swagger UI para incluir en README
analizar_contrato_swagger(
    "http://localhost:8080/v3/api-docs",
    swagger_ui_url="http://localhost:8080/swagger-ui/index.html"
)

# Solo texto, sin generar archivos
analizar_contrato_swagger(
    "https://petstore.swagger.io/v2/swagger.json",
    generar_json=False,
    generar_readme=False
)

# Solo JSON
analizar_contrato_swagger(
    "http://localhost:8080/v3/api-docs",
    generar_readme=False
)
```

### Salidas generadas:

Todos los archivos se guardan automáticamente en `output/swagger_analyzer/`:
- **swagger-analysis.json**: Análisis completo en JSON estructurado
- **API-README.md**: Documentación estilo Swagger UI
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
