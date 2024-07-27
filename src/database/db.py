from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


class DB:
    def __init__(self, db_url: str) -> None:
        self.engine = create_async_engine(db_url, echo=True)
        self.async_session = async_sessionmaker(self.engine,
                                                autoflush=False,
                                                autocommit=False,
                                                expire_on_commit=False,
                                                )
