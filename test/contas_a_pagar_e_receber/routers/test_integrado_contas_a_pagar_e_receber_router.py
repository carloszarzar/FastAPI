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

def test_deve_pegar_por_id():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response_get = client.post("/contas-a-pagar-e-receber", json={
        "descricao": "Curso de Python",
        "valor": 333,
        "tipo": "PAGAR"
    })

    id_da_conta_a_pagar_e_receber = response_get.json()['id']

    response_get = client.get(f"/contas-a-pagar-e-receber/{id_da_conta_a_pagar_e_receber}")

    assert response_get.status_code == 200
    assert response_get.json()['valor'] == 333.0
    assert response_get.json()['tipo'] == "PAGAR"
    assert response_get.json()['descricao'] == "Curso de Python"

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

# Método TDD - Test Drive Development
def test_deve_atualizar_conta_a_pagar_e_receber():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response = client.post("/contas-a-pagar-e-receber/", json={
        "descricao": "Curso de Python",
        "valor": 333,
        "tipo": "PAGAR"
    })
    id_da_conta_a_pagar_e_receber = response.json()['id']

    response_put = client.put(f"/contas-a-pagar-e-receber/{id_da_conta_a_pagar_e_receber}", json={
        "descricao": "Curso de Python",
        "valor": 111,
        "tipo": "PAGAR"
    })
    assert response_put.status_code == 200 
    assert response_put.json()['valor'] == 111

def test_deve_remover_conta_a_pagar_e_receber():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response = client.post("/contas-a-pagar-e-receber/", json={
        "descricao": "Curso de Python",
        "valor": 333,
        "tipo": "PAGAR"
    })
    id_da_conta_a_pagar_e_receber = response.json()['id']

    response_put = client.delete(f"/contas-a-pagar-e-receber/{id_da_conta_a_pagar_e_receber}")
    assert response_put.status_code == 204 
#-------------------------------------------------------

    

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





    #------- Rodar no terminal para fazer o teste ----#
    # python -m pytest ./test/contas_a_pagar_e_receber/routers/test_integrado_contas_a_pagar_e_receber_router.py