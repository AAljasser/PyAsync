class Library(object):
    class __singleInstance:
        def __init__(self):
            #Singleton variables
            self.att = None


    #Public library attributes
    instance = None

    #Python provide __NEW__ to allow for singleton class object
    def __new__(cls):
        if not Library.instance:
            Library.instance = Library.__singleInstance()
        return Library.instance
    #This will allow us to modify singleton attributes
    def __getattr__(self, item):
        return getattr(self.instance,item)
    def __setattr__(self, item):
        return getattr(self.instance,item)