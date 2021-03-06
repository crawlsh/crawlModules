# -*- coding:utf-8 -*-
from crawlMethods import baseCrawlMethod
from utils import crawlUtils
import re


class nbdCrawlMethod(baseCrawlMethod.crawlMethod):
    NAME = "nbd"
    DESCRIPTION = "爬取每经网"
    EXAMPLE_URL = "http://www.nbd.com.cn/articles/2019-06-22/1346011.html"
    USING = "Soup"
    GET_LA_REGEX = re.compile("http://finance\.nbd\.com\.cn/columns/119\?last_article=(.+?)&")
    EXTRACT_LINKS_REGEX = re.compile("href=\\\"http://www\.nbd\.com\.cn/articles/(.+?)\.html\\\" ")
    REQUIREMENT = {
        "info": {
            "labels": ['author', 'title', 'time', 'tag', 'article'],  # Implement here!
            "isCrawlByIDAvailable": False,  # Implement here!
            "isCrawlByTimeAvailable": False,  # Implement here!
            "isCrawlByOrderAvailable": True,  # Implement here!
        }
    }

    @staticmethod
    def requestAPIForURL(amount):
        html = crawlUtils.crawlWorker("http://finance.nbd.com.cn/", "Anon", 0)[0]
        lastArticleID = nbdCrawlMethod.GET_LA_REGEX.findall(html)[0]
        amount = float(amount)
        i = amount / 30
        j = amount // 30
        needPages = int(i) if i == j else int(i) + 1
        result = []
        for i in range(1, 1 + needPages):
            try:
                url = "http://finance.nbd.com.cn/columns/119?last_article=%s" % lastArticleID
                APIHTML = crawlUtils.crawlWorker(url, "Anon", 0)[0]
                links = ["http://www.nbd.com.cn/articles/%s.html" % x
                         for x in nbdCrawlMethod.EXTRACT_LINKS_REGEX.findall(APIHTML)]
                lastArticleID = nbdCrawlMethod.GET_LA_REGEX.findall(APIHTML)[0]
                result += links
            except:
                pass
        return result

    @staticmethod
    def generateLinks(userParamObj):
        if userParamObj["crawlBy"] == "ORDER":
            return nbdCrawlMethod.requestAPIForURL(int(userParamObj["info"]["amount"]))
        return

    @staticmethod
    def generateRules(userParamObj):
        rulesObj = []

        if 'author' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'author', 'rule': ['span', {'class': 'source'}, 0]})

        if 'time' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'tag', 'rule': ['span', {'class': 'time'}, 0]})

        if 'tag' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'tag', 'rule': ['div', {'class': 'u-aticle-tag'}, 0]})

        if 'title' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'title', 'rule': ['h1', {}, 0]})

        if 'article' in userParamObj["info"]["requiredContent"]:
            rulesObj.append({'name': 'article', 'rule': ['div', {'class': 'g-articl-text'}, 0]})

        return rulesObj

    @staticmethod
    def replaceSoup(soup):
        return soup
