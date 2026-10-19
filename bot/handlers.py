from aiogram import html, F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from core.llm import LlmClient

router = Router()

sessions: dict[int, LlmClient] = {}


def get_session(user_id: int) -> LlmClient:
    if user_id not in sessions:
        sessions[user_id] = LlmClient(size=10, max_tokens=1024, reasoning="medium")
    return sessions[user_id]


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"First of all, welcome to the club, {html.bold(message.from_user.full_name)}!")
    await message.answer(f'Please, tell me something about yourself before we will begin(Your english level,'
                         f'maybe something you want to learn, your strong sides)'
                         f'\nAll will be helpful')


@router.message(F.text)
async def echo_handler(message: Message) -> None:
    session = get_session(message.from_user.id)
    ai_response = await session.chat(message.text)
    await message.answer(ai_response)
