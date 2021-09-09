import asyncio
import msvcrt
import sys


class Client():

    username = input("Enter username:")
    HOST = "127.0.0.1"
    PORT = 50000
    response_reader = None
    response_writer = None
    client_input = ""

    async def login(self):
        request = "login"
        self.client_input = f"{request}:{self.username}"
        self.response_writer.write(self.client_input.encode("utf-8"))
        await self.response_writer.drain()
        self.client_input = ""
        response = await self.response_reader.read(4096)
        message = response.decode("utf-8")
        print(message)
        return True


    async def get_message(self):
        await asyncio.sleep(.1)
        self.response_reader, self.response_writer = await asyncio.open_connection(self.HOST, self.PORT)
        #print("Getting messages")
        request = "get"
        outgoing_message = f"{request}:{self.username}"
        #print(outgoing_message)
        self.response_writer.write(outgoing_message.encode("utf-8"))
        await self.response_writer.drain()
        response = await self.response_reader.read(4096)
        #print("received response")
        incoming_message = response.decode("utf-8")
        if incoming_message != "":
            print(incoming_message)
    
    async def send_message(self):
        if self.client_input.count("\r") > 0:
            self.response_reader, self.response_writer = await asyncio.open_connection(self.HOST, self.PORT)
            print("Sending message:")
            request = "post"
            outgoing_message = f"{request}:{self.username}:{self.client_input}"
            print(outgoing_message)
            self.response_writer.write(outgoing_message.encode("utf-8"))
            await self.response_writer.drain()
            response = await self.response_reader.read(4096)
            if response.decode("utf-8") != "ok":
                print(f'ERROR: {response.decode("utf-8")}')
            self.client_input = ""

    async def run_messenger(self):
        logged_in = False
        self.response_reader, self.response_writer = await asyncio.open_connection(self.HOST, self.PORT)
        logged_in = await self.login()
        self.response_writer.close()
        print(f"login status: {logged_in}")
        print("Enter messages in format Recipient:Message\n")

        while logged_in:

            try:
                if msvcrt.kbhit():
                    new_char = msvcrt.getch()
                    msvcrt.putch(new_char)
                    self.client_input = self.client_input + new_char.decode()

                await self.get_message()
                await self.send_message()

            except ConnectionAbortedError:
                print("Connection closed by host.")
                break
            finally:
                self.response_writer.close()

client = Client()
asyncio.run(client.run_messenger())

    