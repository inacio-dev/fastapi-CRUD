from datetime import date, datetime

from app.core.schemas.base import SchemaBase


class CronLogsSchema(SchemaBase):
    status: str
    descricao: str
    data: datetime | None = None

    class Config:
        from_attributes = True
        exclude_none = True


class Pctsra001FuncionariosSchema(SchemaBase):
    index: int
    idmatricula: int | None = None
    matricula: str | None = None
    nome: str | None = None
    admissao: date | None = None
    idccusto: int | None = None
    idcargo: int | None = None
    iddepto: int | None = None
    demissao: date | None = None
    idfuncao: int | None = None
    cpf: str | None = None
    email: str | None = None
    situacao: str | None = None
    banco: str | None = None
    agencia: str | None = None
    conta: str | None = None

    class Config:
        from_attributes = True
        exclude_none = True


class EquipeBEQSchema(SchemaBase):
    equipe_id: int
    descricao: str
    habilitado: str
    idccusto: int
    centro_custo_id: str
    chefe_turma: str
    carro_placa: str
    matricula_gerente: str
    matricula_coordenador: str
    matricula_supervisor: str
    base_id: int

    class Config:
        from_attributes = True
        exclude_none = True


class EquipesFuncionariosBEQSchema(SchemaBase):
    equipe_id: int
    matricula: str

    class Config:
        from_attributes = True
        exclude_none = True


class SupervisorBEQSchema(SchemaBase):
    matricula: str
    nome: str

    class Config:
        from_attributes = True
        exclude_none = True


class ChefeTurmaBEQSchema(SchemaBase):
    matricula: str
    nome: str

    class Config:
        from_attributes = True
        exclude_none = True


class Pctsq3001CargoSchema(SchemaBase):
    index: int
    idcargo: int | None = None
    cargo: str | None = None
    descricao: str | None = None

    class Config:
        from_attributes = True
        exclude_none = True


class Pctctt001CentroDeCustoSchema(SchemaBase):
    index: int
    idccusto: int | None = None
    ccusto: str | None = None
    descricao: str | None = None
    existencia: str | None = None
    contrato: str | None = None

    class Config:
        from_attributes = True
        exclude_none = True


class Pctsqb001DepartamentoSchema(SchemaBase):
    index: int
    iddepto: int | None = None
    depto: str | None = None
    descricao: str | None = None

    class Config:
        from_attributes = True
        exclude_none = True


class Pctsrj001FuncaoSchema(SchemaBase):
    index: int
    idfuncao: int | None = None
    funcao: str | None = None
    descricao: str | None = None
    cbo: str | None = None

    class Config:
        from_attributes = True
        exclude_none = True
