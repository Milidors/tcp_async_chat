import socket
import asyncio
from aioconsole import ainput

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
        print("Connect")
        if num_connect is None:
            num_connect = (await loop.sock_recv(self.server, 255)).decode("utf-8")
            print(num_connect)
        asyncio.create_task(self.listen(num_connect))
        while msg != "q":
            try:
                msg = await ainput(">> ")
                if msg:
                    await loop.sock_sendall(self.server, (num_connect+msg + " " + str(self.server)).encode("utf-8"))                    
            except Exception:
                self.server.close()
                exit()
        
    async def listen(self, num_connect):
        loop = asyncio.get_event_loop()
        while True:
            response = (await loop.sock_recv(self.server, 255)).decode("utf-8")
            if response[0] == num_connect:
                print("YOU: ",response[1:])
            else:
                print(response[1:])


if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server = ClientTCP(sock, 10808)
    asyncio.run(server.connection())