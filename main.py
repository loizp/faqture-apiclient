import sys
import os
sys.stdout.encoding
'UTF-8'
sys.path.append(".")
sys.path.append(os.getcwd())

import wx
from daos import ConfigThreadsApi
from views import newAPIVentana

ConfigThreadsApi().setInicial()

app = wx.App()
newAPIVentana()
app.MainLoop()