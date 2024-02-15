import sys
import urllib3
import time
import random
from eth_account import Account
import threading

from loguru import logger
from config import PAUSE, PAUSE_RETRIES
from modules.check_status import CheckStatus
from modules.form import Form
from concurrent.futures import ThreadPoolExecutor
from utilities.common import read_files

file_lock = threading.Lock()


def configuration():
    urllib3.disable_warnings()
    logger.remove()
    logger.add(sys.stdout, colorize=True,
               format="<light-cyan>{time:HH:mm:ss}</light-cyan> | <level> {level: <8}</level> | - <white>{"
                      "message}</white>")


def append_to_file(file_path, string_to_append):
    with file_lock:
        with open(file_path, 'a') as file:
            file.write(string_to_append + '\n')


def remove_line_from_file(file_path, string_to_remove):
    with file_lock:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        with open(file_path, 'w') as file:
            for line in lines:
                if line.strip("\n") != string_to_remove:
                    file.write(line)


def check(index, key, proxy):
    login = CheckStatus(index, key, proxy)
    username = login.execute()
    if username == "Not robot":
        append_to_file("./data/success_accounts.txt", f"{key}:{proxy}:{username}")
    elif username:
        append_to_file("./data/robot_accounts.txt", f"{key}:{proxy}:{username}")
    else:
        append_to_file("./data/failed_accounts.txt", f"{key}:{proxy}:{username}")
    time.sleep(random.randint(PAUSE[0], PAUSE[1]))


def check_appeal(index, key, proxy, token, answer):
    login = CheckStatus(index, key, proxy)
    username = login.execute()
    account = Account.from_key(key)

    if username == "Not robot":
        append_to_file("./data/success_accounts.txt", f"{key}:{proxy}:{username}:{token}")
    elif username:
        form = Form(index, proxy, username, token, account.address, answer)
        ok, success = form.login()
        if success:
            append_to_file("./data/success_accounts.txt", f"{key}:{proxy}:{username}:{token}:{answer}")
            remove_line_from_file("data/proxies.txt", proxy)
            remove_line_from_file("data/discord_tokens.txt", token)
            remove_line_from_file("data/private_keys.txt", key)
            remove_line_from_file("data/appeal_text.txt", answer)

        else:
            append_to_file("./data/failed_accounts.txt", f"{key}:{proxy}:{username}:{token}:{answer}")
    else:
        append_to_file("./data/failed_accounts.txt", f"{key}:{proxy}:{username}:{token}:{answer}")
    time.sleep(random.randint(PAUSE[0], PAUSE[1]))


def check_if_form_is_working(form):
    ok, success = form.login()
    if success:
        logger.success("Form is working. Starting all accounts!")
        return "ok"
    else:
        return "form dead"


def main():
    configuration()
    private_keys, tokens, proxies, answers = read_files()

    print("Choose an option:")
    print("1. Run checker")
    print("2. Run checker + appeal")
    choice = int(input("Enter your choice: "))
    num_threads = int(input("Enter the number of threads: "))

    indexes = [index + 1 for index in range(len(private_keys))]

    if choice == 1:
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            executor.map(check, indexes, private_keys, proxies)

    elif choice == 2:
        login = CheckStatus(1, private_keys[0], proxies[0])
        username = login.execute()
        account = Account.from_key(private_keys[0])

        if username == "Not robot":
            logger.info("Account is not a robot. Please paste another account.")
            return "not robot"

        elif username:
            while True:
                form = Form(1, proxies[0], username, tokens[0], account.address, answers[0])
                ok = check_if_form_is_working(form)
                if ok == "ok":
                    break
                
                elif ok == "form dead":
                    time.sleep(random.randint(PAUSE_RETRIES[0], PAUSE_RETRIES[1]))
                    continue

                else:
                    return

        else:
            logger.info("Account is not working. Please paste another account.")
            return "not working"

        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            executor.map(check_appeal, indexes, private_keys, proxies, tokens, answers)


if __name__ == "__main__":
    main()
