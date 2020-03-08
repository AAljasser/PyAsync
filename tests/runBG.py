import threading
from main.sServer import sServer

class runBG():
    def __init__(self):
        x = BG()
        x.start()

class BG(threading.Thread):
    _server =None
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        self._server = sServer()


def main():
    x = runBG()
    print("TRUE)")


if __name__ == '__main__':
    main()