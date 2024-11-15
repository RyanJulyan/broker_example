from dataclasses import dataclass
from typing import Optional, Callable

import pandas as pd

from models.storage.i_connect_params import IConnectParams


@dataclass
class PandasCSVReadParams(IConnectParams):
    filter_func: Optional[Callable[[pd.DataFrame], pd.DataFrame]] = None
