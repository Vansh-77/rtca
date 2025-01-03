from flask import Flask , render_template 
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

@app.route("/")
def home():
    return render_template("index.html")

@socketio.on("message") 
def handle_message(message):
    print(f"{message['userid']}: {message['message']}")
    socketio.emit("message",message)

@socketio.on("connection")
def handle_connection(userid):
    print(f"{userid} joined the chat")
    socketio.emit("message",{"userid":userid,"message":"joined the chat","type":"status"})

@socketio.on("ichooseu")
def ichooseu(userid):
    socketio.emit("ichooseu",userid)

if __name__ == "__main__":
    
    socketio.run(app)


