# app/services/scraper_service.py
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.job import Job
from app.scraper.remoteok import RemoteOKScraper
from app.scraper.base import JobData

class ScraperService:
    """Orquestra a coleta de vagas e gravação na BD"""

    def __init__(self, db: Session):
        self.db = db
        # Lista de scrapers ativos
        self.scrapers = [RemoteOKScraper()]
    
    async def run_all(self) -> dict:
        """Corre todos os scrapers e grava os resultados"""
        results = {}

        for scraper in self.scrapers:
            try:
                jobs = await scraper.fetch()
                saved, skipped = self._save_jobs(jobs)
                results[scraper.source_name] = {
                    "fetched": len(jobs),
                    "saved": saved,
                    "skipped": skipped, # duplicados ignorados
                }
            except Exception as e:
                results[scraper.source_name] = {"error": str(e)}
        return results
    
    def _save_jobs(self, jobs: list[JobData]) -> tuple[int, int]:
        """Grava vagas na BD"""
        saved = 0
        skipped = 0

        for job_data in jobs:
            # Verifica se ja existe vaga com esse URL
            exists = self.db.execute(
                select(Job.id).where(Job.url == job_data.url)
            ).first()

            if exists:
                skipped += 1
                continue

            job = Job(**vars(job_data))
            self.db.add(job)
            saved += 1

        self.db.commit()
        return saved, skipped