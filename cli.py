#!/usr/bin/env python3

import json
from time import sleep

import httpx
import typer

from config import application_id, discord_token
from helpers import configure_logging
from interactions.commands import (
    get_command_locations,
)

logger = configure_logging(__name__)

app = typer.Typer()


class RetriesExceededError(Exception):
    """
    Raise when we've run out of retries when making a request
    """

    def __init__(self: "RetriesExceededError") -> None:
        super().__init__("Number of retries has been exceeded")


class RateLimit(httpx.BaseTransport):
    def __init__(
        self: "RateLimit",
        retry_count: int = 3,
    ) -> None:
        super().__init__()
        self.transport = httpx.HTTPTransport()
        self.retry_count = retry_count

    def handle_request(self: "RateLimit", request: httpx.Request) -> httpx.Response:
        retries = self.retry_count

        while retries:
            response = self.transport.handle_request(request)
            response.read()

            if response.status_code == httpx.codes.TOO_MANY_REQUESTS:
                retry_after = response.json().get("retry_after", 1)
                logger.debug(
                    "You are being ratelimited, retrying in %s",
                    retry_after,
                )
                retries -= 1
                sleep(retry_after)

            else:
                return response

        raise RetriesExceededError


transport = RateLimit()
base_url = "https://discord.com/api/v10"
api_client = httpx.Client(
    base_url=base_url,
    headers={"Authorization": f"Bot {discord_token}"},
    transport=transport,
)


@app.command()
def install_guild_commands(delete_previous: bool = False) -> None:  # noqa: FBT001, FBT002
    guild_commands, _ = get_command_locations()

    for guild in guild_commands:
        # delete the previously configured commands
        if delete_previous:
            command_json = api_client.get(
                f"/applications/{application_id}/guilds/{guild}/commands",
            ).json()
            for command in command_json:
                r = api_client.delete(
                    f"/applications/{application_id}/guilds/{guild}/commands/{command['id']}",
                )
            print(f"Removed {len(command_json)} guild commands")

        # install the current configured commands
        for command in guild_commands[guild]:
            r = api_client.post(
                f"/applications/{application_id}/guilds/{guild}/commands",
                json=command,
            )

            if r.status_code == httpx.codes.CREATED:
                print(f"Created the command: {command['name']}")
            elif r.status_code == httpx.codes.OK:
                print(f"Updated the command: {command['name']}")
            else:
                print(r.status_code, r.text)


@app.command()
def install_private_commands(delete_previous: bool = False) -> None:  # noqa: FBT001,FBT002
    if delete_previous:
        command_json = api_client.get(
            f"/applications/{application_id}/commands",
        ).json()

        for command in command_json:
            r = api_client.delete(
                f"/applications/{application_id}/commands/{command['id']}",
            )

        print(f"Removed {len(command_json)} private commands")

    _, global_commands = get_command_locations()

    for command in global_commands:
        r = api_client.post(
            f"/applications/{application_id}/commands",
            json=command,
        )

        if r.status_code == httpx.codes.CREATED:
            print(f"Created the command: {command['name']}")
        elif r.status_code == httpx.codes.OK:
            print(f"Updated the command: {command['name']}")
        else:
            print(r.status_code, r.text)


@app.command()
def list_global_commands() -> None:
    command_json = api_client.get(
        f"/applications/{application_id}/commands",
    ).json()
    print(json.dumps(command_json, indent=True))


@app.command()
def delete_global_commands() -> None:
    command_json = api_client.get(
        f"/applications/{application_id}/commands",
    ).json()

    for command in command_json:
        api_client.delete(
            f"/applications/{application_id}/commands/{command['id']}",
        )

    print(f"Removed {len(command_json)} global commands")


if __name__ == "__main__":
    app()
