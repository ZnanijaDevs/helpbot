from typing import Any, Optional
from .attachments import Attachment
from .blocks import Block
from .entry_with_mapping import EntryWithMapping


class BaseMessage(EntryWithMapping):
    """
    A Slack message object that can be converted to a JSON string for use with
    the Slack message API.
    """

    def __init__(
        self,
        channel: Optional[str] = None,
        text: Optional[str] = "",
        blocks: Optional[list[Block] | Block] = None,
        attachments: Optional[list[Attachment]] = None,
        thread_ts: Optional[str] = None
    ):
        if isinstance(blocks, list):
            self.blocks = blocks
        elif isinstance(blocks, Block):
            self.blocks = [blocks, ]
        else:
            self.blocks = None

        self.channel = channel
        self.text = text
        self.attachments = attachments or []
        self.thread_ts = thread_ts

    def resolve(self) -> dict[str, Any]:
        message = {}

        if self.channel:
            message["channel"] = self.channel
        if self.blocks:
            message["blocks"] = [block.resolve() for block in self.blocks]
        if self.attachments:
            message["attachments"] = [attachment.resolve() for attachment in self.attachments]
        if self.thread_ts:
            message["thread_ts"] = self.thread_ts
        if self.text or self.text == "":
            message["text"] = self.text

        return message


class Message(BaseMessage):
    """A class that represents a Slack message"""


class MessageResponse(BaseMessage):
    """
    A required, immediate response that confirms your app received the payload.
    """

    def __init__(
        self,
        text: Optional[str] = "",
        blocks: Optional[list[Block] | Block] = None,
        attachments: Optional[list[Attachment]] = None,
        thread_ts: Optional[str] = None,
        replace_original: bool = False,
        ephemeral: bool = False
    ):
        super().__init__(text=text, blocks=blocks, attachments=attachments, thread_ts=thread_ts)

        self.replace_original = replace_original
        self.ephemeral = ephemeral

    def _resolve(self) -> dict[str, Any]:
        result = {**super().resolve(), "replace_original": self.replace_original}

        if self.ephemeral:
            result["response_type"] = "ephemeral"

        return result
