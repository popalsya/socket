from .model import Model

class View:
    def __init__(self, websocket):
        self.model = Model()
        self.websocket = websocket

    def onmessage(self, **data):
        print('message')
        print(data)
        #new message
        return

    def onconnect(self, **data):
        print('connection accept')
        print(data)
        #connection accept
        return

    def onclose(self, **data):
        print('close')
        print(data)
        #connection closed
        return
