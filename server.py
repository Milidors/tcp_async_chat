import socket
import asyncio
# РЕАЛИЗОВАТЬ ОБЩИЙ ЧАТ ++++++
# РЕАЛИЗОВАТЬ ЛС

class ServerTCP:
    def __init__(self, server, port):
        self.server = server
        self.port = port

    # Прием подключений 
    async def accept_connection(self):
        loop = asyncio.get_event_loop()
        while True:
            try:
                self.server.setblocking(False)
                self.connetcion, self.addr = await loop.sock_accept(self.server)
                # Если в списке существует подключение то можно отправлять сообщения
                if self.connetcion in self.list_connections:
                    client = loop.create_task(self.handle_client())
                    await client
                # Иначе добавляем подключение в список 
                else:  
                    print("+1")                  
                    self.list_connections.append(self.connetcion)
                    await loop.sock_sendall(self.connetcion, str(self.list_connections.index(self.connetcion)).encode("utf-8"))
                    client = loop.create_task(self.handle_client())
                    await client
            except Exception:
                pass
           
    async def handle_client(self):
            data = " "
            loop = asyncio.get_event_loop()
            # Создаем новый поток для принятия новых подключений
            asyncio.create_task(self.accept_connection())

            while data != "q":
                try:
                    data = (await loop.sock_recv(self.list_connections[self.list_connections.index(self.connetcion)], 255)).decode("utf-8")
                    response = str(data)
                    self.connetcion = self.list_connections[int(response[0])]
                    print("USER", response[response.find("("):response.find(")")+1], response[1:response.find("<")])
                    asyncio.create_task(self.send_all_msg(response))
                    if response[0:2] == response[0]+"q":
                        data='q'
                        print("DISCONNECT: ", response[response.find("("):response.find(")")+1])
                        self.list_connections[int(response[0])].close()
                        exit()
                except Exception:
                    pass

    async def send_all_msg(self, response):
        for client in self.list_connections:
            await loop.sock_sendall(client, response[0:response.find("<")].encode("utf-8"))

    
    async def run_server(self):
        self.server.bind(("", self.port))
        self.server.listen(3)   # кол - во подключений
        self.list_connections = [] # Списко подключений
        self.connetcion = {}
        loop = asyncio.get_event_loop()
        accept_connection = loop.create_task(self.accept_connection())
        await accept_connection


if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server = ServerTCP(sock, 10808)
    loop = asyncio.get_event_loop()
    print("START SERVER")
    # loop.run_until_complete(server.run_server())
    asyncio.run(server.run_server())
