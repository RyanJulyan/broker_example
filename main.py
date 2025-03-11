from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    String,
    insert,
    select,
    update,
    delete,
)

# Sqlalchemy Broker
from brokers.storage.sqlalchemy_stoage_broker.sqlalchemy_storage_broker import (
    SQLAlchemyStorageBroker, )
from models.storage.sqlalchemy_broker_models.sqlalchemy_connect_params import (
    SQLAlchemyConnectParams, )
from models.storage.sqlalchemy_broker_models.sqlalchemy_create_params import (
    SQLAlchemyCreateParams, )
from models.storage.sqlalchemy_broker_models.sqlalchemy_read_params import (
    SQLAlchemyReadParams, )
from models.storage.sqlalchemy_broker_models.sqlalchemy_update_params import (
    SQLAlchemyUpdateParams, )
from models.storage.sqlalchemy_broker_models.sqlalchemy_delete_params import (
    SQLAlchemyDeleteParams, )

# Pandas Broker
from brokers.storage.pandas_stoage_broker.pandas_csv_storage_broker import (
    PandasCSVStorageBroker, )
from models.storage.pandas_broker_models.pandas_csv_connect_params import (
    PandasCSVConnectParams, )
from models.storage.pandas_broker_models.pandas_csv_create_params import (
    PandasCSVCreateParams, )
from models.storage.pandas_broker_models.pandas_csv_read_params import (
    PandasCSVReadParams, )
from models.storage.pandas_broker_models.pandas_csv_update_params import (
    PandasCSVUpdateParams, )
from models.storage.pandas_broker_models.pandas_csv_delete_params import (
    PandasCSVDeleteParams, )

# Simple Service
from services.storage.simple_storage_service import SimpleStorageService

##############
# Sqlalchemy #
##############

# Instantiate the broker
broker = SQLAlchemyStorageBroker()

# Connect to the in-memory database
connect_params = SQLAlchemyConnectParams(database_url="sqlite:///:memory:",
                                         echo=True)
broker.connect(connect_params)

# Create the table schema
metadata = MetaData()
users_table = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("email", String),
)
metadata.create_all(broker.engine)

# Create a record
stmt_create = insert(users_table).values(id=1,
                                         name="Alice",
                                         email="alice@example.com")
create_params = SQLAlchemyCreateParams(statement=stmt_create)
broker.create(create_params)

# Read records
stmt_read = select(users_table).where(users_table.c.name == "Alice")
read_params = SQLAlchemyReadParams(statement=stmt_read)
records = broker.read(read_params)
print(f"Records: {records}")

# Update a record
stmt_update = (update(users_table).where(users_table.c.id == 1).values(
    email="alice_new@example.com"))
update_params = SQLAlchemyUpdateParams(statement=stmt_update)
broker.update(update_params)

# Read updated records
stmt_read_all = select(users_table)
read_params = SQLAlchemyReadParams(statement=stmt_read_all)
records = broker.read(read_params)
print(f"Updated Records: {records}")

# Delete a record
stmt_delete = delete(users_table).where(users_table.c.id == 1)
delete_params = SQLAlchemyDeleteParams(statement=stmt_delete)
broker.delete(delete_params)

# Read remaining records
stmt_read_remaining = select(users_table)
read_params = SQLAlchemyReadParams(statement=stmt_read_remaining)
records = broker.read(read_params)
print(f"Remaining Records: {records}")

##########
# Pandas #
##########

# Initialize the broker
broker = PandasCSVStorageBroker()

# Connect to CSV file
connect_params = PandasCSVConnectParams(file_path="data.csv")
broker.connect(connect_params)

# Create (append) data
create_params = PandasCSVCreateParams(data=[{
    "id": 1,
    "name": "Alice",
    "email": "alice@example.com"
}])
broker.create(create_params)


# Read data with a filter function
def filter_func(df):
    return df[df["name"] == "Alice"]


read_params = PandasCSVReadParams(filter_func=filter_func)
result = broker.read(read_params)
print(result)


# Update data with an update function
def update_func(df):
    df.loc[df["id"] == 1, "email"] = "alice_new@example.com"
    return df


update_params = PandasCSVUpdateParams(update_func=update_func)
broker.update(update_params)

# Read updated data
read_params = PandasCSVReadParams()
result = broker.read(read_params)
print(result)


# Delete data with a delete function
def delete_func(df):
    return df[df["id"] != 1]


delete_params = PandasCSVDeleteParams(delete_func=delete_func)
broker.delete(delete_params)

# Read remaining data
result = broker.read(PandasCSVReadParams())
print(result)

# Instantiate the Pandas CSV Storage Broker
pandas_csv_broker = PandasCSVStorageBroker()

# Instantiate the SimpleStorageService with PandasCSVStorageBroker
storage_service = SimpleStorageService[
    PandasCSVStorageBroker,
    PandasCSVConnectParams,
    PandasCSVCreateParams,
    PandasCSVReadParams,
    PandasCSVUpdateParams,
    PandasCSVDeleteParams,
](storeage_broker=pandas_csv_broker)

print()
print("storage_service:")
print(storage_service)
print()
