#!/usr/bin/python
# -*- coding: utf8 -*-

import pygame as pg
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as msgBox


def Format(H, M, S):
    if H != 0:
        ft = "%02d:" % H
    else:
        ft = ""
    return ft + "%02d:%02d" % (M, S)


class Countdown:
    def __init__(self):
        self.Ready = False
        self.HH = 0
        self.MM = 30
        self.SS = 0
        self.Reset()
        self.window = tk.Tk()
        self.window.title("CD")
        self.Wt = 200
        self.Wl = 84
        self.Ht = 60
        self.Hb = 52
        self.Mb = 10
        size = '%dx%d+%d+%d' % (self.Wt, self.Ht, 5, 28)
        self.window.geometry(size)
        self.window.resizable(0, 0)
        self.CFont = ("Sans", 20, "bold")
        self.TFont = ("Sans", 12, "normal")
        self.run = tk.Button(self.window, text=Format(self.H, self.M, self.S),
                             command=self.Clicked, font=self.CFont,
                             relief='groove')
        self.PlaceButton()
        self.run.bind("<Double-1>", self.DoubleClicked)
        self.label = tk.Label(self.window, text="Click to start.", fg="#CCC",
                              bg="white", font=self.TFont)
        self.TIME = tk.StringVar()
        self.enter = tk.Entry(self.window, textvariable=self.TIME, width=10,
                              justify='center', font=self.CFont)
        self.PreTIME = self.TIME
        self.TIME.trace('w', self.EditChanging)
        self.enter.bind("<Key-Return>", self.EditChanged)
        self.pgBar = ttk.Progressbar(self.window)
        self.pgBar.place(x=0, y=self.Hb, width=self.Wt, height=self.Ht - self.Hb)
        self.Ready = True
        self.Reset()
        self.SetTimer()
        self.window.mainloop()

    def Reset(self, DONE=False):
        self.done = DONE
        self.running = False
        self.H = self.HH
        self.M = self.MM
        self.S = self.SS
        self.T = 10
        if self.Ready:
            self.UpdateTime()
            self.label.place(x=(self.Wt - self.Wl)/2, y=(self.Ht - 16)/2 + 15,
                             width=self.Wl, height=16)

    def Clicked(self, event=None):
        if self.done:
            self.Reset()
            self.label['text'] = "Click to restart."
            pg.mixer.music.stop()
            return
        self.running = not self.running
        if self.running:
            self.UpdateTime()
            self.label.place_forget()
        else:
            self.run['text'] = "Paused"

    def DoubleClicked(self, event=None):
        if self.running:
            self.Reset()
        self.run.place_forget()
        self.enter.delete(0, tk.END)
        self.enter.insert(tk.END, Format(self.HH, self.MM, self.SS))
        self.enter.place(x=0, y=0, width=self.Wt, height=self.Hb)

    def EditChanging(self, var=None, mode=None, event=None):
        pass

    def PlaceButton(self):
        self.run.place(x=self.Mb, y=0, width=self.Wt-2*self.Mb, height=self.Hb)

    def EditChanged(self, event=None):
        cTime = self.TIME.get()
        cTime = cTime.strip()
        ids = cTime.find('s')
        idm = cTime.find('m')
        idh = cTime.find('h')
        LT = []
        if idh >= 0:
            LT.append(cTime[0: idh])
        else:
            LT.append("00")
        if idm >= 0:
            LT.append(cTime[(idh + 1): idm])
        else:
            LT.append("00")
        if ids >= 0:
            LT.append(cTime[(max(idh, idm) + 1): ids])
        else:
            LT.append("00")
        if LT == ["00", "00", "00"]:
            LT = cTime.split(':')
            if len(LT) == 2:
                LT = ["00"] + LT
            if len(LT) != 3:
                msgBox.showerror("格式错误", cTime + "不是有效的时间格式HH:MM:SS或MM:SS！")
                return
        try:
            self.HH = int(LT[0])
            self.MM = int(LT[1])
            self.SS = int(LT[2])
            self.enter.place_forget()
            self.PlaceButton()
            self.Reset()
        except ValueError:
            msgBox.showerror("格式错误", cTime + "不是有效的时间格式HH:MM:SS或MM:SS！")
            return

    def UpdateTime(self):
        totalTT = ((self.HH * 60 + self.MM) * 60 + self.SS) * 10 + 10
        totalT = ((self.H * 60 + self.M) * 60 + self.S) * 10 + self.T
        self.pgBar['value'] = 100.0 * (totalTT - totalT) / (totalTT - 10)
        self.run['text'] = Format(self.H, self.M, self.S)

    def SetTimer(self):
        self.OnTimer()
        self.window.after(100, self.SetTimer)

    def OnTimer(self):
        if self.running:
            self.H += min((self.M + self.S + self.T - 1, 0))
            self.M += min((self.S + self.T - 1, 0)) + 60
            self.M %= 60
            self.S += min((self.T - 1, 0)) + 60
            self.S %= 60
            self.T = (self.T + 9) % 10
            self.UpdateTime()
            if self.H <= 0 and self.M <= 0 and self.S <= 0:
                self.Reset(True)
                self.run['text'] = "Time is up! "
                self.label['text'] = "Click to return."
                pg.mixer.init()
                pg.mixer.music.load("ring.mp3")
                pg.mixer.music.play()
                self.window.after(10, lambda: msgBox.showwarning("提示", "时间到！"))


Countdown()
