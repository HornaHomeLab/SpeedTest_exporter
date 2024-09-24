from pydantic import BaseModel, Field, field_serializer

class Result(BaseModel):
    id: str = Field(default="-")
    url: str = Field(default="-")
    persisted: bool = Field(default=False)
    
    @field_serializer('persisted')
    def serialize_persisted(self, persisted: int, _info):
        return str(persisted)