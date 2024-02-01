import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from typing import Type
# ruta al archivo sqlite del directorio anterior
fichero = "../pokedex.sqlite"

# directorio actual del archivo "base_de_datos"
directorio = os.path.dirname(os.path.realpath(__file__))

# direccion base
ruta = f"sqlite:///{os.path.join(directorio,fichero)}"

# creamos un motor
motor = create_engine(ruta, echo=True)

# creamos la sesion
sesion = sessionmaker(bind=motor)

# crear base para manejar las tablas

base: Type[DeclarativeMeta] = declarative_base()
