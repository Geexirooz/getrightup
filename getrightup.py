from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from time import sleep  # this should go at the top of the file
from bs4 import BeautifulSoup
import json
import requests
import sys
import argparse

parser = argparse.ArgumentParser(
    "bountydog.py",
    formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=40),
)

parser.add_argument(
    "-d",
    "--discord",
    help="Discord's channel Webhook",
    dest="webhook",
    default=sys.maxsize,
    required=True,
    type=str,
)

args = parser.parse_args()


def get_pentesterland_rendered_source() -> str:
    # set headless browser option
    options = Options()
    options.add_argument("--headless")
    # Get the page
    browser = webdriver.Firefox(options=options)
    browser.get("https://pentester.land/writeups/")
    # wait until it's fully rendered
    sleep(5)
    # get the rendered source code via executing a javascript code
    src = browser.execute_script(
        "return document.getElementsByTagName('html')[0].innerHTML"
    )
    browser.close

    return src


def get_trs(src) -> list:
    trs = src.find("tbody")
    lst_os_writeups = []
    for tr in trs.children:
        writeup = tr.find("a").contents
        writeup.append(tr.find("a")["href"])
        lst_os_writeups.append(writeup)

    return lst_os_writeups


def discordit(msg: str, webhook: str) -> None:
    # Discord does not allow sending a message containing more than 2000 chars
    if len(msg) > 2000:
        num_of_chunks = len(msg) // 1900 + 1
        lst = msg.split("\n")
        sized_msg = ""
        for i in range(num_of_chunks):
            while len(sized_msg) <= 1900 and len(lst) > 0:
                sized_msg = sized_msg + lst.pop(0) + "\n"
            if len(lst) != 0:
                sized_msg = (
                    sized_msg
                    + "\n#########################\nTo Be Continued .......\n#########################\n"
                )
            data = {"content": sized_msg}
            requests.post(webhook, json=data)
    else:
        data = {"content": msg}
        requests.post(webhook, json=data)

    return


def getrightup():
    src = BeautifulSoup(get_pentesterland_rendered_source(), "html.parser")
    new_writeups = get_trs(src)

    with open("writeups.lst") as f:
        old_writeups = json.load(f)

    newly_released_writeups = [i for i in new_writeups if i not in old_writeups]

    # print(newly_released_writeups)
    # print(len(newly_released_writeups))
    # for i in newly_released_writeups:
    #    print(i)
    #    print(type(i))

    if newly_released_writeups:
        for writeup in newly_released_writeups:
            msg = "{:s}:\n{:s}\n".format(writeup[0], writeup[1])
            discordit(msg, args.webhook)

        with open("writeups.lst", "w") as f:
            json.dump(new_writeups, f)

    return


getrightup()
