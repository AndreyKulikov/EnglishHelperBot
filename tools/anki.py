import httpx


async def add_card(cards: list[dict[str, str]]) -> str:
    url = "http://localhost:8765"
    payload = {
        "action": "addNotes",
        "version": 6,
        "params": {
            "notes": [
                {
                    "deckName": "English",
                    "modelName": "Basic",
                    "fields": {
                        "Front": card["Front"],
                        "Back": card["Back"]
                    }
                }
                for card in cards
            ]
        }
    }
    try:
        async with httpx.AsyncClient() as x_client:
            response = await x_client.post(url, json=payload)
            print(response)
            res_data = response.json()
            print(res_data)
            if res_data.get("error"):
                return f"Anki error: {res_data['error']}"
            return f"Successfully added {len(cards)} cards to Anki!"
    except Exception as e:
        return f"Some error occured: {e}"
