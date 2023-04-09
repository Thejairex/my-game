import socket
import pickle
import threading

class Server:
    def __init__(self, ip=str, port=int):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((f"{ip}", port))
        self.client_sockets = []

    def run(self):
        self.server_socket.listen()
        print("Servidor iniciado en localhost:5555")

        while True:
            client_socket, address = self.server_socket.accept()
            print(f'se ha conectado : {address}')
            self.client_sockets.append(client_socket)
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def countClient(self):
        return len(self.client_sockets)

    def handle_client(self, client_socket):
        while True:
            data = client_socket.recv(4096)
            if not data:
                break
            player_position =pickle.loads(data)
            print(player_position)
            pos = pickle.dumps((player_position))

            for sock in self.client_sockets:
                if sock != client_socket: 
                    sock.send(pos)

        client_socket.close()
        self.client_sockets.remove(client_socket)

# if __name__ == "__main__":
#     server = Server()
    
