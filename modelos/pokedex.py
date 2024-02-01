from sqlalchemy import Column, String, DateTime

from config.base_de_datos import base


class pokedex(base):
    # nombre de la tabla
    __tablename__ = "pokedex"
    name = Column(String, primary_key=True)
    height = Column(String)
    weight = Column(String)
    created_date = Column(DateTime)
