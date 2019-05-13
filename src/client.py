import xmlrpc.client
import select
import sys
import time


# This function check whether user input something or not.
def user_input_message():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

# Rigster self as a new client
def regist():
    print('Input your name:')
    user_name = sys.stdin.readline().strip()

    try:
        user_id = server.regist_new_user(user_name)
        print('User id:', user_id, 'User Name:', user_name)
        print('You can start chatting now! (type quit to leave).')

    except:
        print('Server Closed.')
        sys.exit()

    return user_id, user_name


def display_user_online():
    try:
        print('Current User online:')

        user_list = server.display_user_in_server()

        for user_info in user_list:
            print(user_info)
    except:
        print('Error')
        sys.exit()


def choose_user_to_talk_with():
    print('\nWho do you want to talk with?\n')
    print('Choose specific user id')

    user_choice = sys.stdin.readline().strip()

    try:
        user_choice = int(user_choice)

    except:
        print('Invalid input')
        sys.exit()

    talk_to = 0

    if user_choice <= 0:
        print('User id should start from 1.')
        sys.exit()

    else:
        print('Entering Individual')
        talk_to = user_choice

    return talk_to



# When user type quit_msg, user will exit from chat.
quit_msg = 'quit'

# ****************************************************** #
# Main Logic start here

# Set server
server = xmlrpc.client.ServerProxy('http://localhost:8000')

# regist self as a new user
user_id, user_name = regist()

display_user_online()

print('\n>>>Note:You need to specify each other on both user side.<<<')

talk_to = choose_user_to_talk_with()

while True:

    time.sleep(1)   # Control frequency

    # Display other user message here.
    try:
        message_list = server.display_message(user_id)
    
        for message in message_list:
            print(message)

        #TODO : add info when new user enter the chatting room
        # server.notify_new_user_enter()
    except:
        print('Server Closed.')
        sys.exit()

    # If user input some message and press <Enter> Key.
    if user_input_message():

        user_message = sys.stdin.readline().strip()

        if user_message == quit_msg:         
            print('Exit chat room.')

            try:
                server.user_leave(user_id, talk_to)
            except:
                print('Server Closed.')

            sys.exit()

        else:
            print('<You>:', user_message)
            
            try:
                server.send_message(user_id, user_message, talk_to)
            except:
                print('Server Closed.')
                sys.exit()
