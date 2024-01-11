import numpy as np

from json_reader import Conversation


def len_none(iterable):
    return len(iterable) if iterable is not None else None


class ComputingConversation:
    def __init__(self, conversation: Conversation):
        self.title = conversation.title
        self.participants = np.array([p.name for p in conversation.participants])
        self.messages = np.array([[message.sender_name, message.timestamp_ms, message.content, len_none(message.photos), len_none(message.reactions)] for message in conversation.messages])

    def participants_all_messages_number(self):
        numbers = np.zeros((self.participants.size, ))
        for i in range(self.participants.size):
            numbers[i] = np.sum(self.messages[:, 0] == self.participants[i])
        return numbers

