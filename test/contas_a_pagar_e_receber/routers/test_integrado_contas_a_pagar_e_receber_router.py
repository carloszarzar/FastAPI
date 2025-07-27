from fastapi.testclient import TestClient
from main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from shared.dependencies import get_db
from shared.database import Base

client = TestClient(app)

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

def test_deve_listar_contas_a_pagar_e_receber():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    client.post("/contas-a-pagar-e-receber/", json={'descricao': 'Aluguel', 'valor': 1000.5, 'tipo': 'PAGAR'})
    client.post("/contas-a-pagar-e-receber/", json={'descricao': 'Salário', 'valor': 5000.0, 'tipo': 'RECEBER'})

    response = client.get("/contas-a-pagar-e-receber/")
    assert response.status_code == 200
    # print(response.json())
    assert response.json() == [
        {'id': 1, 'descricao': 'Aluguel', 'valor': 1000.5, 'tipo': 'PAGAR'}, 
        {'id': 2, 'descricao': 'Salário', 'valor': 5000.0, 'tipo': 'RECEBER'}
    ]


#--- teste api criar conta (post) ---#
def test_deve_criar_conta_a_pagar_e_receber():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    payload = {
        "descricao": "Curso FastAPI",
        "valor": 299.90,
        "tipo": "PAGAR"
    }

    response = client.post("/contas-a-pagar-e-receber/", json=payload)

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "descricao": "Curso FastAPI",
        "valor": 299.90,
        "tipo": "PAGAR"
    }

def teste_deve_retornar_erro_quando_exceder_a_descricao():
    response = client.post("/contas-a-pagar-e-receber/", json={
        "descricao": "0123456789012345678901234567890",
        "valor": 333,
        "tipo": "PAGAR"
    })
    assert response.status_code == 422
    assert response.json()['detail'][0]['loc'] == ['body','descricao']

def teste_deve_retornar_erro_quando_a_descricao_for_menor_que_o_necessario():
    response = client.post("/contas-a-pagar-e-receber/", json={
        "descricao": "01",
        "valor": 333,
        "tipo": "PAGAR"
    })
    assert response.status_code == 422
    assert response.json()['detail'][0]['loc'] == ['body','descricao']

def teste_deve_retornar_erro_quando_o_valor_for_zero_ou_menor():
    response = client.post("/contas-a-pagar-e-receber/", json={
        "descricao": "Teste",
        "valor": 0,
        "tipo": "PAGAR"
    })
    assert response.status_code == 422
    assert response.json()['detail'][0]['loc'] == ['body','valor']

    response = client.post("/contas-a-pagar-e-receber/", json={
        "descricao": "Teste",
        "valor": -1,
        "tipo": "PAGAR"
    })
    assert response.status_code == 422
    assert response.json()['detail'][0]['loc'] == ['body','valor']

def teste_deve_retornar_erro_quando_o_tipo_for_invalido():
    response = client.post("/contas-a-pagar-e-receber/", json={
        "descricao": "Teste",
        "valor": 100,
        "tipo": "InváLIDO"
    })
    assert response.status_code == 422
    assert response.json()['detail'][0]['loc'] == ['body','tipo']