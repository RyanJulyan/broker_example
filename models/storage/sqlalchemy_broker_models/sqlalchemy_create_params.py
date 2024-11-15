from dataclasses import dataclass

from sqlalchemy.sql import Executable

from models.storage.i_create_params import ICreateParams


@dataclass
class SQLAlchemyCreateParams(ICreateParams):
    statement: Executable
