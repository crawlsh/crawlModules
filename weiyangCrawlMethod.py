# -*- coding:utf-8 -*-
from crawlMethods import baseCrawlMethod
from utils import crawlUtils
import re


class weiyangCrawlMethod(baseCrawlMethod.crawlMethod):
    NAME = "weiyang"
    DESCRIPTION = "爬取未央网"
    EXAMPLE_URL = "https://www.weiyangx.com/332784.html"
    USING = "Soup"
    REGEX_FINDING_NONCE = re.compile("nonce: \'(.+?)\'")
    REQUIREMENT = {
        "info": {
            "labels": ['author', 'time', 'title', 'tag', 'article'],  # Implement here!
            "isCrawlByIDAvailable": True,  # Implement here!
            "isCrawlByTimeAvailable": False,  # Implement here!
            "isCrawlByOrderAvailable": True,  # Implement here!
        }
    }

    @staticmethod
    def requestAPIForURL(amount):
        amount = float(amount)
        i = amount / 7
        j = amount // 7
        needPages = int(i) if i == j else int(i) + 1
        result = []
        homePage = crawlUtils.requestWithProxy("https://www.weiyangx.com")[0]
        nonce = weiyangCrawlMethod.REGEX_FINDING_NONCE.findall(homePage)[0]
        for i in range(1, 1 + needPages):
            APIURL = "https://www.weiyangx.com/wp-admin/admin-ajax.php"
            jsonData = crawlUtils.requestJsonWithProxy(APIURL, needCut=True,
                                                       method="post",
                                                       payload={"action": "home_load_more_news",
                                                                "postOffset": i * 8, "tagId": 0,
                                                                "_ajax_nonce": nonce})
            result += [x["url"] for x in jsonData["data"]]
        return result

    @staticmethod
    def generateLinks(userParamObj):
        urlTemplate = "https://www.weiyangx.com/%s.html"
        if userParamObj["crawlBy"] == "ORDER":
            return weiyangCrawlMethod.requestAPIForURL(int(userParamObj["info"]["amount"]))
        if userParamObj["crawlBy"] == "ID":
            result = [urlTemplate % i for i in range(
                int(userParamObj["info"]["idRangeStart"]),
                int(userParamObj["info"]["idRangeEnd"]))
                      ]
            return result
        return

    @staticmethod
    def generateRules(userParamObj):
        rulesObj = []

        if 'author' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'author', 'rule': ['p', {'class': 'uk-article-meta'}, 0]})

        if 'time' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'tag', 'rule': ['p', {'class': 'uk-article-meta'}, 1]})

        if 'title' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'title', 'rule': ['h1', {}, 0]})

        if 'tag' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'tag', 'rule': ['p', {'class': 'uk-article-meta'}, 2]})

        if 'article' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'article', 'rule': ['article', {}, 0]})

        return rulesObj

    @staticmethod
    def replaceSoup(soup):
        return soup
