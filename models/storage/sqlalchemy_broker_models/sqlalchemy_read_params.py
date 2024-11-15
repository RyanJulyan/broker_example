from dataclasses import dataclass

from sqlalchemy.sql import Executable

from models.storage.i_read_params import IReadParams


@dataclass
class SQLAlchemyReadParams(IReadParams):
    statement: Executable
