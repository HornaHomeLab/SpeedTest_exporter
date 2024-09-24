from pydantic import BaseModel, Field, field_serializer


class Interface(BaseModel):
    internal_ip: str = Field(alias='internalIp', default="-")
    name: str = Field(default="-")
    mac_address: str = Field(alias='macAddr', default="-")
    is_vpn: bool = Field(alias='isVpn', default="-")
    external_ip: str = Field(alias='externalIp', default="-")

    @field_serializer('is_vpn')
    def serialize_persisted(self, is_vpn: int, _info):
        return str(is_vpn)