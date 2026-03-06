import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import asyncio
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from phase1_backend.app.main import app
from phase1_backend.app.database import Base, get_db

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# ✅ Fix: provide a session-scoped event loop explicitly
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="session")
async def test_engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()

@pytest_asyncio.fixture(scope="session")
async def db_session(test_engine):
    TestSession = async_sessionmaker(test_engine, expire_on_commit=False)
    async with TestSession() as session:
        yield session

@pytest_asyncio.fixture(scope="session")
async def client(db_session):
    async def override_get_db():
        yield db_session
    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_get_db_direct():
    """Covers database.py lines 13-14 by exercising the real get_db generator."""
    gen = get_db()
    session = await gen.__anext__()
    assert isinstance(session, AsyncSession)
    try:
        await gen.asend(None)
    except StopAsyncIteration:
        pass
