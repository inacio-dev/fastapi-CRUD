from datetime import datetime

from sqlalchemy import BigInteger, Date, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.models.base import AbstractModel


class CronLogs(AbstractModel):
    __tablename__ = "apps_cron_CRON_LOGS"

    status: Mapped[str] = mapped_column(String(40))
    descricao: Mapped[str] = mapped_column(String(2000))
    data: Mapped[datetime] = mapped_column(DateTime, nullable=True)


class Pctsra001Funcionarios(AbstractModel):
    __tablename__ = "apps_cron_PCTSRA001_Funcionarios"

    index: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    idmatricula: Mapped[int] = mapped_column(BigInteger, nullable=True)
    matricula: Mapped[str] = mapped_column(String, nullable=True)
    nome: Mapped[str] = mapped_column(String, nullable=True)
    admissao: Mapped[Date] = mapped_column(Date, nullable=True)
    idccusto: Mapped[int] = mapped_column(BigInteger, nullable=True)
    idcargo: Mapped[int] = mapped_column(BigInteger, nullable=True)
    iddepto: Mapped[int] = mapped_column(BigInteger, nullable=True)
    demissao: Mapped[Date] = mapped_column(Date, nullable=True)
    idfuncao: Mapped[int] = mapped_column(BigInteger, nullable=True)
    cpf: Mapped[str] = mapped_column(String, nullable=True)
    email: Mapped[str] = mapped_column(String, nullable=True)
    situacao: Mapped[str] = mapped_column(String, nullable=True)
    banco: Mapped[str] = mapped_column(String, nullable=True)
    agencia: Mapped[str] = mapped_column(String, nullable=True)
    conta: Mapped[str] = mapped_column(String, nullable=True)


class EquipeBEQ(AbstractModel):
    __tablename__ = "apps_cron_Turma_Equipes"

    equipe_id: Mapped[int] = mapped_column(Integer, primary_key=True, name="Id")
    descricao: Mapped[str] = mapped_column(String(100), name="Descricao")
    habilitado: Mapped[str] = mapped_column(String(10), name="Habilitado")
    idccusto: Mapped[int] = mapped_column(Integer, name="IDCCUSTO")
    centro_custo_id: Mapped[str] = mapped_column(String(100), name="CentroCustoId")
    chefe_turma: Mapped[str] = mapped_column(String(10), name="Chefe_Turma")
    carro_placa: Mapped[str] = mapped_column(String(10), name="Carro_Placa")
    matricula_gerente: Mapped[str] = mapped_column(String(10), name="Mat_Gerente")
    matricula_coordenador: Mapped[str] = mapped_column(String(10), name="Mat_Coordenador")
    matricula_supervisor: Mapped[str] = mapped_column(String(10), name="Mat_Supervisor")
    base_id: Mapped[int] = mapped_column(Integer, name="Base_Id")


class EquipesFuncionariosBEQ(AbstractModel):
    __tablename__ = "apps_cron_Turma_Usuario_Equipes_Funcionarios"

    equipe_id: Mapped[int] = mapped_column(Integer, primary_key=True, name="Turma_id")
    matricula: Mapped[str] = mapped_column(String(6), name="Matricula")


class SupervisorBEQ(AbstractModel):
    __tablename__ = "apps_cron_supervisorbeq"

    matricula: Mapped[str] = mapped_column(String(10), primary_key=True, name="MATRICULA")
    nome: Mapped[str] = mapped_column(String(100), name="NOME")


class ChefeTurmaBEQ(AbstractModel):
    __tablename__ = "apps_cron_chefe_turmabeq"

    matricula: Mapped[str] = mapped_column(String(10), primary_key=True, name="MATRICULA")
    nome: Mapped[str] = mapped_column(String(100), name="NOME")


class Pctsq3001Cargo(AbstractModel):
    __tablename__ = "apps_cron_PCTSQ3001_Cargo"

    index: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    idcargo: Mapped[int] = mapped_column(BigInteger, nullable=True)
    cargo: Mapped[str] = mapped_column(String, nullable=True)
    descricao: Mapped[str] = mapped_column(String, nullable=True)


class Pctctt001CentroDeCusto(AbstractModel):
    __tablename__ = "apps_cron_PCTCTT001_Centro_de_Custo"

    index: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    idccusto: Mapped[int] = mapped_column(BigInteger, nullable=True)
    ccusto: Mapped[str] = mapped_column(String, nullable=True)
    descricao: Mapped[str] = mapped_column(String, nullable=True)
    existencia: Mapped[str] = mapped_column(String, nullable=True)
    contrato: Mapped[str] = mapped_column(String, nullable=True)


class Pctsqb001Departamento(AbstractModel):
    __tablename__ = "apps_cron_PCTSQB001_Departamento"

    index: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    iddepto: Mapped[int] = mapped_column(BigInteger, nullable=True)
    depto: Mapped[str] = mapped_column(String, nullable=True)
    descricao: Mapped[str] = mapped_column(String, nullable=True)


class Pctsrj001Funcao(AbstractModel):
    __tablename__ = "apps_cron_PCTSRJ001_Funcao"

    index: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    idfuncao: Mapped[int] = mapped_column(BigInteger, nullable=True)
    funcao: Mapped[str] = mapped_column(String, nullable=True)
    descricao: Mapped[str] = mapped_column(String, nullable=True)
    cbo: Mapped[str] = mapped_column(String, nullable=True)
