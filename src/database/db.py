from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession


class DB:
    def __init__(self, db_url: str) -> None:
        self.engine = create_async_engine(db_url, echo=False)
        self.async_session = async_sessionmaker(
            self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
            class_=AsyncSession,
        )
