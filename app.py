#!/usr/bin/python3
import RPi.GPIO as GPIO
from threading import Lock
from flask import Flask, render_template, session, request, \
    copy_current_request_context
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
import eventlet
eventlet.monkey_patch()
#import gevent
# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()
global XYZ
XYZ = 0
global flg
flg = 0
global text_file
text_file = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN)   

print("Starting App.py");

def read_data(self):
    global XYZ
    global flg
    GPIO.setup(4, GPIO.IN)
    flg = 1
    print('INTERRUPT!!!', flg)
    # reset interrupt source
    GPIO.setup(4, GPIO.OUT)
    GPIO.output(4, GPIO.LOW)

GPIO.add_event_detect(4, GPIO.RISING, callback=read_data)

def background_thread():
    global XYZ
    global flg
    global text_file
    """send server generated events to clients."""
    count = 0
    while True:
        socketio.sleep(1)
        count += 1
              
        if flg == 1:
            flg = 0
            
            
            socketio.emit('my_response0',
                    #  {'count1': '' , 'data1': ''},
                      {},
                      namespace='/test')
                      
            #read tag name file
            global text_file
            try:
                 with open("/var/tmp/tp.txt", "r") as ins:
                   array = []
                   for line in ins:
                     print(line)
                     socketio.emit('my_response1',
                       {'count1': '' , 'data1': line},
                       namespace='/test')
                     #print(array)
                     #array.append(line + "\r\n")
            except:
                 print('tp.txt not found.')
                 open("/var/tmp/tp.txt", "w+")
            '''
            socketio.emit('my_response1',
                      {'count1': XYZ , 'data1': array},
                      namespace='/test')
            '''
        XYZ += 2
        

@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

@socketio.on('my_info', namespace='/test')
def test_info(message):
    print("Server responding", message['data'])  

    ant = open("/var/tmp/ant.txt", "w")
    ant.write(message['data'])
    ant.close()
    emit('my_info',
         {'data': message['data']}, broadcast = True)

@socketio.on('my_event', namespace='/test')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']})


@socketio.on('my_broadcast_event', namespace='/test')
def test_broadcast_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']},
         broadcast=True)


@socketio.on('join', namespace='/test')
def join(message):
    join_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})


@socketio.on('leave', namespace='/test')
def leave(message):
    leave_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})


@socketio.on('close_room', namespace='/test')
def close(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response', {'data': 'Room ' + message['room'] + ' is closing.',
                         'count': session['receive_count']},
         room=message['room'])
    close_room(message['room'])


@socketio.on('my_room_event', namespace='/test')
def send_room_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']},
         room=message['room'])


@socketio.on('disconnect_request', namespace='/test')
def disconnect_request():
    @copy_current_request_context
    def can_disconnect():
        disconnect()

    session['receive_count'] = session.get('receive_count', 0) + 1
    # for this emit we use a callback function
    # when the callback function is invoked we know that the message has been
    # received and it is safe to disconnect
    emit('my_response',
         {'data': 'Disconnected!', 'count': session['receive_count']},
         callback=can_disconnect)
    

@socketio.on('my_ping', namespace='/test')
def ping_pong():
    emit('my_pong')


@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)
    emit('my_response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)


if __name__ == '__main__':
    GPIO.setup(4, GPIO.OUT)
    GPIO.output(4, GPIO.LOW)
    socketio.run(app, host='0.0.0.0', debug=False)

