from dataclasses import dataclass

from models.storage.i_connect_params import IConnectParams


@dataclass
class PandasCSVConnectParams(IConnectParams):
    file_path: str
    delimiter: str = ","
