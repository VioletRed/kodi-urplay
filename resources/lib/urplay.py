# -*- coding: utf-8 -*-
import urllib
import re

import helper
import CommonFunctions as common
from resources.lib.helper import convertChar

URPLAY_BASE_URL = "http://urplay.se"
UR_BASE_URL = "http://ur.se"


URL_A_TO_O = URPLAY_BASE_URL + "/sok?rows=999"
URL_TO_SEARCH = UR_BASE_URL + "/Produkter?q="
URL_TO_INSPIRATION = UR_BASE_URL + "/Inspiration"
URL_TO_LAST_CHANCE = URPLAY_BASE_URL + "/Sista-chansen"
URL_TO_LATEST = URPLAY_BASE_URL + "/Senaste"
URL_TO_PLAYED = URPLAY_BASE_URL + "/Mest-spelade"
URL_TO_SHARED = URPLAY_BASE_URL + "/Mest-delade"

JSON_SUFFIX = "?output=json"

SECTION_POPULAR = "popular-videos"
SECTION_LATEST_VIDEOS = "latest-videos"
SECTION_LAST_CHANCE = "last-chance-videos"
SECTION_UR_EPISODES = "product-puff"
SECTION_URPLAY_EPISODES = "tv|radio"
SECTION_LIVE_PROGRAMS = "live-channels"

CLASS_UR_EPISODES = "puff (?:tv|radio) (?:video|audio)"
CLASS_URPLAY_EPISODES = "tv|radio"
CONTAINER_UR_EPISODES = "selected|result-list"
CONTAINER_URPLAY_EPISODES = "scroll-x"

SEARCH_LIST_TITLES = "[^\"']*playJs-search-titles[^\"']*"
SEARCH_LIST_EPISODES = "[^\"']*playJs-search-episodes[^\"']*"

def getAtoOProducts(container, letter=""):

    lis = common.parseDOM(container, "li", attrs={"class":"series" })
    if not lis:
        helper.errorMsg("No items found for letter '" + letter + "'")
        return None

    programs = []

    for li in lis:
        program = parseURPlayArticle(li)
        programs.append(program)

    return programs


def getAtoO():
    """
    Returns a list of all programs, sorted A-Z.
    """
    html = helper.getPage(URL_A_TO_O)
    container = common.parseDOM(html, "div", attrs={"id":"all-series"})
    return getAtoOProducts(container)


def getCategories():
    """
    Hardcoded list of categories.
    """
    urls = [ "/Dokumentar",
            "/Forelasningar-debatt",
            "/Vetenskap",
            "/Kultur-historia",
            "/Samhalle",
            "/Sprak",
            "/Barn" ]
    categoryNames = ["Dokumentär",
                     "Föreläsningar och debatt",
                     "Vetenskap",
                     "Kultur och historia",
                     "Samhälle",
                     "Språk"]

    categories = []
    for index, categoryName in enumerate(categoryNames):
        category = {}
        category["url"] = URPLAY_BASE_URL + urls[index]
        category["title"] = categoryName
        categories.append(category)

    return categories


def getSubjects():
    """
    Returns a list of all categories.
    """
    html = helper.getPage(UR_BASE_URL)

    container = common.parseDOM(html, "nav", attrs={ "id": "Huvudmeny-amnen" })
    if not container:
        helper.errorMsg("Could not find container")
        return None
    container = container[0]
    # print container.encode("utf-8","ignore")
    groups = common.parseDOM(container, "ul")
    allArticles = []
    allURL = []
    for group in groups[1:]: # First group is always "Inspiration"
        #print "**************"
        #print group.encode("utf-8","ignore")
        #print "**************"
        articles = common.parseDOM(group, "a", attrs={"href": "./"})
        articlesURL = common.parseDOM(group, "a", attrs={"href": "./"}, ret="href")
        if not articles:
            continue
        articles[0] = "[B]" + articles[0] + "[/B]"
        if len(articles) > 1:
            articles[1:] = map(lambda i: "   " + i, articles[1:])
        allArticles.extend(articles)
        allURL.extend(articlesURL)

    categories = []
    for index, article in enumerate(allArticles):
        category = {}
        category["url"] = UR_BASE_URL + allURL[index]

        category["title"] = common.replaceHTMLCodes(article)
        categories.append(category)

    return categories


def getProgramsForCategory(url):
    """
    Returns a list of programs for a specific category URL.
    """
    html = helper.getPage(url)

    container = common.parseDOM(html, "div", attrs={ "id" : "[^\"']*playJs-alphabetic-list[^\"']*" })

    if not container:
        helper.errorMsg("Could not find container for URL " + url)
        return None

    articles = common.parseDOM(container, "article", attrs={ "class" : "[^\"']*play_videolist-element[^\"']*" })

    if not articles:
        helper.errorMsg("Could not find program links for URL " + url)
        return None

    programs = []
    for article in articles:
        url = common.parseDOM(article, "a", ret="href")[0]
        title = common.parseDOM(article, "span", attrs={ "class" : "play_videolist-element__title-text" })[0]
        title = common.replaceHTMLCodes(title)
        thumbnail = common.parseDOM(article, "img", ret="src")[0]
        program = { "title": title, "url": url, "thumbnail": thumbnail}
        programs.append(program)

    return programs


def getAlphas():
    """
    Returns a list of all letters in the alphabet that has programs.
    """
    html = helper.getPage(URL_A_TO_O)
    container = common.parseDOM(html, "div", attrs={ "class" : "anchor-menu" })

    if not container:
        helper.errorMsg("No container found!")
        return None

    letters = common.parseDOM(container[0], "a", attrs={ "data-key" : "." })

    if not letters:
        helper.errorMsg("Could not find any letters!")
        return None

    alphas = []

    for letter in letters:
        alpha = {}
        alpha["title"] = letter.encode('utf-8', 'ignore')
        alpha["char"] = letter.encode('utf-8', 'ignore')
        alphas.append(alpha)

    return alphas


def getProgramsByLetter(letter):
    """
    Returns a list of all program starting with the supplied letter.
    """
    letter = convertChar(urllib.unquote(letter))

    html = helper.getPage(URL_A_TO_O)

    res = re.search("<a id=\"%s\">" % letter, html)
    if not res:
        helper.errorMsg("No containers found for letter '%s'" % letter)
        return None

    letterbox = common.parseDOM(html[res.start():], "ul", attrs={ })
    letterbox = letterbox[0]
    if not letterbox:
        helper.errorMsg("No containers found for letter '%s'" % letter)
        return None

    return getAtoOProducts(letterbox, letter)

def getSearchResults(url):
    """
    Returns a list of both clips and programs
    for the supplied search URL.
    """
    results = getArticles(url, parseURPlayArticle, 50)
    return results


def getSearchResultsForList(html, list_id):
    """
    Returns the items in the supplied list.
   
    Lists are the containers on a program page that contains clips or programs.
    """
    container = common.parseDOM(html, "div", attrs={ "id" : list_id })
    if not container:
        helper.errorMsg("No container found for list ID '" + list_id + "'")
        return None

    articles = common.parseDOM(container, "article")
    if not articles:
        helper.errorMsg("No articles found for list ID '" + list_id + "'")
        return None

    titles = common.parseDOM(container, "article", ret="data-title")

    results = []
    for index, article in enumerate(articles):
        thumbnail = common.parseDOM(article, "img", attrs={ "class" : "[^\"']*play_videolist-element__thumbnail-image[^\"']*" }, ret="src")[0]
        url = common.parseDOM(article, "a", ret="href")[0]
        title = common.replaceHTMLCodes(titles[index])
        thumbnail = helper.prepareThumb(thumbnail, baseUrl=URPLAY_BASE_URL)

        item_type = "video"
        if list_id == SEARCH_LIST_TITLES:
            item_type = "program"
        results.append({"item": { "title" : title, "thumbnail" : thumbnail, "url" : url  }, "type" : item_type })

    return results

def getChannels():
    """
    Returns the live channels from the page "Kanaler".
    """
    anchor_class = "[^\"']*play_zapper__menu-item-link[^\"']*"
    html = helper.getPage("")

    container = common.parseDOM(html, "ul", attrs={ "data-play_tabarea" : "ta-schedule"})
    if not container:
        helper.errorMsg("No container found for channels")
        return None

    channels = []
    ch_boxes = common.parseDOM(container, "li")
    for box in ch_boxes:
        title = common.parseDOM(box, "a", attrs={"class" : anchor_class}, ret="data-channel")[0]
        url = common.parseDOM(box, "a", attrs={"class" : anchor_class}, ret="href")[0]
        plot = common.parseDOM(box, "span", attrs={"class" : "[^\"']*play_zapper__menu-item-title[^\"']*"})[0]
        thumbnail = URPLAY_BASE_URL + common.parseDOM(box, "a", attrs={"class" : anchor_class}, ret="data-thumbnail")[0]
        channels.append({
          "title" : title,
          "url" : url,
          "thumbnail" : thumbnail,
          "info" : { "title" : plot, "plot" : plot}
        })

    return channels

def getPopular():
    """
    Returns the 'popular' items.
    """
    pass

def getLatestVideos():
    """
    Returns the latest videos.
    """
    pass

def getLastChance():
    """
    Returns the 'last chance' videos
    """
    pass

def getLivePrograms():
    """
    Returns the 'live' channels (differs from 'channels')
    """
    pass

def getEpisodes(url):
    """
    Returns the episodes for a program URL.
    """
    # print "Episodes for " + url
    if not url:
        url = URPLAY_BASE_URL
    return getArticles(url, parseURPlayArticle )


def parseURPlayArticle(article):
    
    info = {}
    new_article = {}
    title = common.parseDOM(article, "h3")
    if len(title) >= 1:
        title = common.replaceHTMLCodes(title[0])
        info["title"] = title
    plot = common.parseDOM(article, "p", attrs={"class":"description"})
    if len(plot) >= 1:
        plot = common.replaceHTMLCodes(plot[0])
        info["plot"] = plot
    duration = common.parseDOM(article, "dd")
    if len(duration) >= 1:
        info["duration"] = helper.convertDuration(duration[0])
    thumbnail = common.parseDOM(article, "img", ret="src")
    if len(thumbnail) >= 1:
        new_article["thumbnail"] = thumbnail[0]
        info["fanart"] = thumbnail[0].replace("_t.jpg","_l.jpg")

    new_url = common.parseDOM(article, "a", ret="href")
    # print new_url
    if (new_url is None) or (len(new_url) < 1): return []
    new_article["url"] = UR_BASE_URL + new_url[0]
    new_article["title"] = title.encode("utf-8", "ignore")
    new_article["info"] = info

    return new_article


def getArticles(url, parse_article, max_articles=200):
    """
    Returns a list of the articles in a section as program items.

    Program items have 'title', 'thumbnail', 'url' and 'info' keys.
    """
    if not url:
        return None

    html = helper.getPage(url)

    containers = common.parseDOM(html, "div", attrs={ "id" : "scroller", "class" : "scroll-x" })
    if not containers:
        helper.errorMsg("No container found for episodes!")
        return None
    
    articles = []
    for container in containers:
        container_articles = common.parseDOM(container, "li", attrs={ })
        if len(container_articles) > 0: articles.extend(container_articles)

    if not articles:
        helper.errorMsg("No articles found for section 'episodes' !")
        return None
    
    new_articles = []
    print articles
    for article in articles:
        new_articles.append(parse_article(article))
    if len(new_articles) > max_articles:
        new_articles[:-max_articles] = []

    return new_articles


