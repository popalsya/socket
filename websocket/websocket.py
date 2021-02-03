import selectors
import socket

import struct

from .model import WebSocketModel
from . import settings


class WebSocket:
    selector = selectors.DefaultSelector()
    apps = {}

    def __init__(self):
        self.model = WebSocketModel()

    def server(self, port = 5000):
        self.port = port

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(('0.0.0.0', self.port))

        self.server_socket.listen()
        self.selector.register(self.server_socket, selectors.EVENT_READ, self.server_event)

        self.initial_apps()


    def listen(self):
        while True:
            events = self.selector.select()

            for key, _ in events:
                callback = key.data
                callback(key.fileobj)


    def server_event(self, socket):
        connection, address = socket.accept()
        self.model.register_client(connection, address)
        self.selector.register(connection, selectors.EVENT_READ, self.client_event)


    def client_event(self, connection):
        request = connection.recv(1024)

        if not request:
            self.onclose(client = connection)
            self.model.close_connection(connection)
            self.selector.unregister(connection)
            return

        if not self.model.accepted(connection):
            query = self.model.process_browser_request(request)

            if settings.handshake:
                self.model.accept_connection(connection, query[settings.security_key])
            else:
                self.model.client[connection]['accepted'] = True

            self.onconnect(client = connection, request = query)
            return

        if self.model.is_close_connection_code(request):
            return

        message = self.model.unpack_frame(request)
        self.onmessage(client = connection, message = message)


    def send(self, connection, message):
        connection.send(self.model.pack_frame(message))

    def onconnect(self, **request):
        connection = request['client']
        app = request['request']['app']

        if not self.apps.get(app):
            connection.send(b'unknown app\n')
            self.model.close_connection(connection)
            self.selector.unregister(connection)
            return

        self.model.client[connection]['app'] = app

        view = self.apps[app]

        view.onconnect(
            client = self.model.client[connection]['address'],
            connection = connection,
            request = request['request']['app'],
            data = None if not settings.client_data else request['request'][settings.client_data],
        )


    def onmessage(self, **data):
        app = self.model.client[ data['client'] ]['app']
        view = self.apps[app]
        view.onmessage(
            client = self.model.client[ data['client'] ]['address'],
            connection = data['client'],
            message = data['message'].decode(),
        )

    def onclose(self, **data):
        app = self.model.client[ data['client'] ]['app']
        view = self.apps[app]

        view.onclose(
            client = self.model.client[ data['client'] ]['address']
        )


    def initial_apps(self):
        for key, app in settings.apps.items():
            self.apps[key] = app(self)
