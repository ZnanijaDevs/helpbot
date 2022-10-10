from enum import Enum
from typing import Any
from .blocks import Block
from .entry_with_mapping import EntryWithMapping


class Color(Enum):
    """
    Color utility class for use with the Slack secondary attachments API.
    """
    GOOD = "good"
    WARNING = "warning"
    DANGER = "danger"
    RED = "#ff0000"
    BLUE = "#0000ff"
    YELLOW = "#ffff00"
    GREEN = "#00ff00"
    ORANGE = "#ff8800"
    PURPLE = "#8800ff"
    BLACK = "#000000"


class Field(EntryWithMapping):
    """
    Field text objects for use with Slack's secondary attachment API.
    """

    def __init__(
        self,
        title: str = None,
        value: str = None,
        short: bool = False
    ):
        self.title = title
        self.value = value
        self.short = short

    def resolve(self):
        field = {"short": self.short}

        if self.title:
            field["title"] = self.title
        if self.value:
            field["value"] = self.value

        return field


class Attachment(EntryWithMapping):
    """
    Secondary content can be attached to messages to include lower priority content
     - content that doesn't necessarily need to be seen to appreciate the intent of
    the message, but perhaps adds further context or additional information.
    """

    def __init__(
        self,
        blocks: list[Block] | Block = None,
        color: str | Color = None
    ):
        if isinstance(blocks, list):
            self.blocks = blocks
        elif isinstance(blocks, Block):
            self.blocks = [blocks]
        else:
            self.blocks = None

        if isinstance(color, Color):
            self.color = color.value
        elif isinstance(color, str):
            if len(color) == 7 and color.startswith("#"):
                self.color = color
            else:
                raise ValueError("Color must be a valid hex code (e.g. #ffffff)")
        else:
            self.color = None

    def resolve(self) -> dict[str, Any]:
        attachment = {}

        if self.blocks:
            attachment["blocks"] = [block.resolve() for block in self.blocks]
        if self.color:
            attachment["color"] = self.color

        return attachment
