from sqlalchemy import create_engine, Column, Integer, String, Float, Enum
from sqlalchemy.orm import declarative_base, sessionmaker
import enum
import os
from dotenv import load_dotenv
# Crie no postgresql um bacno de dados chamado db_fastapi antes de tudo. Depois rode esse script "python crair_db.py"

# Carrega variáveis do .env
load_dotenv()

# Conexão com o banco via variável de ambiente
DATABASE_URL = os.getenv("DATABASE_URL")

# Conecta ao banco
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

# Define modelo base
Base = declarative_base()

# Enum para tipo
class TipoConta(str, enum.Enum):
    PAGAR = "PAGAR"
    RECEBER = "RECEBER"

# Modelo da tabela
class ContaPagarReceber(Base):
    __tablename__ = "contas_a_pagar_e_receber"

    id = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String(30), nullable=False)
    valor = Column(Float, nullable=False)
    tipo = Column(Enum(TipoConta), nullable=False)

# Cria as tabelas no banco
Base.metadata.create_all(bind=engine)

# Dados a serem inseridos
dados_iniciais = [
    {"id": 1, "descricao": "Aluguel", "valor": 1000.5, "tipo": TipoConta.PAGAR},
    {"id": 2, "descricao": "Salário", "valor": 5000.0, "tipo": TipoConta.RECEBER},
]

# Verifica se a tabela já tem dados
if not session.query(ContaPagarReceber).first():
    for dado in dados_iniciais:
        conta = ContaPagarReceber(**dado)
        session.add(conta)
    session.commit()
    print("Dados inseridos com sucesso.")
else:
    print("A tabela já contém dados. Nenhuma inserção realizada.")

session.close()
