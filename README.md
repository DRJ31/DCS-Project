# DCS Chat

This is a Small chatting software, which is Distributed Computing System course project.

## Dependencies

- GUI: PyQt5
- Communication: xmlrpc
- Database: MySQL5.7

You need to install:
- pymysql
- pyqt5
- pillow

## Features

- User Registration (You must have an avatar)
- Private Chat (Even with yourself)
- Search for users
- History records (Without group talk)
- Group talk (With all the users. Messages won't save into database)

## Run the project

- Client: src/main.py
- Server: src/server.py

If you want to modify server's name and port, you have to modify them in **server.py, controller/Client.py, controller/RegisterController.py and utils/AvatarTool.py**

## License
The project is under the License of GNU GPL v3.
