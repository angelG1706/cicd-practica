import pytest
from app import app, sumar, es_palindromo, calcular_descuento

# ============================================================
# PRUEBAS UNITARIAS - prueban funciones individuales
# ============================================================

class TestSumar:
    def test_sumar_positivos(self):
        assert sumar(2, 3) == 5

    def test_sumar_negativos(self):
        assert sumar(-1, -1) == -2

    def test_sumar_con_cero(self):
        assert sumar(5, 0) == 5

    def test_sumar_decimales(self):
        assert sumar(1.5, 2.5) == 4.0


class TestPalindromo:
    def test_palindromo_simple(self):
        assert es_palindromo("oso") == True

    def test_no_palindromo(self):
        assert es_palindromo("python") == False

    def test_palindromo_con_espacios(self):
        assert es_palindromo("anita lava la tina") == True

    def test_palindromo_mayusculas(self):
        assert es_palindromo("Ana") == True


class TestDescuento:
    def test_descuento_normal(self):
        assert calcular_descuento(100, 10) == 90.0

    def test_descuento_cero(self):
        assert calcular_descuento(100, 0) == 100.0

    def test_descuento_total(self):
        assert calcular_descuento(100, 100) == 0.0

    def test_descuento_invalido(self):
        with pytest.raises(ValueError):
            calcular_descuento(100, 150)


# ============================================================
# PRUEBAS DE INTEGRACIÓN - prueban las rutas HTTP
# ============================================================

@pytest.fixture
def cliente():
    app.config['TESTING'] = True
    with app.test_client() as cliente:
        yield cliente

class TestRutas:
    def test_ruta_inicio(self, cliente):
        respuesta = cliente.get('/')
        assert respuesta.status_code == 200
        datos = respuesta.get_json()
        assert datos['status'] == 'ok'

    def test_ruta_sumar(self, cliente):
        respuesta = cliente.get('/sumar/5/3')
        assert respuesta.status_code == 200
        datos = respuesta.get_json()
        assert datos['resultado'] == 8

    def test_ruta_palindromo(self, cliente):
        respuesta = cliente.get('/palindromo/oso')
        assert respuesta.status_code == 200
        datos = respuesta.get_json()
        assert datos['es_palindromo'] == True

    def test_ruta_salud(self, cliente):
        respuesta = cliente.get('/salud')
        assert respuesta.status_code == 200
