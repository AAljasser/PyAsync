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
    _patreon = {}
    _staff = {}
    _admin = 'admin'


    def userLogin(selfs,info):
        name = None
        oIfo = None
        if ',' in info:
            logInfo = info.split(',')
            name = logInfo[0]
            oIfo = logInfo[1]
        else:
            name = info
        if name.casefold() == 'admin':
            return iD.A_MENU
        elif name.casefold() == 'staff':
            #TODO: CHECK IF THE STAFF IDENTIFIED EXISTS
            return iD.INCORRECT_INPUT
        else:
            #TODO: Check if the associated patreon exists
            return iD.INCORRECT_INPUT