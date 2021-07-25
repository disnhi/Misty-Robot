import zmq, json, datetime, time, sys

context = zmq.Context()
obs_socket = context.socket(zmq.PUB)
obs_socket.bind('tcp://127.0.0.1:12003')

action_socket = zmq.Context().socket(zmq.SUB)
action_socket.connect("tcp://127.0.0.1:12004")
action_socket.setsockopt(zmq.SUBSCRIBE, b'') # '' means all topics

time.sleep(1)

messages = [
    {'name': 'nhi', 'itemHelp':'vanilla', 'engagement':'yes', 'levelHelp':'3', 'userLocation':'center','taskLocation':'down', 'objLocation':'lowerLeft', 'urgencyLevel':'high'},
    {'name': 'willie', 'itemHelp':'chocolate', 'engagement':'no', 'levelHelp':'3', 'userLocation':'center','taskLocation':'down', 'objLocation':'lowerLeft', 'urgencyLevel':'low'},
    ]

for i in range(len(messages)):
    payload = {}
    payload['message'] = messages[i]
    payload['originatingTime'] = datetime.datetime.now().isoformat()
    print("Sending", payload)
    obs_socket.send_multipart(['test-topic'.encode(), json.dumps(payload).encode('utf-8')])

    [topic, message] = action_socket.recv_multipart()
    j = json.loads(message)
    print("Receiving: ", repr(j['message']))
    print("Originating Time: ", repr(j['originatingTime']))


    time.sleep(20)

sys.input("stop")