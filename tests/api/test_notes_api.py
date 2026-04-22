import pytest  # Framework de testing: necesario para marcadores y fixtures


# ─── Tests: Health Check ──────────────────────────────────────────────────────

@pytest.mark.smoke  # Marcador 'smoke': este test es el más básico, se corre primero
class TestHealth:
    """Suite de tests para el endpoint GET /health.

    Verifica que la API está activa y respondiendo correctamente.
    Es el punto de partida de cualquier sesión de testing.
    """

    def test_health_status_code_is_200(self, base_url, http_session):
        """Verifica que el endpoint /health-check retorna HTTP 200 OK."""

        # Construye la URL completa concatenando la base con la ruta del endpoint
        url = f"{base_url}/health-check"

        # Realiza la petición GET al endpoint de salud de la API
        response = http_session.get(url)

        # Afirma que el código de estado HTTP es exactamente 200 (OK)
        assert response.status_code == 200, (
            f"Se esperaba 200 pero se recibió {response.status_code}"
        )

    def test_health_response_is_json(self, base_url, http_session):
        """Verifica que la respuesta del endpoint /health es un JSON válido."""

        # Construye la URL del endpoint de salud
        url = f"{base_url}/health"

        # Realiza la petición GET
        response = http_session.get(url)

        # Intenta parsear el body de la respuesta como JSON
        # Si no es JSON válido, esto lanzará una excepción y el test fallará
        body = response.json()

        # Verifica que el resultado del parseo es un diccionario (objeto JSON)
        assert isinstance(body, dict), (
            f"Se esperaba un diccionario JSON pero se recibió: {type(body)}"
        )

    def test_health_response_contains_success_true(self, base_url, http_session):
        """Verifica que la respuesta contiene el campo 'success' con valor True."""

        # Construye la URL del endpoint de salud
        url = f"{base_url}/health-check"

        # Realiza la petición GET
        response = http_session.get(url)

        # Parsea la respuesta JSON en un diccionario Python
        body = response.json()

        # Verifica que el campo 'success' existe en el cuerpo de la respuesta
        assert "success" in body, "El campo 'success' no está en la respuesta"

        # Verifica que el valor de 'success' es exactamente True (booleano)
        assert body["success"] is True, (
            f"Se esperaba success=True pero se recibió: {body.get('success')}"
        )

    def test_health_response_contains_message(self, base_url, http_session):
        """Verifica que la respuesta contiene el campo 'message' con texto."""

        # Construye la URL del endpoint de salud
        url = f"{base_url}/health"

        # Realiza la petición GET
        response = http_session.get(url)

        # Parsea el body JSON
        body = response.json()

        # Verifica que el campo 'message' existe en la respuesta
        assert "message" in body, "El campo 'message' no está en la respuesta"

        # Verifica que 'message' es un string no vacío
        assert isinstance(body["message"], str) and len(body["message"]) > 0, (
            "El campo 'message' debe ser un string no vacío"
        )


# ─── Tests: Registro de usuarios ─────────────────────────────────────────────

@pytest.mark.regression  # Marcador 'regression': test más completo de funcionalidad
class TestUserRegister:
    """Suite de tests para el endpoint POST /users/register.

    Cubre el flujo de registro exitoso y los casos de error más comunes.
    Cada test usa la fixture 'new_user_payload' que genera datos únicos con Faker.
    """

    def test_register_successful_returns_201(self, base_url, http_session, new_user_payload):
        """Verifica que un registro exitoso retorna HTTP 201 Created."""

        # Construye la URL completa del endpoint de registro
        url = f"{base_url}/users/register"

        # Realiza el POST enviando el payload generado por Faker como JSON
        response = http_session.post(url, json=new_user_payload)

        # Afirma que el código HTTP es 201 (recurso creado exitosamente)
        assert response.status_code == 201, (
            f"Se esperaba 201 pero se recibió {response.status_code}. "
            f"Body: {response.text}"
        )

    def test_register_response_is_json(self, base_url, http_session, new_user_payload):
        """Verifica que la respuesta del registro es un JSON válido."""

        # URL del endpoint de registro
        url = f"{base_url}/users/register"

        # Realiza el POST con datos de usuario generados por Faker
        response = http_session.post(url, json=new_user_payload)

        # Parsea la respuesta como JSON; falla si el formato no es válido
        body = response.json()

        # Verifica que el cuerpo es un diccionario (objeto JSON)
        assert isinstance(body, dict), "La respuesta no es un objeto JSON"

    def test_register_response_contains_success_true(self, base_url, http_session, new_user_payload):
        """Verifica que la respuesta de registro exitoso incluye success=True."""

        # URL del endpoint de registro
        url = f"{base_url}/users/register"

        # Realiza el POST
        response = http_session.post(url, json=new_user_payload)

        # Parsea el JSON
        body = response.json()

        # Verifica la presencia del campo 'success'
        assert "success" in body, "El campo 'success' no está en la respuesta"

        # Verifica que 'success' es True para confirmar que el registro funcionó
        assert body["success"] is True, (
            f"Se esperaba success=True pero se recibió: {body.get('success')}"
        )

    def test_register_response_contains_user_data(self, base_url, http_session, new_user_payload):
        """Verifica que la respuesta incluye los datos del usuario registrado."""

        # URL del endpoint de registro
        url = f"{base_url}/users/register"

        # Realiza el POST
        response = http_session.post(url, json=new_user_payload)

        # Parsea el JSON
        body = response.json()

        # Verifica que existe el campo 'data' con los datos del usuario creado
        assert "data" in body, "El campo 'data' no está en la respuesta"

        # Extrae el objeto de datos del usuario de la respuesta
        user_data = body["data"]

        # Verifica que el email retornado coincide con el que enviamos
        assert user_data.get("email") == new_user_payload["email"], (
            "El email en la respuesta no coincide con el enviado"
        )

        # Verifica que el nombre retornado coincide con el que enviamos
        assert user_data.get("name") == new_user_payload["name"], (
            "El nombre en la respuesta no coincide con el enviado"
        )

    def test_register_response_does_not_expose_password(self, base_url, http_session, new_user_payload):
        """Verifica que la API no devuelve la contraseña del usuario en la respuesta."""

        # URL del endpoint de registro
        url = f"{base_url}/users/register"

        # Realiza el POST
        response = http_session.post(url, json=new_user_payload)

        # Convierte toda la respuesta a string para buscar la contraseña en cualquier campo
        response_text = response.text

        # Afirma que la contraseña enviada NO aparece en ningún lugar de la respuesta
        # Esto es una verificación de seguridad importante
        assert new_user_payload["password"] not in response_text, (
            "SEGURIDAD: La contraseña fue expuesta en la respuesta de la API"
        )

    def test_register_duplicate_email_returns_409(self, base_url, http_session, registered_user):
        """Verifica que registrar un email ya existente retorna HTTP 409 Conflict.

        Usa la fixture 'registered_user' que ya registró el usuario previamente,
        luego intenta registrar el mismo email de nuevo para verificar el error.
        """

        # URL del endpoint de registro
        url = f"{base_url}/users/register"

        # Intenta registrar exactamente el mismo usuario que ya existe
        # (registered_user ya hizo el primer registro en su setup)
        response = http_session.post(url, json=registered_user)

        # Verifica que la API responde con 409 Conflict (duplicado)
        assert response.status_code == 409, (
            f"Se esperaba 409 para email duplicado pero se recibió {response.status_code}"
        )

    def test_register_missing_email_returns_400(self, base_url, http_session, new_user_payload):
        """Verifica que omitir el campo email retorna HTTP 400 Bad Request."""

        # URL del endpoint de registro
        url = f"{base_url}/users/register"

        # Crea un payload incompleto eliminando el campo 'email' obligatorio
        incomplete_payload = {
            "name": new_user_payload["name"],      # Incluye nombre
            "password": new_user_payload["password"],  # Incluye contraseña
            # No incluye 'email' intencionalmente para probar la validación
        }

        # Realiza el POST con payload inválido
        response = http_session.post(url, json=incomplete_payload)

        # Verifica que la API valida correctamente y rechaza la petición
        assert response.status_code == 400, (
            f"Se esperaba 400 para payload sin email pero se recibió {response.status_code}"
        )

    def test_register_missing_password_returns_400(self, base_url, http_session, new_user_payload):
        """Verifica que omitir el campo password retorna HTTP 400 Bad Request."""

        # URL del endpoint de registro
        url = f"{base_url}/users/register"

        # Crea un payload sin el campo 'password'
        incomplete_payload = {
            "name": new_user_payload["name"],   # Incluye nombre
            "email": new_user_payload["email"],  # Incluye email
            # No incluye 'password' intencionalmente
        }

        # Realiza el POST con payload incompleto
        response = http_session.post(url, json=incomplete_payload)

        # Verifica que la API retorna error de validación
        assert response.status_code == 400, (
            f"Se esperaba 400 para payload sin password pero se recibió {response.status_code}"
        )


# ─── Tests: Login de usuarios ─────────────────────────────────────────────────

@pytest.mark.regression  # Marcador 'regression': test de funcionalidad completa
class TestUserLogin:
    """Suite de tests para el endpoint POST /users/login.

    Cubre el flujo de login exitoso y los casos de error de credenciales.
    Depende de la fixture 'registered_user' para tener un usuario válido con qué hacer login.
    """

    def test_login_successful_returns_200(self, base_url, http_session, registered_user):
        """Verifica que un login exitoso retorna HTTP 200 OK."""

        # Construye la URL del endpoint de login
        url = f"{base_url}/users/login"

        # Construye el payload con las credenciales del usuario ya registrado
        login_payload = {
            "email": registered_user["email"],       # Email del usuario registrado
            "password": registered_user["password"],  # Contraseña del usuario registrado
        }

        # Realiza el POST al endpoint de login
        response = http_session.post(url, json=login_payload)

        # Verifica que el login fue exitoso con HTTP 200
        assert response.status_code == 200, (
            f"Se esperaba 200 pero se recibió {response.status_code}. "
            f"Body: {response.text}"
        )

    def test_login_response_contains_token(self, base_url, http_session, registered_user):
        """Verifica que el login exitoso retorna un token de autenticación."""

        # URL del endpoint de login
        url = f"{base_url}/users/login"

        # Payload con credenciales válidas del usuario registrado
        login_payload = {
            "email": registered_user["email"],
            "password": registered_user["password"],
        }

        # Realiza el POST
        response = http_session.post(url, json=login_payload)

        # Parsea la respuesta JSON
        body = response.json()

        # Verifica que existe el campo 'data' en la respuesta
        assert "data" in body, "El campo 'data' no está en la respuesta del login"

        # Extrae los datos del usuario autenticado
        user_data = body["data"]

        # Verifica que el token de autenticación está presente y no está vacío
        # El token se usará en las cabeceras de requests subsiguientes que requieran auth
        assert "token" in user_data, "El campo 'token' no está en data del login"
        assert len(user_data["token"]) > 0, "El token no debe estar vacío"

    def test_login_response_contains_user_info(self, base_url, http_session, registered_user):
        """Verifica que la respuesta del login incluye la información del usuario."""

        # URL del endpoint de login
        url = f"{base_url}/users/login"

        # Payload de credenciales
        login_payload = {
            "email": registered_user["email"],
            "password": registered_user["password"],
        }

        # Realiza el POST
        response = http_session.post(url, json=login_payload)

        # Parsea la respuesta
        body = response.json()

        # Extrae los datos del usuario
        user_data = body["data"]

        # Verifica que el email en la respuesta coincide con el del login
        assert user_data.get("email") == registered_user["email"], (
            "El email en la respuesta no coincide con el del usuario autenticado"
        )

    def test_login_wrong_password_returns_401(self, base_url, http_session, registered_user, fake):
        """Verifica que usar una contraseña incorrecta retorna HTTP 401 Unauthorized."""

        # URL del endpoint de login
        url = f"{base_url}/users/login"

        # Construye payload con email correcto pero contraseña incorrecta
        login_payload = {
            "email": registered_user["email"],   # Email válido del usuario registrado
            "password": "WrongPass@9999",         # Contraseña deliberadamente incorrecta
        }

        # Realiza el POST con credenciales inválidas
        response = http_session.post(url, json=login_payload)

        # Verifica que la API rechaza el acceso con 401 Unauthorized
        assert response.status_code == 401, (
            f"Se esperaba 401 para contraseña incorrecta pero se recibió {response.status_code}"
        )

    def test_login_nonexistent_email_returns_401(self, base_url, http_session, fake):
        """Verifica que intentar login con un email no registrado retorna 401."""

        # URL del endpoint de login
        url = f"{base_url}/users/login"

        # Construye payload con un email que definitivamente no existe en el sistema
        login_payload = {
            "email": f"nonexistent_{fake.uuid4()[:8]}@nowhere.com",  # Email inventado único
            "password": "SomePass@1234",  # Contraseña cualquiera (el email no existe)
        }

        # Realiza el POST
        response = http_session.post(url, json=login_payload)

        # Verifica que la API retorna 401 para credenciales inválidas
        assert response.status_code == 401, (
            f"Se esperaba 401 para email inexistente pero se recibió {response.status_code}"
        )

    def test_login_missing_email_returns_400(self, base_url, http_session):
        """Verifica que omitir el campo email en el login retorna 400 Bad Request."""

        # URL del endpoint de login
        url = f"{base_url}/users/login"

        # Payload sin el campo 'email' para probar la validación del servidor
        incomplete_payload = {
            "password": "SomePass@1234",  # Solo envía contraseña, sin email
        }

        # Realiza el POST con payload incompleto
        response = http_session.post(url, json=incomplete_payload)

        # Verifica que la API valida y rechaza la petición incompleta
        assert response.status_code == 400, (
            f"Se esperaba 400 para login sin email pero se recibió {response.status_code}"
        )

    def test_login_missing_password_returns_400(self, base_url, http_session, registered_user):
        """Verifica que omitir el campo password en el login retorna 400 Bad Request."""

        # URL del endpoint de login
        url = f"{base_url}/users/login"

        # Payload sin el campo 'password'
        incomplete_payload = {
            "email": registered_user["email"],  # Solo envía email, sin contraseña
        }

        # Realiza el POST con payload incompleto
        response = http_session.post(url, json=incomplete_payload)

        # Verifica que la API rechaza la petición por falta de validación del campo
        assert response.status_code == 400, (
            f"Se esperaba 400 para login sin password pero se recibió {response.status_code}"
        )
