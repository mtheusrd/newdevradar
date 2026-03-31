# app/scraper/remoteok.py
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential
from app.scraper.base import BaseScraper, JobData

class RemoteOKScraper(BaseScraper):
    """Coleta vagas da API do RemoteOK"""

    # URL da Api do RemoteOK
    BASE_URL = "https://remoteok.com/api"

    def __init__(self):
        super().__init__(source_name="remoteok")

    # @retry tenta até 3 vezes a conexão
    # wait_exponential: 1,2,4s entre as try's
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=8))
    async def fetch(self) -> list[JobData]:
        """Busca vagas do RemoteOK"""

        # httpc.AsyncClient é o cliente HTTP assíncrono
        # 'async with' garante que a conexão é fechada
        async with httpx.AsyncClient(timeout=30) as client:
            # Headers para simular um browser
            headers = {"User-Agent": "DevRadar/1.0"}
            response = await client.get(self.BASE_URL, headers=headers)

            # raise_for_status() lança exceção se status >=400
            response.raise_for_status()

            # o primeiro item do array é metadata, ignoro com [1:]
            data = response.json()[1:]

            # List comprehension - transformar listas
            # equivale a um map() com filter()
            jobs =[
                self._parse_job(job)
                for job in data
                if self._is_valid(job)
            
            ]
            return jobs
    
    def _is_valid(self, job: dict) -> bool:
        """Verifica se a vaga tem os campos minimos necessários"""
        return bool(job.get("position") and job.get("company") and job.get("url"))
    
    def _parse_job(self, job: dict) -> JobData:
        """Converte o JSON da API para o formato interno"""
    
        # .get() acesso seguro, retorna None se nao existir
        # diferente de job["key"] que lança KeyError se nao existir
        tags = job.get("tags", [])
        tags_str = ",".join(tags) if tags else None

        return JobData(
            title=self._clean_text(job.get("position", "")),
            company=self._clean_text(job.get("company", "")),
            url=job.get("url", ""),
            source=self.source_name,
            location=job.get("location") or "Remote",
            salary=self._clean_text(job.get("salary")),
            description=self._clean_text(job.get("description")),
            tags=tags_str,
        )
        
