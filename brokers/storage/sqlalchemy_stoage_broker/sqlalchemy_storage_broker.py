from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from brokers.storage.i_storage_broker import IStorageBroker
from models.storage.sqlalchemy_broker_models.sqlalchemy_connect_params import (
    SQLAlchemyConnectParams,
)
from models.storage.sqlalchemy_broker_models.sqlalchemy_create_params import (
    SQLAlchemyCreateParams,
)
from models.storage.sqlalchemy_broker_models.sqlalchemy_read_params import (
    SQLAlchemyReadParams,
)
from models.storage.sqlalchemy_broker_models.sqlalchemy_update_params import (
    SQLAlchemyUpdateParams,
)
from models.storage.sqlalchemy_broker_models.sqlalchemy_delete_params import (
    SQLAlchemyDeleteParams,
)


class SQLAlchemyStorageBroker(
    IStorageBroker[
        SQLAlchemyConnectParams,
        SQLAlchemyCreateParams,
        SQLAlchemyReadParams,
        SQLAlchemyUpdateParams,
        SQLAlchemyDeleteParams,
    ]
):
    def __init__(self, engine=None, session=None):
        self.engine = engine
        self.session = session

    def connect(self, params: SQLAlchemyConnectParams):
        try:
            self.engine = create_engine(params.database_url, echo=params.echo)
            SessionLocal = sessionmaker(bind=self.engine)
            self.session = SessionLocal()
            print(f"Connected to {params.database_url} with echo={params.echo}")
        except SQLAlchemyError as e:
            print(f"Error connecting to database: {e}")
            raise

    def create(self, params: SQLAlchemyCreateParams):
        try:
            self.session.execute(params.statement)
            self.session.commit()
            print(f"Executed create statement: {params.statement}")
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error executing create statement: {e}")
            raise

    def read(self, params: SQLAlchemyReadParams):
        try:
            result = self.session.execute(params.statement)
            records = result.fetchall()
            print(f"Executed read statement: {params.statement}")
            return records
        except SQLAlchemyError as e:
            print(f"Error executing read statement: {e}")
            raise

    def update(self, params: SQLAlchemyUpdateParams):
        try:
            self.session.execute(params.statement)
            self.session.commit()
            print(f"Executed update statement: {params.statement}")
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error executing update statement: {e}")
            raise

    def delete(self, params: SQLAlchemyDeleteParams):
        try:
            self.session.execute(params.statement)
            self.session.commit()
            print(f"Executed delete statement: {params.statement}")
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error executing delete statement: {e}")
            raise
