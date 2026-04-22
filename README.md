# 🧪 ExpandTesting API — Suite de Pruebas Automatizadas

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-8.3.5-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)
![Requests](https://img.shields.io/badge/Requests-2.32.3-FF6F00?style=for-the-badge&logo=python&logoColor=white)
![Faker](https://img.shields.io/badge/Faker-37.1.0-00C897?style=for-the-badge)
![HTML Report](https://img.shields.io/badge/Reporte-pytest--html-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![Tests](https://img.shields.io/badge/Tests-19%20pasando-brightgreen?style=for-the-badge)
![License](https://img.shields.io/badge/Licencia-MIT-yellow?style=for-the-badge)

> Suite profesional de automatización de pruebas de API dirigida a la [ExpandTesting Notes API](https://practice.expandtesting.com/notes/api). Cubre verificaciones de salud, registro de usuarios y flujos de autenticación con datos de prueba generados automáticamente y un reporte HTML completo.

---

## 📋 Tabla de Contenidos

- [Stack Tecnológico](#-stack-tecnológico)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Instalación](#-instalación)
- [Ejecutar las Pruebas](#-ejecutar-las-pruebas)
- [Reporte HTML](#-reporte-html)
- [Suites de Pruebas](#-suites-de-pruebas)
- [Sobre Mí](#-sobre-mí)

---

## 🛠️ Stack Tecnológico

| Herramienta | Versión | Propósito |
|---|---|---|
| **Python** | 3.11+ | Lenguaje principal |
| **Pytest** | 8.3.5 | Framework y ejecutor de pruebas |
| **Requests** | 2.32.3 | Cliente HTTP para llamadas a la API |
| **Faker** | 37.1.0 | Generación dinámica de datos de prueba |
| **pytest-html** | 4.1.1 | Generación automática de reportes HTML |
| **python-dotenv** | 1.1.0 | Gestión de variables de entorno |

---

## 📁 Estructura del Proyecto

```
ExpandTesting-API/
│
├── tests/
│   ├── conftest.py            # Fixtures compartidos: URL base, sesión HTTP, Faker, payloads
│   └── api/
│       └── test_notes_api.py  # Todas las suites de pruebas (Health, Register, Login)
│
├── reports/
│   └── report.html            # Reporte HTML generado automáticamente
│
├── pytest.ini                 # Configuración de Pytest: markers, rutas, salida del reporte
├── requirements.txt           # Dependencias del proyecto
└── README.md
```

**Archivos clave explicados:**

- **`conftest.py`** — Define fixtures reutilizables compartidos entre todas las pruebas: la URL base, una `requests.Session` persistente, una instancia de `Faker`, payloads de usuario y un fixture `registered_user` que pre-registra un usuario en la API antes de ejecutar una prueba.
- **`test_notes_api.py`** — Contiene las tres clases de prueba (`TestHealth`, `TestUserRegister`, `TestUserLogin`) con 19 pruebas en total.
- **`pytest.ini`** — Configura el descubrimiento de pruebas, markers personalizados (`smoke`, `regression`) y habilita el reporte HTML automático en cada ejecución.

---

## ⚙️ Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/your-username/ExpandTesting-API.git
cd ExpandTesting-API
```

### 2. Crear y activar el entorno virtual

```bash
# Crear el entorno virtual
python -m venv venv

# Activar — macOS / Linux
source venv/bin/activate

# Activar — Windows (PowerShell)
venv\Scripts\Activate.ps1

# Activar — Windows (CMD)
venv\Scripts\activate.bat
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## ▶️ Ejecutar las Pruebas

### Ejecutar la suite completa

```bash
pytest
```

### Ejecutar solo pruebas smoke (verificación de salud)

```bash
pytest -m smoke
```

### Ejecutar solo pruebas de regresión (registro + login)

```bash
pytest -m regression
```

### Ejecutar una clase de prueba específica

```bash
pytest tests/api/test_notes_api.py::TestUserLogin
```

### Ejecutar una prueba individual

```bash
pytest tests/api/test_notes_api.py::TestUserRegister::test_register_successful_returns_201
```

### Ejecutar con salida detallada

```bash
pytest -v
```

> **Nota:** El reporte HTML se genera automáticamente en cada ejecución (configurado en `pytest.ini`). No se necesitan flags adicionales.

---

## 📊 Reporte HTML

Después de cualquier ejecución, se genera un reporte HTML autocontenido en:

```
reports/report.html
```

Ábrelo en cualquier navegador:

```bash
# macOS
open reports/report.html

# Linux
xdg-open reports/report.html

# Windows
start reports/report.html
```

El reporte incluye:
- ✅ Estado de aprobado / ❌ fallido por prueba
- Tiempo de ejecución por prueba y duración total
- Trazas completas para cualquier fallo
- Metadatos del entorno (versión de Python, plataforma, plugins)

---

## 🧩 Suites de Pruebas

### 🟢 `TestHealth` — `@pytest.mark.smoke` (4 pruebas)

Valida que la API esté activa y respondiendo correctamente. Son las pruebas más rápidas y se ejecutan primero.

| Prueba | Qué verifica |
|---|---|
| `test_health_status_code_is_200` | `GET /health-check` retorna HTTP 200 |
| `test_health_response_is_json` | El cuerpo de la respuesta es un objeto JSON válido |
| `test_health_response_contains_success_true` | El cuerpo JSON contiene `"success": true` |
| `test_health_response_contains_message` | El cuerpo JSON contiene un string `"message"` no vacío |

---

### 🟡 `TestUserRegister` — `@pytest.mark.regression` (8 pruebas)

Cubre el flujo completo de registro incluyendo ruta feliz, validación de datos, verificaciones de seguridad y manejo de errores. Cada prueba usa Faker para generar un usuario único, evitando conflictos.

| Prueba | Qué verifica |
|---|---|
| `test_register_successful_returns_201` | `POST /users/register` retorna HTTP 201 |
| `test_register_response_is_json` | La respuesta es un objeto JSON válido |
| `test_register_response_contains_success_true` | La respuesta incluye `"success": true` |
| `test_register_response_contains_user_data` | El `data` de la respuesta incluye `email` y `name` correctos |
| `test_register_response_does_not_expose_password` | La contraseña **no** está presente en ningún lugar de la respuesta (verificación de seguridad) |
| `test_register_duplicate_email_returns_409` | Registrar el mismo email nuevamente retorna HTTP 409 Conflict |
| `test_register_missing_email_returns_400` | Payload sin `email` retorna HTTP 400 Bad Request |
| `test_register_missing_password_returns_400` | Payload sin `password` retorna HTTP 400 Bad Request |

---

### 🔵 `TestUserLogin` — `@pytest.mark.regression` (7 pruebas)

Valida el flujo de autenticación. Depende del fixture `registered_user` para garantizar que exista un usuario válido antes de ejecutar las pruebas de login.

| Prueba | Qué verifica |
|---|---|
| `test_login_successful_returns_200` | `POST /users/login` con credenciales válidas retorna HTTP 200 |
| `test_login_response_contains_token` | Un login exitoso retorna un `token` de autenticación no vacío |
| `test_login_response_contains_user_info` | El `data` de la respuesta contiene el `email` del usuario autenticado |
| `test_login_wrong_password_returns_401` | Email correcto + contraseña incorrecta retorna HTTP 401 Unauthorized |
| `test_login_nonexistent_email_returns_401` | Login con email no registrado retorna HTTP 401 |
| `test_login_missing_email_returns_400` | Payload sin `email` retorna HTTP 400 Bad Request |
| `test_login_missing_password_returns_400` | Payload sin `password` retorna HTTP 400 Bad Request |

---

## 👤 Sobre Mí

¡Hola! Soy **Miguel**, un **QA Automation Engineer** apasionado por construir frameworks de pruebas robustos y mantenibles que detecten bugs reales antes de que lleguen a producción.

Me especializo en automatización de pruebas de API usando stacks basados en Python, con enfoque en diseño limpio de pruebas, aserciones significativas y estrategias confiables de datos de prueba. Este proyecto refleja mi enfoque hacia las pruebas de API: pruebas aisladas, datos dinámicos, cero estado hardcodeado y reportes claros.

📫 ¡No dudes en conectar o escribirme!

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Conectar-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/your-profile)
[![GitHub](https://img.shields.io/badge/GitHub-Seguir-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/your-username)

---

<p align="center">Hecho con ❤️ y mucho <code>pytest -v</code></p>
