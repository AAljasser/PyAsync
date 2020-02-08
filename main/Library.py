from IndState import IndState as iD
from main.Patreon import Patreon

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Library(metaclass=Singleton):
    pass
    #Patreons users and passwords stored
    instance = None
    _patreon = {'p1000':Patreon('p1000','abdul')}
    _staff = ['s1000']
    _admin = 'admin'


    def userLogin(self,info):
        name = None
        oIfo = None
        if len(info) > 1:
            name = info[0]
            oIfo = info[1]
        else:
            name = info[0]
        if name.casefold() == 'admin':
            return iD.A_MENU
        elif name.casefold() == 'staff':
            if self.staffExists(oIfo):
                return iD.S_MENU
            else:
                return iD.INCORRECT_INPUT
        elif name.casefold() == 'patreon':
            return iD.P_MENU
        else:
            return iD.INCORRECT_INPUT

    def createStaff(self,id):
        self._staff.append(id.casefold())
    def createPatreon(self, id, name):
        self._patreon[id]=Patreon(id,name)
    def patreonExists(self,id):
        return id.casefold() in self._patreon.keys()
    def staffExists(self,id):
        return id.casefold() in self._staff