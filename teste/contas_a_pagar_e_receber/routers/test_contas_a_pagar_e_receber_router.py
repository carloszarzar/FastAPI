from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_deve_listar_contas_a_pagar_e_receber():
    response = client.get("/contas-a-pagar-e-receber/")
    assert response.status_code == 200
    # print(response.json())
    assert response.json() == [
        {'id': 1, 'descricao': 'Aluguel', 'valor': 1000.5, 'tipo': 'PAGAR'}, 
        {'id': 2, 'descricao': 'Salário', 'valor': 5000.0, 'tipo': 'RECEBER'}
    ]


#--- teste api criar conta (post) ---#
def test_deve_criar_conta_a_pagar_e_receber():
    payload = {
        "descricao": "Curso FastAPI",
        "valor": 299.90,
        "tipo": "PAGAR"
    }

    response = client.post("/contas-a-pagar-e-receber/", json=payload)

    assert response.status_code == 201
    assert response.json() == {
        "id": 3,
        "descricao": "Curso FastAPI",
        "valor": 299.90,
        "tipo": "PAGAR"
    }
