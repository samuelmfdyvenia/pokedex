from jwt import decode, encode


def dame_token(dato: dict) -> str:
    token: str = encode(payload=dato, key="mi_clave", algorithm="HS256")

    return token


def validar_token(token=str) -> dict:
    dato: dict = decode(token, key="mi_clave", algorithms=["HS256"])
    return dato
