from collections.abc import Callable

from pydantic import BaseModel

from discord_api import (
    InteractionMessage,
)
from helpers import configure_logging

logger = configure_logging(__name__)


class ComponentCommand(BaseModel):
    name: str
    cmd_func: Callable


class ComponentResultData(BaseModel):
    content: str


class ComponentResult(BaseModel):
    type: int
    data: InteractionMessage

    def to_json(self: "ComponentResult") -> dict:
        return self.model_dump(exclude_none=True)


async def get_component_result(component_router, interaction) -> ComponentResult:
    interaction_name = interaction.data.custom_id.split(":")[0]
    return await component_router[interaction_name](
        interaction,
    )


all_components = []


def build_component_router() -> dict[str, Callable]:
    component_router = {}

    for component in all_components:
        component_router[component.name] = component.cmd_func

    return component_router
