from dataclasses import dataclass

from models.storage.i_connect_params import IConnectParams


@dataclass
class SQLAlchemyConnectParams(IConnectParams):
	database_url: str
	echo: bool = False
