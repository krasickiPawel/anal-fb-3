import os
import datetime
import paths
import settings
import numpy as np
import re
from zipfile import ZipFile

from computing import ComputingConversation
from json_reader import Conversation


if __name__ != '__main__':
    raise ImportError('importing from the main module is prohibited')


zip_file_path = paths.ZIP_PATH
pattern = re.compile(r"(3[01]|[12][0-9]|0[1-9]).(1[0-2]|0[1-9]).([0-9][0-9][0-9][0-9])")
zip_date = pattern.search(zip_file_path).group()
current_time_dir = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

if not os.path.exists(os.path.join(settings.OUTPUT_DIR, zip_date, f"{current_time_dir}_results")):
    os.makedirs(os.path.join(settings.OUTPUT_DIR, zip_date, f"{current_time_dir}_results"))


with ZipFile(zip_file_path, "r") as zip_file:
    jsons_paths = [path for path in zip_file.namelist() if path.startswith(settings.INBOX_DIR) and path.endswith('.json')]
    conversation_dirs = list(np.unique([os.path.split(os.path.split(path)[0])[1] for path in jsons_paths]))

    for conversation_dir in conversation_dirs:
        conversation_jsons_paths = [path for path in jsons_paths if conversation_dir in path]
        conversation_json_datas = []

        for conversation_jsons_path in conversation_jsons_paths:
            with zip_file.open(conversation_jsons_path) as f:
                conversation_data = Conversation.from_dict(f.read())
                conversation_json_datas.append(conversation_data)

        all_messages = []
        for conversation_json_data in conversation_json_datas:
            all_messages += conversation_json_data.messages

        conversation = Conversation(
            conversation_json_datas[0].title,
            conversation_json_datas[0].participants,
            all_messages
        ).convert_to_utf8()

        computing_conversation = ComputingConversation(conversation)
        numbers = computing_conversation.participants_all_messages_number()
        print(computing_conversation.participants, numbers)
        scores = np.array((len(conversation_dirs), len(conversation.participants), len(settings.AVAILABLE_CATEGORIES)))

        print()
        print(conversation.title)
        print(conversation.participants)
        print(len(conversation.messages))
        print(conversation.messages)
        exit()

