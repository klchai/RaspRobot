import sys
import socket
import threading

robots = {}

COMMANDS = ["forward", "backward", "left", "right","speed"]

sockrobot = None

def handler(client):
    global sockrobot
    MSG_MAX_SIZE = 1024
    while True:
        msg = client.recv(MSG_MAX_SIZE).decode("ascii")
        print("msg recu ",msg)
        if msg.startswith("register") and len(msg.split()) == 2:
            sockrobot = client
            robot_name = msg.split()[1]
            if robot_name in robots:
                msg = f"Robot {robot_name} already registered"
            else:
                msg = "ok"
                robots[robot_name] = None
                print("add robot ",robot_name)

        elif msg.startswith("connect") and len(msg.split()) == 2: 
            robot_name = msg.split()[1]
            if robot_name not in robots:
                msg = f"Robot {robot_name} unknown"
            elif robots[robot_name] is not None:
                msg = f"Robot {robot_name} already used"
            else:
                robots[robot_name] = client
                msg = "ok"
                print("pc connected to robot ",robot_name)

        elif msg.split()[0] not in COMMANDS:
            msg = f"Incorrect msg: {msg}"
        else:
            print("send to robot")
            sockrobot.send(msg.encode("ascii"))
            msg = f"command {msg} ok" 
        client.send(msg.encode("ascii"))
        
    client.close()

def main():
    HOST = "192.168.1.1"
    PORT = 9000

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    sock.listen(5)
    
    print(f"Server is started at port {PORT}")
    try:
        while True:
            client,_ = sock.accept()
            threading.Thread(target=handler, args=(client,)).start()
    except KeyboardInterrupt:
        print("Closing server socket...")
        sock.close()
    
if __name__ == "__main__":
    main()
