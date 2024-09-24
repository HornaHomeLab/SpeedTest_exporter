from pydantic import BaseModel, Field, field_serializer

class Server(BaseModel):
    id: int = Field(default=0)
    host: str = Field(default="-")
    port: int = Field(default=0)
    name: str = Field(default="-")
    location: str = Field(default="-")
    country: str = Field(default="-")
    ip: str = Field(default="-")
    
    @field_serializer('id')
    def serialize_id(self, id: int, _info):
        return str(id)
    
    @field_serializer('port')
    def serialize_port(self, port: int, _info):
        return str(port)