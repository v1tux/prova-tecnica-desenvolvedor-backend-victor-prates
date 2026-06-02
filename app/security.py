from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User

from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext

# Em um projeto real, esses valores devem vir de variáveis de ambiente.
# Para a prova técnica, deixei valores fixos para simplificar a execução.
SECRET_KEY = "prova-tecnica-backend-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Configura o contexto de criptografia usado para gerar e validar hashes.
# O bcrypt é uma escolha comum para proteger senhas.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica se a senha enviada pelo usuário corresponde ao hash salvo no banco.

    A senha original nunca é salva. Durante o login, comparamos a senha enviada
    com o hash armazenado.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Gera o hash de uma senha antes de salvá-la no banco de dados.
    """
    return pwd_context.hash(password)


def create_access_token(data: dict) -> str:
    """
    Cria um token JWT com tempo de expiração.

    O campo 'sub' normalmente identifica o usuário autenticado.
    Neste projeto, usaremos o e-mail do usuário como identificação no token.
    """
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    return encoded_jwt


def decode_access_token(token: str) -> dict | None:
    """
    Decodifica e valida um token JWT.

    Retorna os dados do token se ele for válido.
    Retorna None se o token estiver inválido ou expirado.
    """
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )
        return payload
    except JWTError:
        return None
    
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Valida o token JWT enviado na requisição e retorna o usuário autenticado.

    O token deve ser enviado no cabeçalho Authorization no formato:
    Bearer <token>

    Caso o token esteja inválido, expirado ou o usuário não exista,
    a API retorna erro 401 Unauthorized.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token)

    if payload is None:
        raise credentials_exception

    email = payload.get("sub")

    if email is None:
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()

    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário inativo.",
        )

    return user