from IndState import IndState as iD

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
    _patreon = ['p1000']
    _staff = ['s1000']
    _admin = 'admin'


    def userLogin(selfs,info):
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
            #TODO: CHECK IF THE STAFF IDENTIFIED EXISTS
            return iD.INCORRECT_INPUT
        else:
            #TODO: Check if the associated patreon exists
            return iD.INCORRECT_INPUT

    def createStaff(self,id):
        self._staff.append(id.casefold())
    def staffExists(self,id):
        return id.casefold() in self._staff