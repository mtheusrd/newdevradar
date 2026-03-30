# app/models/job.py
from sqlalchemy import String, Text, Boolean, Index
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, TimestampMixin

class Job(Base, TimestampMixin):
    """Modelo de vaga de emprego."""

    #__tablename__ define o nome da tabela no banco
    __tablename__ = "jobs"

    # Mapped[int] com primary_key=True - SQLAlchemy cria o ID auto
    id: Mapped[int] = mapped_column(primary_key=True)

    # Mapped[str] - coluna VARCHAR obrigatoria
    title: Mapped[str] = mapped_column(String(255), nullable=True)
    company: Mapped[str] = mapped_column(String(255), nullable=True)

    # Mapped[str | None] coluna opcional(permite null)
    location: Mapped[str | None] = mapped_column(String(255), nullable=True)
    salary: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # Text para strings longas
    description: Mapped[str] = mapped_column(Text, nullable=True)

    # URL da vaga
    url: Mapped[str] = mapped_column(String(500), nullable=False, unique=True)

    # Fonte de onde veio a vaga
    source: Mapped[str] = mapped_column(String(100), nullable=False)

    # Tags - guardo como string separado por virgula
    tags: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Bool com valor padrao
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # indices aceleram queries na busca de colunas mais usadas
    __table_args__ = (
        Index("ix_jobs_source", "source"),
        Index("ix_jobs_is_active", "is_active"),
        Index("ix_jobs_company", "company"),
    )

    # __repr__ como o objeto aparece nos logs
    # toString() 
    def __repr__(self) -> str:
        return f"<Job {self.id}: {self.title} @ {self.company}>"
