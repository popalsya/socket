from websocket.base.view.base_view import BaseView
import re

class View(BaseView):
    def onmessage(self, **data):
        print('message')
        print(data)
        print('')
        #new message
        return

    def onconnect(self, **data):
        print('connection accepted')
        print(data)
        print('')
        #connection accept
        return

    def onclose(self, **data):
        print('close')
        print(data)
        #connection closed
        #custom close connection
        return
