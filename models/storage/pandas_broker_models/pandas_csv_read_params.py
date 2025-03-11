from dataclasses import dataclass
from typing import Optional, Callable

import pandas as pd

from models.storage.i_read_params import IReadParams


@dataclass
class PandasCSVReadParams(IReadParams):
    filter_func: Optional[Callable[[pd.DataFrame], pd.DataFrame]] = None
