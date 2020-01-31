import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.expected_conditions import url_changes
from selenium.webdriver.support.wait import WebDriverWait

user_id = "iamaaroncarmen"
pword = "camino1559"

driver = webdriver.Chrome(executable_path="/Users/aarongrycner/Downloads/chromedriver")
url = "https://twitter.com/ItsBennyBlanco?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor"

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

userlist = []

# this code determines whether we are scraping instagram or twitter and handles which piece of HTML to use.
# it also sets the variable 'currentSite' to indicate which site we are scraping for later use.
if "instagram" in url:
    currentSite = "instagram"
elif "twitter" in url:
    searchHtml = soup.find_all("p", class_="ProfileHeaderCard-bio u-dir")
    currentSite = "twitter"
else:
    print("instagram or twitter links only please")

# function to find the email in the bio section of the instagram page and append it to a text file
def findemail(htmltext):
    emailchars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz."
    htmltext = str(htmltext)
    print(htmltext)
    if "@" in htmltext:
        atsignindex = htmltext.find("@")
        email = ""
        i = 0
        while i == 0:
            email = email + htmltext[atsignindex]
            atsignindex = atsignindex + 1
            if htmltext[atsignindex] not in emailchars:
                i = 1
        atsignindex = htmltext.find("@") - 1
        if htmltext[atsignindex] not in emailchars:
            return
        while i == 1:
            email = htmltext[atsignindex] + email
            atsignindex = atsignindex - 1
            if htmltext[atsignindex] not in emailchars:
                i = 2
    else:
        return


    f = open('emails.txt', 'a')
    f.write(str(user) + '\n')
    f.write(str(email) + '\n')
    f.write(str("") + '\n')
    f.close()


def getfollowersinsta():
    driver.implicitly_wait(10)
    driver.get("https://www.instagram.com/accounts/login/?source=auth_switcher")

    # enter login info
    element = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/article/div/div[1]/div/form/div[2]/div/label/input")
    element.send_keys(user_id)
    element = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/article/div/div[1]/div/form/div[3]/div/label/input")
    element.send_keys(pword)

    # clicks login button
    element = driver.find_element_by_xpath(("/html/body/div[1]/section/main/div/article/div/div[1]/div/form/div[4]/button"))
    element.click()

    # clicks away notification
    element = driver.find_element_by_xpath("/html/body/div[4]/div/div/div[3]/button[2]")
    element.click()

    # navigates to inputted page and waits for load
    driver.get(url)
    time.sleep(3)

    # find followers page
    driver.find_element_by_partial_link_text("following").click()

    # after click follower link, wait until dialog appear
    WebDriverWait(driver, 10).until(lambda d: d.find_element_by_css_selector('div[role="dialog"]'))

    # scroll to bottom of followers list
    soup.find("span", class_="g47SY lOXF2")
    i = 1
    z = 1
    while i == 1:
        z = z + 1
        driver.execute_script(
            '''var fDialog = document.querySelector('div[role="dialog"] .isgrP');
            fDialog.scrollTop = fDialog.scrollHeight'''
        )
        if z == 1000:
            i = 2

    # create list of followers to click through
    html2 = driver.page_source
    soup2 = BeautifulSoup(html2, "html.parser")
    linkstring = soup2.findAll("a", class_="FPmhX notranslate _0imsa")
    linkstring = str(linkstring)
    i = 0
    x = 0

    # iterates through the raw html string slicing usernames to a userlist
    while i == 0:
        link = ""
        linkindex = linkstring.find("href") + 7
        slashindex = linkstring.find("/", linkindex)
        link = linkstring[linkindex:slashindex]
        userlist.append(link)
        linkstring = linkstring[slashindex:]
        if "href" not in linkstring:
            i = 1
    print(userlist)


def getfollowerstwitter():
    driver.implicitly_wait(100)
    driver.get("https://twitter.com/login")
    # enter login info
    try:
        driver.find_element_by_xpath("/html/body/div/div/div/div[1]/main/div/div/form/div/div[1]/label/div[2]/div/input"
                                     ).send_keys(user_id)
        driver.find_element_by_xpath("/html/body/div/div/div/div[1]/main/div/div/form/div/div[2]/label/div[2]/div/input"
                                     ).send_keys(pword)
        # click login
        driver.find_element_by_xpath("/html/body/div/div/div/div[1]/main/div/div/form/div/div[3]/div/div").click()
    except:
        driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/div[1]/form/fieldset/div[1]/input"
                                     ).send_keys(user_id)
        driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/div[1]/form/fieldset/div[2]/input"
                                     ).send_keys(pword)
        # click login
        driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/div[1]/form/div[2]/button").click()
    # navigate to inputted page
    driver.get(url)

    # click following link
    driver.find_element_by_xpath(
        "/html/body/div/div/div/div/main/div/div/div/div/div/div[2]/div/div/div[1]/div/div[5]/div[1]/a"
    ).click()

    linkstring = ""

    SCROLL_PAUSE_TIME = 0.5
    WebDriverWait(driver, timeout=1000).until(url_changes)
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # get follower list
        html4 = driver.page_source
        soup4 = BeautifulSoup(html4, "html.parser")
        links = soup4.findAll("span", class_="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0")
        linkstring = str(linkstring) + str(links)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # creates list of usernames from slices of linkstring
    while True:
        link = ""
        atsignindex = linkstring.find("@")
        if "@" not in linkstring:
            break
        elif str(linkstring[atsignindex - 1]).isalpha():
            userlist.append(link)
        else:
            linkstring = linkstring[atsignindex:]
    print("LINKSTRING = " + linkstring)
    print(userlist)


if currentSite == "instagram":
    getfollowersinsta()
    for user in userlist:
        driver.get("https://www.instagram.com/" + user + "/")
        html4 = driver.page_source
        soup4 = BeautifulSoup(html4, "html.parser")
        searchHtml = soup4.find_all("div", class_="-vDIg")
        findemail(searchHtml)
elif currentSite == "twitter":
    getfollowerstwitter()



