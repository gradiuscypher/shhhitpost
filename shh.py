#!/usr/bin/env python3

import uvicorn
from fastapi import APIRouter, Depends, FastAPI

from config import discord_public_key
from depends import ValidateDiscordRequest
from discord_api import DiscordInteraction, InteractionTypes, MessageComponentData
from helpers import configure_logging
from interactions.commands import build_command_routers, get_command_result
from interactions.components import build_component_router, get_component_result

discord_router = APIRouter(
    prefix="/discord",
    dependencies=[Depends(ValidateDiscordRequest(discord_public_key))],
)

logger = configure_logging(__name__)
command_router = build_command_routers()
component_router = build_component_router()


@discord_router.post("/interactions")
async def discord_interactions(
    interaction: DiscordInteraction,
) -> dict:
    """ref: https://discord.com/developers/docs/interactions/receiving-and-responding#responding-to-an-interaction"""
    if interaction.type == InteractionTypes.PING:
        return {"type": 1}

    if interaction.type == InteractionTypes.APPLICATION_COMMAND:
        if interaction.data:
            try:
                result = await get_command_result(command_router, interaction)
            except KeyError as exc:
                logger.exception("No key for command", exc_info=exc)
                return {
                    "type": 4,
                    "data": {"content": "Command was unable to complete.", "flags": 64},
                }

            if result and result.success:
                if result.message:
                    return {"type": 4, "data": result.message.to_json()}

                return {"type": 4, "data": {"content": result.reason, "flags": 68}}

        return {
            "type": 4,
            "data": {
                "content": f"Error while running the command: {result.reason}",
                "flags": 64,
            },
        }

    if (
        interaction.type == InteractionTypes.MESSAGE_COMPONENT
        and interaction.data
        and isinstance(interaction.data, MessageComponentData)
    ):
        try:
            result = await get_component_result(component_router, interaction)
        except KeyError as exc:
            logger.exception("No key for command", exc_info=exc)

        if result:
            return result.to_json()

    return {}


app = FastAPI()
app.include_router(discord_router)


if __name__ == "__main__":
    uvicorn.run("shh:app", reload=True)
