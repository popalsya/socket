
# installed apps
# import app's class View
# set 'app': AppView

from myapp.view import View as MyAppView
from messager.view import View as MessagerView

apps = {
    'myapp': MyAppView,
    'messager': MessagerView,
}


# type of request from client
# http or custom

# all of requests should be look like string 'key: value\r\nkey: value'
# where '\r\n' is delimeter

http_registrations_request = True
regustrations_request_delimeter = '\r\n'


# server gets Sec-WebSocket-Key from http request
# prepares him and send answer

# key looks like dGhlIHNhbXBsZSBub25jZQ==
# server answer s3pPLMBiTxaQ9kYGzzhZRbK+xOo=
# algorithm in websocket.model.create_answer

# !!! first message always processing like register request
# required variables app name as 'app: app_name'

handshake = True


# variable key with security key that uses for handshake
# Sec-WebSocket-Key in browser as example

security_key = 'Sec-WebSocket-Key'


# variable key with client data
# Cookie in browser as example

# this data transmited to 'onconnect' function
# None if it is not necessary

client_data = 'Cookie'
client_data = None
