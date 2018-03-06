#Boa:Frame:Frame1

import wx
import wx.stc
import wx.richtext
from wx.lib.anchors import LayoutAnchors
from wx.lib.embeddedimage import PyEmbeddedImage
import os
import subprocess
import sys
import time
import math
import random
from PIL import Image
from six.moves import input

SCREENSHOT_WAY = 3
G_distance = 450
G_millisecond = 720

def pull_screenshot():
    global SCREENSHOT_WAY
    if 1 <= SCREENSHOT_WAY <= 3:
        process = subprocess.Popen(
            'adb shell screencap -p',
            shell=True, stdout=subprocess.PIPE)
        binary_screenshot = process.stdout.read()
        if SCREENSHOT_WAY == 2:
            binary_screenshot = binary_screenshot.replace(b'\r\n', b'\n')
        elif SCREENSHOT_WAY == 1:
            binary_screenshot = binary_screenshot.replace(b'\r\r\n', b'\n')
        f = open('jump.png', 'wb')
        f.write(binary_screenshot)
        f.close()
    elif SCREENSHOT_WAY == 0:
        os.system('adb shell screencap -p /sdcard/jump.png')
        os.system('adb pull /sdcard/jump.png .')


def check_screenshot():
    global SCREENSHOT_WAY
    if os.path.isfile('jump.png'):
        try:
            os.remove('jump.png')
        except Exception:
            pass
    if SCREENSHOT_WAY < 0:
        return 0
    pull_screenshot()
    try:
        Image.open('./jump.png').load()
    except Exception:
        SCREENSHOT_WAY -= 1
        check_screenshot()
    return 1
        
def jump(msecond):
    x = 541
    y = 1582
    x1 = str(int(random.uniform(x-40, x+40)))
    y1 = str(int(random.uniform(y-40, y+40)))
    x = 591
    y = 1632
    x2 = str(int(random.uniform(x-40, x+40)))
    y2 = str(int(random.uniform(y-40, y+40)))
    cmd ='adb shell input touchscreen swipe '+x1+' '+y1+' '+x2+' '+y2+' ' + msecond
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
def get_distance():
    pull_screenshot()
    #distance=[]
    im = Image.open('./jump.png')
    im_pixel = im.load()
    w, h = im.size
    im.close()
    
    piece_x_sum = 0
    piece_x_c = 0
    piece_x = 0
    board_x_sum = 0
    board_x_c = 0
    board_x = 0
    scan_x_border = int(w / 8) 
    scan_start_y = 0  
    
    for y in range(int(h / 3), int(h*2 / 3), 50):
        last_pixel = im_pixel[0, y]
        for x in range(1, w):
            pixel = im_pixel[x, y]
            if pixel != last_pixel:
                scan_start_y = y - 50
                break
        if scan_start_y:
            break
    
    for y in range(scan_start_y, int(h * 2 / 3)):
        for x in range(scan_x_border, w - scan_x_border):
            pixel = im_pixel[x,y]
            if (50 < pixel[0] < 60)  and (53 < pixel[1] < 63) and (95 < pixel[2] < 110):
                piece_x_sum += x
                piece_x_c += 1
         
    if not piece_x_c :
        return -1
    piece_x = int(piece_x_sum / piece_x_c)
 
    if piece_x < w/2:
        board_x_start = piece_x
        board_x_end = w
    else:
        board_x_start = 0
        board_x_end = piece_x

    for y in range(int(h / 3), int(h * 2 / 3)):
        last_pixel = im_pixel[0, y]
        if board_x:
            break

        for x in range(int(board_x_start), int(board_x_end)):
            pixel = im_pixel[x, y]
            if abs(x - piece_x) < 50:
                continue
            if abs(pixel[0] - last_pixel[0]) + abs(pixel[1] - last_pixel[1]) + abs(pixel[2] - last_pixel[2]) > 10:
                board_x_sum += x
                board_x_c += 1
        if board_x_sum :
            board_x = board_x_sum / board_x_c
            
    distance=abs(board_x - piece_x)
    #distance.append(piece_x)
    #distance.append(board_x)
    return distance

def create(parent):
    return Frame1(parent)

[wxID_FRAME1, wxID_FRAME1BT_ALPHA_AUTO, wxID_FRAME1BT_ALPHA_JUMP, 
 wxID_FRAME1BT_JUMP, wxID_FRAME1BT_SCREENSIZE, wxID_FRAME1PANEL1, 
 wxID_FRAME1RICHTEXTCTRL1, wxID_FRAME1STATICBITMAP1, wxID_FRAME1ST_DISTANCE, 
 wxID_FRAME1ST_MILLISECOND, wxID_FRAME1ST_N, wxID_FRAME1ST_SCREENSIZE, 
 wxID_FRAME1TC_DEBUG, wxID_FRAME1TC_DISTANCE, wxID_FRAME1TC_MILLISECOND, 
 wxID_FRAME1TC_N, wxID_FRAME1TC_SCREENSIZE, 
] = [wx.NewId() for _init_ctrls in range(17)]

class Frame1(wx.Frame):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRAME1, name='', parent=prnt,
              pos=wx.Point(520, 74), size=wx.Size(310, 660),
              style=wx.DEFAULT_FRAME_STYLE, title=u'Alpha-J')
        self.SetClientSize(wx.Size(294, 621))
        self.SetMaxSize(wx.Size(600, 660))
        self.SetMinSize(wx.Size(310, 660))
        self.Show(True)

        self.panel1 = wx.Panel(id=wxID_FRAME1PANEL1, name='panel1', parent=self,
              pos=wx.Point(0, 0), size=wx.Size(294, 621),
              style=wx.TAB_TRAVERSAL)
        self.panel1.SetAutoLayout(True)
        self.panel1.SetConstraints(LayoutAnchors(self.panel1, True, True, False,
              False))
        self.panel1.Show(True)

        self.st_distance = wx.StaticText(id=wxID_FRAME1ST_DISTANCE,
              label=u'distance:', name=u'st_distance', parent=self.panel1,
              pos=wx.Point(8, 40), size=wx.Size(49, 14), style=0)

        self.st_Screensize = wx.StaticText(id=wxID_FRAME1ST_SCREENSIZE,
              label=u'Screen size:', name=u'st_Screensize', parent=self.panel1,
              pos=wx.Point(8, 8), size=wx.Size(65, 14), style=0)

        self.st_millisecond = wx.StaticText(id=wxID_FRAME1ST_MILLISECOND,
              label=u'millisecond:', name=u'st_millisecond', parent=self.panel1,
              pos=wx.Point(8, 72), size=wx.Size(61, 14), style=0)

        self.tc_millisecond = wx.TextCtrl(id=wxID_FRAME1TC_MILLISECOND,
              name=u'tc_millisecond', parent=self.panel1, pos=wx.Point(96, 72),
              size=wx.Size(96, 24), style=0, value=u'720')

        self.bt_jump = wx.Button(id=wxID_FRAME1BT_JUMP, label=u'jump',
              name=u'bt_jump', parent=self.panel1, pos=wx.Point(208, 40),
              size=wx.Size(75, 24), style=0)
        self.bt_jump.Bind(wx.EVT_BUTTON, self.Onbt_jumpButton,
              id=wxID_FRAME1BT_JUMP)

        self.richTextCtrl1 = wx.richtext.RichTextCtrl(id=wxID_FRAME1RICHTEXTCTRL1,
              parent=self.panel1, pos=wx.Point(8, 136), size=wx.Size(280, 288),
              style=wx.richtext.RE_MULTILINE,
              value=u'1\u3001\u53ea\u652f\u6301\u5b89\u5353\u7cfb\u7edf\n2\u3001\u624b\u673a\u6253\u5f00USB\u8c03\u8bd5/\u6a21\u62df\u70b9\u51fb\uff0c\u786e\u4fdd\u6ca1\u6709\u5176\u5b83\u7a0b\u5e8f\u8fde\u63a5\u624b\u673a\u3002\n3\u3001\u8bf7\u5148\u6d4b\u91cfScreensize\u3002\u7b2c\u4e00\u8df3\u9ed8\u8ba4720\u6beb\u79d2\uff0c\u8df3\u4e00\u8df3\u6709\u4e00\u4e2a\u5341\u51e0\u6beb\u79d2\u968f\u673a\u8bef\u5dee\uff0c\u4f60\u53ef\u4ee5\u5c1d\u8bd5\u662f\u5426\u6709\u66f4\u597d\u503c\u3002\n\n jump          \u8df3millisecond\uff1a\u6307\u5b9a\u6beb\u79d2\u3002      \nAlphi-jump   \u5355\u6b65\u667a\u80fd\u8df3\u3002\nAlphi-auto    \u667a\u80fd\u8df3n\u6b21\u3002\n\u667a\u80fd\u8df3\u4e0d\u8981\u8fde\u7eed\u8df3\u5f88\u591a\u6b21\uff0c\u8df3\u4e00\u8df3\u6709\u68c0\u6d4b\u673a\u5668\u4eba\u529f\u80fd\uff0c\u8bf7\u9010\u6b65\u63d0\u9ad8\u4f60\u7684\u5206\u6570\u3002\n\n\u73b0\u5728\u4f60\u53ef\u4ee5\u4eab\u53d7\u8df3\u4e00\u8df3\u7684\u4e50\u8da3\uff0c\u4e0d\u53d7\u6392\u884c\u699c\u7684\u5f71\u54cd\u3002\n\n      \u5982\u679c\u4f60\u9ad8\u5174\uff0c\u8bf7\u968f\u610f\u6253\u8d4f\u70b9\u8d5e\uff01')
        self.richTextCtrl1.SetLabel(u'richText')

        self.staticBitmap1 = wx.StaticBitmap(bitmap=wx.Bitmap(u'wx._gdc_.pyd',
              wx.BITMAP_TYPE_JPEG), id=wxID_FRAME1STATICBITMAP1,
              name='staticBitmap1', parent=self.panel1, pos=wx.Point(64, 432),
              size=wx.Size(169, 183), style=0)

        self.bt_Alpha_jump = wx.Button(id=wxID_FRAME1BT_ALPHA_JUMP,
              label=u'Alpha-jump', name=u'bt_Alpha_jump', parent=self.panel1,
              pos=wx.Point(208, 72), size=wx.Size(75, 24), style=0)
        self.bt_Alpha_jump.Bind(wx.EVT_BUTTON, self.Onbt_Alpha_jumpButton,
              id=wxID_FRAME1BT_ALPHA_JUMP)

        self.bt_Screensize = wx.Button(id=wxID_FRAME1BT_SCREENSIZE,
              label=u'Screen size', name=u'bt_Screensize', parent=self.panel1,
              pos=wx.Point(208, 8), size=wx.Size(75, 24), style=0)
        self.bt_Screensize.Bind(wx.EVT_BUTTON, self.Onbt_screensizeButton,
              id=wxID_FRAME1BT_SCREENSIZE)

        self.tc_Screensize = wx.TextCtrl(id=wxID_FRAME1TC_SCREENSIZE,
              name=u'tc_Screensize', parent=self.panel1, pos=wx.Point(96, 8),
              size=wx.Size(96, 24), style=0, value=u'')

        self.tc_distance = wx.TextCtrl(id=wxID_FRAME1TC_DISTANCE,
              name=u'tc_distance', parent=self.panel1, pos=wx.Point(96, 40),
              size=wx.Size(96, 24), style=0, value=u'450')

        self.bt_Alpha_auto = wx.Button(id=wxID_FRAME1BT_ALPHA_AUTO,
              label=u'Alpha-auto', name=u'bt_Alpha_auto', parent=self.panel1,
              pos=wx.Point(208, 104), size=wx.Size(75, 24), style=0)
        self.bt_Alpha_auto.Bind(wx.EVT_BUTTON, self.Onbt_Alpha_autoButton,
              id=wxID_FRAME1BT_ALPHA_AUTO)

        self.tc_n = wx.TextCtrl(id=wxID_FRAME1TC_N, name=u'tc_n',
              parent=self.panel1, pos=wx.Point(96, 104), size=wx.Size(96, 22),
              style=0, value=u'20')

        self.st_n = wx.StaticText(id=wxID_FRAME1ST_N, label=u'n:', name=u'st_n',
              parent=self.panel1, pos=wx.Point(8, 104), size=wx.Size(11, 16),
              style=0)

        self.tc_debug = wx.TextCtrl(id=wxID_FRAME1TC_DEBUG, name=u'tc_debug',
              parent=self.panel1, pos=wx.Point(312, 16), size=wx.Size(256, 592),
              style=wx.TE_MULTILINE, value=u'')

    def __init__(self, parent):
        self._init_ctrls(parent)
        
    def Onbt_jumpButton(self, event):
        millisecond = self.tc_millisecond.Value
        jump(millisecond)
        event.Skip()
        
    def alpha_jump(self):
        global G_distance
        global G_millisecond 
        
        distance=get_distance()
        #self.tc_debug.AppendText('distance:'+str(distance)+'\n')
        if distance > 0:
            millisecond = str(int(distance*G_millisecond/G_distance))
            jump(millisecond)
            return 1
        return 0

    def Onbt_Alpha_jumpButton(self, event):
        self.alpha_jump()
        event.Skip()

    def Onbt_screensizeButton(self, event):
        global G_distance
        global G_millisecond 
        
        try:      
            if check_screenshot():
                cmd = "adb shell wm size"  
                p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
                p=p[p.find('Override size:')+15:].strip()
                self.tc_Screensize.Value = p  
                distance=get_distance()
                if distance == -1:
                    self.tc_distance.Value = 'open jump!'
                else:
                    self.tc_distance.Value = str(distance)
                G_distance = distance
                G_millisecond = int(self.tc_millisecond.Value)
            else:
                self.tc_Screensize.Value = 'not connect!' 
        except Exception:
            self.tc_Screensize.Value = 'not connect!' 
        event.Skip()

    def Onbt_Alpha_autoButton(self, event):
        n = 0
        self.tc_debug.Clear()
        while n <=int(self.tc_n.Value.encode("ascii")):
            rn = self.alpha_jump()
            if rn == 0:
                self.tc_debug.AppendText('Discern error,please manual jump.\n')
                break
            n += 1
            time.sleep(random.uniform(3.0, 5.0))
        event.Skip()

