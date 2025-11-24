import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.db.base import Base
from src.services.analyzer import AnalyzerService
from src.services.chat_gateway import ChatGateway
from src.data.chat_message_repo import ChatMessageRepository


@pytest_asyncio.fixture
async def session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", future=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        yield session
    await engine.dispose()


@pytest.mark.asyncio
async def test_chat_gateway_stores_messages(session):
    repo = ChatMessageRepository(session)
    analyzer = AnalyzerService(repo=None)
    gateway = ChatGateway(analyzer=analyzer, repo=repo)

    class DummyWebSocket:
        def __init__(self):
            self.sent = []

        async def accept(self):
            return None

        async def send_json(self, data):
            self.sent.append(data)

    ws = DummyWebSocket()
    await gateway.connect(ws, "room1")
    from src.schemas.chat import ChatMessagePayload

    await gateway.handle_message(ws, ChatMessagePayload(room_id="room1", user_id="user1", text="hello"))
    messages = await repo.recent_messages("room1")
    assert len(messages) == 1
