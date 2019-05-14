from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import queue
from model import Contact, Message
# Restrict to a particular path.


class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


# This class defines the variables stored on server:
class ServerDataContainer:
    user_id = 1         # User id start from 1 and increase by 1 each time a new user regist.
    user_list = []      # store online user
    group_chat = 0      # Used for judge whether group chat is selected.


# Create server
with SimpleXMLRPCServer(('localhost', 8000),
                        requestHandler=RequestHandler,
                        allow_none=True,
                        logRequests=False) as server:

    server_data_container = ServerDataContainer()

    # Score : public
    # regist_new_user:
    # create a new user with name 'user_name', id number 'user_id', 
    # and store it into user_list.

    def regist_new_user(user_name):
        # Every user_id is unique
        user_id = server_data_container.user_id

        #Regist:
        info_container = {
            'user_id': user_id,
            'user_name': user_name,
            'message_queue': queue.Queue()
        }

        #Add to user_list
        server_data_container.user_list.append(info_container)
        server_data_container.user_id += 1
        
        #For Debug
        print('New User : User id:', user_id, 'User Name:', user_name)

        return user_id
    
    # Score : public
    # user_leave:
    # print a leave message (for a user with user_id) to other users(talk_to here) and server.
    def user_leave(user_id, talk_to):

        # Group chat here
        if talk_to == server_data_container.group_chat:

            # for user in server_data_container.user_list:

            #     if user['user_id'] == user_id:
            #         message = user['user_name'] + ' left group chat.'

            #         print(message)

            #         # Send message to other user
            #         _inform_user_leave(user_id, message)

            #         # User leave
            #         server_data_container.user_list.remove(user)
            #         _display_remaining_user()
            #         break
            pass

        # individual chat here:
        else:

            for user in server_data_container.user_list:
            # find user in userlist

                if user['user_id'] == user_id:
                    
                    message = user['user_name'] + ' left.'

                    server_data_container.user_list.remove(user)
                            
                    _display_remaining_user()

                    break

            message = _format_leave_message(message)

            print(message)

            # inform other individual that I left chat room.
            for user in server_data_container.user_list:
                if user['user_id'] == talk_to:
                    user['message_queue'].put(message)
                    break


    # Score : public
    # send_message: 
    # store message to all users except the user with user_id.


    def send_message(user_id, user_message, talk_to):
        # Find user's name with user_id
        for user in server_data_container.user_list:
            if user['user_id'] == user_id:
                user_name = user['user_name']
                break

        format_msg = Message(user_id, talk_to, user_message)

        # Group chat here
        if talk_to == server_data_container.group_chat:
        
            # print('Group chat', format_msg)

            # for user in server_data_container.user_list:
            #     if user['user_id'] != user_id:
            #         user['message_queue'].put(format_msg)
            pass
            
        # Individual talk here
        else:
            print('Individual chat', format_msg)

            for user in server_data_container.user_list:
                if user['user_id'] == talk_to:
                    user['message_queue'].put(format_msg)

    # Score : public
    # display_message:
    # return message from other user to user with user_id.

    def display_message(user_id):
        message_list = []
        for user in server_data_container.user_list:
            if user['user_id'] == user_id:
                #Add other user's msg into message_list and return to client
                while not user['message_queue'].empty():
                    message_list.append(user['message_queue'].get())
        return message_list

    # Score : public
    # display_user_in_server:
    # display all user in the server.

    def display_user_in_server():

        user_info_list = []

        for user in server_data_container.user_list:

            message = 'User: ' + user['user_name'] + ', User id: ' + str(user['user_id'])
            user_info_list.append(message)
        return user_info_list

    # Score: public
    # get_online_users:
    # get a list of all users

    def get_online_users():
        user_list = []

        for user in server_data_container.user_list:
            user_list.append(Contact(
                user['user_id'],
                user['user_name'],
                'default.jpg'
            ))
        user_list[-1].avatar = "KizunaAI.jpg"
        return user_list

    server.register_function(user_leave, 'user_leave')    
    server.register_function(regist_new_user, 'regist_new_user')
    server.register_function(send_message, 'send_message')
    server.register_function(display_message, 'display_message')
    server.register_function(display_user_in_server, 'display_user_in_server')
    server.register_function(get_online_users, 'get_online_users')

    # Score : private 
    # _format_user_message
    def _format_user_message(user_name, user_message):
        return '<' + user_name + '>: ' + user_message

    # Score : private 
    # _format_leave_message
    def _format_leave_message(leave_message):
        return '<System>: ' + leave_message

    # Score : private
    # _inform_user_leave
    def _inform_user_leave(user_id, user_message):

        format_msg = _format_leave_message(user_message)

        for user in server_data_container.user_list:
            if user['user_id'] != user_id:
                user['message_queue'].put(format_msg)

    # Score : private
    # _display_remaining_user
    def _display_remaining_user() :
        for user in server_data_container.user_list:
            print("Remaining user: User id:", user['user_id'], "User Name:", user["user_name"])

    # Run the server's main loop
    server.serve_forever()