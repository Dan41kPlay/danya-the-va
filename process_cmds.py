from datetime import datetime
from random import choice

from fuzzywuzzy import fuzz
from num2t4ru import num2text
from langchain.schema import HumanMessage, SystemMessage, BaseMessage
from langchain.chat_models.gigachat import GigaChat

import config
import stt


print(f'{config.VA_NAME} (v{config.VA_VER}) начал свою работу...')

chat = GigaChat(credentials=config.AI_CREDENTIALS, verify_ssl_certs=False)

messages: list[BaseMessage] = [
    SystemMessage(
        content='Ты голосовой ассистент, овечай очень кратко.'
    )
]


def va_respond(voice: str, is_auto: bool) -> str:
    if voice:
        print(voice)
    return '' if not voice.startswith(config.VA_ALIAS) and is_auto else execute_cmd(recognize_cmd(filter_cmd(voice)))


def filter_cmd(raw_voice: str) -> str:
    for word in config.VA_ALIAS + config.VA_TBR:
        raw_voice = raw_voice.replace(word, '').strip()
    return raw_voice


def recognize_cmd(cmd: str) -> str:
    recognized_cmd = {'command': '', 'percent': 0}
    for command, ways_to_say in config.VA_CMDS.items():
        for way_to_say in ways_to_say:
            possibility = fuzz.ratio(cmd[1:], way_to_say)
            if possibility > recognized_cmd['percent']:
                recognized_cmd |= {'command': command, 'percent': possibility}
    return recognized_cmd['command'] if recognized_cmd['percent'] > 70 else cmd


def execute_cmd(cmd: str) -> str:
    match cmd:
        case 'hi':
            return 'Привет! Рад вас снова видеть!'
        case 'bye':
            return 'Пока! До скорой встречи...'
        case 'dela':
            return 'Пока всё отлично!'
        case 'thanks':
            return 'Всегда пожалуйста!'
        case 'current_time':
            now = datetime.now()
            return f'Сейчас {num2text(now.hour)} {'ноль ' if now.minute < 10 else ''}{num2text(now.minute)}.'
        case 'joke':
            return choice(config.JOKES)
        case _:
            if not cmd:
                return 'Что?'
            cmd = ' '.join(num2text(int(word)) if word.isdigit() else word for word in cmd.split(' '))
            messages.append(HumanMessage(content=cmd))
            res = chat(messages)
            messages.append(res)
            return res.content
            # result = cmd if cmd not in {*config.VA_METHODS_TO_ATTRS} else ('!' if car[config.VA_METHODS_TO_ATTRS[cmd]] else '') + cmd
            # print(f'{result=}')
            # eval(f'car.{cmd.strip("!")}()')
            # return config.VA_ATOM_ANSWERS[result] if result else 'Что?'


if __name__ == '__main__':
    for phrase in stt.va_listen():
        va_respond(phrase, False)
