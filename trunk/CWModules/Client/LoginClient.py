#Handles user login to the CodeWorld server.
import pyui
from pyui.dialogs import LineDisplay
from pyui.widgets import Button, FormPanel, Panel, Window

from CWModules import Events, Network, User
from CWModules.Client import Core, ScreenUtils

class LoginWindow(Window):
    def __init__(self, x, y, w, h, topmost = 0):
        Window.__init__(self, x, y, w, h, topmost)
        self.setLayout(pyui.layouts.BorderLayoutManager())

        fields = [
            ('string', 'user', 'Name:', 24, 5),
            ('password', 'pass', 'Password:', 24, 5)
            ]

        self.form = FormPanel(fields)
        self.form.widget_user.handler = self.doLogin
        self.form.widget_pass.handler = self.doLogin

        self.registerEvent(pyui.locals.KEYDOWN, self._pyuiKeyDown)
        
        self.login = Button('Login', self.doLogin)
        self.create = Button('Create Account', self.doLogin)
        
        self.botPanel = Panel()
        self.botPanel.addChild(self.login)
        self.botPanel.addChild(self.create)
        
        self.addChild(self.form, pyui.locals.CENTER)
        self.addChild(self.botPanel, pyui.locals.SOUTH)
        self.pack()

        self.form.widget_user.getFocus()

    def _pyuiKeyDown(self, event):
        if event.key == pyui.locals.K_TAB:
            if event.mods & pyui.locals.MOD_SHIFT:
                self.form.nextTab(-1)
            else:
                self.form.nextTab(+1)
            return 1
        return 0

    def doLogin(self, widget):
        name = self.form.widget_user.text
        pwd = self.form.widget_pass.text

        Events.do('showConsole')

        print "Opening stream socket..."
        tcp = Network.TCPSocket()
        try:
            tcp.connect(Network.serverAddress)
        except:
            print "Could not connect to server."
            print "The server could be down.  Try again later."
            tcp.close()
            return 1
        
        print "Opening datagram socket..."
        udp = Network.UDPSocket()
        tcp.write('bindUDP %i\n' % udp.getsockname()[1])
        
        newUser = User.User(tcp, udp)
        newUser.name = name
        newUser.pwd = pwd
        if(widget == self.create):
            newUser.isNewUser = True

        self.destroy()
        return 1

def init():
    x, y = ScreenUtils.center(350, 90)
    LoginWindow(x, y, 350, 90)

def login(user, command = ''):
    if(command == 'user'):
        print "Sending username..."
        if(user.isNewUser):
            user.tcp.write('login newuser ' + user.name + '\n')
        else:
            user.tcp.write('login user ' + user.name + '\n')
    elif(command == 'pass'):
        print "Sending password..."
        user.tcp.write('login pass ' + user.pwd + '\n')
    elif(command == 'ok'):
        print "Login successful!"
        Core.user = user
        Events.do('hideConsole')
        Events.do('start')
    elif(command == 'badpass'):
        print "Login incorrect.  Bad user/password info."
        user.closeAll()
        init()
    elif(command == 'userdup'):
        print "That username is taken.  Please choose another."
        user.closeAll()
        init()
    elif(command[:6] == 'bindUDP'):
        print "Binding game datagram socket..."
        user.udp.connect((Network.serverAddress[0], int(command[8:])))
        user.tcp.write('login bindUDP ' + user.udp.getsockname()[1])
    else:
        print "An unknown error occured."
        init()
        user.closeAll()
        
        
def logout(user):
    pass
