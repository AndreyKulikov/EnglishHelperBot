add_card_function = {
    "type": "function",
    "name": "add_card_function",
    "description": """Creates an Anki flashcards with target word, Russian translation, and usage sentences. 
                        Array of dicts, each dict represent one sentence and contain 'Front'(english sentence)
                        and 'Back'(Russian Translation) as keys. For example, 
                        if user wanted to create card with word 'arrogant'(or asked for explanation):
                        [{"Front": "She's first in her class, but she's not arrogant about it.,
                        "Back": "Она первая в классе, но при этом не высокомерна."}]
                        create a few such dicts if word have different meaning. 
                        Use this tool whenever user encounters a new word 
                        or tells you to explain the meaning of the word""",
    "parameters": {
        "type": "object",
        "properties": {
            "cards": {"type": "array",
                      "description": "List of flashcard items to create in Anki",
                      "items": {
                          "type": "object",
                          "properties": {
                              "Front": {
                                  "type": "string",
                                  "description": "your generated English sentence with word, "
                                                 "demonstrating usage of the target word"
                              },
                              "Back": {
                                  "type": "string",
                                  "description": "Russian translation of generated sentence"
                              }
                          },
                          "required": ["Front", "Back"]
                      }
                      }
        },
        "required": ["cards"]
    }
}


def get_system_prompt(state: str, user_level: str) -> str:
    if state == "chat":
        system_prompt = (f"""Role: friendly English tutor(You're 24, from USA).
                        User: Current level is {user_level}. User's native language is Russian.
                        Task: Chat casually to help the user practice English.
                        Chat rules: 
                        1. Talk like a real person, 
                        Avoid hyper-correct grammar; use natural contractions (I'm, gonna), casual idioms
                        2. First, reply to the user's message, then, in the end of your reply write
                        short feedback(add a divider ---) on user's mistakes only if User did any.
                        Explain what user wrote wrong and why. If the user is a beginner, or asks for it, 
                        then explain concepts using Russian.
                        3. Strictly adapt your vocabulary and grammar explanations to suit a {user_level} learner""")
    elif state == "roleplay":
        system_prompt = (f"""""")
    elif state == "theme_learning":
        system_prompt = (f"""""")

    return system_prompt


