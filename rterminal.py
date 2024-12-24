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
    if(message['userid']==target_userid and message['type']=="rcommand"):
       print(f"{message["message"]}>",end = "")
    # elif (message["type"]=="status"):
    #     print(f"{message['userid']} {message['message']}")
    #     print("------------------------")

if __name__ == "__main__":
    target_userid = input("enter your target userid: ")
    server_address = "http://192.168.1.7:8080"
    sio.connect(server_address)
    sio.emit("ichooseu",target_userid)
    while True:
        message = input()
        json = {"userid":target_userid,"message":message,"type":"command"}
        if message == "exit":
            break
        sio.emit("message", json) 

    sio.disconnect()