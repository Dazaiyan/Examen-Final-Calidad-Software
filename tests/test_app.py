def test_index_redirects(client):
    """Prueba que la página de inicio redirija al login si no está autenticado."""
    response = client.get('/')
    assert response.status_code == 302
    assert '/login' in response.headers['Location']

def test_login_page(client):
    """Prueba que la página de login se carga correctamente."""
    response = client.get('/login')
    assert response.status_code == 200
    assert 'Iniciar Sesión'.encode('utf-8') in response.data

def test_valid_login(client):
    """Prueba que un usuario puede iniciar sesión con credenciales válidas."""
    # Registra un usuario de prueba
    client.post('/register', data={'username': 'testuser', 'password': 'testpassword'})
    response = client.post('/login', data={'username': 'testuser', 'password': 'testpassword'})
    assert response.status_code == 302
    assert '/empleados' in response.headers['Location']

def test_invalid_login(client):
    """Prueba que un usuario no puede iniciar sesión con credenciales inválidas."""
    response = client.post('/login', data={'username': 'wronguser', 'password': 'wrongpassword'})
    assert response.status_code == 200
    assert 'Nombre de usuario o contraseña incorrectos'.encode('utf-8') in response.data
