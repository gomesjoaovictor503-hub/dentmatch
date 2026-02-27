from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# ===============================
# CONFIGURAÇÕES JWT
# ===============================

SECRET_KEY = "DENTMATCH_SUPER_SECRET_2026_CHANGE_THIS"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# ===============================
# CONTEXTO DE HASH (bcrypt fix)
# ===============================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# ===============================
# ESQUEMA BEARER
# ===============================

security = HTTPBearer()


# ===============================
# HASH DE SENHA
# ===============================

def hash_senha(senha: str):
    return pwd_context.hash(senha)


def verificar_senha(senha: str, senha_hash: str):
    return pwd_context.verify(senha, senha_hash)


# ===============================
# CRIAR TOKEN JWT
# ===============================

def criar_token(dados: dict):
    to_encode = dados.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow()  # issued at
    })

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


# ===============================
# VALIDAR TOKEN JWT
# ===============================

def verificar_token(token: str):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload

    except JWTError as e:
        print("ERRO JWT:", str(e))
        return None


# ===============================
# DEPENDÊNCIA PARA PROTEGER ROTAS
# ===============================

def get_usuario_atual(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    print("CREDENTIALS:", credentials)

    if credentials is None:
        raise HTTPException(status_code=401, detail="Token não enviado")

    print("TOKEN RECEBIDO:", credentials.credentials)

    payload = verificar_token(credentials.credentials)

    if payload is None:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")

    return payload
