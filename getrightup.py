from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from time import sleep
from bs4 import BeautifulSoup
import json
import requests
import sys
import argparse


class col:
    """
    A class to define colors for a nice output printing
    """

    if sys.stdout.isatty():
        green = "\033[32m"
        blue = "\033[94m"
        red = "\033[31m"
        end = "\033[0m"
    else:  # Colours mess up redirected output, disable them
        green = ""
        blue = ""
        red = ""
        end = ""


# get command line args
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
    """
    This function returns html source of the Pentesterlab page after executing all Javascript files.
    """
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
    """
    This function returns a list of all writeups in the first page as a list of their titles and links within
    an embedded list.
    """
    trs = src.find("tbody")
    lst_os_writeups = []
    for tr in trs.children:
        writeup = tr.find("a").contents
        writeup.append(tr.find("a")["href"])
        lst_os_writeups.append(writeup)

    return lst_os_writeups


def discordit(msg: str, webhook: str) -> None:
    """
    This function sends a message to the desired Discord channel.
    """
    data = {"content": msg}
    requests.post(webhook, json=data)

    return None


def getrightup() -> None:
    """
    This function is the main function.
    It parses the page source and get the differences between new writeups list and the one which has been
    derived via the previous run.
    """
    src = BeautifulSoup(get_pentesterland_rendered_source(), "html.parser")
    new_writeups = get_trs(src)
    try:
        with open("writeups.lst") as f:
            old_writeups = json.load(f)

        newly_released_writeups = [i for i in new_writeups if i not in old_writeups]

        if newly_released_writeups:
            for writeup in newly_released_writeups:
                msg = "{:s}:\n{:s}\n".format(writeup[0], writeup[1])
                discordit(msg, args.webhook)

            with open("writeups.lst", "w") as f:
                json.dump(new_writeups, f)
    except json.decoder.JSONDecodeError:
        with open("writeups.lst") as f:
            if f.read() != "":
                print(
                    "{:s}Error occured while reading from writeups.lst (bad data format){:s}".format(
                        col.red, col.end
                    )
                )
                print(
                    "{:s}overwriting the file with new data ...{:s}".format(
                        col.blue, col.end
                    )
                )
                with open("writeups.lst", "w") as f:
                    json.dump(new_writeups, f)
    except FileNotFoundError:
        with open("writeups.lst", "w+") as f:
            json.dump(new_writeups, f)
        print(
            "{:s}You will get notification on your Discord channel from next run!{:s}".format(
                col.green, col.end
            )
        )

    return None


def main() -> None:
    getrightup()

    return None


if __name__ == "__main__":
    main()
