from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Generic

# Models
from models.storage.i_connect_params import IConnectParams
from models.storage.i_create_params import ICreateParams
from models.storage.i_read_params import IReadParams
from models.storage.i_update_params import IUpdateParams
from models.storage.i_delete_params import IDeleteParams

# Broker
from brokers.storage.i_storage_broker import IStorageBroker

# Define type variables bound to their expected classes
TConnectParams = TypeVar('TConnectParams', bound=IConnectParams)
TCreateParams = TypeVar('TCreateParams', bound=ICreateParams)
TReadParams = TypeVar('TReadParams', bound=IReadParams)
TUpdateParams = TypeVar('TUpdateParams', bound=IUpdateParams)
TDeleteParams = TypeVar('TDeleteParams', bound=IDeleteParams)

TStorageBroker = TypeVar('TStorageBroker', bound=IStorageBroker)


@dataclass
class SimpleStorageService(Generic[
    TStorageBroker,
    TConnectParams,
    TCreateParams,
    TReadParams,
    TUpdateParams,
    TDeleteParams,
]):
  storeage_broker: TStorageBroker

  def connect(self, params: TConnectParams):
    return self.storeage_broker.connect(params=params)

  def create(self, params: TCreateParams):
    return self.storeage_broker.create(params=params)

  def read(self, params: TReadParams):
    return self.storeage_broker.read(params=params)

  def update(self, params: TUpdateParams):
    return self.storeage_broker.update(params=params)

  def delete(self, params: TDeleteParams):
    return self.storeage_broker.delete(params=params)
