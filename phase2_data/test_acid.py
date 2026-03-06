import asyncio
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import text, Integer, String, Numeric, Column
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True)
    owner = Column(String(50))
    balance = Column(Numeric(10, 2))

# ✅ Fix: module-scoped event loop to match module-scoped engine fixture
@pytest.fixture(scope="module")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="module")
async def engine():
    eng = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with eng.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with AsyncSession(eng) as s:
        s.add_all([
            Account(owner="Alice", balance=1000),
            Account(owner="Bob", balance=500)
        ])
        await s.commit()
    yield eng
    await eng.dispose()

@pytest.mark.asyncio
async def test_acid_rollback_on_failure(engine):
    """Debit succeeds but credit fails — full rollback must occur."""
    async with AsyncSession(engine) as session:
        try:
            async with session.begin():
                await session.execute(
                    text("UPDATE accounts SET balance = balance - 200 WHERE owner = 'Alice'")
                )
                raise Exception("Simulated network failure mid-transaction")
        except Exception:
            pass  # Rollback is automatic on context manager exit

    async with AsyncSession(engine) as verify:
        result = await verify.execute(
            text("SELECT balance FROM accounts WHERE owner='Alice'")
        )
        alice_balance = result.scalar()
        assert alice_balance == 1000, f"ROLLBACK FAILED — got {alice_balance}"

@pytest.mark.asyncio
async def test_successful_transfer(engine):
    async with AsyncSession(engine) as session:
        async with session.begin():
            await session.execute(
                text("UPDATE accounts SET balance = balance - 100 WHERE owner = 'Alice'")
            )
            await session.execute(
                text("UPDATE accounts SET balance = balance + 100 WHERE owner = 'Bob'")
            )

    async with AsyncSession(engine) as verify:
        r1 = await verify.execute(text("SELECT balance FROM accounts WHERE owner='Alice'"))
        r2 = await verify.execute(text("SELECT balance FROM accounts WHERE owner='Bob'"))
        assert r1.scalar() == 900
        assert r2.scalar() == 600
