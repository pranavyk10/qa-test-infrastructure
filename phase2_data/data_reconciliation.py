"""
Data Reconciliation Script: Compares API response against direct DB state.
Run: python -m phase2_data.data_reconciliation
"""
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import text

async def fetch_db_state(engine, user_id: int) -> dict:
    async with AsyncSession(engine) as s:
        result = await s.execute(text("SELECT id, name, email FROM users WHERE id = :id"), {"id": user_id})
        row = result.fetchone()
        return dict(row._mapping) if row else {}

def simulate_api_response(user_id: int) -> dict:
    # In real usage, replace with: httpx.get(f"/users/{user_id}").json()
    return {"id": user_id, "name": "Alice", "email": "alice@example.com"}

async def reconcile(user_id: int):
    engine = create_async_engine("sqlite+aiosqlite:///./test.db", echo=False)
    db_state = await fetch_db_state(engine, user_id)
    api_state = simulate_api_response(user_id)
    await engine.dispose()

    discrepancies = {}
    for key in api_state:
        if str(api_state.get(key)) != str(db_state.get(key)):
            discrepancies[key] = {"api": api_state.get(key), "db": db_state.get(key)}

    if discrepancies:
        print(f"[SILENT CORRUPTION DETECTED] User {user_id}: {discrepancies}")
    else:
        print(f"[OK] User {user_id}: API and DB are in sync.")

if __name__ == "__main__":
    asyncio.run(reconcile(1))
