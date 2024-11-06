from collections.abc import Callable

from pydantic import BaseModel

from discord_api import (
    ApplicationCommandData,
    ApplicationCommandOptionType,
    DiscordInteraction,
    InteractionDefinition,
    InteractionDefinitionOption,
    InteractionIntegrationType,
    InteractionMessage,
)


class InteractionResult(BaseModel):
    message: InteractionMessage | None = None
    success: bool
    reason: str


# Interaction Definitions - The commands our app will run
async def hidden_message_fn(interaction: DiscordInteraction) -> InteractionResult:
    """
    A function for hidden messages
    """
    if interaction.data and isinstance(interaction.data, ApplicationCommandData):
        user_id = None
        if interaction.user:
            user_id = interaction.user["id"]

    print("Command from: ", user_id)
    return InteractionResult(success=True, reason="This is a test message")


hidden_message = InteractionDefinition(
    cmd_func=hidden_message_fn,
    name="shh",
    description="Send a hidden message for your friends to read",
    integration_types=[
        InteractionIntegrationType.USER_INSTALL,
    ],
    options=[
        InteractionDefinitionOption(
            name="message",
            type=ApplicationCommandOptionType.STRING,
            description="the message",
            required=True,
        ),
    ],
)


# Helper Functions and classes
def get_json_model(command: InteractionDefinition) -> dict:
    return command.model_dump(exclude_none=True, exclude={"cmd_func"})


def get_command_locations() -> tuple[dict, list]:
    global_commands = [
        get_json_model(hidden_message),
    ]

    return (all_guild_commands, global_commands)


"""
a dict of guild IDs to list of commands:

guild_commands = {
    "12345": [
        get_json_model(save_link),
    ]
}
"""

all_guild_commands = {}

all_commands = [hidden_message]


def build_command_routers() -> dict[str, Callable]:
    command_router = {}

    for command in all_commands:
        command_router[command.name] = command.cmd_func

    return command_router


async def get_command_result(command_router, interaction) -> InteractionResult:
    return await command_router[interaction.data.name](
        interaction,
    )
