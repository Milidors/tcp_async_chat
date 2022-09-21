import socket
import asyncio
from sys import flags
# РЕАЛИЗОВАТЬ ОБЩИЙ ЧАТ ++++++
# РЕАЛИЗОВАТЬ ЛС -----------
# графический интерфейс Qtpython


class ServerTCP:
    def __init__(self, server, port):
        self.server = server
        self.port = port
        self.id = 0

    # Прием подключений 
    async def accept_connection(self):
        loop = asyncio.get_event_loop()
        while True:
            try:
                self.server.setblocking(False)
                self.connetcion, self.addr = await loop.sock_accept(self.server)
                self.user_name = (await loop.sock_recv(self.connetcion, 1024)).decode("utf-8")
                await loop.sock_sendall(self.connetcion, self.user_name.encode("utf-8"))
                # Если в списке существует подключение то можно отправлять сообщения
                if self.connetcion in self.list_connections:
                    continue
                # Иначе добавляем подключение в список 
                else:  
                    print(f"USER CONNECT: IP-> {self.addr}\nUser name-> {self.user_name}")                  
                    self.list_connections.append(self.connetcion)
                    await loop.sock_sendall(self.connetcion, str(self.id).encode("utf-8"))
                    client = loop.create_task(self.handle_client(self.connetcion, self.user_name))
                    await client
            except Exception:
                pass
           
        #    переработать структуру кода 
        # сохранение название сокета 
    async def handle_client(self, client, user_name):
        try:
            data = " "
            flag = True
            loop = asyncio.get_event_loop()
            # Создаем новый поток для принятия новых подключений
            self.id += self.id + 1
            asyncio.create_task(self.accept_connection())

            while flag:
                
                    data = (await loop.sock_recv(client, 1024)).decode("utf-8")
                    response = str(data)
                    print(f"USER: {user_name}, msg: {response}")
                    # доработать выход из чата 
                    asyncio.create_task(self.send_all_msg(response, user_name))
                    if response[0:] == "q":
                        print(f"DISCONNECT: {user_name}")
                        if client in self.list_connections:
                            indx = self.list_connections.index(client)
                            self.list_connections[indx].close()
                            self.list_connections.pop(indx)
        except Exception:
            pass            

    async def send_all_msg(self, response, user_name):
        try:
            print(response)
            for client in self.list_connections:
                await loop.sock_sendall(client, (user_name+": "+response).encode("utf-8"))
        except Exception:
            exit()

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
    asyncio.run(server.run_server())
