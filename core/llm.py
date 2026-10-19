from openai import AsyncOpenAI, RateLimitError, APIConnectionError, PermissionDeniedError, APITimeoutError, BadRequestError, APIStatusError
import os
from dotenv import load_dotenv
from collections import deque
import json

from core.schemas_prompts import add_card_function, get_system_prompt
from tools.anki import add_card

load_dotenv()


class LlmClient:
    def __init__(
            self,
            size: int,
            max_tokens: int,
            reasoning: str,
            model: str = "google/gemma-4-26b-a4b-it:free"):
        self.client = AsyncOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY")
        )
        self.max_tokens = max_tokens
        self.reasoning = reasoning
        self.model = model
        self.user_level = "B2"
        self.tools = [add_card_function]
        self.messages: deque[dict] = deque(maxlen=size)

    async def _call(self, state: str, input_: list):
        try:
            response = await self.client.responses.create(
                model=self.model,
                reasoning={"effort": self.reasoning},
                instructions=get_system_prompt(state, self.user_level),
                input=input_,
                tools=self.tools,
                max_output_tokens=self.max_tokens
            )
        except RateLimitError:
            return 'I\'m broke so I use the free model. Please wait a little before trying again)'
        except (APITimeoutError, APIConnectionError):
            return 'Sorry, seems something wrong with provider or host pc.'
        except (PermissionDeniedError, BadRequestError, APIStatusError):
            return 'Hm, how strange, can\'t get an access to model/provider'
        return response

    async def _call_tools(self, call) -> str:
        if call.name == "add_card_function":
            try:
                cards = json.loads(call.arguments)["cards"]
            except (json.JSONDecodeError, KeyError):
                return "Wrong schema, invalid args for add_cards function"
            return await add_card(cards)
        else:
            return "Requested unknown tool"

    async def chat(self, user_message: str) -> str:
        user_input = {"role": "user", "content": user_message}
        self.messages.append(user_input)

        response = await self._call("chat", list(self.messages))

        if isinstance(response, str):
            return response

        tool_calls = [i for i in response.output if i.type == "function_call"]

        if tool_calls:
            temp_input = (list(self.messages))

            for call in tool_calls:
                result = await self._call_tools(call)
                temp_input.append(call.model_dump())
                temp_input.append({"type": "function_call_output", "call_id": call.call_id, "output": result})

            response = await self._call("chat", temp_input)

            if isinstance(response, str):
                return response

        assistant_text = response.output_text
        self.messages.append({"role": "assistant", "content": assistant_text})
        return assistant_text

    # ----------------------------------------------
    def get_conversation(self):
        return list(self.messages)