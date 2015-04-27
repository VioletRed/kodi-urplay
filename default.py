# -*- coding: utf-8 -*-
import re
import json
import sys
import time
import urllib
import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin
import CommonFunctions as common
import resources.lib.helper as helper
import resources.lib.urplay as ur
import resources.lib.PlaylistManager as PlaylistManager
import resources.lib.FavoritesManager as FavoritesManager
from resources.lib.PlaylistDialog import PlaylistDialog

MODE_A_TO_O = "a-o"
MODE_PROGRAM = "pr"
MODE_KIDS = "kids"
MODE_INSPIRATION = "inspiration"
MODE_VIDEO = "video"
MODE_CATEGORIES = "categories"
MODE_SUBJECTS = "subjects"
MODE_LETTER = "letter"
MODE_SEARCH = "search"
MODE_VIEW_TITLES = "view_titles"
MODE_VIEW_EPISODES = "view_episodes"
MODE_PLAYLIST_MANAGER = "playlist-manager"
MODE_FAVORITES = "favorites"

S_DEBUG = "debug"
S_HIDE_SIGN_LANGUAGE = "hidesignlanguage"
S_SHOW_SUBTITLES = "showsubtitles"
S_USE_ALPHA_CATEGORIES = "alpha"

PLUGIN_HANDLE = int(sys.argv[1])

addon = xbmcaddon.Addon("plugin.video.urplay")
localize = addon.getLocalizedString
xbmcplugin.setContent(PLUGIN_HANDLE, "tvshows")

common.plugin = addon.getAddonInfo('name') + ' ' + addon.getAddonInfo('version')
common.dbg = helper.getSetting(S_DEBUG)


def viewStart():

    #addDirectoryItem(localize(30012), { "mode": MODE_INSPIRATION })
    addDirectoryItem(localize(30013), { "mode": MODE_SUBJECTS })
    addDirectoryItem(localize(30001), { "mode": MODE_CATEGORIES })
    addDirectoryItem(localize(30010), { "mode": MODE_PROGRAM, "url": ur.URL_TO_PLAYED })
    addDirectoryItem(localize(30011), { "mode": MODE_PROGRAM, "url": ur.URL_TO_SHARED })
    addDirectoryItem(localize(30003), { "mode": MODE_PROGRAM, "url": ur.URL_TO_LATEST })
    addDirectoryItem(localize(30009), { "mode": MODE_PROGRAM, "url": ur.URL_TO_LAST_CHANCE })
    #addDirectoryItem(localize(30002), { "mode": MODE_KIDS })
    addDirectoryItem(localize(30000), { "mode": MODE_A_TO_O })
    addDirectoryItem(localize(30006), { "mode": MODE_SEARCH })
    #addDirectoryItem(localize(30405), { "mode": MODE_FAVORITES })
    #addDirectoryItem(localize(30400), { "mode": MODE_PLAYLIST_MANAGER }, folder=False)

def viewFavorites():
    favorites = FavoritesManager.get_all()

    for item in favorites:
        list_item = xbmcgui.ListItem(item["title"])
        fm_script = "special://home/addons/plugin.video.urplay/resources/lib/FavoritesManager.py"
        fm_action = "remove"
        list_item.addContextMenuItems(
            [( localize(30407),
                "XBMC.RunScript("+fm_script+", "+fm_action+", "+item["id"]+")"
            )], replaceItems=False)
        params = {}
        params["url"] = item["url"]
        params["mode"] = MODE_PROGRAM
        xbmcplugin.addDirectoryItem(PLUGIN_HANDLE, sys.argv[0] + '?' + urllib.urlencode(params), list_item, True)


def viewManagePlaylist():
    plm_dialog = PlaylistDialog()
    plm_dialog.doModal()
    del plm_dialog

def viewAtoO():
    programs = ur.getAtoO()

    for program in programs:
        addDirectoryItem(program["title"], { "mode": MODE_PROGRAM, "url": program["url"] })

def viewSubjects():
    categories = ur.getSubjects()

    for category in categories:
        addDirectoryItem(category["title"], { "mode": MODE_PROGRAM, "url": category["url"] })

def viewCategories():
    categories = ur.getCategories()

    for category in categories:
        addDirectoryItem(category["title"], { "mode": MODE_PROGRAM, "url": category["url"] })

def viewAlphaDirectories():
    alphas = ur.getAlphas()
    if not alphas:
        return
    for alpha in alphas:
        addDirectoryItem(alpha["title"], { "mode": MODE_LETTER, "letter": alpha["char"] })

def viewProgramsByLetter(letter):
    programs = ur.getProgramsByLetter(letter)

    if not programs: return

    for program in programs:
        addDirectoryItem(program["title"], { "mode": MODE_PROGRAM, "url": program["url"] })

def viewChannels():
    channels = ur.getChannels()
    if not channels:
        return
    for channel in channels:
        createDirItem(channel, MODE_VIDEO)

def viewEpisodes(url):
    """
    Displays the episodes for a program with URL 'url'.
    """
    episodes = ur.getEpisodes(url)
    if not episodes:
        helper.errorMsg("No episodes found!")
        return

    for episode in episodes[:-1]:
        createDirItem(episode, MODE_VIDEO)
    if episodes[-1]["url"] is not "":
        addDirectoryItem(localize(30101), { "mode" : MODE_PROGRAM, "url" : episodes[-1]["url"] })

def viewSearch():
    keyword = common.getUserInput(localize(30102))
    if keyword == "" or not keyword:
        viewStart()
        return
    keyword = urllib.quote(keyword)
    helper.infoMsg("Search string: " + keyword)

    keyword = re.sub(r" ", "+", keyword)

    url = ur.URL_TO_SEARCH + keyword

    results = ur.getSearchResults(url)
    for result in results:
        mode = MODE_VIDEO
        if result["type"] == "program":
            mode = MODE_PROGRAM
        createDirItem(result["item"], mode)


def createDirItem(article, mode):
    """
    Given an article and a mode; create directory item
    for the article.
    """
    if not helper.getSetting(S_HIDE_SIGN_LANGUAGE) or (article["title"].lower().endswith("teckentolkad") == False and article["title"].lower().find("teckenspråk".decode("utf-8")) == -1):
        params = {}
        params["mode"] = mode
        params["url"] = article["url"]
        folder = False

        if mode == MODE_PROGRAM:
            folder = True
        info = None
        if "info" in article.keys():
            info = article["info"]
        addDirectoryItem(article["title"], params, article["thumbnail"], folder, False, info)


def startVideo(url):
    """
    Starts the XBMC player if a valid video URL is
    found for the given page URL.
    """
    show_obj = helper.resolveShowURL(url)
    player = xbmc.Player()
    startTime = time.time()

    if show_obj["videoUrl"]:
        xbmcplugin.setResolvedUrl(PLUGIN_HANDLE, True, xbmcgui.ListItem(path=show_obj["videoUrl"]))

        if show_obj["subtitleUrl"]:
            while not player.isPlaying() and time.time() - startTime < 10:
                time.sleep(1.)

            player.setSubtitles(show_obj["subtitleUrl"])

            if not helper.getSetting(S_SHOW_SUBTITLES):
                player.showSubtitles(False)
    else:
        # No video URL was found
        dialog = xbmcgui.Dialog()
        dialog.ok("UR Play", localize(30100))


def addDirectoryItem(title, params, thumbnail = None, folder = True, live = False, info = None):

    if True:
        pass
    try:
        pass
        li = xbmcgui.ListItem(title)
        
        if thumbnail:
            li.setThumbnailImage(thumbnail)
        
        if live:
            li.setProperty("IsLive", "true")
        
        if not folder:
            if params["mode"] == MODE_VIDEO:
                li.setProperty("IsPlayable", "true")
                # Add context menu item for adding a video to playlist
                plm_script = "special://home/addons/plugin.video.urplay/resources/lib/PlaylistManager.py"
                plm_action = "add"
                if not thumbnail:
                    thumbnail = ""
                li.addContextMenuItems(
                    [( localize(30404),
                        "XBMC.RunScript("+plm_script+", "+plm_action+", "+params["url"]+", "+title+", "+thumbnail+")"
                    )], replaceItems=False)
                # Add context menu item to find similar videos
                li.addContextMenuItems(
                    [( localize(30408),
                        "XBMC.ActivateWindow(video, plugin://plugin.video.urplay/?mode=%s&url=%s)"%(MODE_PROGRAM,urllib.quote(params["url"]))
                    )], replaceItems=False)

        if params["mode"] == MODE_PROGRAM:
            # Add context menu item for adding programs as favorites
            fm_script = "special://home/addons/plugin.video.urplay/resources/lib/FavoritesManager.py"
            fm_action = "add"
            li.addContextMenuItems(
                [( localize(30406),
                    "XBMC.RunScript("+fm_script+", "+fm_action+", "+title+", "+params["url"]+")"
                 )], replaceItems=False)

        if info:
            li.setInfo("Video", info)
            if "fanart" in info.keys() and helper.getSetting("showfanart"):
                li.setArt({"fanart": info["fanart"]})
        
        xbmcplugin.addDirectoryItem(PLUGIN_HANDLE, sys.argv[0] + '?' + urllib.urlencode(params), li, folder)
    except:
        pass

# Main segment of script
ARG_PARAMS = helper.getUrlParameters(sys.argv[2])
ARG_MODE = ARG_PARAMS.get("mode")
ARG_URL = urllib.unquote_plus(ARG_PARAMS.get("url", ""))

if not ARG_MODE:
    viewStart()
elif ARG_MODE == MODE_A_TO_O:
    if helper.getSetting(S_USE_ALPHA_CATEGORIES):
        viewAlphaDirectories()
    else:
        viewAtoO()
elif ARG_MODE == MODE_INSPIRATION:
    viewEpisodes(ur.URL_TO_INSPIRATION)
elif ARG_MODE == MODE_SUBJECTS:
    viewSubjects()
elif ARG_MODE == MODE_CATEGORIES:
    viewCategories()
elif ARG_MODE == MODE_PROGRAM:
    viewEpisodes(ARG_URL)
elif ARG_MODE == MODE_VIDEO:
    startVideo(ARG_URL)
elif ARG_MODE == MODE_LETTER:
    viewProgramsByLetter(ARG_PARAMS.get("letter"))
elif ARG_MODE == MODE_SEARCH:
    viewSearch()
elif ARG_MODE == MODE_PLAYLIST_MANAGER:
    viewManagePlaylist()
elif ARG_MODE == MODE_FAVORITES:
    viewFavorites()

xbmcplugin.endOfDirectory(PLUGIN_HANDLE)
