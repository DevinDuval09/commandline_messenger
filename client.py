import asyncio
import msvcrt
from logger import Messenger_Logger


class Client():

    username = input("Enter username:")
    HOST = "127.0.0.1"
    PORT = 50000
    response_reader = None
    response_writer = None
    client_input = ""
    logger = Messenger_Logger("Client")

    async def login(self):
        self.logger.info("Logging in as %s" % self.username)
        request = "login"
        self.client_input = f"{request}:{self.username}"
        self.response_writer.write(self.client_input.encode("utf-8"))
        await self.response_writer.drain()
        self.client_input = ""
        response = await self.response_reader.read(4096)
        message = response.decode("utf-8")
        self.logger.info("Response from server: %s" % message)
        print(message)
        return True


    async def get_message(self):
        await asyncio.sleep(.01)
        self.logger.info("Connecting to %s/%s to retrieve messages" % (self.HOST, self.PORT))
        self.response_reader, self.response_writer = await asyncio.open_connection(self.HOST, self.PORT)
        request = "get"
        outgoing_message = f"{request}:{self.username}"
        self.response_writer.write(outgoing_message.encode("utf-8"))
        await self.response_writer.drain()
        self.logger.info("Request: %s sent" % outgoing_message)
        response = await self.response_reader.read(4096)
        incoming_message = response.decode("utf-8")
        self.logger.info("Response: %s received" % incoming_message)
        if incoming_message != "":
            print(incoming_message)
    
    async def send_message(self):
        self.logger.info("Current message: %s" % self.client_input)
        if self.client_input.count("\r") > 0:
            self.logger.info("Connecting to %s/%s to send message %s" % (self.HOST, self.PORT, self.client_input))
            self.response_reader, self.response_writer = await asyncio.open_connection(self.HOST, self.PORT)
            request = "post"
            outgoing_message = f"{request}:{self.username}:{self.client_input}"
            self.logger.info("Request: %s" % outgoing_message)
            self.response_writer.write(outgoing_message.encode("utf-8"))
            await self.response_writer.drain()
            response = await self.response_reader.read(4096)
            response_message = response.decode("utf-8")
            if response_message != "ok":
                self.logger.info("ERROR: Server responded %s, expected ok" % response_message)
                print(f'ERROR: {response.decode("utf-8")}')
            else:
                self.logger.info("Response: %s received" % response_message)
            self.client_input = ""

    async def run_messenger(self):
        logged_in = False
        self.logger.info("Connecting to %s/%s to login" % (self.HOST, self.PORT))
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
                self.logger.info("Connection closed by host.")
                print("Connection closed by host.")
                break
            finally:
                self.response_writer.close()

client = Client()
asyncio.run(client.run_messenger())

    