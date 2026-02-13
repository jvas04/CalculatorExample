#  Calculadora – Aplicación de SRP y High Cohesion

## Dominio

Herramienta de cálculo matemático (utility de productividad).

El proyecto consiste en refactorizar una calculadora básica para aplicar principios de diseño de software y mejorar su calidad estructural.

---

##  Problema de Diseño Inicial

La clase `Calculator` concentraba múltiples responsabilidades:

- Operaciones matemáticas  
- Gestión de historial  
- Impresión en consola  
- Guardado en archivo  

Esto generaba:

- Violación del **Single Responsibility Principle (SRP)**  
- Baja cohesión  
- Alto acoplamiento  
- Dificultad para extender o mantener el código  

---

##  Principios Aplicados

###  Single Responsibility Principle (SRP)

Se separaron responsabilidades en clases específicas:

- `CalculatorOperations` → Lógica matemática  
- `HistoryManager` → Manejo de historial  
- `FileManager` → Persistencia  
- `CalculatorApp` → Coordinación del sistema  

Cada clase tiene **una única razón para cambiar**.

---

###  High Cohesion (GRASP)

Cada clase contiene funciones relacionadas entre sí, reduciendo dependencias innecesarias y mejorando claridad y mantenibilidad.

---

## Decisiones de Diseño

- Separación clara de responsabilidades  
- Uso de composición en lugar de herencia  
- Manejo de errores mediante excepciones  
- Clase coordinadora para desacoplar componentes  

---

##  Resultado

El sistema pasó de ser un diseño monolítico a una arquitectura modular, más mantenible, extensible y fácil de probar.

Este proyecto demuestra cómo la aplicación práctica de principios de diseño mejora la calidad del software.
