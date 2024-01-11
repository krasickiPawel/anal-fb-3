import numpy as np
from msgspec import Struct
from msgspec.json import decode
from typing import Optional
from encoding import convert_to_utf8


class Participant(Struct):
    name: str


class Photo(Struct):
    uri: str


class Reaction(Struct):
    reaction: str
    actor: str


class Share(Struct):
    link: str
    share_text: Optional[str] = None


class Message(Struct):
    sender_name: str
    timestamp_ms: int
    content: Optional[str] = None
    photos: Optional[list[Photo]] = None
    reactions: Optional[list[Reaction]] = None
    share: Optional[Share] = None


class Conversation(Struct):
    title: str
    participants: list[Participant]
    messages: list[Message]

    @classmethod
    def from_dict(cls, file_content):
        return decode(file_content, type=Conversation)

    def convert_to_utf8(self):
        self.title = convert_to_utf8(self.title)
        for participant in self.participants:
            participant.name = convert_to_utf8(participant.name)

        for message in self.messages:
            message.content = convert_to_utf8(message.content) if message.content is not None else None
            message.sender_name = convert_to_utf8(message.sender_name)
            if message.share is not None:
                message.share.share_text = convert_to_utf8(message.share.share_text) if message.share.share_text is not None else None
            if message.reactions:
                for reaction in message.reactions:
                    reaction.reaction = convert_to_utf8(reaction.reaction)
                    reaction.actor = convert_to_utf8(reaction.actor)

        return self
