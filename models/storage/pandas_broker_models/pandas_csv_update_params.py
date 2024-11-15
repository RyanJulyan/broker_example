from dataclasses import dataclass
from typing import Callable

import pandas as pd

from models.storage.i_connect_params import IConnectParams


@dataclass
class PandasCSVUpdateParams(IConnectParams):
    update_func: Callable[[pd.DataFrame], pd.DataFrame]
