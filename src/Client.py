import xmlrpc.client

server = xmlrpc.client.ServerProxy('http://192.168.1.100:8000')

inputName = input("Please input your name: ")
index, name = server.assign_name(inputName)
#TODO: identify whether the input is repeated in server name list
print("Index of this client is: " + str(index) + ", And your name is: " + name)

print("Now the user connecting to this server are:" + str(server.get_identities()))

while True:
    #send msg
    inputMsg = input("What you want to say?\n")
    server.send_msg(inputMsg)

    #receive msg
    msg = server.get_msg()
    print(msg)

    #Maybe I can store all msg into a list on server, and only the user's id == list id, then user can receive msg.

print("All function available are: "+ server.system.listMethods())