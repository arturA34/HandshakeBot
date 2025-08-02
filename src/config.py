from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str


@dataclass
class Config:
    tgbot: TgBot

def load_conf(path=None):
    env = Env()
    env.read_env(path=path)
    return Config(tgbot=TgBot(token=env('BOT_TOKEN')))

print('Конфигурация прошла успешно, бот запущен!')