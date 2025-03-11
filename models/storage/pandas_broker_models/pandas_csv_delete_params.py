from dataclasses import dataclass
from typing import Callable

import pandas as pd

from models.storage.i_delete_params import IDeleteParams


@dataclass
class PandasCSVDeleteParams(IDeleteParams):
    delete_func: Callable[[pd.DataFrame], pd.DataFrame]
