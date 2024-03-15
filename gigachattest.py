from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat

import config

# Авторизация в сервисе GigaChat
chat = GigaChat(credentials=config.AI_CREDENTIALS, verify_ssl_certs=False)

messages = [
    SystemMessage(
        content='Ты голосовой ассистент, тебе следует овечать кратко.'
    )
]

while True:
    # Ввод пользователя
    user_input = input('User: ')
    messages.append(HumanMessage(content=user_input))
    res = chat(messages)
    messages.append(res)
    # Ответ модели
    print('Bot: ', res.content)
