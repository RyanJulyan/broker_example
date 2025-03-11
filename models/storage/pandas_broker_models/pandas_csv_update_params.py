from dataclasses import dataclass
from typing import Callable

import pandas as pd

from models.storage.i_update_params import IUpdateParams


@dataclass
class PandasCSVUpdateParams(IUpdateParams):
    update_func: Callable[[pd.DataFrame], pd.DataFrame]
