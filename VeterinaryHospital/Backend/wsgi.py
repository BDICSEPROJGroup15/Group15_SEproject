from src.extension import socketio
from src import app
if __name__ == '__main__':
	socketio.run(app,host='0.0.0.0')
