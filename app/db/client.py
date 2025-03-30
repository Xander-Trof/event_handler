from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base


class Client:
    def __init__(self):
        self._engine = create_engine("postgresql+psycopg2://event_handler:111111@localhost:5432/postgres")
        self._session_maker = sessionmaker(bind=self._engine)
        self._session = self._session_maker()
        self._init_db()

    def _init_db(self):
        Base.metadata.create_all(bind=self._engine)

db_client = Client()