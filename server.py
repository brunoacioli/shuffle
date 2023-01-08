import sys
import socket
import select
import random
from common_comm import send_dict, recv_dict, sendrecv_dict

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65431

N = [1,2,3,4,5,6,7,9,10]

players_list = {}
player_id = 0

def add_client(client_sock):
    global player_id
    player_id += 1
    if player_id not in players_list:
        players_list[player_id] = {'sock': client_sock, 'deck': []}
    return player_id


def new_msg(client_sock):
    global player_id

    msg = recv_dict(client_sock)
    print(msg)

    if msg["op"] == "START" :
        print("Entrei start")
        
        id = add_client(client_sock)
        print("Hello player %d" % id)
        
        resp = input("digite a resposta: ")
        resp_test = {"id": id, "op": msg["op"], "reply": resp}
    
    #elif player_id == 3: terminar shuffle amanha
        

    else:
        resp = input("digite a resposta 222: ")
        resp_test = {"id": msg["id"], "op": msg["op"], "reply": resp}

    send_dict(client_sock, resp_test)



def main(args):
        
        server_socket = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind ((HOST, PORT))
        server_socket.listen (10)
        clients = []
        print("Server started")
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
if __name__ == "__main__":
        main(sys.argv)