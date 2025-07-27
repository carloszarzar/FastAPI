import uvicorn
from fastapi import FastAPI

from contas_a_pagar_e_receber.routers import contas_a_pagar_e_receber_router


#---- Pode Apagar ----#
# from shared.database import engine, Base
#from contas_a_pagar_e_receber.models.conta_a_pagar_e_receber_model import ContaPagarReceber
#Base.metadata.drop_all(bind=engine)
#Base.metadata.create_all(bind=engine)
#-----------------------


app = FastAPI()

@app.get("/")
def oi_eu_sou_programador() -> str:
    return "Oi, eu sou programador"

app.include_router(contas_a_pagar_e_receber_router.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True) # 0.0.0.0 todas as intervaces da rede. Pode ser acessado pela rede local ou internet (se firewall/liberação permitir)
    # 127.0.0.1	Somente localhost	Apenas pelo mesmo computador


