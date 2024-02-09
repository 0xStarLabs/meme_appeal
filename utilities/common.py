import random
import requests
from pyuseragents import random as random_useragent


def read_files():
    with open("./data/private_keys.txt") as file:
        private_keys = [line.strip() for line in file if line.strip()]

    with open("./data/proxies.txt") as file:
        proxies = [line.strip() for line in file if line.strip()]

    with open("./data/discord_tokens.txt") as file:
        tokens = [line.strip() for line in file if line.strip()]

    with open("./data/appeal_text.txt") as file:
        answers = [line.strip() for line in file if line.strip()]

    while len(proxies) < len(private_keys):
        proxies.append(random.choice(proxies))

    return private_keys, tokens, proxies, answers

def create_client(proxy: str) -> requests.Session:
    session = requests.Session()

    if proxy:
        session.proxies.update({
            "http": "http://" + proxy,
            "https": "http://" + proxy,
        })

    session.headers.update({
        'authority': 'memefarm-api.memecoin.org',
        'accept': 'application/json',
        'accept-language': 'uk',
        'origin': 'https://www.memecoin.org',
        'user-agent': random_useragent()
    })

    return session