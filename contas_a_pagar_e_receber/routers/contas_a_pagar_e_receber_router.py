from fastapi import APIRouter, Depends
# from pydantic import BaseModel
from pydantic import BaseModel, ConfigDict # Atualização
from typing import List
from sqlalchemy.orm import Session
from pydantic import Field
from enum import Enum

from contas_a_pagar_e_receber.models.conta_a_pagar_e_receber_model import ContaPagarReceber
from shared.dependencies import get_db


router = APIRouter(prefix="/contas-a-pagar-e-receber")

class ContaPagarReceberResponse(BaseModel):
    id: int
    descricao: str
    valor: float
    tipo: str # PAGAR, RECEBER
    # Atualização do Pydantic 2.x 
    #class Config:
    #    orm_mode = True
    model_config = ConfigDict(from_attributes=True)

class ContaPagarReceberTipoEnum(str, Enum):
    PAGAR = 'PAGAR'
    RECEBER = 'RECEBER'

class ContaPagarReceberRequest(BaseModel):
    descricao: str = Field(min_length=3, max_length=30)
    valor: float = Field(gt=0)
    tipo: ContaPagarReceberTipoEnum = Field() # PAGAR, RECEBER

@router.get("/", response_model=List[ContaPagarReceberResponse])
def listar_contas(db: Session = Depends(get_db)) -> List[ContaPagarReceberResponse]:
    return db.query(ContaPagarReceber).all()


@router.post("/", response_model=ContaPagarReceberResponse, status_code=201)
def criar_conta(conta_a_pagar_e_receber_request: ContaPagarReceberRequest, db: Session = Depends(get_db)) -> ContaPagarReceberResponse:
    contas_a_pagar_e_receber = ContaPagarReceber(
        # descricao = conta.descricao, valor = conta.valor, tipo = conta.tipo
        #**conta_a_pagar_e_receber_request.dict()
        **conta_a_pagar_e_receber_request.model_dump() # Atualização do Pydantic
    )
    db.add(contas_a_pagar_e_receber)
    db.commit()
    db.refresh(contas_a_pagar_e_receber)
    #return ContaPagarReceberResponse(
        # id=3,
        # descricao=conta_a_pagar_e_receber_request.descricao,
        # valor=conta_a_pagar_e_receber_request.valor,
        # tipo=conta_a_pagar_e_receber_request.tipo
    #    **contas_a_pagar_e_receber.__dict__
    #)
    return contas_a_pagar_e_receber

