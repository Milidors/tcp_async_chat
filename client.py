from re import L
import socket
import asyncio
from sys import flags
from aioconsole import ainput
# 185.40.7.41:51820

class ClientTCP:
    def __init__(self, server, port):
        self.server = server
        self.port = port
    
    async def connection(self):
        self.msg = None
        self.flag = True
        id_connections = None
        list_user_names = []
        self.user_name = input("Please input your nickname: ")
        loop = asyncio.get_event_loop()
        self.server.setblocking(False)
        await loop.sock_connect(self.server, ('', self.port))
        await loop.sock_sendall(self.server, self.user_name.encode("utf-8"))
        list_user_names.append((await loop.sock_recv(self.server, 1024)).decode("utf-8"))
        print(f"Connect {list_user_names[-1]}")
        if id_connections is None:
            id_connections = (await loop.sock_recv(self.server, 255)).decode("utf-8")
            print(id_connections)
        asyncio.create_task(self.listen(id_connections))
        while self.flag:
            try:
                self.msg = await ainput(">> ")
                if self.msg and self.msg != "q":
                    await loop.sock_sendall(self.server, (self.msg).encode("utf-8"))
                if self.msg == "q":
                    await loop.sock_sendall(self.server, (self.msg).encode("utf-8"))
                    break
            except SystemExit:
                self.flag = False
                
    async def listen(self, id_connections):
        loop = asyncio.get_event_loop()
        while True:
            try:
                
                if self.msg != "q":
                    response = (await loop.sock_recv(self.server, 255)).decode("utf-8")
                    print(response[0:])
                else:
                    exit()
            except IndexError:
                exit()


if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server = ClientTCP(sock, 10808)
    asyncio.run(server.connection())