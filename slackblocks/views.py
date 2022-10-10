from .blocks import Block
from .entry_with_mapping import EntryWithMapping


class HomeView(EntryWithMapping):
    """
    A home view object that is used to represent the bot's home tab.
    (https://api.slack.com/reference/surfaces/views)
    """

    def __init__(self, user_id: str, blocks: list[Block]):
        self.blocks = blocks
        self.user_id = user_id

    def resolve(self) -> dict[str, str | dict]:
        return {
            "user_id": self.user_id,
            "view": {
                "blocks": [block.resolve() for block in self.blocks],
                "type": "home"
            }
        }
