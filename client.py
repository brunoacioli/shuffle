import sys
import socket
from common_comm import send_dict, recv_dict, sendrecv_dict

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65431

player_id = 0


def run_client(client_sock):
    global player_id
    while True:
        print(player_id)
        if player_id == 0:
            print("if")
            test = sendrecv_dict(client_sock, {"op": "START", "msg": "teste"})
            print(test)
            player_id = test["id"]
        else:
            print("else")
            msg = input("Digite a mensagem: ")
            test = sendrecv_dict(client_sock, {"id": player_id, "op": "SHUFFLE", "msg": msg})
            print(test)

def main(args):
    
    print("Player started")

    client_sock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect((HOST, PORT))
    run_client(client_sock)

    client_sock.close ()
    sys.exit (0)

if __name__ == "__main__":
    main(sys.argv)
