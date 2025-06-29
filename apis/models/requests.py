from datetime import datetime
from pydantic import BaseModel


class TranslateTextRequest(BaseModel):
    source_text: str
    source_language: str = "auto"
    target_language: str = "es"


class TranslateMultipleTextRequest(BaseModel):
    source_text: list[str]
    source_language: str = "auto"
    target_language: str = "es"


class TranslateJsonRequest(BaseModel):
    msg_o: str
    from: str = "customer"
    name: str
    ts: datetime
    msg: str
    source_lang: str = None
    channel: str = "api"