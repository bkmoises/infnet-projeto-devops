import flask
from app.app import app, home

def test_home():
    with app.app_context():
        response = home()
        assert isinstance(response, flask.Response)
        assert response.status_code == 200
        assert response.get_json() == {"mensagem": "Bem-vindo à API de Filmes!"}
