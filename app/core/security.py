#app/core/security.py
from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

# CONSTS em caixa alta
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# CryptContext configura o algoritmo de hash de passwords
# 'bcrypt' é o padrão da indústria para passwords
pwd_context = CryptContext(schemes["bcrypt"], deprecated="auto")

# FUNÇÕES PURAS - recebem input, retornam output
# Type hints nos parametros e retorno tornam o contrato explicito

def hash_password(password: str) -> str:
    """Recebe password em texto plano, retorna hash bcrypy"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a password em texto plano corresponde ao hash."""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(
        subject: str | int, # 'str | int' = aceita string OU inteiro
        expires_delta: timedelta | None = None,
) -> str:
    """Cria um JWT token com expiração."""

# datetime.now com timezone UTC - usar sempre timezone-aware
now = datetime.now(timezone.utc)

expire = now + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

# Dicionário com os dados do token(payload em JWT)
payload: dict[str, Any] = {
    "sub": str(subject), # normalmente o ID do utilizador
    "iat": now,          # issued at
    "exp": expire,       # expiration
}

return jwt.encode(payload, settings.secret_key, algorithm = ALGORITHM)

def decode_access_token(token: str) -> dict[str, Any] | None:
    """Decodifica e valida um JWT token. Retorna None se inválido"""
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None