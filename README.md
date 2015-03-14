# Kodi UR addon

With this addon you can stream content from UR (ur.se).
The plugin fetches the video URL from the UR website and feeds it to the XBMC video player. HLS (m3u8) is the preferred video format by the plugin.

Based on [SVT Play addon from nilzen](https://github.com/nilzen/xbmc-svtplay)

It has been tested with Helix (14.0).

To open the **context menu**, press "c" on a keyboard or long press "Menu" on Apple TV 2 (ATV2).

## Favorites
TV programs in the A-Ö and category listings can be added as favorites. To add a program as a favorite, open the context menu, when a program is highlighted in the menu, and then click on "Add to favorites".

Favorites can be accessed from the top-level menu item "Favorites".

To remove a favorite, open the context menu, when a favorite is highlighted in the "Favorites" menu, and then clock on "Remove from favorites".

## Explaination of Settings

* (General) Show subtitles
  * Force programs to start with subtitles enabled. Subtitles can till be toggled on/off by using XBMC's controller shortcuts.
* (Advanced) Display icon as fanart
  * Uses the thumbnail as the fanart as well. The fanart is used by XBMC skins in different ways. However, the most common way is to have the fanart as some kind of background.
* (Advanced) Don't use avc1.77.30 streams
  * Forces the addon to choose the stream that supports the highest bandwidth but does not use the avc1.77.30 profile.
* (Advanced) Set bandwidth manually
  * Forces the addon to choose stream according to the set bandwidth. This option can be used to force lower resolution streams on devices with lower bandwidth capacity (i.e mobile devices). This option can only be used if "Don't use avc1.77.30 streams" is disabled.

## Known Issues

## Development

### Running tests
The module responsible for parsing the SVT Play website has a couple of tests that can be run to verify its functionality. To run these tests, execute the following commands from this repository's root folder:
```
cd tests
python -m unittest testSvt
```
