import asyncio
from logger import Messenger_Logger
from logging import INFO

logger = Messenger_Logger("Server")
logger.handlers[1].setLevel(INFO)

client_messages = {}

async def route_message(reader, writer):

    logger.info("Starting route_message")
    logger.info(f"Connected clients: {client_messages.keys()}")
    logger.info(f"Messages: {client_messages}")
    logger.info("Awaiting requests")
    #while True:
    data = await reader.read(4096)
    decoded_data = data.decode("utf-8")
    logger.info("Data: %s" % decoded_data)
    decoded_list = decoded_data.split(":")
    decoded = [arg.strip() for arg in decoded_list]
    request = decoded.pop(0)
    username = ""
    try:
        username = decoded[0]
    except IndexError as e:
        logger.critical(e)
        logger.critical("request: %s" % request)
        logger.critical("decoded: %s" % decoded)
        #break

    logger.info(f"request: {request}\tuser: {username}")
    if request == "post":
        author, recipient, message = decoded
        logger.info(f"author, recipient, message: {author} {recipient} {message}")
        client_messages[recipient].append(f"{author}: {message}")
        response = "ok"
        writer.write(f"{response}".encode("utf-8"))
        await writer.drain()
    elif request == "get":
        for user, messages in client_messages.items():
            if user == username:
                message = ""
                logger.info(f"Messages: {messages}")
                if len(messages) > 0:
                    message = messages.pop(0)
                writer.write(f"{message}".encode("utf-8"))
                await writer.drain()
                logger.info(f"Sent message: {message}")
    elif request == "login":
        client_messages[username] = []
        writer.write(f"Thank you {username}.".encode("utf-8"))
        await writer.drain()
        logger.info(f"{username} successfully logged in.")
    else:
        logger.critical(f"Error:\tuser: {username}\trequest:{request}")
        response = "error"
        writer.write(f"{response}".encode("utf-8"))
        await writer.drain()
    writer.close()
    logger.info("End of route message")

async def route():
    server = await asyncio.start_server(route_message, '127.0.0.1', 50000)
    logger.info("Server started.")

    async with server:
        await server.serve_forever()

asyncio.run(route())
    