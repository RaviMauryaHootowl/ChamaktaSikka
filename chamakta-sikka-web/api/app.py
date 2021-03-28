import time
from flask import Flask, request
from uuid import uuid4
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)

app.config['SECRET_KEY'] = 'csk'

socketIO = SocketIO(app, cors_allowed_origins="*")

# List of all users online
users_online = []


def removeUser(sid):
    for i, user in enumerate(users_online):
        if user['sid'] == sid:
            del(users_online[i])
            break
    return True

@app.route('/time')
def get_current_time():
    return {'time': time.time()}

@socketIO.on('connect')
def connected():
    print('Connected')

@socketIO.on('disconnect')
def disconnected():
    isRemoved = removeUser(request.sid)
    if isRemoved:
        emit('userRefresh', users_online, broadcast=True)
    print('Disconnected')

@socketIO.on("message")
def sendSomethign(msg):
    print(msg)
    send(msg, broadcast=True)
    return None


@socketIO.on("addNewUser")
def addNewUser(data):
    print(data['username'])
    user_to_add = {}
    user_to_add['username'] = data['username']
    user_to_add['sid'] = request.sid
    user_to_add['uuid'] = str(uuid4()).replace("-","")
    user_to_add['wallet_balance'] = int(data['initamount'])
    users_online.append(user_to_add)
    print(users_online)
    emit('userInfo', user_to_add, room=request.sid)
    emit("userRefresh", users_online, broadcast=True)
    return None


if __name__ == '__main__':
    socketIO.run(app, debug=True)