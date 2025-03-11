from abc import ABC, abstractmethod
from dataclasses import dataclass, is_dataclass, asdict
from typing import TypeVar, Generic, get_args, get_origin, get_type_hints

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

  def __post_init__(self):
    """Extracts generic types dynamically from the broker class."""
    base = get_origin(self.storage_broker.__class__)
    if base and issubclass(base, IStorageBroker):
      self.method_type_map = get_type_hints(self.storage_broker)
    else:
      raise TypeError(
          "Invalid storage broker. It must be a subclass of IStorageBroker.")

  def _validate_params(self, params, expected_type):
    """Ensures params match the expected type structurally and by instance type."""
    if not isinstance(params, expected_type):
      raise TypeError(f"Expected parameter of type {expected_type.__name__}, "
                      f"but got {type(params).__name__}")

    # Ensure it's a dataclass and has correct fields (optional but useful)
    if is_dataclass(params):
      param_keys = set(asdict(params).keys())
      expected_keys = set(asdict(expected_type()).keys())
      if not expected_keys.issubset(param_keys):
        raise ValueError(
            f"Missing required fields in {type(params).__name__}. "
            f"Expected: {expected_keys}, but got: {param_keys}")

  def __getattribute__(self, name):
    """
      Intercepts method calls to ensure parameter validation runs automatically.
      """
    storage_broker = super().__getattribute__("storage_broker")
    method_type_map = super().__getattribute__("method_type_map")

    if name in method_type_map and hasattr(storage_broker, name):
      broker_method = getattr(storage_broker, name)

      def wrapper(params, *args, **kwargs):
        expected_type = method_type_map[name]

        # Validate parameters automatically
        self._validate_params(params, expected_type)

        # Call the actual method
        return broker_method(params, *args, **kwargs)

      return wrapper  # Return the dynamically wrapped method

    return super().__getattribute__(
        name)  # Default behavior for non-broker methods

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
