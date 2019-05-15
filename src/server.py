from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import xmlrpc.client
import queue

from utils.Database import MySQL
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

    def regist_new_user(user_name, password):
        # Every user_id is unique
        db = MySQL()
        result = db.select("SELECT * FROM User WHERE username=%s AND password=%s", user_name, password)
        if not result:
            return False
        user_id = result[0][0]

        #Regist:
        info_container = {
            'user_id': user_id,
            'user_name': user_name,
            'message_queue': queue.Queue()
        }

        for user in server_data_container.user_list:
            if user['user_id'] == info_container['user_id']:
                server_data_container.user_list.remove(user)

        #Add to user_list
        server_data_container.user_list.append(info_container)

        #For Debug
        print('New User : User id:', user_id, 'User Name:', user_name)

        return user_id

    # Score: public
    # get_username_by_id:
    # Get username by user_id.
    def get_username_by_id(user_id):
        db = MySQL()
        result = db.select("SELECT * FROM User WHERE id=%s", int(user_id))
        if not result:
            return False
        return result[0][1]

    # Score : public
    # user_leave:
    # print a leave message (for a user with user_id) to other users(talk_to here) and server.
    def user_leave(user_id):

        # individual chat here:
        # else:
        message = ""
        for user in server_data_container.user_list:
        # find user in userlist

            if user['user_id'] == user_id:

                message = user['user_name'] + ' left.'

                server_data_container.user_list.remove(user)

                _display_remaining_user()

                break

        message = _format_leave_message(message)

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
        if talk_to == 0:
        
            print('Group chat', format_msg)

            for user in server_data_container.user_list:
                if user['user_id'] != user_id:
                    user['message_queue'].put(format_msg)
            
        # Individual talk here
        else:
            print('Individual chat', format_msg)

            for user in server_data_container.user_list:
                if user['user_id'] == talk_to and user_id != talk_to:
                    user['message_queue'].put(format_msg)
            db = MySQL()
            db.modify("INSERT INTO Message (user_id, content, destination) VALUES (%s,%s,%s)",
                      int(user_id), user_message, int(talk_to))

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

    # Score: public
    # get_avatar:
    # get avatar binary

    def get_avatar(username):
        db = MySQL()
        result = db.select("SELECT * FROM User WHERE username=%s", username)
        avatar = xmlrpc.client.Binary(result[0][3])
        return avatar

    # Score: public
    # get_history_messages:
    # get history messages stored in database

    def get_history_messages(user_id):
        messages = []
        db = MySQL()
        results = db.select("SELECT * FROM Message WHERE user_id=%s OR destination=%s", int(user_id), int(user_id))
        for result in results:
            messages.append(Message(
                result[1],
                result[3],
                result[2]
            ))
        return messages

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
    # search_users:
    # search for exist users

    def search_users(keyword):
        user_list = []

        db = MySQL()
        results = db.select("SELECT * FROM User WHERE username LIKE %s", "%" + keyword + "%")
        for result in results:
            user_list.append(Contact(
                result[0],
                result[1],
                result[1] + ".jpg"
            ))

        return user_list

    # Score: public
    # get_online_users:
    # get a list of all users

    def get_online_users():
        user_list = []

        for user in server_data_container.user_list:
            user_list.append(Contact(
                user['user_id'],
                user['user_name'],
                user['user_name'] + '.jpg'
            ))
        return user_list

    # Score: public
    # user_register:
    # save user into database

    def user_register(username, password, img):
        db = MySQL()
        result = db.select("SELECT * FROM User WHERE username=%s", username)
        if result:
            return False
        db.connect()
        db.modify("INSERT INTO User (username, password, avatar) VALUES (%s,%s,%s)", username, password, img.data)
        return True

    # Score: public
    # delete_history_records:
    # delete all the history records between 2 users

    def delete_history_records(user_id):
        db = MySQL()
        db.modify("DELETE FROM Message WHERE user_id=%s OR destination=%s", int(user_id), int(user_id))

    server.register_function(user_leave, 'user_leave')    
    server.register_function(regist_new_user, 'regist_new_user')
    server.register_function(send_message, 'send_message')
    server.register_function(display_message, 'display_message')
    server.register_function(display_user_in_server, 'display_user_in_server')
    server.register_function(get_online_users, 'get_online_users')
    server.register_function(get_username_by_id, 'get_username_by_id')
    server.register_function(user_register, 'user_register')
    server.register_function(get_avatar, 'get_avatar')
    server.register_function(get_history_messages, 'get_history_messages')
    server.register_function(search_users, 'search_users')
    server.register_function(delete_history_records, 'delete_history_records')

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