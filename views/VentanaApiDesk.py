import sys
sys.stdout.encoding
'UTF-8'
import wx, wx.adv, wx.aui
from daos import Emisor, ConfigThreadsApi, SourceAPImongo, SourceDBemisor, SourceAPIpgsql
from services import iniciarSesion, testConnect, onListen, onForward

class ViewLogin(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"APIfaqtureClient", pos=wx.DefaultPosition,
                          size=wx.Size(280, 430), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        self.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_ACTIVECAPTION))
        self.SetBackgroundColour(wx.Colour(58, 99, 148))

        ico = wx.Icon(u"./resources/images/faqture_24x24.png", wx.BITMAP_TYPE_PNG)
        self.SetIcon(ico)

        loginLayout = wx.BoxSizer(wx.VERTICAL)

        self.faqtureLogo = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(
            u"./resources/images/faqture_logo_white_cursiva.png",
            wx.BITMAP_TYPE_ANY), wx.DefaultPosition, wx.Size(200, 155), 0)
        loginLayout.Add(self.faqtureLogo, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        formLayout = wx.BoxSizer(wx.VERTICAL)

        self.lbl_username = wx.StaticText(self, wx.ID_ANY, u"Ingrese su nombre de usuario:", wx.Point(-1, -1),
                                          wx.Size(200, -1), wx.ALIGN_LEFT)
        self.lbl_username.Wrap(-1)
        self.lbl_username.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(), 73, 90, 90, False, wx.EmptyString))
        self.lbl_username.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_ACTIVECAPTION))
        self.lbl_username.SetMinSize(wx.Size(200, -1))
        self.lbl_username.SetMaxSize(wx.Size(200, -1))

        formLayout.Add(self.lbl_username, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        self.etx_username = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(200, -1),
                                        wx.TE_LEFT)
        self.etx_username.SetMinSize(wx.Size(200, -1))
        self.etx_username.SetMaxSize(wx.Size(200, -1))

        formLayout.Add(self.etx_username, 0, wx.ALIGN_CENTER | wx.ALL, 1)

        self.lbl_password = wx.StaticText(self, wx.ID_ANY, u"Ingrese su contraseña:", wx.DefaultPosition,
                                          wx.Size(200, -1), wx.ALIGN_LEFT)
        self.lbl_password.Wrap(-1)
        self.lbl_password.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(), 73, 90, 90, False, wx.EmptyString))
        self.lbl_password.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_ACTIVECAPTION))
        self.lbl_password.SetMinSize(wx.Size(200, -1))
        self.lbl_password.SetMaxSize(wx.Size(200, -1))

        formLayout.Add(self.lbl_password, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        self.etx_password = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(200, -1),
                                        wx.TE_LEFT | wx.TE_PASSWORD)
        self.etx_password.SetMinSize(wx.Size(200, -1))
        self.etx_password.SetMaxSize(wx.Size(200, -1))

        formLayout.Add(self.etx_password, 0, wx.ALIGN_CENTER | wx.ALL, 1)

        self.btn_startlogin = wx.Button(self, wx.ID_ANY, u"Iniciar Sesión", wx.DefaultPosition, wx.Size(200, -1),
                                        wx.NO_BORDER)
        self.btn_startlogin.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(), 73, 94, 92, False, wx.EmptyString))
        self.btn_startlogin.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
        self.btn_startlogin.SetBackgroundColour(wx.Colour(77, 120, 191))
        self.btn_startlogin.SetMinSize(wx.Size(200, -1))
        self.btn_startlogin.SetMaxSize(wx.Size(200, -1))

        formLayout.Add(self.btn_startlogin, 0, wx.ALIGN_CENTER | wx.ALL, 15)

        self.lbl_message = wx.StaticText(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(270, -1),
                                         wx.ALIGN_CENTRE)
        self.lbl_message.Wrap(-1)
        self.lbl_message.SetFont(wx.Font(8, 74, 93, 90, False, "Arial"))
        self.lbl_message.SetForegroundColour(wx.Colour(255, 0, 0))

        formLayout.Add(self.lbl_message, 0, wx.ALIGN_CENTER | wx.ALL | wx.BOTTOM | wx.EXPAND, 0)

        loginLayout.Add(formLayout, 1, wx.ALIGN_CENTER | wx.EXPAND, 5)

        self.SetSizer(loginLayout)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.Bind(wx.EVT_CLOSE, self.cerrarLogin)
        self.btn_startlogin.Bind(wx.EVT_BUTTON, self.loginStart)

    def __del__(self):
        pass

    def cerrarLogin(self, event):
        viewConf = ViewConfigurations(None)
        viewConf.Show()
        event.Skip()

    def loginStart(self, event):
        uname = self.etx_username.GetValue()
        upass = self.etx_password.GetValue()
        if not uname or uname.strip() == "" or not upass or upass.strip() == "":
            self.lbl_message.SetLabelText("Los datos son incorrectos")
        else:
            self.lbl_message.SetLabelText(wx.EmptyString)
            resp = iniciarSesion(uname,upass)
            if resp.isSuccess():
                self.Close()
            else:
                self.lbl_message.SetLabelText(resp.message)
        event.Skip()

class ApiClientTrayMenu(wx.adv.TaskBarIcon):
    def __init__(self, frame):
        wx.adv.TaskBarIcon.__init__(self)
        self.frame = frame
        icon = wx.Icon(u"./resources/images/faqture_24x24.png", wx.BITMAP_TYPE_PNG)
        self.SetIcon(icon, "APIfaqtureClient: Cliente de la aplicación faqture")
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DCLICK, self.OnTaskBarClick)
        self.Bind(wx.adv.EVT_TASKBAR_CLICK, self.OnTaskBarClick)

    def OnTaskBarClick(self, evt):
        if self.frame:
            self.frame.Show()
            self.frame.Restore()
        else:
            viewConf = ViewConfigurations(None)
            viewConf.Show()
            self.Destroy()
            self.RemoveIcon()

class ViewConfigurations(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"APIfaqtureClient", pos=wx.DefaultPosition,
                          size=wx.Size(650, 420), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        self.SetBackgroundColour(wx.Colour(78, 133, 207))

        ico = wx.Icon(u"./resources/images/faqture_24x24.png", wx.BITMAP_TYPE_PNG)
        self.SetIcon(ico)

        self.tbicon = ApiClientTrayMenu(self)

        mainLayout = wx.BoxSizer(wx.HORIZONTAL)

        self.infoPanel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(280, -1), wx.TAB_TRAVERSAL)
        self.infoPanel.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_ACTIVECAPTION))
        self.infoPanel.SetBackgroundColour(wx.Colour(54, 82, 120))
        self.infoPanel.SetMaxSize(wx.Size(280, -1))

        infoLayout = wx.BoxSizer(wx.VERTICAL)

        self.faqtureLogo = wx.StaticBitmap(self.infoPanel, wx.ID_ANY, wx.Bitmap(
            u"./resources/images/faqture_logo_white_cursiva.png",
            wx.BITMAP_TYPE_ANY), wx.DefaultPosition, wx.Size(200, 155), 0)
        infoLayout.Add(self.faqtureLogo, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        self.lbl_tituloinfo = wx.StaticText(self.infoPanel, wx.ID_ANY, u"Datos del Producto", wx.DefaultPosition,
                                            wx.Size(200, -1), wx.ALIGN_CENTRE)
        self.lbl_tituloinfo.Wrap(-1)
        self.lbl_tituloinfo.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString))
        self.lbl_tituloinfo.SetForegroundColour(wx.Colour(0, 0, 0))

        infoLayout.Add(self.lbl_tituloinfo, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        webproductoLayout = wx.BoxSizer(wx.HORIZONTAL)

        self.lbl_cabdomain = wx.StaticText(self.infoPanel, wx.ID_ANY, u"Sitio Web :", wx.DefaultPosition,
                                           wx.Size(80, -1), 0)
        self.lbl_cabdomain.Wrap(-1)
        self.lbl_cabdomain.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString))
        self.lbl_cabdomain.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_ACTIVECAPTION))
        self.lbl_cabdomain.SetMaxSize(wx.Size(80, -1))

        webproductoLayout.Add(self.lbl_cabdomain, 0, wx.ALL, 5)

        self.lbl_detdomain = wx.StaticText(self.infoPanel, wx.ID_ANY, u"http://www.faqture.com", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.lbl_detdomain.Wrap(-1)
        webproductoLayout.Add(self.lbl_detdomain, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        infoLayout.Add(webproductoLayout, 1, wx.EXPAND, 5)

        empresaLayout = wx.BoxSizer(wx.HORIZONTAL)

        self.lbl_cabempresa = wx.StaticText(self.infoPanel, wx.ID_ANY, u"Razon Social :", wx.DefaultPosition,
                                            wx.Size(80, -1), 0)
        self.lbl_cabempresa.Wrap(-1)
        self.lbl_cabempresa.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString))
        self.lbl_cabempresa.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_ACTIVECAPTION))
        self.lbl_cabempresa.SetMaxSize(wx.Size(80, -1))

        empresaLayout.Add(self.lbl_cabempresa, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.lbl_detempresa = wx.StaticText(self.infoPanel, wx.ID_ANY, u"Quantum Inc S.A.C.", wx.DefaultPosition,
                                            wx.DefaultSize, 0)
        self.lbl_detempresa.Wrap(-1)
        empresaLayout.Add(self.lbl_detempresa, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        infoLayout.Add(empresaLayout, 1, wx.EXPAND, 5)

        rucempresaLayout = wx.BoxSizer(wx.HORIZONTAL)

        self.lbl_cabrucempresa = wx.StaticText(self.infoPanel, wx.ID_ANY, u"RUC :", wx.DefaultPosition,
                                              wx.Size(80, -1), 0)
        self.lbl_cabrucempresa.Wrap(-1)
        self.lbl_cabrucempresa.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString))
        self.lbl_cabrucempresa.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_ACTIVECAPTION))
        self.lbl_cabrucempresa.SetMaxSize(wx.Size(80, -1))

        rucempresaLayout.Add(self.lbl_cabrucempresa, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.lbl_detrucempresa = wx.StaticText(self.infoPanel, wx.ID_ANY, u"20603088981",
                                             wx.DefaultPosition, wx.DefaultSize, 0)
        self.lbl_detrucempresa.Wrap(-1)
        rucempresaLayout.Add(self.lbl_detrucempresa, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        infoLayout.Add(rucempresaLayout, 1, wx.EXPAND, 5)

        direccionLayout = wx.BoxSizer(wx.HORIZONTAL)

        self.lbl_cabdireccion = wx.StaticText(self.infoPanel, wx.ID_ANY, u"Dirección :", wx.DefaultPosition,
                                              wx.Size(80, -1), 0)
        self.lbl_cabdireccion.Wrap(-1)
        self.lbl_cabdireccion.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString))
        self.lbl_cabdireccion.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_ACTIVECAPTION))
        self.lbl_cabdireccion.SetMaxSize(wx.Size(80, -1))

        direccionLayout.Add(self.lbl_cabdireccion, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.lbl_detdireccion = wx.StaticText(self.infoPanel, wx.ID_ANY, u"San Martín, Perú",
                                             wx.DefaultPosition, wx.DefaultSize, 0)
        self.lbl_detdireccion.Wrap(-1)
        direccionLayout.Add(self.lbl_detdireccion, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        infoLayout.Add(direccionLayout, 1, wx.EXPAND, 5)

        ncontactoLayout = wx.BoxSizer(wx.HORIZONTAL)

        self.lbl_cabncontacto = wx.StaticText(self.infoPanel, wx.ID_ANY, u"Email :", wx.DefaultPosition,
                                              wx.Size(80, -1), 0)
        self.lbl_cabncontacto.Wrap(-1)
        self.lbl_cabncontacto.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString))
        self.lbl_cabncontacto.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_ACTIVECAPTION))
        self.lbl_cabncontacto.SetMaxSize(wx.Size(80, -1))

        ncontactoLayout.Add(self.lbl_cabncontacto, 0, wx.ALL, 5)

        self.lbl_detcontacto = wx.StaticText(self.infoPanel, wx.ID_ANY, u"contacto@faqture.com",
                                             wx.DefaultPosition, wx.DefaultSize, 0)
        self.lbl_detcontacto.Wrap(-1)
        ncontactoLayout.Add(self.lbl_detcontacto, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        infoLayout.Add(ncontactoLayout, 1, wx.EXPAND, 5)

        telefonoLayout = wx.BoxSizer(wx.HORIZONTAL)

        self.lbl_cabtelefono = wx.StaticText(self.infoPanel, wx.ID_ANY, u"Teléfono :", wx.DefaultPosition,
                                              wx.Size(80, -1), 0)
        self.lbl_cabtelefono.Wrap(-1)
        self.lbl_cabtelefono.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString))
        self.lbl_cabtelefono.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_ACTIVECAPTION))
        self.lbl_cabtelefono.SetMaxSize(wx.Size(80, -1))

        telefonoLayout.Add(self.lbl_cabtelefono, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.lbl_dettelefono = wx.StaticText(self.infoPanel, wx.ID_ANY, u"+51 999 999 999",
                                             wx.DefaultPosition, wx.DefaultSize, 0)
        self.lbl_dettelefono.Wrap(-1)
        telefonoLayout.Add(self.lbl_dettelefono, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        infoLayout.Add(telefonoLayout, 1, wx.EXPAND, 5)

        self.infoPanel.SetSizer(infoLayout)
        self.infoPanel.Layout()
        mainLayout.Add(self.infoPanel, 1, wx.ALL | wx.EXPAND, 0)

        self.confPanel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(350, -1), wx.TAB_TRAVERSAL)
        confLayout = wx.BoxSizer(wx.VERTICAL)

        self.lbl_tituloconf = wx.StaticText(self.confPanel, wx.ID_ANY, u"Configuraciones ApiClient", wx.DefaultPosition,
                                            wx.Size(280, -1), wx.ALIGN_CENTRE)
        self.lbl_tituloconf.Wrap(-1)
        self.lbl_tituloconf.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString))

        confLayout.Add(self.lbl_tituloconf, 0, wx.ALIGN_CENTER | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 10)

        self.lbl_mensaje = wx.StaticText(self.confPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                         wx.Size(300, -1), wx.ALIGN_CENTRE)
        self.lbl_mensaje.Wrap(-1)
        self.lbl_mensaje.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 93, 90, False, wx.EmptyString))
        self.lbl_mensaje.SetForegroundColour(wx.Colour(0, 0, 255))

        confLayout.Add(self.lbl_mensaje, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        authLayout = wx.BoxSizer(wx.HORIZONTAL)

        self.lbl_auth = wx.StaticText(self.confPanel, wx.ID_ANY, u"Autenticada y Autorizada :", wx.DefaultPosition,
                                      wx.Size(230, -1), 0)
        self.lbl_auth.Wrap(-1)
        self.lbl_auth.SetMaxSize(wx.Size(230, -1))

        authLayout.Add(self.lbl_auth, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        if Emisor().isAuth():
            self.chk_auth = wx.CheckBox(self.confPanel, wx.ID_ANY, u"SI", wx.DefaultPosition, wx.DefaultSize, 0)
            self.chk_auth.SetValue(True)
            self.chk_auth.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString))
            self.chk_auth.SetForegroundColour(wx.Colour(0, 244, 0))
        else:
            self.chk_auth = wx.CheckBox(self.confPanel, wx.ID_ANY, u"NO", wx.DefaultPosition, wx.DefaultSize, 0)
            self.chk_auth.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 90, False, wx.EmptyString))
            self.chk_auth.SetForegroundColour(wx.Colour(255, 128, 0))

        authLayout.Add(self.chk_auth, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        confLayout.Add(authLayout, 1, wx.EXPAND, 10)

        connectdbLayout = wx.BoxSizer(wx.HORIZONTAL)

        self.lbl_connectdb = wx.StaticText(self.confPanel, wx.ID_ANY, u"Cambiar conexiones a BD :", wx.DefaultPosition,
                                           wx.Size(230, -1), 0)
        self.lbl_connectdb.Wrap(-1)
        self.lbl_connectdb.SetMaxSize(wx.Size(230, -1))

        connectdbLayout.Add(self.lbl_connectdb, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.btn_conectdb = wx.Button(self.confPanel, wx.ID_ANY, u"Modificar", wx.DefaultPosition, wx.DefaultSize, 0)
        connectdbLayout.Add(self.btn_conectdb, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        confLayout.Add(connectdbLayout, 1, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 5)

        mongoLayout = wx.BoxSizer(wx.HORIZONTAL)

        self.lbl_mongo = wx.StaticText(self.confPanel, wx.ID_ANY, u"Almacenar en MongoDB :", wx.DefaultPosition,
                                       wx.Size(230, -1), 0)
        self.lbl_mongo.Wrap(-1)
        self.lbl_mongo.SetMaxSize(wx.Size(230, -1))

        mongoLayout.Add(self.lbl_mongo, 0,wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        if ConfigThreadsApi().usaMongoDB():
            self.chk_mongo = wx.CheckBox(self.confPanel, wx.ID_ANY, u"SI", wx.DefaultPosition, wx.DefaultSize, 0)
            self.chk_mongo.SetValue(True)
            self.chk_mongo.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString))
            self.chk_mongo.SetForegroundColour(wx.Colour(0, 244, 0))
        else:
            self.chk_mongo = wx.CheckBox(self.confPanel, wx.ID_ANY, u"NO", wx.DefaultPosition, wx.DefaultSize, 0)
            self.chk_mongo.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 90, False, wx.EmptyString))
            self.chk_mongo.SetForegroundColour(wx.Colour(255, 128, 0))

        mongoLayout.Add(self.chk_mongo, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        confLayout.Add(mongoLayout, 1, wx.EXPAND, 10)

        pgsqlLayout = wx.BoxSizer(wx.HORIZONTAL)

        self.lbl_pgsql = wx.StaticText(self.confPanel, wx.ID_ANY, u"Almacenar en PostgreSQL :", wx.DefaultPosition,
                                       wx.Size(230, -1), 0)
        self.lbl_pgsql.Wrap(-1)
        self.lbl_pgsql.SetMaxSize(wx.Size(230, -1))

        pgsqlLayout.Add(self.lbl_pgsql, 0, wx.ALL, 5)

        if ConfigThreadsApi().usaPostgreSQL():
            self.chk_pgsql = wx.CheckBox(self.confPanel, wx.ID_ANY, u"SI", wx.DefaultPosition, wx.DefaultSize, 0)
            self.chk_pgsql.SetValue(True)
            self.chk_pgsql.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString))
            self.chk_pgsql.SetForegroundColour(wx.Colour(0, 244, 0))
        else:
            self.chk_pgsql = wx.CheckBox(self.confPanel, wx.ID_ANY, u"NO", wx.DefaultPosition, wx.DefaultSize, 0)
            self.chk_pgsql.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 90, False, wx.EmptyString))
            self.chk_pgsql.SetForegroundColour(wx.Colour(255, 128, 0))

        pgsqlLayout.Add(self.chk_pgsql, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        confLayout.Add(pgsqlLayout, 1, wx.EXPAND, 10)

        timereenvioLayout = wx.BoxSizer(wx.HORIZONTAL)

        self.lbl_timereenvio = wx.StaticText(self.confPanel, wx.ID_ANY, u"Tiempo en horas de Reenvio :",
                                             wx.DefaultPosition, wx.Size(230, -1), 0)
        self.lbl_timereenvio.Wrap(-1)
        self.lbl_timereenvio.SetMaxSize(wx.Size(230, -1))

        timereenvioLayout.Add(self.lbl_timereenvio, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.spn_timereenvio = wx.SpinCtrl(self.confPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                           wx.DefaultSize, wx.SP_ARROW_KEYS, 2, 72, ConfigThreadsApi().getTimeForward())
        timereenvioLayout.Add(self.spn_timereenvio, 0, wx.ALL, 5)

        confLayout.Add(timereenvioLayout, 1, wx.EXPAND, 10)

        serviciosLayout = wx.StaticBoxSizer(wx.StaticBox(self.confPanel, wx.ID_ANY, u"Servicios del ApiClient"),
                                            wx.HORIZONTAL)

        if ConfigThreadsApi().isListening():
            self.tgb_listen = wx.ToggleButton(serviciosLayout.GetStaticBox(), wx.ID_ANY, u"Escuchando emisor",
                                              wx.DefaultPosition, wx.DefaultSize, 0)
            self.tgb_listen.SetValue(True)
        else:
            self.tgb_listen = wx.ToggleButton(serviciosLayout.GetStaticBox(), wx.ID_ANY, u"Sin escuchar emisor",
                                          wx.DefaultPosition, wx.DefaultSize, 0)
        serviciosLayout.Add(self.tgb_listen, 0,
                            wx.ALIGN_CENTER | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL | wx.ALL | wx.EXPAND,
                            10)

        if ConfigThreadsApi().isForwarding():
            self.tgb_forward = wx.ToggleButton(serviciosLayout.GetStaticBox(), wx.ID_ANY, u"Reenvio activo",
                                               wx.DefaultPosition, wx.DefaultSize, 0)
            self.tgb_forward.SetValue(True)
        else:
            self.tgb_forward = wx.ToggleButton(serviciosLayout.GetStaticBox(), wx.ID_ANY, u"Reenvio no activo",
                                           wx.DefaultPosition, wx.DefaultSize, 0)
        serviciosLayout.Add(self.tgb_forward, 0, wx.ALIGN_CENTER | wx.ALIGN_LEFT | wx.ALL | wx.EXPAND | wx.LEFT, 10)

        confLayout.Add(serviciosLayout, 1, wx.EXPAND, 10)

        self.confPanel.SetSizer(confLayout)
        self.confPanel.Layout()
        mainLayout.Add(self.confPanel, 1, wx.EXPAND | wx.ALL, 10)

        self.SetSizer(mainLayout)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.chk_auth.Bind(wx.EVT_CHECKBOX, self.checkAuth)
        self.btn_conectdb.Bind(wx.EVT_BUTTON, self.setConnectDB)
        self.chk_mongo.Bind(wx.EVT_CHECKBOX, self.checkMongo)
        self.chk_pgsql.Bind(wx.EVT_CHECKBOX, self.checkPgsql)
        self.tgb_listen.Bind(wx.EVT_TOGGLEBUTTON, self.onListen)
        self.tgb_forward.Bind(wx.EVT_TOGGLEBUTTON, self.onForward)

    def __del__(self):
        pass

    def OnTaskBarLeftClick(self, evt):
        self.PopupMenu(self.tbicon.CreatePopupMenu())

    # Virtual event handlers, overide them in your derived class
    def checkAuth(self, event):
        viewlogin = ViewLogin(None)
        viewlogin.Show()
        self.tbicon.Destroy()
        self.tbicon.RemoveIcon()
        self.Close()
        event.Skip()

    def setConnectDB(self, event):
        viewConnectdb = ViewConeccionDB(None)
        viewConnectdb.Show()
        self.tbicon.Destroy()
        self.tbicon.RemoveIcon()
        self.Close()
        event.Skip()

    def checkMongo(self, event):
        ConfigThreadsApi().setMongoDB(self.chk_mongo.IsChecked())
        if self.chk_mongo.IsChecked():
            if testConnect("mongo"):
                self.chk_mongo.SetLabelText("SI")
                self.chk_mongo.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString))
                self.chk_mongo.SetForegroundColour(wx.Colour(0, 244, 0))
            else:
                ConfigThreadsApi().setMongoDB(False)
                self.chk_mongo.SetValue(False)
                self.lbl_mensaje.SetLabelText("No se puede establecer conexión con MongoDB")
        else:
            self.chk_mongo.SetLabelText("NO")
            self.chk_mongo.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 90, False, wx.EmptyString))
            self.chk_mongo.SetForegroundColour(wx.Colour(255, 128, 0))
        event.Skip()

    def checkPgsql(self, event):
        ConfigThreadsApi().setPostgreSQL(self.chk_pgsql.IsChecked())
        if self.chk_pgsql.IsChecked():
            if testConnect("pgsql"):
                self.chk_pgsql.SetLabelText("SI")
                self.chk_pgsql.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString))
                self.chk_pgsql.SetForegroundColour(wx.Colour(0, 244, 0))
            else:
                ConfigThreadsApi().setPostgreSQL(False)
                self.chk_pgsql.SetValue(False)
                self.lbl_mensaje.SetLabelText("No se puede establecer conexión con PostgreSQL")
        else:
            self.chk_pgsql.SetLabelText("NO")
            self.chk_pgsql.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 90, False, wx.EmptyString))
            self.chk_pgsql.SetForegroundColour(wx.Colour(255, 128, 0))
        event.Skip()

    def onListen(self, event):
        if self.chk_mongo.IsChecked() or self.chk_pgsql.IsChecked():
            if self.tgb_listen.GetValue():
                self.lbl_mensaje.SetLabelText(wx.EmptyString)
                ConfigThreadsApi().setStopListen(False)
                onListen()
                self.tgb_listen.SetLabelText("Escuchando emisor")
            else:
                ConfigThreadsApi().setStopListen(True)
                self.lbl_mensaje.SetLabelText("El servicio se detendrá dentro de 30 segundos")
                self.tgb_listen.SetLabelText("Sin escuchar emisor")
        else:
            self.tgb_listen.SetValue(False)
            self.lbl_mensaje.SetLabelText("Debe seleccionar al menos una BD")
        event.Skip()

    def onForward(self, event):
        if self.chk_mongo.IsChecked() or self.chk_pgsql.IsChecked():
            if self.tgb_forward.GetValue():
                ConfigThreadsApi().setStopForward(False)
                self.lbl_mensaje.SetLabelText(wx.EmptyString)
                onForward(self.spn_timereenvio.GetValue())
                self.tgb_forward.SetLabelText("Reenvio activo")
            else:
                ConfigThreadsApi().setStopForward(True)
                self.lbl_mensaje.SetLabelText("El servicio se detendrá dentro de %s horas"%(self.spn_timereenvio.GetValue()))
                self.tgb_forward.SetLabelText("Reenvio no activo")
        else:
            self.tgb_forward.SetValue(False)
            self.lbl_mensaje.SetLabelText("Debe seleccionar al menos una BD")
        event.Skip()

    def show_balloon(self, msg):
        print("mostrando mensaje de notificación '%s'" % msg)
        self.tbicon.ShowBalloon("APIfaqtureClient", msg, 6000, wx.ICON_INFORMATION)


class ViewConeccionDB(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"APIfaqtureClient", pos=wx.DefaultPosition,
                          size=wx.Size(500, 420), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        ico = wx.Icon(u"./resources/images/faqture_24x24.png", wx.BITMAP_TYPE_PNG)
        self.SetIcon(ico)

        connectLayout = wx.BoxSizer(wx.VERTICAL)

        self.connectContainer = wx.aui.AuiNotebook(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                                   wx.aui.AUI_NB_DEFAULT_STYLE)
        self.connectContainer.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))

        self.emisorPanel = wx.Panel(self.connectContainer, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                    wx.TAB_TRAVERSAL)
        emisordbLayout = wx.BoxSizer(wx.VERTICAL)

        motordbemisorLayout = wx.BoxSizer(wx.HORIZONTAL)

        self.lbl_motordbemisor = wx.StaticText(self.emisorPanel, wx.ID_ANY, u"Motor de base de datos :",
                                               wx.DefaultPosition, wx.Size(250, -1), 0)
        self.lbl_motordbemisor.Wrap(-1)
        self.lbl_motordbemisor.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString))
        self.lbl_motordbemisor.SetMinSize(wx.Size(250, -1))

        motordbemisorLayout.Add(self.lbl_motordbemisor, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        cho_motordbemisorChoices = [u"PostgreSQL"]
        self.cho_motordbemisor = wx.Choice(self.emisorPanel, wx.ID_ANY, wx.DefaultPosition, wx.Size(180, -1),
                                           cho_motordbemisorChoices, 0)
        if SourceDBemisor().getDBMotor() == "pgsql":
            self.cho_motordbemisor.SetSelection(0)
        self.cho_motordbemisor.SetMinSize(wx.Size(180, -1))

        motordbemisorLayout.Add(self.cho_motordbemisor, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        emisordbLayout.Add(motordbemisorLayout, 1, wx.EXPAND, 5)

        hostdbemisorLayout = wx.BoxSizer(wx.HORIZONTAL)

        self.lbl_hostdbemisor = wx.StaticText(self.emisorPanel, wx.ID_ANY, u"Server host :", wx.DefaultPosition,
                                              wx.Size(250, -1), 0)
        self.lbl_hostdbemisor.Wrap(-1)
        self.lbl_hostdbemisor.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString))
        self.lbl_hostdbemisor.SetMinSize(wx.Size(250, -1))

        hostdbemisorLayout.Add(self.lbl_hostdbemisor, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        hp = SourceDBemisor().getHostPort()

        self.etx_hostdbemisor = wx.TextCtrl(self.emisorPanel, wx.ID_ANY, hp['host'], wx.DefaultPosition,
                                            wx.Size(180, -1), 0)
        self.etx_hostdbemisor.SetMinSize(wx.Size(180, -1))

        hostdbemisorLayout.Add(self.etx_hostdbemisor, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        emisordbLayout.Add(hostdbemisorLayout, 1, wx.EXPAND, 5)

        portdbemisorLayout = wx.BoxSizer(wx.HORIZONTAL)

        self.lbl_portdbemisor = wx.StaticText(self.emisorPanel, wx.ID_ANY, u"Server port :", wx.DefaultPosition,
                                              wx.Size(250, -1), 0)
        self.lbl_portdbemisor.Wrap(-1)
        self.lbl_portdbemisor.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString))
        self.lbl_portdbemisor.SetMinSize(wx.Size(250, -1))

        portdbemisorLayout.Add(self.lbl_portdbemisor, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.etx_portdbemisor = wx.TextCtrl(self.emisorPanel, wx.ID_ANY, hp['port'], wx.DefaultPosition,
                                            wx.Size(180, -1), 0)
        self.etx_portdbemisor.SetMinSize(wx.Size(180, -1))

        portdbemisorLayout.Add(self.etx_portdbemisor, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        emisordbLayout.Add(portdbemisorLayout, 1, wx.EXPAND, 5)

        dbnamedbemisorLayout = wx.BoxSizer(wx.HORIZONTAL)

        self.lbl_dbnamedbemisor = wx.StaticText(self.emisorPanel, wx.ID_ANY, u"Nombre de la base de datos :",
                                                wx.DefaultPosition, wx.Size(250, -1), 0)
        self.lbl_dbnamedbemisor.Wrap(-1)
        self.lbl_dbnamedbemisor.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString))
        self.lbl_dbnamedbemisor.SetMinSize(wx.Size(250, -1))

        dbnamedbemisorLayout.Add(self.lbl_dbnamedbemisor, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.etx_dbnamedbemisor = wx.TextCtrl(self.emisorPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                              wx.Size(180, -1), 0)
        self.etx_dbnamedbemisor.SetMinSize(wx.Size(180, -1))
        self.etx_dbnamedbemisor.SetHint(u"[Default - Cambie si desea]")

        dbnamedbemisorLayout.Add(self.etx_dbnamedbemisor, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        emisordbLayout.Add(dbnamedbemisorLayout, 1, wx.EXPAND, 5)

        schemadbemisorLayout = wx.BoxSizer(wx.HORIZONTAL)

        self.lbl_schemadbemisor = wx.StaticText(self.emisorPanel, wx.ID_ANY, u"Nombre del esquema a usar en BD :",
                                                wx.DefaultPosition, wx.Size(250, -1), 0)
        self.lbl_schemadbemisor.Wrap(-1)
        self.lbl_schemadbemisor.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString))
        self.lbl_schemadbemisor.SetMinSize(wx.Size(250, -1))

        schemadbemisorLayout.Add(self.lbl_schemadbemisor, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.etx_schemadbemisor = wx.TextCtrl(self.emisorPanel, wx.ID_ANY, SourceDBemisor().getSchema(), wx.DefaultPosition,
                                              wx.Size(180, -1), 0)
        self.etx_schemadbemisor.SetMinSize(wx.Size(180, -1))

        schemadbemisorLayout.Add(self.etx_schemadbemisor, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        emisordbLayout.Add(schemadbemisorLayout, 1, wx.EXPAND, 5)

        dbuserdbemisorLayout = wx.BoxSizer(wx.HORIZONTAL)

        self.lbl_dbuserdbemisor = wx.StaticText(self.emisorPanel, wx.ID_ANY, u"Usuario de conexión a BD :",
                                                wx.DefaultPosition, wx.Size(250, -1), 0)
        self.lbl_dbuserdbemisor.Wrap(-1)
        self.lbl_dbuserdbemisor.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString))
        self.lbl_dbuserdbemisor.SetMinSize(wx.Size(250, -1))

        dbuserdbemisorLayout.Add(self.lbl_dbuserdbemisor, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.etx_dbuserdbemisor = wx.TextCtrl(self.emisorPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                              wx.Size(180, -1), 0)
        self.etx_dbuserdbemisor.SetMinSize(wx.Size(180, -1))
        self.etx_dbuserdbemisor.SetHint(u"[Default - Cambie si desea]")

        dbuserdbemisorLayout.Add(self.etx_dbuserdbemisor, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        emisordbLayout.Add(dbuserdbemisorLayout, 1, wx.EXPAND, 5)

        dbupassdbemisorLayout = wx.BoxSizer(wx.HORIZONTAL)

        self.lbl_dbupassdbemisor = wx.StaticText(self.emisorPanel, wx.ID_ANY, u"Contraseña de conexión a BD :",
                                                 wx.DefaultPosition, wx.Size(250, -1), 0)
        self.lbl_dbupassdbemisor.Wrap(-1)
        self.lbl_dbupassdbemisor.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString))
        self.lbl_dbupassdbemisor.SetMinSize(wx.Size(250, -1))

        dbupassdbemisorLayout.Add(self.lbl_dbupassdbemisor, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.etx_dbupassdbemisor = wx.TextCtrl(self.emisorPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                               wx.Size(180, -1), 0)
        self.etx_dbupassdbemisor.SetMinSize(wx.Size(180, -1))
        self.etx_dbupassdbemisor.SetHint(u"[Default - Cambie si desea]")

        dbupassdbemisorLayout.Add(self.etx_dbupassdbemisor, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        emisordbLayout.Add(dbupassdbemisorLayout, 1, wx.EXPAND, 5)

        self.btn_dbemisor = wx.Button(self.emisorPanel, wx.ID_ANY, u"Guardar", wx.DefaultPosition, wx.DefaultSize, 0)
        emisordbLayout.Add(self.btn_dbemisor, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        self.emisorPanel.SetSizer(emisordbLayout)
        self.emisorPanel.Layout()
        emisordbLayout.Fit(self.emisorPanel)
        self.connectContainer.AddPage(self.emisorPanel, u"ConnectEmisorDB", True, wx.NullBitmap)
        self.pgsqlPanel = wx.Panel(self.connectContainer, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                   wx.TAB_TRAVERSAL)
        pgsqlLayout = wx.BoxSizer(wx.VERTICAL)

        hostpgsqlLayout = wx.BoxSizer(wx.HORIZONTAL)

        self.lbl_hostpgsql = wx.StaticText(self.pgsqlPanel, wx.ID_ANY, u"Server host :", wx.DefaultPosition,
                                           wx.Size(250, -1), 0)
        self.lbl_hostpgsql.Wrap(-1)
        self.lbl_hostpgsql.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString))
        self.lbl_hostpgsql.SetMinSize(wx.Size(250, -1))

        hostpgsqlLayout.Add(self.lbl_hostpgsql, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        hp = SourceAPIpgsql().getHostPort()

        self.etx_hostpgsql = wx.TextCtrl(self.pgsqlPanel, wx.ID_ANY, hp['host'], wx.DefaultPosition,
                                         wx.Size(180, -1), 0)
        self.etx_hostpgsql.SetMinSize(wx.Size(180, -1))

        hostpgsqlLayout.Add(self.etx_hostpgsql, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        pgsqlLayout.Add(hostpgsqlLayout, 1, wx.EXPAND, 5)

        portpgsqlLayout = wx.BoxSizer(wx.HORIZONTAL)

        self.lbl_portpgsql = wx.StaticText(self.pgsqlPanel, wx.ID_ANY, u"Server port :", wx.DefaultPosition,
                                           wx.Size(250, -1), 0)
        self.lbl_portpgsql.Wrap(-1)
        self.lbl_portpgsql.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString))
        self.lbl_portpgsql.SetMinSize(wx.Size(250, -1))

        portpgsqlLayout.Add(self.lbl_portpgsql, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.etx_portpgsql = wx.TextCtrl(self.pgsqlPanel, wx.ID_ANY, hp['port'], wx.DefaultPosition,
                                         wx.Size(180, -1), 0)
        self.etx_portpgsql.SetMinSize(wx.Size(180, -1))

        portpgsqlLayout.Add(self.etx_portpgsql, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        pgsqlLayout.Add(portpgsqlLayout, 1, wx.EXPAND, 5)

        dbnamepgsqlLayout = wx.BoxSizer(wx.HORIZONTAL)

        self.lbl_dbnamepgsql = wx.StaticText(self.pgsqlPanel, wx.ID_ANY, u"Nombre de la base de datos :",
                                             wx.DefaultPosition, wx.Size(250, -1), 0)
        self.lbl_dbnamepgsql.Wrap(-1)
        self.lbl_dbnamepgsql.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString))
        self.lbl_dbnamepgsql.SetMinSize(wx.Size(250, -1))

        dbnamepgsqlLayout.Add(self.lbl_dbnamepgsql, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.etx_dbnamepgsql = wx.TextCtrl(self.pgsqlPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                           wx.Size(180, -1), 0)
        self.etx_dbnamepgsql.SetMinSize(wx.Size(180, -1))
        self.etx_dbnamepgsql.SetHint(u"[Default - Cambie si desea]")

        dbnamepgsqlLayout.Add(self.etx_dbnamepgsql, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        pgsqlLayout.Add(dbnamepgsqlLayout, 1, wx.EXPAND, 5)

        schemapgsqlLayout = wx.BoxSizer(wx.HORIZONTAL)

        self.lbl_schemapgsql = wx.StaticText(self.pgsqlPanel, wx.ID_ANY, u"Nombre del esquema a usar en BD :",
                                             wx.DefaultPosition, wx.Size(250, -1), 0)
        self.lbl_schemapgsql.Wrap(-1)
        self.lbl_schemapgsql.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString))
        self.lbl_schemapgsql.SetMinSize(wx.Size(250, -1))

        schemapgsqlLayout.Add(self.lbl_schemapgsql, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.etx_schemapgsql = wx.TextCtrl(self.pgsqlPanel, wx.ID_ANY, SourceAPIpgsql().getSchema(), wx.DefaultPosition,
                                           wx.Size(180, -1), 0)
        self.etx_schemapgsql.SetMinSize(wx.Size(180, -1))

        schemapgsqlLayout.Add(self.etx_schemapgsql, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        pgsqlLayout.Add(schemapgsqlLayout, 1, wx.EXPAND, 5)

        dbuserpgsqlLayout = wx.BoxSizer(wx.HORIZONTAL)

        self.lbl_dbuserpgsql = wx.StaticText(self.pgsqlPanel, wx.ID_ANY, u"Usuario de conexión a BD :",
                                             wx.DefaultPosition, wx.Size(250, -1), 0)
        self.lbl_dbuserpgsql.Wrap(-1)
        self.lbl_dbuserpgsql.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString))
        self.lbl_dbuserpgsql.SetMinSize(wx.Size(250, -1))

        dbuserpgsqlLayout.Add(self.lbl_dbuserpgsql, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.etx_dbuserpgsql = wx.TextCtrl(self.pgsqlPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                           wx.Size(180, -1), 0)
        self.etx_dbuserpgsql.SetMinSize(wx.Size(180, -1))
        self.etx_dbuserpgsql.SetHint(u"[Default - Cambie si desea]")

        dbuserpgsqlLayout.Add(self.etx_dbuserpgsql, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        pgsqlLayout.Add(dbuserpgsqlLayout, 1, wx.EXPAND, 5)

        dbupasspgsqlLayout = wx.BoxSizer(wx.HORIZONTAL)

        self.lbl_dbupasspgsql = wx.StaticText(self.pgsqlPanel, wx.ID_ANY, u"Contraseña de conexión a BD :",
                                              wx.DefaultPosition, wx.Size(250, -1), 0)
        self.lbl_dbupasspgsql.Wrap(-1)
        self.lbl_dbupasspgsql.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString))
        self.lbl_dbupasspgsql.SetMinSize(wx.Size(250, -1))

        dbupasspgsqlLayout.Add(self.lbl_dbupasspgsql, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.etx_dbupasspgsql = wx.TextCtrl(self.pgsqlPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                            wx.Size(180, -1), 0)
        self.etx_dbupasspgsql.SetMinSize(wx.Size(180, -1))
        self.etx_dbupasspgsql.SetHint(u"[Default - Cambie si desea]")

        dbupasspgsqlLayout.Add(self.etx_dbupasspgsql, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        pgsqlLayout.Add(dbupasspgsqlLayout, 1, wx.EXPAND, 5)

        self.btn_pgsql = wx.Button(self.pgsqlPanel, wx.ID_ANY, u"Guardar", wx.DefaultPosition, wx.DefaultSize, 0)
        pgsqlLayout.Add(self.btn_pgsql, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        self.pgsqlPanel.SetSizer(pgsqlLayout)
        self.pgsqlPanel.Layout()
        pgsqlLayout.Fit(self.pgsqlPanel)
        self.connectContainer.AddPage(self.pgsqlPanel, u"ConnectAPIpgsql", False, wx.NullBitmap)
        self.mongoPanel = wx.Panel(self.connectContainer, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                   wx.TAB_TRAVERSAL)
        mongoLayout = wx.BoxSizer(wx.VERTICAL)

        pgsqlLayout1 = wx.BoxSizer(wx.VERTICAL)

        hostmongoLayout = wx.BoxSizer(wx.HORIZONTAL)

        self.lbl_hostmongo = wx.StaticText(self.mongoPanel, wx.ID_ANY, u"Server host :", wx.DefaultPosition,
                                           wx.Size(250, -1), 0)
        self.lbl_hostmongo.Wrap(-1)
        self.lbl_hostmongo.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString))
        self.lbl_hostmongo.SetMinSize(wx.Size(250, -1))

        hostmongoLayout.Add(self.lbl_hostmongo, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        dsn = SourceAPImongo().getDataSourceConnection()

        self.etx_hostmongo = wx.TextCtrl(self.mongoPanel, wx.ID_ANY, dsn['host'], wx.DefaultPosition,
                                         wx.Size(180, -1), 0)
        self.etx_hostmongo.SetMinSize(wx.Size(180, -1))

        hostmongoLayout.Add(self.etx_hostmongo, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        pgsqlLayout1.Add(hostmongoLayout, 1, wx.EXPAND, 5)

        portmongoLayout = wx.BoxSizer(wx.HORIZONTAL)

        self.lbl_portmongo = wx.StaticText(self.mongoPanel, wx.ID_ANY, u"Server port :", wx.DefaultPosition,
                                           wx.Size(250, -1), 0)
        self.lbl_portmongo.Wrap(-1)
        self.lbl_portmongo.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString))
        self.lbl_portmongo.SetMinSize(wx.Size(250, -1))

        portmongoLayout.Add(self.lbl_portmongo, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.etx_portmongo = wx.TextCtrl(self.mongoPanel, wx.ID_ANY, dsn['port'], wx.DefaultPosition,
                                         wx.Size(180, -1), 0)
        self.etx_portmongo.SetMinSize(wx.Size(180, -1))

        portmongoLayout.Add(self.etx_portmongo, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        pgsqlLayout1.Add(portmongoLayout, 1, wx.EXPAND, 5)

        dbusermongoLayout = wx.BoxSizer(wx.HORIZONTAL)

        self.lbl_dbusermongo = wx.StaticText(self.mongoPanel, wx.ID_ANY, u"Usuario de conexión a BD :",
                                             wx.DefaultPosition, wx.Size(250, -1), 0)
        self.lbl_dbusermongo.Wrap(-1)
        self.lbl_dbusermongo.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString))
        self.lbl_dbusermongo.SetMinSize(wx.Size(250, -1))

        dbusermongoLayout.Add(self.lbl_dbusermongo, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.etx_dbusermongo = wx.TextCtrl(self.mongoPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                           wx.Size(180, -1), 0)
        self.etx_dbusermongo.SetMinSize(wx.Size(180, -1))
        self.etx_dbusermongo.SetHint(u"[Default - Cambie si desea]")

        dbusermongoLayout.Add(self.etx_dbusermongo, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        pgsqlLayout1.Add(dbusermongoLayout, 1, wx.EXPAND, 5)

        dbupassmongoLayout = wx.BoxSizer(wx.HORIZONTAL)

        self.lbl_dbupassmongo = wx.StaticText(self.mongoPanel, wx.ID_ANY, u"Contraseña de conexión a BD :",
                                              wx.DefaultPosition, wx.Size(250, -1), 0)
        self.lbl_dbupassmongo.Wrap(-1)
        self.lbl_dbupassmongo.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString))
        self.lbl_dbupassmongo.SetMinSize(wx.Size(250, -1))

        dbupassmongoLayout.Add(self.lbl_dbupassmongo, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.etx_dbupassmongo = wx.TextCtrl(self.mongoPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                            wx.Size(180, -1), 0)
        self.etx_dbupassmongo.SetMinSize(wx.Size(180, -1))
        self.etx_dbupassmongo.SetHint(u"[Default - Cambie si desea]")

        dbupassmongoLayout.Add(self.etx_dbupassmongo, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        pgsqlLayout1.Add(dbupassmongoLayout, 1, wx.EXPAND, 5)

        mongoLayout.Add(pgsqlLayout1, 1, wx.EXPAND, 5)

        self.btn_mongo = wx.Button(self.mongoPanel, wx.ID_ANY, u"Guardar", wx.DefaultPosition, wx.DefaultSize, 0)
        mongoLayout.Add(self.btn_mongo, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        self.mongoPanel.SetSizer(mongoLayout)
        self.mongoPanel.Layout()
        mongoLayout.Fit(self.mongoPanel)
        self.connectContainer.AddPage(self.mongoPanel, u"ConnectAPImongo", False, wx.NullBitmap)

        connectLayout.Add(self.connectContainer, 1, wx.EXPAND | wx.ALL, 0)

        self.SetSizer(connectLayout)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.Bind(wx.EVT_CLOSE, self.cerrarConnectDB)
        self.btn_dbemisor.Bind(wx.EVT_BUTTON, self.guardaDBemisor)
        self.btn_pgsql.Bind(wx.EVT_BUTTON, self.guardaDBpgsql)
        self.btn_mongo.Bind(wx.EVT_BUTTON, self.guardaDBmongo)

    def __del__(self):
        pass

    def cerrarConnectDB(self, event):
        viewConf = ViewConfigurations(None)
        viewConf.Show()
        event.Skip()

    # Virtual event handlers, overide them in your derived class
    def guardaDBemisor(self, event):
        if self.cho_motordbemisor.Selection == 0:
            SourceDBemisor().setDBMotor("pgsql")
            print("motor emisor guardados")

        host = self.etx_hostdbemisor.GetValue()
        port = self.etx_portdbemisor.GetValue()
        if host and host.strip() != "" and port and port.strip() != "":
            SourceDBemisor().setHostPort(host, port)
            print("host y port emisor guardados")

        if self.etx_schemadbemisor.GetValue() and self.etx_schemadbemisor.GetValue().strip() !="":
            SourceDBemisor().setSchema(self.etx_schemadbemisor.GetValue())
            print("schema emisor guardados")

        bdname = self.etx_dbnamedbemisor.GetValue()
        user = self.etx_dbuserdbemisor.GetValue()
        upass = self.etx_dbupassdbemisor.GetValue()
        if bdname and bdname.strip() != "" and user and user.strip() != "" and upass and upass.strip() != "":
            SourceDBemisor().setDBmainConnect(bdname, user, upass)
            print("dbname, dbuser y dbpassword emisor guardados")
        event.Skip()

    def guardaDBpgsql(self, event):
        host = self.etx_hostpgsql.GetValue()
        port = self.etx_portpgsql.GetValue()
        if host and host.strip() != "" and port and port.strip() != "":
            SourceAPIpgsql().setHostPort(host, port)
            print("host y port pgsql guardados")

        if self.etx_schemapgsql.GetValue() and self.etx_schemapgsql.GetValue().strip() != "":
            SourceAPIpgsql().setSchema(self.etx_schemapgsql.GetValue())
            print("schema pgsql guardados")

        bdname = self.etx_dbnamepgsql.GetValue()
        user = self.etx_dbuserpgsql.GetValue()
        upass = self.etx_dbupasspgsql.GetValue()
        if bdname and bdname.strip() != "" and user and user.strip() != "" and upass and upass.strip() != "":
            SourceAPIpgsql().setDBmainConnect(bdname, user, upass)
            print("dbname, dbuser y dbpassword pgsql guardados")
        event.Skip()

    def guardaDBmongo(self, event):
        host = self.etx_hostmongo.GetValue()
        port = self.etx_portmongo.GetValue()
        if host and host.strip() != "" and port and port.strip() != "":
            SourceAPImongo().setDataSourceConnection(host, port, self.etx_dbusermongo.GetValue(),
                                                     self.etx_dbupassmongo.GetValue())
            print("datos de la conexión a MongoDB guardados")
        event.Skip()