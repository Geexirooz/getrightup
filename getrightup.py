from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from time import sleep  # this should go at the top of the file
from bs4 import BeautifulSoup

# Options set
options = Options()
options.add_argument("--headless")

# Get the page
browser = webdriver.Firefox(options=options)
browser.get("https://pentester.land/writeups/")

# wait until it's processed
sleep(5)

# get the rendered source code
src = browser.execute_script(
    "return document.getElementsByTagName('html')[0].innerHTML"
)


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
