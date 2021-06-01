import sys
import socket

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 client.py router_ip")
    else:
        ROUTER_IP = sys.argv[1]
        PORT = 9000
        MSG_MAX_SIZE = 1024

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ROUTER_IP, PORT))
        print(f"You are connected to router {ROUTER_IP} at port {PORT}")

        while True:
            print("> ", end="")
            cmd = input()
            sock.send(cmd.encode("ascii"))
            print("A: ",sock.recv(MSG_MAX_SIZE).decode("ascii"))

if __name__ == "__main__":
    main()