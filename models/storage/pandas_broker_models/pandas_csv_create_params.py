from dataclasses import dataclass
from typing import Union, List, Dict

import pandas as pd

from models.storage.i_create_params import ICreateParams


@dataclass
class PandasCSVCreateParams(ICreateParams):
    data: Union[pd.DataFrame, List[Dict]]
