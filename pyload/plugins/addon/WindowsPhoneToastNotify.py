# -*- coding: utf-8 -*-

import httplib
import time

from pyload.plugins.Addon import Addon


class WindowsPhoneToastNotify(Addon):
    __name    = "WindowsPhoneToastNotify"
    __type    = "addon"
    __version = "0.03"

    __config = [("force"      , "bool", "Force even if client is connected"       , False),
                ("pushId"     , "str" , "pushId"                                  , ""   ),
                ("pushUrl"    , "str" , "pushUrl"                                 , ""   ),
                ("pushTimeout", "int" , "Timeout between notifications in seconds", 0    )]

    __description = """Send push notifications to Windows Phone"""
    __license     = "GPLv3"
    __authors     = [("Andy Voigt", "phone-support@hotmail.de")]


    def getXmlData(self):
        myxml = ("<?xml version='1.0' encoding='utf-8'?> <wp:Notification xmlns:wp='WPNotification'> "
                 "<wp:Toast> <wp:Text1>Pyload Mobile</wp:Text1> <wp:Text2>Captcha waiting!</wp:Text2> "
                 "</wp:Toast> </wp:Notification>")
        return myxml


    def doRequest(self):
        URL = self.getConfig("pushUrl")
        request = self.getXmlData()
        webservice = httplib.HTTP(URL)
        webservice.putrequest("POST", self.getConfig("pushId"))
        webservice.putheader("Host", URL)
        webservice.putheader("Content-type", "text/xml")
        webservice.putheader("X-NotificationClass", "2")
        webservice.putheader("X-WindowsPhone-Target", "toast")
        webservice.putheader("Content-length", "%d" % len(request))
        webservice.endheaders()
        webservice.send(request)
        webservice.close()
        self.setStorage("LAST_NOTIFY", time.time())


    def captchaTask(self, task):
        if not self.getConfig("pushId") or not self.getConfig("pushUrl"):
            return False

        if self.core.isClientConnected() and not self.getConfig("force"):
            return False

        if (time.time() - float(self.getStorage("LAST_NOTIFY", 0))) < self.getConf("pushTimeout"):
            return False

        self.doRequest()
