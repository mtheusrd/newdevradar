# app/schemas/job.py
from datetime import datetime
from pydantic import BaseModel, HttpUrl, field_validator

# Schema BASE são os campos comuns a todos schemas
class JobBase(BaseModel):
    title: str
    company: str
    location: str | None = None
    salary: str | None = None
    description: str | None = None
    url: str
    source: str
    tags: str | None = None
    is_active: bool = True


# Schema de CRIAÇÂO - o que a API aceita no body do POST
# herda tudo do JobBase
class JobCreate(JobBase):
    pass

# Schema de ATT - todos os campos opcionais (PATCH)
# None como default é para não alterar esse campo
class JobUpdate(BaseModel):
    title: str | None = None
    company: str | None = None
    location: str | None = None
    salary: str | None = None
    description: str | None = None
    is_active: bool | None = None
    tags: str | None = None

# Schema de RESPOSTA
# inclui os campos gerados pela BD(id, created_at, updated_at)
class JobResponse(JobBase):
    id: int
    created_at: datetime
    updated_at: datetime

    # model_config diz ao Pydantic para ler objetos SQLAlchemy
    model_config = {"from_attributes": True}

# Schema de LISTAGEM é a paginação
class JobListResponse(BaseModel):
    items: list[JobResponse]
    total: int
    page: int
    size: int 

