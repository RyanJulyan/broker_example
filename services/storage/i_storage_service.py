from abc import ABC, abstractmethod
from dataclasses import dataclass, field, fields, is_dataclass, asdict
import inspect
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

TStorageBroker = TypeVar("TStorageBroker", bound=IStorageBroker)


@dataclass
class IStorageService(ABC, Generic[
    TStorageBroker,
    TConnectParams,
    TCreateParams,
    TReadParams,
    TUpdateParams,
    TDeleteParams,
]):
  storage_broker: TStorageBroker

  # We'll store method -> param-type annotation here
  _method_type_map: dict = field(init=False, default_factory=dict)

  def __post_init__(self):
    """
      Extract parameter annotations from each method in the storage broker,
      using inspect.signature instead of get_type_hints.
      """
    if not isinstance(self.storage_broker, IStorageBroker):
      raise TypeError(
          "Invalid storage broker. It must be a subclass of IStorageBroker.")

    # Inspect the broker's class, grabbing each function
    for name, func in inspect.getmembers(self.storage_broker.__class__,
                                         inspect.isfunction):
      # We'll parse the signature to see if there's an annotation on param 'params'
      sig = inspect.signature(func)
      params = list(sig.parameters.values())

      # Typically the first param is 'self', the second param is your typed `params`
      if len(params) > 1:
        second_param = params[1]  # e.g., def connect(self, params: SomeType)
        annotation = second_param.annotation
        # If there's a recognized annotation (not just inspect._empty),
        # store it in _method_type_map
        if annotation != inspect._empty:
          self._method_type_map[name] = annotation

  def _validate_params(self, params, expected_type):
    if not isinstance(params, expected_type):
      raise TypeError(f"Expected parameter of type {expected_type.__name__}, "
                      f"but got {type(params).__name__}")

    # If it's a dataclass, gather field names without constructing an instance
    if is_dataclass(params):
      param_keys = set(asdict(params).keys())
      expected_keys = set(f.name for f in fields(
          expected_type))  # <--- This avoids calling expected_type()

      if not expected_keys.issubset(param_keys):
        raise ValueError(
            f"Missing required fields in {type(params).__name__}. "
            f"Expected: {expected_keys}, but got: {param_keys}")

  def __getattribute__(self, name):
    """
      Intercepts method calls to ensure parameter validation runs automatically.
      """
    # Let normal logic handle private attrs (including _method_type_map)
    if name.startswith("_"):
      return super().__getattribute__(name)

    storage_broker = super().__getattribute__("storage_broker")
    method_type_map = super().__getattribute__("_method_type_map")

    # If the name appears in the param-type map and there's a corresponding broker method:
    if name in method_type_map and hasattr(storage_broker, name):
      broker_method = getattr(storage_broker, name)

      def wrapper(params, *args, **kwargs):
        expected_type = method_type_map[name]
        self._validate_params(params, expected_type)
        return broker_method(params, *args, **kwargs)

      return wrapper

    # Otherwise, let standard attribute lookup occur
    return super().__getattribute__(name)

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
