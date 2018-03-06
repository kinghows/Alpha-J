#!/usr/bin/env python
#Boa:App:BoaApp

import wx

import JP_Frame1

modules ={u'JP_Frame1': [1, 'Main frame of Application', u'JP_Frame1.py']}

class BoaApp(wx.App):
    def OnInit(self):
        self.main = JP_Frame1.create(None)
        self.main.Show()
        self.SetTopWindow(self.main)
        return True

def main():
    application = BoaApp(0)
    application.MainLoop()

if __name__ == '__main__':
    main()
