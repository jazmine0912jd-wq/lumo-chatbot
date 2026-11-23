from mistralai import Mistral

from .config import Config


class MistralChatClient:
    def __init__(self, config: Config) -> None:
        self._config = config
        self._client = Mistral(api_key=config.api_key)

    def complete(self, messages: list[dict]) -> str:
        response = self._client.chat.complete(
            model=self._config.model,
            messages=messages,
            temperature=self._config.temperature,
            max_tokens=self._config.max_tokens,
        )
        content = response.choices[0].message.content
        if isinstance(content, str):
            return content
        return "".join(
            getattr(block, "text", "") for block in content if hasattr(block, "text")
        )
