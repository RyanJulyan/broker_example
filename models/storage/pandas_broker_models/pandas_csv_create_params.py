from dataclasses import dataclass
from typing import Union, List, Dict

import pandas as pd

from models.storage.i_connect_params import IConnectParams


@dataclass
class PandasCSVCreateParams(IConnectParams):
    data: Union[pd.DataFrame, List[Dict]]
