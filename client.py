import sys
import socket
from common_comm import send_dict, recv_dict, sendrecv_dict
import random

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432

player_id = 0
shuffle = False
flag = False


def run_client(client_sock):
    global player_id
    global shuffle
    while True:
        print(player_id)
        if player_id == 0:
            print("if")
            test = sendrecv_dict(client_sock, {"op": "START", "msg": "teste"})
            print("$$$$$", test)
            player_id = test["id"]
            shuffle = True
        else:
            print("else")
            msg = "player %d" % player_id
            if shuffle:
                test = sendrecv_dict(client_sock, {"id": player_id, "op": "SHUFFLE", "msg": msg})
                shuffle = False
                print("test: ",test)
            if test['op'] == "SHUFFLING":
                if test["status"] == False:
                    while True:
                        test = sendrecv_dict(client_sock, {"id": player_id, "op": "SHUFFLING", "status": test["status"]})
                        if test["status"]:
                            break
        
            answer = sendrecv_dict(client_sock, {"id": player_id, "op": "SHUFFLING", "status": test["status"]})
    
        
            print("!!!! " ,answer)
            deck_shuffled = answer["deck"].copy()
            random.shuffle(deck_shuffled)
            print(deck_shuffled)
            answer["op"] = "SHUFFLED"
            answer["deck"] = deck_shuffled
            answer["status"] = True
            answer = sendrecv_dict(client_sock, answer)
            print("## ",answer)

def main(args):
    
    print("Player started")

    client_sock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect((HOST, PORT))
    run_client(client_sock)

    client_sock.close ()
    sys.exit (0)

if __name__ == "__main__":
    main(sys.argv)
