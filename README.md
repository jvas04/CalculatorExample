# Calculadora Pro – Refactorización con SRP, Alta Cohesión y Arquitectura MVC

## Dominio

Herramienta de cálculo matemático con interfaz gráfica (Tkinter), que incluye operaciones aritméticas básicas, funciones científicas, gestión de memoria, historial de operaciones, estadísticas de uso, persistencia en archivos y soporte de temas visuales.

---

## Problema de Diseño Inicial (God Class)

La clase original `Calculator` concentraba **múltiples responsabilidades** en una sola clase monolítica:

- Operaciones matemáticas (suma, resta, multiplicación, división)
- Operaciones científicas (raíz cuadrada, potencia, porcentaje)
- Construcción y gestión de la interfaz gráfica (Tkinter)
- Gestión de historial de operaciones
- Memoria de la calculadora (M+, M-, MR, MC)
- Persistencia en archivos (JSON / texto)
- Formateo de números para el display
- Validación de entrada del usuario
- Registro de errores
- Estadísticas de uso
- Gestión de temas visuales (oscuro / claro)

### Problemas detectados

| Problema | Descripción |
|---|---|
| **Violación de SRP** | Una clase con más de 10 razones para cambiar |
| **Baja cohesión** | Métodos de UI mezclados con lógica de negocio y persistencia |
| **Alto acoplamiento** | Cambiar cualquier funcionalidad implicaba modificar la misma clase |
| **Dificultad de testing** | Imposible probar la lógica de cálculo sin instanciar toda la UI |
| **Dificultad de mantenimiento** | Archivo extenso y complejo difícil de navegar |
| **Baja extensibilidad** | Agregar nuevas funcionalidades aumentaba la complejidad exponencialmente |

---

## Principios de Diseño Aplicados

### 1. Single Responsibility Principle (SRP) — SOLID

> _"Una clase debe tener una, y solo una, razón para cambiar."_ — Robert C. Martin

La clase monolítica fue descompuesta en **12 clases especializadas**, cada una con una única responsabilidad claramente definida y una única razón para cambiar:

| Clase | Capa | Responsabilidad Única | Razón para cambiar |
|---|---|---|---|
| `MathEngine` | Model | Operaciones aritméticas (+, −, ×, ÷) | Cambio en operaciones básicas |
| `ScientificOperations` | Model | Operaciones científicas (√, x², %, ±, π) | Cambio en operaciones científicas |
| `MemoryManager` | Model | Memoria numérica (MC, MR, M+, M−) | Cambio en operaciones de memoria |
| `HistoryManager` | Model | Gestión del historial de operaciones | Cambio en estructura del historial |
| `StatisticsReporter` | Model | Conteo y reporte de estadísticas de uso | Cambio en métricas o formato del reporte |
| `CalculatorView` | View | Construcción y actualización de la interfaz gráfica | Cambio en layout o componentes UI |
| `HistoryView` | View | Ventana emergente del historial | Cambio en presentación del historial |
| `CalculatorController` | Controller | Orquestación y coordinación entre capas | Cambio en flujo de coordinación |
| `FileManager` | Service | Persistencia en archivos (JSON / texto) | Cambio en formato o destino de persistencia |
| `ErrorLogger` | Service | Registro de errores en archivo de log | Cambio en formato o destino del log |
| `ThemeManager` | Utility | Definición y alternancia de temas visuales | Cambio en requisitos visuales |
| `NumberFormatter` | Utility | Formateo de números para el display | Cambio en reglas de formato numérico |
| `InputValidator` | Utility | Validación de datos de entrada | Cambio en reglas de validación |

### 2. Alta Cohesión (GRASP)

> _"Cada clase debe contener únicamente métodos y datos estrechamente relacionados entre sí."_

Cada clase presenta **alta cohesión funcional**: todos sus métodos operan sobre el mismo concepto o dato interno.

**Ejemplos concretos:**

- **`MemoryManager`**: todos los métodos (`clear`, `recall`, `add`, `subtract`, `has_value`) operan sobre el mismo atributo `_memory`.
- **`HistoryManager`**: todos los métodos (`add_record`, `get_all_records`, `clear`, `count`, `is_empty`) operan sobre la lista `_records`.
- **`MathEngine`**: todos los métodos son cálculos aritméticos puros (`add`, `subtract`, `multiply`, `divide`, `calculate`).
- **`ThemeManager`**: todos los métodos gestionan paletas de colores y estado del tema visual.
- **`NumberFormatter`**: todos los métodos transforman datos numéricos a representaciones de texto.

### 3. Patrón Arquitectónico MVC (Model-View-Controller)

La aplicación sigue una arquitectura **MVC** que separa claramente las tres capas:

```
┌──────────────────────────────────────────────────────────┐
│                      CONTROLLER                          │
│              CalculatorController                        │
│   (Orquesta la comunicación entre Vista y Modelos)       │
├──────────────┬───────────────────────────┬───────────────┤
│    VIEWS     │         MODELS            │   SERVICES    │
│              │                           │   & UTILS     │
│ Calculator   │  MathEngine               │ FileManager   │
│   View       │  ScientificOperations     │ ErrorLogger   │
│ HistoryView  │  MemoryManager            │ ThemeManager  │
│              │  HistoryManager            │ NumberFormat. │
│              │  StatisticsReporter        │ InputValid.   │
└──────────────┴───────────────────────────┴───────────────┘
```

- **Models**: Contienen la lógica de negocio pura, sin conocimiento de la UI.
- **Views**: Construyen y actualizan la interfaz gráfica, sin lógica de negocio. Los callbacks son inyectados por el Controller.
- **Controller**: Único punto de coordinación. No contiene lógica de negocio ni de UI; solo orquesta el flujo entre capas.

### 4. Composición sobre Herencia

Se utilizó **composición** (inyección de dependencias) en lugar de herencia. El `CalculatorController` recibe e instancia sus dependencias como componentes independientes:

```python
self.theme      = ThemeManager()
self.formatter  = NumberFormatter()
self.validator  = InputValidator()
self.logger     = ErrorLogger()
self.math       = MathEngine()
self.scientific = ScientificOperations()
self.memory     = MemoryManager()
self.history    = HistoryManager()
self.file_mgr   = FileManager()
self.stats      = StatisticsReporter()
```

Esto permite reemplazar o extender cualquier componente sin afectar a los demás.

### 5. Bajo Acoplamiento (GRASP)

Cada componente depende únicamente de las interfaces públicas de los demás. Los modelos no conocen la vista, la vista no conoce los modelos, y el controlador actúa como mediador.

---

## Estructura del Proyecto

```
CalculatorExample/
│
├── calculator_main.py              # Punto de entrada de la aplicación
│
├── controllers/
│   └── calculator_controller.py    # Orquestador MVC (coordina vista ↔ modelos)
│
├── models/
│   ├── math_engine.py              # Operaciones aritméticas básicas
│   ├── scientific_operations.py    # Operaciones científicas avanzadas
│   ├── memory_manager.py           # Memoria numérica (M+, M−, MR, MC)
│   ├── history_manager.py          # Historial de operaciones con timestamps
│   └── statistics_reporter.py      # Estadísticas y reportes de uso
│
├── views/
│   ├── calculator_view.py          # Interfaz gráfica principal (Tkinter)
│   └── history_view.py             # Ventana emergente del historial
│
├── services/
│   ├── file_manager.py             # Persistencia en JSON y texto plano
│   └── error_logger.py             # Registro de errores en archivo .log
│
├── utils/
│   ├── theme_manager.py            # Gestión de temas oscuro/claro
│   ├── number_formatter.py         # Formateo de números para display
│   └── input_validator.py          # Validación de datos de entrada
│
├── diagrama_clases.html            # Diagrama de clases (post-refactorización)
└── diagrama_godclass.html          # Diagrama de la God Class original
```

---

## Decisiones de Diseño

| Decisión | Justificación |
|---|---|
| **Separación en 5 capas** (controllers, models, views, services, utils) | Organización clara por tipo de responsabilidad |
| **Composición en lugar de herencia** | Mayor flexibilidad y menor acoplamiento entre componentes |
| **Callbacks inyectados en la Vista** | La vista no conoce al controlador; los botones reciben funciones como parámetros |
| **Métodos `@staticmethod` en modelos puros** | `MathEngine`, `ScientificOperations`, `NumberFormatter` e `InputValidator` no requieren estado interno para sus cálculos |
| **Manejo de errores mediante excepciones** | `FileManager` lanza excepciones que el controlador captura y muestra al usuario |
| **`ErrorLogger` separado** | Permite cambiar la estrategia de logging sin afectar la lógica de negocio |
| **Dos formatos de persistencia** (JSON / texto) | `FileManager` decide el formato según la extensión del archivo |
| **Temas definidos como diccionarios constantes** | `ThemeManager` almacena `DARK_THEME` y `LIGHT_THEME` como mapas de colores reutilizables |
| **`StatisticsReporter` independiente** | Permite generar reportes de uso sin depender de la UI o del historial |

---

## Refactorización Realizada

### De God Class a Arquitectura Modular

**Antes:** Una sola clase `Calculator` con todas las responsabilidades mezcladas.

**Después:** 12 clases especializadas organizadas en 5 paquetes, cada una con una responsabilidad única y alta cohesión interna.

### Resumen del proceso de refactorización

1. **Identificación de responsabilidades**: Se analizó la clase original y se identificaron más de 10 responsabilidades distintas.
2. **Extracción de modelos**: Se crearon `MathEngine`, `ScientificOperations`, `MemoryManager`, `HistoryManager` y `StatisticsReporter` para encapsular la lógica de negocio.
3. **Extracción de vistas**: Se crearon `CalculatorView` y `HistoryView` para encapsular la construcción y actualización de la interfaz gráfica.
4. **Extracción de servicios**: Se crearon `FileManager` y `ErrorLogger` para la persistencia y el logging.
5. **Extracción de utilidades**: Se crearon `ThemeManager`, `NumberFormatter` e `InputValidator` como funciones de soporte transversales.
6. **Creación del controlador**: `CalculatorController` se diseñó como el único orquestador que conecta todas las capas mediante inyección de callbacks.
7. **Documentación del código**: Cada clase incluye comentarios de cabecera que indican su responsabilidad SRP, su cohesión y su razón única para cambiar.

---

## Funcionalidades

- Operaciones aritméticas: suma, resta, multiplicación, división
- Operaciones científicas: raíz cuadrada, potencia al cuadrado, porcentaje, cambio de signo, constante π
- Memoria: almacenar, recuperar, sumar y restar valores (MC, MR, M+, M−)
- Historial de operaciones con timestamps
- Guardado del historial en JSON o texto plano
- Estadísticas de uso con reporte detallado
- Tema oscuro y claro con alternancia dinámica
- Soporte de teclado físico (números, operadores, Enter, Backspace, Escape)
- Validación de entrada y manejo de errores (división por cero, raíz de negativos)
- Registro de errores en archivo `.log`

---

## Ejecución

```bash
python calculator_main.py
```

---

## Resultado

El sistema evolucionó de un diseño **monolítico (God Class)** a una **arquitectura modular MVC** con:

- **12 clases** con responsabilidad única (SRP)
- **Alta cohesión** en cada clase
- **Bajo acoplamiento** entre componentes
- **5 paquetes** organizados por tipo de responsabilidad
- Código **documentado** con docstrings y comentarios de principios aplicados
- Arquitectura **extensible** y **fácil de mantener**

Este proyecto demuestra cómo la aplicación práctica de los principios **SOLID (SRP)**, **GRASP (Alta Cohesión, Bajo Acoplamiento)** y el patrón **MVC** transforma un código difícil de mantener en una arquitectura limpia, modular y profesional.
