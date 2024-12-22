import socketio

sio = socketio.Client()
@sio.event()
def connect():
    print("Connected to the server")
    print("------------------------")

@sio.event()
def disconnect():
    print("Disconnected")
    print("------------------------")

@sio.event()
def message(message):
    if (message['userid']!=myuserid and message["type"]=="message"):
        print(f"{message['userid']}: {message['message']}")
        print("------------------------")
    elif (message['userid']!=myuserid and message["type"]=="status"):
        print(f"{message['userid']} {message['message']}")
        print("------------------------")

if __name__ == "__main__":
    myuserid = input("enter your userid: ")
    server_address = "http://192.168.1.7:8080"
    sio.connect(server_address)
    sio.emit("connection",myuserid)
    while True:
        message = input()
        print("------------------------")
        json = {"userid":myuserid,"message":message,"type":"message"}
        if message == "exit":
            sio.emit("message",{"userid":myuserid,"message":"left the chat","type":"status"})
            break
        sio.emit("message", json) 

    sio.disconnect()
