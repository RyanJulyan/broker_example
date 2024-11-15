from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from models.storage.i_connect_params import IConnectParams
from models.storage.i_create_params import ICreateParams
from models.storage.i_read_params import IReadParams
from models.storage.i_update_params import IUpdateParams
from models.storage.i_delete_params import IDeleteParams

TConnectParams = TypeVar('TConnectParams', bound=IConnectParams)
TCreateParams = TypeVar('TCreateParams', bound=ICreateParams)
TReadParams = TypeVar('TReadParams', bound=IReadParams)
TUpdateParams = TypeVar('TUpdateParams', bound=IUpdateParams)
TDeleteParams = TypeVar('TDeleteParams', bound=IDeleteParams)


class IStorageBroker(ABC, Generic[
    TConnectParams,
    TCreateParams,
    TReadParams,
    TUpdateParams,
    TDeleteParams,
]):

  @abstractmethod
  def connect(self, params: TConnectParams):
    pass

  @abstractmethod
  def create(self, params: TCreateParams):
    pass

  @abstractmethod
  def read(self, params: TReadParams):
    pass

  @abstractmethod
  def update(self, params: TUpdateParams):
    pass

  @abstractmethod
  def delete(self, params: TDeleteParams):
    pass
