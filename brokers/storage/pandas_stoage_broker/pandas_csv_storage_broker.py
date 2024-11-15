import pandas as pd

from brokers.storage.i_storage_broker import IStorageBroker
from models.storage.pandas_broker_models.pandas_csv_connect_params import (
    PandasCSVConnectParams,
)
from models.storage.pandas_broker_models.pandas_csv_create_params import (
    PandasCSVCreateParams,
)
from models.storage.pandas_broker_models.pandas_csv_read_params import (
    PandasCSVReadParams,
)
from models.storage.pandas_broker_models.pandas_csv_update_params import (
    PandasCSVUpdateParams,
)
from models.storage.pandas_broker_models.pandas_csv_delete_params import (
    PandasCSVDeleteParams,
)


class PandasCSVStorageBroker(
    IStorageBroker[
        PandasCSVConnectParams,
        PandasCSVCreateParams,
        PandasCSVReadParams,
        PandasCSVUpdateParams,
        PandasCSVDeleteParams,
    ]
):
    def __init__(self):
        self.df = None  # DataFrame to hold CSV data
        self.file_path = None
        self.delimiter = ","

    def connect(self, params: PandasCSVConnectParams):
        self.file_path = params.file_path
        self.delimiter = params.delimiter
        try:
            self.df = pd.read_csv(self.file_path, delimiter=self.delimiter)
            print(
                f"Connected to CSV at {self.file_path} with delimiter '{self.delimiter}'"
            )
        except FileNotFoundError:
            # If file does not exist, create an empty DataFrame
            self.df = pd.DataFrame()
            print(f"File {self.file_path} not found. Created empty DataFrame.")

    def create(self, params: PandasCSVCreateParams):
        if isinstance(params.data, pd.DataFrame):
            new_df = params.data
        else:
            new_df = pd.DataFrame(params.data)
        self.df = pd.concat([self.df, new_df], ignore_index=True)
        # Save back to CSV
        self.df.to_csv(self.file_path, index=False, sep=self.delimiter)
        print(f"Appended new data to CSV.")

    def read(self, params: PandasCSVReadParams):
        if params.filter_func:
            result = params.filter_func(self.df.copy())
        else:
            result = self.df.copy()
        print(f"Read data from CSV.")
        return result

    def update(self, params: PandasCSVUpdateParams):
        self.df = params.update_func(self.df.copy())
        # Save back to CSV
        self.df.to_csv(self.file_path, index=False, sep=self.delimiter)
        print(f"Updated CSV data.")

    def delete(self, params: PandasCSVDeleteParams):
        self.df = params.delete_func(self.df.copy())
        # Save back to CSV
        self.df.to_csv(self.file_path, index=False, sep=self.delimiter)
        print(f"Deleted data from CSV.")
