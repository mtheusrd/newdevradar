# app/services/job_service.py
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from app.models.job import Job
from app.schemas.job import JobCreate, JobUpdate

class JobService:
    """Serviço responsável por todas as operações de vagas."""

    def __init__(self, db: Session):
        # Injeção de dependencia, recebe a sessão da DB em vez de criar a propria
        self.db = db
    
    def create(self, data: JobCreate) -> Job:
        """Cria uma nova vaga."""
        # model_dump() converte o schema Pydantic para dicionario
        job = Job(**data.model_dump())
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job) # att o objeto com dados da BD(id, timestamps)
        return job

    def get_by_id(self, job_id: int) -> Job | None:
        """Busca uma vaga pelo ID."""
        return self.db.get(Job, job_id)
    
    def list(
            self,
            page: int = 1,
            size: int = 20,
            source: str | None = None,
            is_active: bool | None = None,
    ) -> tuple[list[Job], int]:
        """Lista vagas com filtros e paginação"""

        # select() cria a query
        query = select(Job)

        # Filtros opcionais 
        if source:
            query = query.where(Job.source == source)
        if is_active is not None:
            query = query.where(Job.is_active == is_active)
        
        # conta o local total antes de paginar
        count_query = select(func.count()).select_from(query.subquery())
        total = self.db.execute(count_query).scalar_one()

        # paginação
        offset = (page - 1) * size
        query = query.offset(offset).limit(size).order_by(Job.created_at.desc())

        jobs = list(self.db.execute(query).scalars().all())
        return jobs, total
    
    def update(self, job_id: int, data: JobUpdate) -> Job | None:
        """Atualiza uma vaga"""
        job = self.get_by_id(job_id)
        if not job:
            return None
        
        # exclude_unset=True so atualiza os campos que foram enviados
        updates = data.model_dump(exclude_unset=True)
        for field, value in updates.items():
            setattr(job, field, value)

        self.db.commit()
        self.db.refresh(job)
        return job
    
    def delete(self, job_id: int) -> bool:
        """Remove uma vaga. Retorna True se existia, False se não"""
        job = self.get_by_id(job_id)
        if not job:
            return False
        self.db.delete(job)
        self.db.commit()
        return True
    





