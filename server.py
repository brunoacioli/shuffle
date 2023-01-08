import os
import sys
import socket
import select
import random
from common_comm import send_dict, recv_dict, sendrecv_dict

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432

deck = [1,2,3,4,5,6,7,9,10]

players_list = {}
player_id = 0
count_shuffle = 0

def add_client(client_sock):
    global player_id
    player_id += 1
    if player_id not in players_list:
        players_list[player_id] = {'sock': client_sock, 'deck': [], 'shuffled_array': [], 'shuffle_ready': False, "shuffle_done": False}
    return player_id

def verifiy_shuffle(id):
        print("entrei %d" % id)
        for i in range(id):
                if i == 0:
                        continue
                elif i > 0:
                        if not players_list[i]["shuffle_done"]:
                                return False

        return True


def shuffle_cards(client_sock, id, past_deck = None):
        global deck
        if verifiy_shuffle(id):
                players_list[id]["shuffle_done"] = True
                print("Id: %d" % id)
                if not past_deck:
                        send_dict(client_sock, {"id":id, "op": "SHUFFLING", "status": True, "deck": deck})
                else:
                        send_dict(client_sock, {"id":id, "op": "SHUFFLING", "status": True, "deck": past_deck})
        else:
                send_dict(client_sock, {"id":id, "op": "SHUFFLING", "status": False})

def new_msg(client_sock):
        global player_id
        global count_shuffle

        msg = recv_dict(client_sock)
        print(msg)
        # START ADICIONA CLIENT AO DICIONARIO
        if msg["op"] == "START" :
                id = add_client(client_sock)
                print(players_list)
                print("Hello player %d" % id)
                resp = input("Type ur message: ")
                resp_test = {"id": id, "op": msg["op"], "reply": resp}
                send_dict(client_sock, resp_test)

        # SHUFFLE ESPERA QUE TODOS OS CLEINTES ESTEJAM EM SHUFFLE PARA COMEÇAR A EMBARALHAR
        elif msg["op"] == "SHUFFLE" and not players_list[msg["id"]]["shuffle_ready"]:
                count_shuffle += 1
                players_list[msg["id"]]["shuffle_ready"] = True
                print("count_shuffle: " + str(count_shuffle))
                print("####" + str(msg["id"]))
                if msg["id"] == 1:
                        send_dict(client_sock, {"id": msg["id"], "op": "SHUFFLING", "status": True})
                else:
                        send_dict(client_sock, {"id": msg["id"], "op": "SHUFFLING", "status": False})
        # SHUFFLING COMEÇA A EMBARALHAR
        elif msg["op"] == "SHUFFLING":
                if msg["id"] == 1:
                        shuffle_cards(client_sock, msg["id"])
                else:
                        print("ELSE SHUFFLING %d" % msg["id"])
                        shuffle_cards(client_sock, msg["id"], players_list[msg["id"]-1]["shuffled_array"])


        '''else:
                resp = "Shuffle player %d"  % msg["id"]
                resp_test = {"id": msg["id"], "op": msg["op"], "reply": resp}
                send_dict(client_sock, resp_test)'''



def main(args):
        
        server_socket = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind ((HOST, PORT))
        server_socket.listen (10)
        clients = []
        print("Server started")
        try:
                while True:
                        try:
                                available = select.select ([server_socket] + clients, [], [])[0]
                        except ValueError:
                                # Sockets may have been closed, check for that
                                for client_sock in clients:
                                        if client_sock.fileno () == -1: client_sock.remove (client) # closed
                                continue # Reiterate select
                        for client_sock in available:
                                # New client?
                                if client_sock is server_socket:
                                        newclient, addr = server_socket.accept ()
                                        clients.append (newclient)
                                # Or an existing client
                                else:
                                        # See if client sent a message
                                        if len (client_sock.recv (1, socket.MSG_PEEK)) != 0:
                                                # client socket has a message
                                                ##print ("server" + str (client_sock))
                                                new_msg(client_sock)
                                        else: # Or just disconnected
                                                clients.remove (client_sock)
                                                #clean_client (client_sock)
                                                client_sock.close()
                                                break # Reiterate select
        except KeyboardInterrupt:
                os.system("pkill -f client.py")
                #os.system("pkill -f player.py")
                sys.exit(0)

if __name__ == "__main__":
        main(sys.argv)