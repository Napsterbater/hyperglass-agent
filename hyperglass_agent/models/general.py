import ipaddress
from typing import Union
from pydantic import validator
from hyperglass_agent.exceptions import ConfigError
from hyperglass_agent.constants import SUPPORTED_NOS
from hyperglass_agent.models._utils import HyperglassModel


class General(HyperglassModel):
    debug: bool = False
    listen_address: Union[ipaddress.IPv4Address, ipaddress.IPv6Address] = "0.0.0.0"
    port: int = 8080
    mode: str

    @validator("mode")
    def validate_mode(cls, value):
        if value not in SUPPORTED_NOS:
            raise ConfigError(
                f"mode must be one of '{*SUPPORTED_NOS}'. Received '{value}'"
            )
        return value
