import os

from dotenv import load_dotenv

load_dotenv()

discord_public_key = os.getenv("DISCORD_PUBLIC_KEY", "default_value_if_not_set")
discord_token = os.getenv("DISCORD_TOKEN", "default_value_if_not_set")
application_id = os.getenv("APPLICATION_ID", "default_value_if_not_set")
