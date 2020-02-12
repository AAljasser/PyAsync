class Book():
    _id = None
    _title = None

    def __init__(self,title,id):
        self._id = id
        self._title = title
    def get_id(self):
        return self._id
    def get_title(self):
        return self._title