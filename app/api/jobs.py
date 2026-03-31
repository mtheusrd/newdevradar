# app/api/jobs.py
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.job import JobCreate, JobUpdate, JobResponse, JobListResponse
from app.services.job_service import JobService
from app.services.scraper_service import ScraperService

# APIRouter agrupa os endpoints
# prefix - todos os endpoints começam como /jobs
# tags agrupa no Swagger
router = APIRouter(prefix="/jobs", tags=["jobs"])

# Depends(get_db) injeção de dependencia do FastAPI
# O FastAPI chama get_db(), da a sessão e fecha no final
def get_service(db: Session = Depends(get_db)) -> JobService:
    return JobService(db)

@router.post("/", response_model=JobResponse, status_code=status.HTTP_201_CREATED)

def create_job(data: JobCreate, service: JobService = Depends(get_service)):
    """Cria uma nova vaga"""
    return service.create(data)

@router.get("/", response_model=JobListResponse)
def list_jobs(
    page: int = Query(default=1, ge=1),  # ge=1 == maior ou igual a 1
    size: int = Query(default=20, ge=1, le=100), # entre 1 e 100  
    source: str | None = Query(default=None),
    is_active: bool | None = Query(default=None),
    service: JobService = Depends(get_service),
):
    """Lista vagas com filtros e paginação"""
    jobs, total = service.list(page=page, size=size, source=source, is_active=is_active)
    return JobListResponse(items=jobs, total=total, page=page, size=size)

@router.get("/{job_id}", response_model=JobResponse)
def get_job(job_id: int, service: JobService = Depends(get_service)):
    """Busca uma vaga pelo ID"""
    job = service.get_by_id(job_id)
    if not job:
        # HTTPException o FastAPI converte para JSON
        raise HTTPException(status_code=404, detail="Vaga não encontrada")
    return job

@router.patch("/{job_id}", response_model=JobResponse)
def update_job(job_id: int, data: JobUpdate, service: JobService = Depends(get_service)):
    """Atualiza uma vaga"""
    job = service.update(job_id, data)
    if not job:
        raise HTTPException(status_code=404, detail="Vaga não encontrada")
    return job

@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job(job_id: int, service: JobService = Depends(get_service)):
    """Remove uma vaga"""
    if not service.delete(job_id):
        raise HTTPException(status_code=404, detail="Vaga não encontrada")
    


@router.post("/scrape", tags=["scraper"])
async def run_scraper(db: Session = Depends(get_db)):
    """Dispara o scraper manualmente e grava as vagas encontradas."""
    service = ScraperService(db)
    results = await service.run_all()
    return {"status": "done", "results": results}