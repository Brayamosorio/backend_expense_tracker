<<<<<<< HEAD
# 💰 Expense Tracker — Sistema de Gestión de Gastos Personales

### Autor: **Brayam Osorio**  
📧 Contacto: [osoriobrayam9@gmail.com](mailto:osoriobrayam9@gmail.com)  
📆 Versión: 1.0  
🧪 Cobertura actual de pruebas: **91%**

---

## 🧭 Descripción General

**Expense Tracker** es una aplicación desarrollada en **Python 3.12** que permite **gestionar, analizar y visualizar los gastos personales** de manera estructurada y automatizada.  
El proyecto fue diseñado bajo un enfoque **modular y orientado a pruebas (TDD)**, integrando herramientas de **análisis, persistencia, reportes y notificaciones**.

El propósito principal es demostrar la aplicación de **buenas prácticas de desarrollo de software**, incluyendo:
- Programación modular.
- Pruebas automatizadas unitarias e integradas.
- Generación de reportes estadísticos.
- Manejo de persistencia y exportación de datos.
- Uso de patrones de diseño simples y código reutilizable.

---

## ⚙️ Estructura del Proyecto

expense_tracker/
│
├── src/
│ ├── analytics.py # Cálculos estadísticos y métricas de gasto
│ ├── api.py # Endpoints simulados para operaciones REST
│ ├── backup.py # Copias de seguridad automáticas
│ ├── budget.py # Control de presupuestos mensuales
│ ├── charts.py # Gráficos ASCII por categoría y mes
│ ├── currency.py # Conversión de divisas (COP, USD, EUR)
│ ├── logger.py # Registro de acciones y errores
│ ├── notifications.py # Alertas de inactividad o exceso de gasto
│ ├── report.py # Reportes promedio y análisis temporal
│ ├── storage.py # Persistencia en archivos JSON
│ ├── tracker.py # CRUD principal de gastos
│ ├── users.py # Gestión de usuarios y sesiones
│ └── validator.py # Validaciones de fechas y montos
│
├── tests/ # Suite completa de pruebas unitarias
│ ├── test_analytics.py
│ ├── test_api.py
│ ├── test_backup.py
│ ├── test_budget.py
│ ├── test_charts.py
│ ├── test_currency.py
│ ├── test_logger.py
│ ├── test_notifications.py
│ ├── test_report.py
│ ├── test_storage.py
│ ├── test_tracker.py
│ ├── test_users.py
│ └── test_validator.py
│
├── htmlcov/ # Reporte visual de cobertura de código
├── pytest.ini # Configuración de pytest
├── requirements.txt # Dependencias del entorno virtual
├── main.py # Script principal de ejecución
└── README.md # Documentación principal

yaml
Copiar código

---

## 🚀 Instalación y Ejecución

### 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/osoriobrayam9/expense_tracker.git
cd expense_tracker
2️⃣ Crear entorno virtual
bash
Copiar código
python -m venv .venv
3️⃣ Activar entorno (Windows)
bash
Copiar código
.venv\Scripts\activate
4️⃣ Instalar dependencias
bash
Copiar código
pip install -r requirements.txt
5️⃣ Ejecutar la aplicación
bash
Copiar código
python main.py
🧪 Pruebas Automatizadas
El proyecto incluye 28 pruebas unitarias e integradas que validan el correcto funcionamiento de cada módulo.

▶️ Ejecutar todas las pruebas:
bash
Copiar código
pytest -v
▶️ Ejecutar con reporte de cobertura:
bash
Copiar código
pytest -v --cov=src --cov-report=term-missing --cov-report=html
📊 Ver el reporte gráfico:
Abre el archivo htmlcov/index.html en tu navegador.

📈 Resultados de Cobertura
Módulo	Cobertura
analytics.py	✅ 89%
api.py	✅ 92%
backup.py	✅ 95%
budget.py	✅ 88%
charts.py	✅ 97%
currency.py	✅ 100%
logger.py	✅ 100%
notifications.py	✅ 91%
report.py	✅ 88%
storage.py	✅ 87%
tracker.py	✅ 91%
users.py	✅ 94%
validator.py	✅ 100%
Total	91%

📊 Funcionalidades Destacadas
🧾 Gestión de gastos (CRUD)
Agregar, editar y eliminar registros.

Clasificación por categorías.

Exportación a CSV.

📈 Reportes y análisis
Cálculo de promedios diarios y mensuales.

Identificación de categorías más costosas.

Detección de días sin gasto.

📊 Visualización de datos
Gráficos ASCII por categoría y por mes.

Estadísticas resumidas.

💵 Conversión de divisas
COP a USD y EUR.

Validación de montos.

🔔 Notificaciones
Alertas automáticas por inactividad o sobrepresupuesto.

💾 Respaldo y persistencia
Guardado en archivos JSON.

Copias de seguridad automáticas.

🧠 Enfoque de Desarrollo
Este proyecto fue desarrollado siguiendo las etapas del Ciclo de Vida del Software (SDLC):

Análisis – Identificación de requisitos funcionales y no funcionales.

Diseño – Arquitectura modular y separación lógica del código.

Implementación – Desarrollo en Python con principios DRY y KISS.

Pruebas – Diseño de test unitarios con pytest y coverage.

Mantenimiento – Validación de cobertura e integración continua.

🧩 Tecnologías Utilizadas
Python 3.12.5

Pytest 8.4.2

Coverage.py 7.0.0

JSON / CSV

Git & GitHub

🧑‍💻 Autor
👤 Brayam Osorio
Estudiante de Ingeniería de Software
Fundación de Estudios Superiores Comfanorte (FESC)
📧 osoriobrayam9@gmail.com

🏁 Conclusión
El proyecto Expense Tracker demuestra una implementación sólida, modular y completamente testeada de un sistema de control financiero personal.
Su estructura y cobertura de pruebas reflejan las buenas prácticas de ingeniería de software, garantizando mantenibilidad, confiabilidad y escalabilidad del código.
=======
# backend_expense_tracker
>>>>>>> 95783c08b6c555bff2a6f1385c3af6f026951df6
