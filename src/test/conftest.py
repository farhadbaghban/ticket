import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from main import app
from db.engine import Base, get_db

SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5434/ticket"

# Create a SQLAlchemy engine
engine = create_async_engine(SQLALCHEMY_DATABASE_URL)

# Create a sessionmaker to manage sessions
TestingSessionLocal = sessionmaker(
    bind=engine, autoflush=False, autocommit=False, class_=AsyncSession
)


# Asynchronously create tables in the database
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Fixture to Drop tables in the database
@pytest.fixture(scope="function", autouse=True)
async def setup_database():
    """Initialize the database schema and drop all tables after tests."""
    await init_db()
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# Fixture to start and close db connection for any Sessions
@pytest.fixture(scope="function")
async def db_session():
    """Create a new database session with a rollback at the end of the test."""
    async with engine.connect() as connection:
        async with connection.begin() as transaction:
            session = TestingSessionLocal(bind=connection)
            try:
                yield session
            finally:
                await session.close()
                await transaction.rollback()


@pytest.fixture(scope="function")
async def async_client(db_session):
    """Create a test client that uses the override_get_db fixture to return a session."""

    async def override_get_db():
        try:
            yield db_session
        finally:
            pass  # db_session will be closed by the db_session fixture itself

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client

    # Cleanup after test
    app.dependency_overrides.pop(get_db, None)


# Fixture to generate a user payload
@pytest.fixture()
def user_payload():
    """Generate a user payload."""
    return {
        "email": "test@email.com",
        "password": "123@456",
    }
