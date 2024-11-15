from dataclasses import dataclass

from sqlalchemy.sql import Executable

from models.storage.i_delete_params import IDeleteParams


@dataclass
class SQLAlchemyDeleteParams(IDeleteParams):
    statement: Executable
