'''
   YouTube plugin for XBMC
   Copyright (C) 2010-2012 Tobias Ussing And Henrik Mosgaard Jensen

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import sys

# Some of this code has been taken from 
# https://github.com/AddonScriptorDE/plugin.program.chrome.launcher
class YouTubeBrowser():
    def __init__(self):
        self.xbmcaddon = sys.modules["__main__"].xbmcaddon
        self.common = sys.modules["__main__"].common
        self.xbmc = sys.modules["__main__"].xbmc
        self.os = sys.modules["__main__"].os
        self.subprocess = sys.modules["__main__"].subprocess
        
        self.osWin = self.xbmc.getCondVisibility('system.platform.windows')
        self.osOsx = self.xbmc.getCondVisibility('system.platform.osx')
        self.osLinux = self.xbmc.getCondVisibility('system.platform.linux')
        self.addon = self.xbmcaddon.Addon()
        self.addonPath = self.addon.getAddonInfo('path')
        
    def playVideo(self, videoid):
        self.xbmc.executebuiltin('LIRC.Stop')
        
        if self.osLinux:
            # the browser.sh has the specific url that is required to work with the specific linux browser
            # plus whatever remote control scripting that is required.
            path = self.browserPath = self.os.path.join(self.addonPath, 'browser.sh')
            self.common.log("Opening %s with videoid %s" % (path, videoid));
            
            self.subprocess.call('"'+path+'" "'+videoid+'"', shell=True)
            
        elif self.osOsx:
            # TODO - create external osx specific browser script so this stuff can all
            # be customised for specific installations.
            url = "https://www.youtube.com/embed/%s?autoplay=1&autohide=1" % videoid
            path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
            fullUrl = self.getFullPath(path, url)
        else: # self.osWin:
            # TODO - create external windows specific browser.bat so this stuff can all
            # be customised for specific installations.
            url = "https://www.youtube.com/embed/%s?autoplay=1&autohide=1" % videoid
            path = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
            path64 = 'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'
            if self.os.path.exists(path):
                fullUrl = self.getFullPath(path, url)
                self.subprocess.Popen(fullUrl, shell=True)
            elif self.os.path.exists(path64):
                fullUrl = self.getFullPath(path, url)
                self.subprocess.Popen(fullUrl, shell=True)
                
        self.xbmc.executebuiltin('LIRC.Start')
        
    def getFullPath(self, path, url):
        return '"'+path+'" --start-maximized --disable-translate --disable-new-tab-first-run --no-default-browser-check --no-first-run --kiosk "'+url+'"'
