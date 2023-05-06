from selenium import webdriver
from time import sleep  # this should go at the top of the file
import unicodedata
from bs4 import BeautifulSoup
import re

browser = webdriver.Firefox()
browser.get("https://pentester.land/writeups/")
sleep(5)
src = browser.execute_script(
    "return document.getElementsByTagName('html')[0].innerHTML"
)
# src = unicodedata.normalize("NFKD", src).encode("ascii", "ignore")

print(type(src))
soup = BeautifulSoup(src, "html.parser")
odd_trs = soup.find_all("tr", {"class": "odd"})
even_trs = soup.find_all("tr", {"class": "even"})
lst_of_writeups = []
for odd_tr in odd_trs:
    # The following gives a list
    writeup = odd_tr.find("a").contents
    # let's add the link to the list
    writeup.append(odd_tr.find("a")["href"])
    lst_of_writeups.append(writeup)


for even_tr in even_trs:
    writeup = even_tr.find("a").contents
    writeup.append(even_tr.find("a")["href"])
    lst_of_writeups.append(writeup)

print(len(lst_of_writeups))
