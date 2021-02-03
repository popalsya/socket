import sys, os
from websocket.websocket import WebSocket

def new_app():
    app_name = 'myapp' if len(sys.argv) < 3 else sys.argv[2]
    if os.path.exists(app_name):
        print('app already exists')
        sys.exit()

    os.makedirs(app_name)
    create_files(app_name)

    print('start app', app_name)


def create_files(app_name):
    with open('websocket/templates/model.py', 'r') as model:
        model_data = model.read()

    with open(app_name + '/model.py', 'w') as new_model:
        new_model.write(model_data)

    with open('websocket/templates/view.py', 'r') as view:
        view_data = view.read()

    with open(app_name + '/view.py', 'w') as new_view:
        new_view.write(view_data)


def run_server():
    address = '0.0.0.0'
    port = 5000 if len(sys.argv) < 3 else sys.argv[2]

    ws = WebSocket()
    ws.server(int(port))
    print('run server on', address, ':', port)
    ws.listen()


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('ploho')
        sys.exit()

    function = sys.argv[1]

    if function == 'newapp':
        new_app()

    elif function == 'runserver':
        run_server()

    else:
        print('unexpected function')
        sys.exit()
