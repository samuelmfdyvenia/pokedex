import requests
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from pydantic import BaseModel
import datetime

import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

from config.base_de_datos import base, motor, sesion
from jwt_config import validar_token
from modelos.pokedex import (
    pokedex as pokedexmodelo,
)  # le ponemos un alias para evitar confundir el nombre con otros parecidos que ya hemos definido

app = FastAPI()
app.title = "Pokedex de Samuel"
app.version = "1.0.1"


base.metadata.create_all(bind=motor)


class Usuario(BaseModel):
    email: str
    clave: str


class Pokemon(BaseModel):  # creamos un modelo
    name: str
    height: str
    weight: str
    created_at: str


class Portador(HTTPBearer):
    async def __call__(self, request: Request):
        autorizacion = await super().__call__(request)
        dato = validar_token(autorizacion.credentials)

        if dato["email"] != "1234":
            raise HTTPException(status_code=403, detail="No autorizado")


@app.get("/pokemon/{name}", tags=["Pokemon"])
def fetch_pokemon(name: str):
    with sesion() as db:
        existing_pokemon = db.query(pokedexmodelo).filter_by(name=name).first()
        if existing_pokemon:
            return existing_pokemon
        else:
            try:
                # Llamada a la API de la Pokédex
                api_url = f"https://pokeapi.co/api/v2/pokemon/{name}"
                response = requests.get(api_url)

                if response.status_code == 200:
                    data: dict = response.json()

                    new_pokemon = pokedexmodelo(
                        name=data.get("name", "Sin Nombre"),
                        height=str(data.get("height", 0)),
                        weight=str(data.get("weight", 0)),
                        created_date=datetime.datetime.now(),
                    )

                    db.add(new_pokemon)
                    db.commit()
                    return {
                        "name": new_pokemon.name,
                        "height": new_pokemon.height,
                        "weight": new_pokemon.weight,
                        "created_date": new_pokemon.created_date.strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),
                    }

                else:
                    return JSONResponse(
                        content={
                            "mensaje": f"Error al hacer la solicitud. Código de estado: {response.status_code}"
                        }
                    )
            except Exception as e:
                return JSONResponse(
                    content={"mensaje": f"Error en el servidor: {str(e)}"}
                )


@app.delete("/pokemon/{name}", tags=["Pokemon"])
def delete_pokemon(name: str):
    with sesion() as db:
        resultado = db.query(pokedexmodelo).filter(pokedexmodelo.name == name).first()
        if not resultado:
            raise HTTPException(
                status_code=404, detail="No se ha encontrado el pokemon"
            )

        db.delete(resultado)
        db.commit()
        return {"mensaje": f"El pokemon {name} se ha eliminado correctamente"}


# @app.post('/login',tags=['Autenticacion'])
# def login(usuario:Usuario):
#     if usuario.email == '1234' and usuario.clave == '1234':
#         token:str=dame_token(usuario.dict())
#         return JSONResponse(status_code=200,content=token)
#     return JSONResponse(content={'message':'Error de autenticacion'},status_code=401)
