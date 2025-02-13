import os
from openai import OpenAI


class ChatClient:
    def __init__(self, client="openai", max_tokens=3000, temperature=0.1, model="gpt-3.5-turbo"):
        self.client = self._get_client_obj(client)  # handle invalid client input
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.model = model
        self.history = []

    def _get_client_obj(self, client_str) -> OpenAI:
        match client_str:
            case "openai":
                return OpenAI(
                    api_key=os.environ.get("OPENAI_API_KEY"),
                )
            case _:
                raise ValueError("no client found")

    def clear_history(self):
        self.history = []

    def add_context_prompt(self, string: str):
        developer_input = {
            "role": "developer"
        }

    def client_prompt(self, string: str, *stringargs):
        user_input = {
            "role": "user",
            "content": string
        }
        self.history.append(user_input)
        for message in stringargs:
            self.history.append({
                "role": "user",
                "content": message
            })
        res = self.client.chat.completions.create(
            model=self.model,
            messages=self.history,
            stream=False,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
        )
        res_output_string = res.choices[0].message.content
        assistant_input = {
            "role": "assistant",
            "content": res_output_string
        }
        self.history.append(assistant_input)
        return res_output_string
