import pytest          # Framework de testing: necesario para los decoradores @pytest.fixture
import requests        # Librería HTTP: se usará para hacer las llamadas a la API
from faker import Faker  # Generador de datos falsos: crea nombres, emails, passwords únicos


# ─── Constantes globales ──────────────────────────────────────────────────────

# URL base de la API que se va a testear
# Todas las rutas de los tests se construirán concatenando sobre esta URL
BASE_URL = "https://practice.expandtesting.com/notes/api"


# ─── Fixtures de configuración ────────────────────────────────────────────────

@pytest.fixture(scope="session")
def base_url():
    """Retorna la URL base de la API.

    scope="session" significa que esta fixture se crea una sola vez
    para toda la sesión de tests (no se recrea entre tests individuales).
    """
    return BASE_URL  # Devuelve la URL base para que los tests la usen


@pytest.fixture(scope="session")
def http_session():
    """Crea y retorna una sesión HTTP reutilizable.

    requests.Session() permite reutilizar la conexión TCP entre requests,
    lo que hace los tests más rápidos. También mantiene headers comunes.
    scope="session" garantiza que se use la misma sesión en todos los tests.
    """
    session = requests.Session()  # Crea la sesión HTTP persistente

    # Header que indica al servidor que esperamos respuestas en formato JSON
    session.headers.update({"Content-Type": "application/json"})

    yield session  # Entrega la sesión a los tests que la soliciten

    session.close()  # Cierra la sesión al terminar todos los tests (cleanup)


@pytest.fixture(scope="function")
def fake():
    """Crea y retorna una instancia de Faker configurada en inglés.

    scope="function" significa que se crea una instancia NUEVA de Faker
    para cada función de test, garantizando independencia entre tests.
    El locale "en_US" genera datos en formato estadounidense (nombres, emails, etc.).
    """
    return Faker("en_US")  # Instancia Faker con localización en inglés


@pytest.fixture(scope="function")
def new_user_payload(fake):
    """Genera un payload completo con datos únicos para registrar un usuario nuevo.

    Utiliza la fixture 'fake' para generar datos aleatorios cada vez,
    evitando colisiones con usuarios previamente registrados.
    scope="function" asegura datos distintos en cada test que lo use.
    """
    return {
        # Genera un nombre completo falso como "John Smith"
        "name": fake.name(),

        # Genera un email único usando un UUID corto para evitar duplicados
        # Ejemplo: "qa_a3f2b1@example.com"
        "email": f"qa_{fake.uuid4()[:8]}@example.com",

        # Genera una contraseña que cumple los requisitos de la API:
        # mínimo 6 caracteres, con al menos una mayúscula y un número
        "password": "Test@" + fake.numerify("####"),  # Ejemplo: "Test@7382"
    }


@pytest.fixture(scope="function")
def registered_user(base_url, http_session, new_user_payload):
    """Registra un usuario en la API y lo retorna listo para ser usado en tests.

    Esta fixture encadena otras fixtures para crear un usuario real en la API.
    Es útil para tests que necesitan un usuario existente (como el login).
    scope="function" garantiza un usuario fresco y único para cada test.
    """
    # Hace el POST a /users/register con los datos generados por new_user_payload
    response = http_session.post(
        f"{base_url}/users/register",  # URL completa del endpoint de registro
        json=new_user_payload,          # Envía el payload como JSON en el body
    )

    # Verifica que el registro fue exitoso antes de continuar
    # Si falla, el test que use esta fixture fallará aquí con un mensaje claro
    assert response.status_code == 201, (
        f"Setup fallido: no se pudo registrar el usuario. "
        f"Status: {response.status_code}, Body: {response.text}"
    )

    # Retorna el payload original para que el test sepa qué email/password usar
    return new_user_payload
