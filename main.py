from app import *

app = create_app()

socketio = SocketIO(app, cors_allowed_origins='*')
socketio.on_namespace(Chat('/talk'))
socketio.run(app, host='0.0.0.0', debug=True)