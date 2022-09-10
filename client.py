import socket
import asyncio


class ClientTCP:
    def __init__(self, server, port):
        self.server = server
        self.port = port
    
    async def connection(self):
        msg = None
        num_connect = None
        loop = asyncio.get_event_loop()
        self.server.setblocking(False)
        await loop.sock_connect(self.server, ('', self.port))
        print("Подключилися")
        if num_connect is None:
            num_connect = (await loop.sock_recv(self.server, 255)).decode("utf-8")
            print(num_connect)
        while msg != "q":
            try:
                msg = input(">> ")
                
                # response = self.server.recv(1024).decode("utf-8")

                if msg:
                    # self.server.sendall(msg.encode("utf-8"))
                    await loop.sock_sendall(self.server, (num_connect+msg + " " + str(self.server)).encode("utf-8"))                    
                    # response = self.server.recv(1024).decode("utf-8")
                    response = (await loop.sock_recv(self.server, 255)).decode("utf-8")
                    print(response)
            except Exception:
                self.server.close()
                exit()
                

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server = ClientTCP(sock, 10808)
    asyncio.run(server.connection())