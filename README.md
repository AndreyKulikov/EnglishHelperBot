<div align="center">

# English Helper Bot

**AI-powered English tutor in Telegram: casual conversation, mistake corrections
and Anki flashcards generation**

![Python](https://img.shields.io/badge/python-3.11+-3776AB?logo=python&logoColor=white)
![Aiogram](https://img.shields.io/badge/aiogram-3-26A69A?logo=telegram&logoColor=white)
![OpenAI SDK](https://img.shields.io/badge/client-OpenAI%20SDK-412991?logo=openai&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)

</div>

## What is this?

A Telegram bot that helps Russian-speaking learners practice English through
conversations. It adapts to the user's level, corrects mistakes inline,
and turns new vocabulary into Anki flashcards via tool calling.

## Features

- Casual chat with per-user conversation memory
- Mistake feedback adapted to user's level
- Anki card generation via LLM tool calling 
- Persistent memory (planned)
- User profile extraction (planned)
- Theme learning based on user's common mistakes (planned)
- Roleplay scenarios (planned)

## Stack

| Component | Tech |
|---|---|
| Bot framework | Aiogram | 
| LLM access | OpenAI SDK (& OpenRouter) |
| Memory | Sliding window (using `collections.deque`) |
| Flashcards | AnkiConnect |
| HTTP | httpx |

## Project structure

```
EnglishHelperBot/
├── main.py                  # entry point: bot, dispatcher
├── bot/
│   └── handlers.py          # Aiogram routers
├── core/
│   ├── llm.py               # LLM client: sliding window, tool loop, errors handling
│   └── schemas_prompts.py   # system prompts + tool JSON schemas
├── tools/
│   └── anki.py              # AnkiConnect client integration
├── requirements.txt
└── LICENSE
```

## Quick start

**Prerequisites:** Python 3.11+, Anki desktop with the
[AnkiConnect](https://foosoft.net/projects/anki-connect/) add-on enabled,
an OpenRouter API key(or other router, you can change it in llm.py) and a BotFather bot Token.

```bash
git clone https://github.com/AndreyKulikov/EnglishHelperBot.git
cd EnglishHelperBot
python -m venv venv && source venv/bin/activate 
pip install -r requirements.txt
python main.py
```

Example `.env`:
```env
BOT_TOKEN=your_telegram_bot_token
OPENROUTER_API_KEY=sk-or-v1-...
```

## License

[MIT](LICENSE)
