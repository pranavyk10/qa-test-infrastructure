"""
Simulates 'eventually consistent' NoSQL behavior using a mock.
In production, swap MockMongoCollection with a real motor/pymongo collection.
"""
import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock

class MockMongoCollection:
    def __init__(self):
        self._store = {}
        self._pending_writes = {}

    async def insert_one(self, doc: dict):
        self._pending_writes[doc["_id"]] = doc

    async def find_one(self, query: dict):
        _id = query.get("_id")
        return self._store.get(_id)  # Returns None if write hasn't synced yet

    async def sync(self):
        self._store.update(self._pending_writes)
        self._pending_writes.clear()

@pytest.mark.asyncio
async def test_eventual_consistency_window():
    collection = MockMongoCollection()
    await collection.insert_one({"_id": "u1", "name": "Dave"})

    # Read BEFORE sync — simulates 50ms lag in distributed system
    result_before_sync = await collection.find_one({"_id": "u1"})
    assert result_before_sync is None, "Data should not be readable before sync"

    # Simulate sync completing
    await collection.sync()
    result_after_sync = await collection.find_one({"_id": "u1"})
    assert result_after_sync["name"] == "Dave", "Data should be readable after sync"
