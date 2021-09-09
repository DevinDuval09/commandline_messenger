import asyncio

client_messages = {}

async def route_message(reader, writer):

    while True:
        print(f"Messages: {client_messages}")
        #print("Awaiting requests")
        data = await reader.read(4096)
        decoded_data = data.decode("utf-8")
        print("decoded_data: ", decoded_data)
        decoded_list = decoded_data.split(":")
        if "post" in decoded_list:
            print(decoded_list)
        #print("decoded_list: ", decoded_list)
        decoded = [arg.strip() for arg in decoded_list]
        #print("decoded: ", decoded)
        request = decoded.pop(0)
        username = ""
        try:
            username = decoded[0]
        except IndexError:
            #print("request", request)
            #print("decoded", decoded)
            break

        #print(f"request: {request}")
        if request == "post":
            author, recipient, message = decoded
            print(f"{author} {recipient} {message}")
            client_messages[recipient].append(f"{author}: {message}")
            response = "ok"
            writer.write(f"{response}".encode("utf-8"))
            await writer.drain()
        elif request == "get":
            #print(f"user: {username}")
            for user, messages in client_messages.items():
                #print(f"key: {user} :: messages: {messages}")
                if user == username:
                    message = ""
                    #print(f"Messages: {messages}")
                    if len(messages) > 0:
                        message = messages.pop(0)
                    writer.write(f"{message}".encode("utf-8"))
                    await writer.drain()
                    #print(f"Sent message: {message}")
                    #verification = await reader.read(4096)
                    #verification = verification.decode("utf-8")
                    #if verification != "ok":
                    #    print(f"Client responded {verification}")
                    #    break
                    #await writer.drain()
        elif request == "login":
            client_messages[username] = []
            writer.write(f"Thank you {username}.".encode("utf-8"))
            await writer.drain()
        else:
            #print("Error:")
            #print(f"user: {username}")
            #print(request)
            response = "error"
            writer.write(f"{response}".encode("utf-8"))
            await writer.drain()
        writer.close()
        #print("End of route message")

async def route():
    server = await asyncio.start_server(route_message, '127.0.0.1', 50000)
    print("Server started.")
    print(f"Connected clients: {client_messages}")

    async with server:
        await server.serve_forever()

asyncio.run(route())
    