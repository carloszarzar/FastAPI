# uvicorn é o servidor que vai rodar nossa aplicação FastAPI
import uvicorn
# FastAPI é o framework web que usamos para criar a API
from fastapi import FastAPI

# Importa o arquivo de rotas da parte de "contas a pagar e receber"
from contas_a_pagar_e_receber.routers import contas_a_pagar_e_receber_router
from contas_a_pagar_e_receber.routers import fornecedor_cliente_router
from shared.exceptions import NotFound
from shared.exceptions_handler import not_found_exception_handler 

# Aqui criamos uma instância da nossa aplicação FastAPI
app = FastAPI() # Cria a aplicação
# Quando o usuário acessar a URL raiz ("/"), ele vai receber esse texto como resposta
@app.get("/") # Define uma rota GET na raiz
def oi_eu_sou_programador() -> str:
    return "Oi, eu sou programador"
# Aqui a gente "inclui" as rotas que estão no arquivo contas_a_pagar_e_receber_router.py
app.include_router(contas_a_pagar_e_receber_router.router) # Adiciona rotas (módulos) de outros arquivos. Indica o controlador de funções (métodos)
app.include_router(fornecedor_cliente_router.router)
app.add_exception_handler(NotFound, not_found_exception_handler)

# Rodando o servidor com Uvicorn
if __name__ == "__main__":
    # Inicia o servidor
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True) # 0.0.0.0 todas as intervaces da rede. Pode ser acessado pela rede local ou internet (se firewall/liberação permitir)
    # 127.0.0.1	Somente localhost	Apenas pelo mesmo computador


