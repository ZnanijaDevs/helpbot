from enum import Enum
from typing import Any
from uuid import uuid4
from .elements import Element, ElementType, Text, TextType
from .entry_with_mapping import EntryWithMapping


class BlockType(Enum):
    """
    Convenience class for identifying the different types of blocks available
    in the Slack Blocks API and their programmatic names.
    """
    SECTION = "section"
    DIVIDER = "divider"
    IMAGE = "image"
    ACTIONS = "actions"
    CONTEXT = "context"
    FILE = "file"
    HEADER = "header"


class Block(EntryWithMapping):
    """Basis block containing attributes and behaviour common to all blocks."""

    def __init__(self, type_: BlockType, block_id: str | None = None):
        self.type = type_
        self.block_id = block_id if block_id else str(uuid4())

    def __add__(self, other: "Block"):
        return [self, other]

    def _attributes(self):
        return {
            "type": self.type.value,
            "block_id": self.block_id
        }


class SectionBlock(Block):
    """
    A section is one of the most flexible blocks available -
    it can be used as a simple text block, in combination with text fields,
    or side-by-side with any of the available block elements.
    """

    def __init__(
        self,
        text: str | Text,
        block_id: str = None,
        fields: list[Text] = None,
        accessory: Element = None
    ):
        super().__init__(type_=BlockType.SECTION, block_id=block_id)

        if isinstance(text, Text):
            self.text = text
        else:
            self.text = Text(text)

        self.fields = fields
        self.accessory = accessory

    def resolve(self) -> dict[str, Any]:
        section = self._attributes()
        section["text"] = self.text.resolve()

        if self.fields:
            section["fields"] = [field.resolve() for field in self.fields]
        if self.accessory:
            section["accessory"] = self.accessory.resolve()

        return section


class DividerBlock(Block):
    """
    A content divider, like an <hr>, to split up different blocks inside of
    a message. The divider block is nice and neat, requiring only a type.
    """

    def __init__(self, block_id: str = None):
        super().__init__(type_=BlockType.DIVIDER, block_id=block_id)

    def resolve(self):
        return self._attributes()


class ImageBlock(Block):
    """A simple image block, designed to make those cat photos really pop."""

    def __init__(
        self,
        image_url: str,
        alt_text: str = "",
        title: Text | str = None,
        block_id: str = None
    ):
        super().__init__(type_=BlockType.IMAGE, block_id=block_id)

        self.image_url = image_url
        self.alt_text = alt_text

        if title and isinstance(title, Text):
            if title.text_type == TextType.MARKDOWN:
                self.title = Text(
                    text=title.text,
                    type_=TextType.PLAINTEXT,
                    emoji=title.emoji,
                    verbatim=title.verbatim
                )
            else:
                self.title = title
        elif title:
            self.title = Text(text=title, type_=TextType.PLAINTEXT)
        else:
            self.title = Text(text=" ", type_=TextType.PLAINTEXT)

    def resolve(self) -> dict[str, Any]:
        image = self._attributes()
        image["image_url"] = self.image_url
        image["alt_text"] = self.alt_text

        if self.title:
            image["title"] = self.title.resolve()

        return image


class ActionsBlock(Block):
    """A block that is used to hold interactive elements."""

    def __init__(self, elements: list[Element] = None, block_id: str = None):
        super().__init__(type_=BlockType.ACTIONS, block_id=block_id)

        if isinstance(elements, Element):
            self.elements = [elements]
        elif (isinstance(elements, list) and all([isinstance(el, Element) for el in elements])):
            self.elements = elements

    def resolve(self):
        actions = self._attributes()
        actions["elements"] = [element.resolve() for element in self.elements]
        return actions


class ContextBlock(Block):
    """Displays message context, which can include both images and text."""

    def __init__(
        self,
        elements: list[Element] | Element = None,
        block_id: str = None
    ):
        super().__init__(type_=BlockType.CONTEXT, block_id=block_id)

        self.elements = []

        if not isinstance(elements, list):
            elements = [elements]

        for element in elements:
            if element.type == ElementType.TEXT or element.type == ElementType.IMAGE:
                self.elements.append(element)

    def resolve(self) -> dict[str, Any]:
        context = self._attributes()
        context["elements"] = [element.resolve() for element in self.elements]
        return context


class FileBlock(Block):
    """Displays a remote file."""

    def __init__(self, external_id: str, source: str, block_id: str):
        super().__init__(type_=BlockType.FILE, block_id=block_id)

        self.external_id = external_id
        self.source = source

    def resolve(self) -> dict[str, Any]:
        file = self._attributes()
        file["external_id"] = self.external_id
        file["source"] = self.source
        return file


class HeaderBlock(Block):
    """A header is a plain-text block that displays in a larger, bold font."""

    def __init__(self, text: str | Text, block_id: str = None):
        super().__init__(type_=BlockType.HEADER, block_id=block_id)

        if isinstance(text, Text):
            self.text = text
        else:
            self.text = Text(text, type_=TextType.PLAINTEXT, verbatim=False)

    def resolve(self) -> dict[str, Any]:
        header = self._attributes()
        header["text"] = self.text.resolve()
        return header
