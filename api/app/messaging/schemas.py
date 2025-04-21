from pydantic import BaseModel

class AnaliseMessage(BaseModel):
    transaction_id: str

    def serialize(self) -> bytes:
        return self.model_dump_json().encode('utf-8')