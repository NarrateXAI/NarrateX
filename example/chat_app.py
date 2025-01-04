from __future__ import annotations as _annotations

import asyncio
import json
import sqlite3
from collections.abc import AsyncIterator
from concurrent.futures.thread import ThreadPoolExecutor
from contextlib import asynccontextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from functools import partial
from pathlib import Path
from typing import Annotated, Any, Callable, Literal, TypeVar

import fastapi
import logfire
from fastapi import Depends, Request, Query
from fastapi.responses import HTMLResponse, Response, StreamingResponse
from pydantic import Field, TypeAdapter, Discriminator
from typing import Annotated, Union
from typing_extensions import LiteralString, ParamSpec, TypedDict
import uuid
from logging import basicConfig, getLogger
import logfire

from pydantic_ai import Agent, RunContext
from pydantic_ai.exceptions import UnexpectedModelBehavior
from pydantic_ai.messages import (
    ModelMessage,
    ModelMessagesTypeAdapter,
    ModelRequest,
    ModelResponse,
    TextPart,
    UserPromptPart
)

from markdown import to_markdown

from character import *

# 'if-token-present' means nothing will be sent (and the example will work) if you don't have logfire configured
logfire.configure(send_to_logfire='if-token-present')
logfire.configure()
basicConfig(handlers=[logfire.LogfireLoggingHandler()])

logger = getLogger(__name__)

agent = Agent('ollama:llama3.2', deps_type=Character_Lore, system_prompt="You are an astronaut on a mission to explore uncharted regions of outer space. Your name is Madival Voyager. As an experienced explorer and scientist, you are tasked with conducting research, analyzing anomalies, navigating the cosmos, and ensuring the safety of your spacecraft and crew. You are resourceful, adaptable, and highly trained in space survival, engineering, and astrophysics. Respond to situations as a human astronaut would—balancing logic, intuition, and emotion. Embrace the wonder of discovery while maintaining focus on your mission\'s objectives and the well-being of your team.")
THIS_DIR = Path(__file__).parent

@agent.system_prompt
async def add_character_lore(ctx: RunContext[Character_Lore]) -> str:
    return f"Character details: {to_markdown(ctx.deps)}"

@asynccontextmanager
async def lifespan(_app: fastapi.FastAPI):
    async with Database.connect() as db:
        yield {'db': db}


app = fastapi.FastAPI(lifespan=lifespan)
logfire.instrument_fastapi(app)


@app.get('/')
async def index() -> HTMLResponse:
    return HTMLResponse((THIS_DIR / 'chat_app.html').read_bytes())


@app.get('/chat_app.ts')
async def main_ts() -> Response:
    """Get the raw typescript code, it's compiled in the browser, forgive me."""
    return Response((THIS_DIR / 'chat_app.ts').read_bytes(), media_type='text/plain')


async def get_db(request: Request) -> Database:
    return request.state.db


# Updated FastAPI Endpoints
@app.get('/chat/')
async def get_chat(
    database: Database = Depends(get_db),
    session_id: str = Query(default=None),
) -> Response:
    if not session_id:
        session_id = str(uuid.uuid4())  # Generate a new session ID if none provided
    msgs = await database.get_messages(session_id)
    return Response(
        b'\n'.join(json.dumps(to_chat_message(m)).encode('utf-8') for m in msgs),
        media_type='text/plain',
    )

@app.get('/chat-history/')
async def get_chat_history(database: Database = Depends(get_db)) -> Response:
    msgs = await database.get_all_messages()
    return Response(
        b'\n'.join(json.dumps(to_chat_message(m)).encode('utf-8') for m in msgs),
        media_type='text/plain',
    )


class ChatMessage(TypedDict):
    """Format of messages sent to the browser."""

    role: Literal['user', 'model']
    timestamp: str
    content: str


def to_chat_message(m: ModelMessage) -> ChatMessage:
    first_part = m.parts[0]
    last_part = m.parts[-1]
    if isinstance(m, ModelRequest):
        if isinstance(last_part, UserPromptPart):
            return {
                'role': 'user',
                'timestamp': last_part.timestamp.isoformat(),
                'content': last_part.content,
            }
    elif isinstance(m, ModelResponse):
        if isinstance(first_part, TextPart):
            return {
                'role': 'model',
                'timestamp': m.timestamp.isoformat(),
                'content': first_part.content,
            }
    raise UnexpectedModelBehavior(f'Unexpected message type for chat app: {m}')


@app.post('/chat/')
async def post_chat(
    prompt: Annotated[str, fastapi.Form()],
    database: Database = Depends(get_db),
    session_id: str = Query(default=None),
) -> StreamingResponse:
    if not session_id:
        session_id = str(uuid.uuid4())  # Generate a new session ID if none provided

    async def stream_messages():
        """Streams new line delimited JSON `Message`s to the client."""
        # Stream the user prompt to the frontend
        yield (
            json.dumps(
                {
                    'role': 'user',
                    'timestamp': datetime.now(tz=timezone.utc).isoformat(),
                    'content': prompt,
                }
            ).encode('utf-8')
            + b'\n'
        )
        # Get the chat history for this session
        messages = await database.get_messages(session_id)
        # Run the AI agent
        async with agent.run_stream(prompt, message_history=messages, deps=mc_lore) as result:
            async for text in result.stream(debounce_by=0.01):
                m = ModelResponse.from_text(content=text, timestamp=result.timestamp())
                yield json.dumps(to_chat_message(m)).encode('utf-8') + b'\n'
        print(result.all_messages_json())
        # Save new messages to the database
        await database.add_messages(session_id, result.new_messages_json())

    return StreamingResponse(stream_messages(), media_type='text/plain')


MessageTypeAdapter: TypeAdapter[ModelMessage] = TypeAdapter(
    Annotated[ModelMessage, Field(discriminator='kind')]
)
P = ParamSpec('P')
R = TypeVar('R')


@dataclass
class Database:
    """Rudimentary database to store chat messages in SQLite.

    The SQLite standard library package is synchronous, so we
    use a thread pool executor to run queries asynchronously.
    """

    con: sqlite3.Connection
    _loop: asyncio.AbstractEventLoop
    _executor: ThreadPoolExecutor

    @classmethod
    @asynccontextmanager
    async def connect(
        cls, file: Path = THIS_DIR / '.chat_app_messages.sqlite'
    ) -> AsyncIterator[Database]:
        with logfire.span('connect to DB'):
            loop = asyncio.get_event_loop()
            executor = ThreadPoolExecutor(max_workers=1)
            con = await loop.run_in_executor(executor, cls._connect, file)
            slf = cls(con, loop, executor)
        try:
            yield slf
        finally:
            await slf._asyncify(con.close)

    @staticmethod
    def _connect(file: Path) -> sqlite3.Connection:
        con = sqlite3.connect(str(file))
        con = logfire.instrument_sqlite3(con)
        cur = con.cursor()
        cur.execute(
            'CREATE TABLE IF NOT EXISTS messages ('
            'id INTEGER PRIMARY KEY, '
            'session_id TEXT, '
            'message_list TEXT'
            ');'
        )
        con.commit()
        return con

    async def add_messages(self, session_id: str, messages: bytes):
        await self._asyncify(
            self._execute,
            'INSERT INTO messages (session_id, message_list) VALUES (?, ?);',
            session_id,
            messages,
            commit=True,
        )
        await self._asyncify(self.con.commit)

    async def get_messages(self, session_id: str) -> list[ModelMessage]:
        c = await self._asyncify(
            self._execute,
            'SELECT message_list FROM messages WHERE session_id = ? ORDER BY id DESC;',
            session_id,
        )
        rows = await self._asyncify(c.fetchall)
        messages: list[ModelMessage] = []
        for row in rows:
            messages.extend(ModelMessagesTypeAdapter.validate_json(row[0]))
        return messages
    
    async def get_all_messages(self) -> list[ModelMessage]:
        c = await self._asyncify(
            self._execute,
            'SELECT message_list FROM messages ORDER BY id DESC;',
        )
        rows = await self._asyncify(c.fetchall)
        messages: list[ModelMessage] = []
        for row in rows:
            messages.extend(ModelMessagesTypeAdapter.validate_json(row[0]))
        return messages

    def _execute(
        self, sql: LiteralString, *args: Any, commit: bool = False
    ) -> sqlite3.Cursor:
        cur = self.con.cursor()
        cur.execute(sql, args)
        if commit:
            self.con.commit()
        return cur

    async def _asyncify(
        self, func: Callable[P, R], *args: P.args, **kwargs: P.kwargs
    ) -> R:
        return await self._loop.run_in_executor(  # type: ignore
            self._executor,
            partial(func, **kwargs),
            *args,  # type: ignore
        )


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(
        'chat_app:app', reload=True, reload_dirs=[str(THIS_DIR)]
    )