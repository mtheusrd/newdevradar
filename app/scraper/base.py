# app/scraper/base.py
from abc import ABC, abstractmethod
from dataclasses import dataclass

# dataclass e o decorator que gera __init__, __repr__ auto
# e como um schema mas sem validação

@dataclass
class JobData:
    """Estrutura de dados brutos coletados pelo scraper"""
    title: str
    company: str
    url: str
    source: str
    location: str | None = None
    salary: str | None = None
    description: str | None = None
    tags: str | None = None

# ABC abstract base class
# define um contrato que todas as subclasses devem implementar
class BaseScraper(ABC):
    """Classe base para todos os scrapers do DevRadar"""
    
    def __init__(self, source_name:str):
        self.source_name = source_name

    # @abstractmethod e o metodo obrigatorio nas subclasses
    @abstractmethod
    async def fetch(self) -> list[JobData]:
        """Busca vagas da fonte. deve ser implementado por cada scraper."""

    def _clean_text(self, text: str | None) -> str | None:
        """Remove espaços extras e caracteres indesejados."""
        if not text:
            return None
        return " ".join(text.split())