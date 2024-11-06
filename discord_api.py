from collections.abc import Callable
from enum import Enum, IntEnum

from pydantic import BaseModel


class ApplicationCommandType(IntEnum):
    CHAT_INPUT = 1
    USER = 2
    MESSAGE = 3


class ApplicationCommandOptionType(IntEnum):
    SUB_COMMAND = 1
    SUB_COMMAND_GROUP = 2
    STRING = 3
    INTEGER = 4
    BOOLEAN = 5
    USER = 6
    CHANNEL = 7
    ROLE = 8
    MENTIONABLE = 9
    NUMBER = 10
    ATTACHMENT = 11


class ButtonStyle(IntEnum):
    PRIMARY = 1
    SECONDARY = 2
    SUCCESS = 3
    DANGER = 4
    LINK = 5


class ChannelTypes(IntEnum):
    GUILD_TEXT = 0
    DM = 1
    GUILD_VOICE = 2
    GROUP_DM = 3
    GUILD_CATEGORY = 4
    GUILD_ANNOUNCEMENT = 5
    ANNOUNCEMENT_THREAD = 10
    PUBLIC_THREAD = 11
    PRIVATE_THREAD = 12
    GUILD_STAGE_VOICE = 13
    GUILD_DIRECTORY = 14
    GUILD_FORUM = 15
    GUILD_MEDIA = 16


class InteractionIntegrationType(IntEnum):
    GUILD_INSTALL = 0
    USER_INSTALL = 1


class InteractionContextType(IntEnum):
    GUILD = 0
    BOT_DM = 1
    PRIVATE_CHANNEL = 2


class InteractionTypes(IntEnum):
    PING = 1
    APPLICATION_COMMAND = 2
    MESSAGE_COMPONENT = 3
    APPLICATION_COMMAND_AUTOCOMPLETE = 4
    MODAL_SUBMIT = 5


class MessageComponentType(IntEnum):
    ACTION_ROW = 1
    BUTTON = 2
    STRING_SELECT = 3
    TEXT_INPUT = 4
    USER_SELECT = 5
    ROLE_SELECT = 6
    MENTIONABLE_SELECT = 7
    CHANNEL_SELECT = 8


class SelectMenuDefaultValueType(Enum):
    USER = "user"
    ROLE = "role"
    CHANNEL = "channel"


class MessageType(IntEnum):
    DEFAULT = 0
    RECIPIENT_ADD = 1
    RECIPIENT_REMOVE = 2
    CALL = 3
    CHANNEL_NAME_CHANGE = 4
    CHANNEL_ICON_CHANGE = 5
    CHANNEL_PINNED_MESSAGE = 6
    USER_JOIN = 7
    GUILD_BOOST = 8
    GUILD_BOOST_TIER_1 = 9
    GUILD_BOOST_TIER_2 = 10
    GUILD_BOOST_TIER_3 = 11
    CHANNEL_FOLLOW_ADD = 12
    GUILD_DISCOVERY_DISQUALIFIED = 14
    GUILD_DISCOVERY_REQUALIFIED = 15
    GUILD_DISCOVERY_GRACE_PERIOD_INITIAL_WARNING = 16
    GUILD_DISCOVERY_GRACE_PERIOD_FINAL_WARNING = 17
    THREAD_CREATED = 18
    REPLY = 19
    CHAT_INPUT_COMMAND = 20
    THREAD_STARTER_MESSAGE = 21
    GUILD_INVITE_REMINDER = 22
    CONTEXT_MENU_COMMAND = 23
    AUTO_MODERATION_ACTION = 24
    ROLE_SUBSCRIPTION_PURCHASE = 25
    INTERACTION_PREMIUM_UPSELL = 26
    STAGE_START = 27
    STAGE_END = 28
    STAGE_SPEAKER = 29
    STAGE_TOPIC = 31
    GUILD_APPLICATION_PREMIUM_SUBSCRIPTION = 32
    GUILD_INCIDENT_ALERT_MODE_ENABLED = 36
    GUILD_INCIDENT_ALERT_MODE_DISABLED = 37
    GUILD_INCIDENT_REPORT_RAID = 38
    GUILD_INCIDENT_REPORT_FALSE_ALARM = 39
    PURCHASE_NOTIFICATION = 44


class Message(BaseModel):
    """
    A Discord message
    https://discord.com/developers/docs/resources/channel#message-object
    """

    id: str
    channel_id: str
    author: dict
    content: str
    timestamp: str
    edited_timestamp: str | None = None
    tts: bool
    mention_everyone: bool
    mentions: list[dict]
    mention_roles: list[dict]
    mention_channels: list[dict] | None = None
    attachments: list[dict]
    embeds: list[dict]
    reactions: list[dict] | None = None
    nonce: str | None = None
    pinned: bool
    webhook_id: str | None = None
    type: MessageType
    activity: dict | None = None
    application: dict | None = None
    application_id: str | None = None
    message_reference: dict | None = None
    flags: int | None = None
    referenced_message: dict | None = None
    interaction_metadata: dict | None = None
    interaction: dict | None = None
    thread: dict | None = None
    components: list[dict] | None = None
    sticker_items: list[dict] | None = None
    stickers: list[dict] | None = None
    position: int | None = None
    role_subscription_data: dict | None = None
    resolved: dict | None = None
    poll: dict | None = None
    call: dict | None = None


class NestedInteractionOption(BaseModel):
    """
    Discord Interaction option nested within InteractionOption
    https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object-application-command-interaction-data-option-structure
    """

    name: str
    type: int
    value: str | int | float | bool | None = None
    options: dict | None = None
    focused: bool | None = None


class InteractionOption(BaseModel):
    """
    Discord Interaction options
    https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object-application-command-interaction-data-option-structure
    """

    name: str
    type: int
    value: str | int | float | bool | None = None
    options: list[NestedInteractionOption] | None = None
    focused: bool | None = None


class ResolvedMessageObjectMap(BaseModel):
    """
    A collection of resolved partial message objects
    https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object-resolved-data-structure
    """

    messages: dict[str, Message]


class ApplicationCommandData(BaseModel):
    """
    Discord Interaction data from commands
    https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object-interaction-data
    """

    id: str
    name: str
    type: int
    resolved: ResolvedMessageObjectMap | None = None
    options: list[InteractionOption] | None = None
    guild_id: str | None = None
    target_id: str | None = None

    def get_option(
        self,  # noqa: ANN101
        name: str,
    ) -> InteractionOption | None:
        if self.options:
            for option in self.options:
                if option.name == name:
                    return option
        return None

    def get_option_value(
        self,  # noqa: ANN101
        name: str,
        default: str | float | bool | None = None,
    ) -> str | int | float | bool | None:
        if self.options:
            for option in self.options:
                if option.name == name:
                    return option.value
        return default


class Emoji(BaseModel):
    id: str
    name: str
    animated: bool = True


class AvatarDecorationData(BaseModel):
    asset: str
    sku_id: str


class User(BaseModel):
    accent_color: int | None = None
    avatar_decoration_data: AvatarDecorationData | None = None
    avatar: str | None = None
    banner: str | None = None
    bot: bool | None = None
    clan: dict | None = None
    discriminator: str
    email: str | None = None
    flags: int | None = None
    global_name: str | None = None
    id: str
    locale: str | None = None
    mfa_enabled: bool | None = None
    premium_type: int | None = None
    public_flags: int | None = None
    system: bool | None = None
    username: str
    verified: bool | None = None


class Member(BaseModel):
    avatar: str | None = None
    user: User | None = None
    communication_disabled_until: str | None = None
    deaf: bool
    flags: int
    joined_at: str | None = None
    mute: bool
    nick: str | None = None
    pending: bool | None = None
    permissions: str | None = None
    premium_since: str | None = None
    roles: list[str]
    unusual_dm_activity_until: str | None = None


class ResolvedData(BaseModel):
    """
    https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object-message-component-data-structure
    """

    users: dict[str, User] | None = None
    members: dict[str, str] | None = None
    roles: dict[str, str] | None = None
    channels: dict[str, str] | None = None
    messages: dict[str, str] | None = None
    attachments: dict[str, str] | None = None


class StringSelectMenuOptions(BaseModel):
    label: str
    value: str
    description: str | None = None
    emoji: Emoji | None = None
    default: bool = False


class MessageComponentData(BaseModel):
    """
    Message Component data model
    https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object-message-component-data-structure
    """

    custom_id: str
    component_type: MessageComponentType
    values: list[StringSelectMenuOptions] | None = None
    resolved: ResolvedData | None = None


class DiscordInteraction(BaseModel):
    """
    Model for Discord Interactions via HTTP
    Reference: https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object-interaction-structure
    """

    app_permissions: str | None = None
    application_id: str
    authorizing_integration_owners: dict | None = None
    channel_id: str | None = None
    channel: dict | None = None
    context: int | None = None
    data: MessageComponentData | ApplicationCommandData | None = None
    entitlement_sku_ids: list[int] | None = None
    entitlements: list = []
    guild: dict | None = None
    guild_id: str | None = None
    guild_locale: str | None = None
    id: str
    locale: str | None = None
    member: dict | None = None
    message: dict | None = None
    token: str
    type: InteractionTypes
    user: dict | None = None
    version: int


class InteractionOptionChoice(BaseModel):
    name: str
    value: str | int | float


class NestedInteractionDefinitionOption(BaseModel):
    type: ApplicationCommandOptionType
    name: str
    description: str
    required: bool | None = None
    choices: list[InteractionOptionChoice] | None = None
    channel_types: list[ChannelTypes] | None = None
    min_value: int | float | None = None
    max_value: int | float | None = None
    min_length: int | None = None
    max_length: int | None = None
    autocomplete: bool | None = None


class InteractionDefinitionOption(BaseModel):
    type: ApplicationCommandOptionType
    name: str
    description: str
    required: bool | None = None
    choices: list[InteractionOptionChoice] | None = None
    options: list[NestedInteractionDefinitionOption] | None = None
    channel_types: list[ChannelTypes] | None = None
    min_value: int | float | None = None
    max_value: int | float | None = None
    min_length: int | None = None
    max_length: int | None = None
    autocomplete: bool | None = None


class InteractionDefinition(BaseModel):
    cmd_func: Callable
    context_types: list[InteractionContextType] | None = None
    default_member_permissions: str | None = None
    description: str
    guild_id: str | None = None
    integration_types: list[InteractionIntegrationType] | None = None
    name: str
    nsfw: bool | None = None
    options: list[InteractionDefinitionOption] | None = None
    type: ApplicationCommandType | None = ApplicationCommandType.CHAT_INPUT


class MessageComponent(BaseModel):
    type: MessageComponentType


class ButtonComponent(MessageComponent):
    type: MessageComponentType = MessageComponentType.BUTTON
    style: ButtonStyle
    label: str
    emoji: Emoji | None = None
    custom_id: str
    url: str | None = None
    disabled: bool = False


class SelectMenuDefaultValue(BaseModel):
    id: str
    type: SelectMenuDefaultValueType


class SelectMenuComponentBase(MessageComponent):
    type: MessageComponentType
    custom_id: str
    placeholder: str | None = None
    min_values: int = 1
    max_values: int = 1
    disabled: bool = False


class TextInput(MessageComponent):
    type: MessageComponentType = MessageComponentType.TEXT_INPUT
    custom_id: str
    style: None
    label: str
    min_length: int | None = None
    max_length: int | None = None
    required: bool = True
    value: str | None = None
    placeholder: str | None = None


class StringSelectMenu(SelectMenuComponentBase):
    type: MessageComponentType = MessageComponentType.STRING_SELECT
    options: list[StringSelectMenuOptions]


class ChannelSelectMenu(SelectMenuComponentBase):
    type: MessageComponentType = MessageComponentType.CHANNEL_SELECT
    channel_types: list[ChannelTypes]
    default_values: list[SelectMenuDefaultValue]


class UserSelectMenu(SelectMenuComponentBase):
    type: MessageComponentType = MessageComponentType.USER_SELECT
    default_values: list[SelectMenuDefaultValue]


class RoleSelectMenu(SelectMenuComponentBase):
    type: MessageComponentType = MessageComponentType.ROLE_SELECT
    default_values: list[SelectMenuDefaultValue]


class MentionableSelectMenu(SelectMenuComponentBase):
    type: MessageComponentType = MessageComponentType.MENTIONABLE_SELECT
    default_values: list[SelectMenuDefaultValue]


class ComponentActionRow(BaseModel):
    type: MessageComponentType = MessageComponentType.ACTION_ROW
    components: list[
        ButtonComponent
        | StringSelectMenu
        | TextInput
        | UserSelectMenu
        | RoleSelectMenu
        | MentionableSelectMenu
        | ChannelSelectMenu
    ]


class EmbedField(BaseModel):
    name: str
    value: str
    inline: bool = True


class MessageEmbed(BaseModel):
    title: str | None = None
    description: str | None = None
    url: str | None = None
    color: int | None = None
    footer: str | None = None
    image: str | None = None
    thumbnail: str | None = None
    video: str | None = None
    author: str | None = None
    fields: list[EmbedField] | None = None


class InteractionMessage(BaseModel):
    content: str = ""
    embeds: list[MessageEmbed] | None = None
    # https://discord.com/developers/docs/resources/channel#message-object-message-flags
    # default flags: (EPHEMERAL) 64
    flags: int = 64
    components: list[ComponentActionRow] = []

    def to_json(self: "InteractionMessage") -> dict:
        return self.model_dump(exclude_none=True)
