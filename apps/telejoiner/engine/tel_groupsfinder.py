from bs4 import BeautifulSoup
import requests, cssutils, logging, re
from config.source import ServerConfig

cssutils.log.setLevel(logging.CRITICAL)


class GroupsFinder:
    def __init__(self, data) -> None:
        self.query = data.get("query")
        self.username = data.get("username")

    def demojify(self, text: str) -> str:
        return re.sub("[^A-Za-z0-9]+", " ", text).title()

    def getimageURL(self, iconcontainer):
        style = cssutils.parseStyle(iconcontainer)['background-image']
        iconurl = style.replace('url(', '').replace(')', '')
        return iconurl if iconurl.startswith("http") else f"https://tdirectory.me{iconurl}"

    def getGroups(self):
        scrappedTelegramGroups = []
        data = requests.get(f"https://tdirectory.me/search/{self.query}")
        soup = BeautifulSoup(data.text, features="html.parser")
        groupsContainer = soup.find("div", {"id": "groups"})
        groupsRowContainer = groupsContainer.find("div", {"class": "row"})
        groupCards = groupsRowContainer.find("div", {"class": "search-wrapper2 text-center"})
        groups = groupCards.findAll("div", {"class": "col-md-3 col-sm-6 col-xs-12"})
        for group in groups:
            title = self.demojify(group.find("a").get("title"))
            icon = self.getimageURL(group.find("i").get("style"))
            members = group.find("p").getText().replace("\n", "")
            link = group.find('a').get('href').replace("/group/", "")
            scrappedTelegramGroups.append({"link": link, "title": title, "members": members, "icon": icon})
        print("========== Groups Send ==========")
        ServerConfig.sendevent( self.username,"foundgroups", scrappedTelegramGroups)

    def getGroupLink(self):
        data = requests.get(f"https://tdirectory.me/gogroup/{self.query}")
        soup = BeautifulSoup(data.text, features="html.parser")
        telegramButton = soup.find("a", {"class": "tgme_action_button_new"}).get("href")
        return f"https://telegram.me/{telegramButton.split('?domain=')[1]}"