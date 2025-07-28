## Esse script é responsável por expor a API de contas a pagar/receber:
# Recebe requisições da web.
# Valida os dados automaticamente.
# Interage com o banco de dados via SQLAlchemy.
# Organiza as rotas com APIRouter.

from fastapi import APIRouter, Depends, HTTPException
# from pydantic import BaseModel
from pydantic import BaseModel, ConfigDict # Atualização
from typing import List
from sqlalchemy.orm import Session
from pydantic import Field
from enum import Enum
# Importanto os módulos e dependencias criadas no projeto
from contas_a_pagar_e_receber.models.conta_a_pagar_e_receber_model import ContaPagarReceber
from shared.dependencies import get_db
from shared.exceptions import NotFound

# Cria um "roteador" que agrupa todas as rotas (módulos) com o prefixo /contas-a-pagar-e-receber.
router = APIRouter(prefix="/contas-a-pagar-e-receber")
# Modelo de Resposta da API, Define como os dados serão retornados na API (resposta).
class ContaPagarReceberResponse(BaseModel):
    id: int
    descricao: str
    valor: float
    tipo: str # PAGAR, RECEBER
    # Atualização do Pydantic 2.x 
    #class Config:
    #    orm_mode = True
    model_config = ConfigDict(from_attributes=True) # Permite que o Pydantic use objetos ORM (como do SQLAlchemy).

# Padronização dos dados. Enum (tipo da conta), Define os únicos dois valores válidos para o campo tipo.
class ContaPagarReceberTipoEnum(str, Enum):
    PAGAR = 'PAGAR'
    RECEBER = 'RECEBER'

# Modelo de Requisição da API (entrada de dados)
class ContaPagarReceberRequest(BaseModel):
    descricao: str = Field(min_length=3, max_length=30)
    valor: float = Field(gt=0)
    tipo: ContaPagarReceberTipoEnum = Field() # PAGAR, RECEBER

# GET – Listar contas, 
@router.get("/", response_model=List[ContaPagarReceberResponse]) # Essa rota responde ao método GET em /contas-a-pagar-e-receber/.
def listar_contas(db: Session = Depends(get_db)) -> List[ContaPagarReceberResponse]: # Retorna uma lista de objetos no formato ContaPagarReceberResponse.
    return db.query(ContaPagarReceber).all() # Busca todos os registros da tabela ContaPagarReceber.
#---------------------------------------------
@router.get("/{id_da_conta_a_pagar_e_receber}", response_model=ContaPagarReceberResponse) # Essa rota responde ao método GET em /contas-a-pagar-e-receber/.
def obter_conta_por_id(id_da_conta_a_pagar_e_receber: int,
                  db: Session = Depends(get_db)) -> List[ContaPagarReceberResponse]: # Retorna uma lista de objetos no formato ContaPagarReceberResponse.
    #conta_a_pagar_e_receber: ContaPagarReceber = db.get(ContaPagarReceber, id_da_conta_a_pagar_e_receber) # Busca todos os registros da tabela ContaPagarReceber.
        
    return busca_conta_por_id(id_da_conta_a_pagar_e_receber, db)
#---------------------------------------------
# POST – Criar uma nova conta
@router.post("/", response_model=ContaPagarReceberResponse, status_code=201) # Essa rota responde ao método POST em /contas-a-pagar-e-receber/.
def criar_conta(conta_a_pagar_e_receber_request: ContaPagarReceberRequest, db: Session = Depends(get_db)) -> ContaPagarReceberResponse:
    contas_a_pagar_e_receber = ContaPagarReceber(
        # descricao = conta.descricao, valor = conta.valor, tipo = conta.tipo
        #**conta_a_pagar_e_receber_request.dict()
        **conta_a_pagar_e_receber_request.model_dump() # Atualização do Pydantic # Converte o objeto Pydantic para dicionário com .model_dump() (Pydantic v2).
    )
    db.add(contas_a_pagar_e_receber)
    db.commit()
    db.refresh(contas_a_pagar_e_receber)
    return contas_a_pagar_e_receber

# PUT – Inserir dados no banco de dados
@router.put("/{id_da_conta_a_pagar_e_receber}", response_model=ContaPagarReceberResponse, status_code=200) # Essa rota responde ao método PUT em /contas-a-pagar-e-receber/.
def atualizar_conta(id_da_conta_a_pagar_e_receber: int,
                conta_a_pagar_e_receber_request: ContaPagarReceberRequest,
                db: Session = Depends(get_db)) -> ContaPagarReceberResponse:
    #conta_a_pagar_e_receber: ContaPagarReceber = db.get(ContaPagarReceber, id_da_conta_a_pagar_e_receber)
    conta_a_pagar_e_receber = busca_conta_por_id(id_da_conta_a_pagar_e_receber, db)
    conta_a_pagar_e_receber.tipo = conta_a_pagar_e_receber_request.tipo
    conta_a_pagar_e_receber.valor = conta_a_pagar_e_receber_request.valor
    conta_a_pagar_e_receber.descricao = conta_a_pagar_e_receber_request.descricao
    db.add(conta_a_pagar_e_receber)
    db.commit()
    db.refresh(conta_a_pagar_e_receber)
    return conta_a_pagar_e_receber

@router.delete("/{id_da_conta_a_pagar_e_receber}",status_code=204)
def excluir_conta(id_da_conta_a_pagar_e_receber: int,
                db: Session = Depends(get_db)) -> None:
    
    
    #if conta_a_pagar_e_receber is None:
    #    raise HTTPException(status_code=404, detail="Conta não encontrada")
    
    conta_a_pagar_e_receber = busca_conta_por_id(id_da_conta_a_pagar_e_receber, db)

    db.delete(conta_a_pagar_e_receber)
    db.commit()



#---------------------------------------------
def busca_conta_por_id(id_da_conta_a_pagar_e_receber: int, db: Session) -> ContaPagarReceber:
    conta_a_pagar_e_receber = db.get(ContaPagarReceber, id_da_conta_a_pagar_e_receber)


    if conta_a_pagar_e_receber is None:
        raise NotFound("conta_a_pagar_e_receber")
    
    return conta_a_pagar_e_receber


