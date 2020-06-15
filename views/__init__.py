import sys
sys.stdout.encoding
'UTF-8'
from .VentanaApiDesk import ViewLogin
from .VentanaApiDesk import ViewConfigurations
from .VentanaApiDesk import ViewConeccionDB

def newAPIVentana(trayMsg = None):
    viewConf = ViewConfigurations(None)
    viewConf.Show()
    if trayMsg:
        viewConf.show_balloon(trayMsg)
    viewConf.Restore()