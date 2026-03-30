# app/models/base.py

from datetime import datetime, timezone
from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# DeclarativeBase e a clase pai de todos os modelos SQLAlchemy
# Todos os modelos do projeto vao herdar de 'Base'

class Base(DeclarativeBase):
    pass

# Mixin - uma classe que adiciona comportamento a outras classes
# sem ser um modelo por si
class TimestampMixin:
    """Adiciona created_at e updated_at a qualquer modelo."""

    # Mapped[datetime] e o tipo do python mapeado para coluna do banco
    # server_default=func.now() - o banco preenche auto
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )