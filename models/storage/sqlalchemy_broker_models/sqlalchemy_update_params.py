from dataclasses import dataclass

from sqlalchemy.sql import Executable

from models.storage.i_update_params import IUpdateParams


@dataclass
class SQLAlchemyUpdateParams(IUpdateParams):
    statement: Executable
