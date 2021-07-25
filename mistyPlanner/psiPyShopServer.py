import zmq, json, datetime
from wrapper import *

class PyShopServer:
    def __init__(self):
        self.state = {}
        self.receive_port = '12003'
        self.send_port = '12004'
        self.setup_connection()

    def setup_connection(self):
        # receive socket
        self.obs_socket = zmq.Context().socket(zmq.SUB)
        self.obs_socket.connect("tcp://127.0.0.1:{}".format(self.receive_port))
        self.obs_socket.setsockopt(zmq.SUBSCRIBE, b'')
        # send socket
        self.action_socket = zmq.Context().socket(zmq.PUB)
        self.action_socket.bind("tcp://127.0.0.1:{}".format(self.send_port))

    def run_connection(self):
        self.setup_connection()
        print("running PyShop server, ports: {}, {}".format(self.receive_port, self.send_port))
        while True:
            [topic, message] = self.obs_socket.recv_multipart()
            j = json.loads(message)
            self.originatingTime =  repr(j['originatingTime'])
            message = self.receive(j)
            self.send(message)

    def receive(self, incoming):

        #intent = repr(incoming['message']['Text Input'])[1:-1]

        name = repr(incoming['message']["name"])[1:-1]
        itemHelp = repr(incoming['message']["itemHelp"])[1:-1]
        engagement = repr(incoming['message']["engagement"])[1:-1]
        levelHelp = repr(incoming['message']["levelHelp"])[1:-1]
        userLocation = repr(incoming['message']["userLocation"])[1:-1]
        taskLocation = repr(incoming['message']["taskLocation"])[1:-1]
        objLocation = repr(incoming['message']["objLocation"])[1:-1]
        urgencyLevel = repr(incoming['message']["urgencyLevel"])[1:-1]

        #incoming is input json
        return self.process(name, itemHelp, engagement, levelHelp, userLocation, taskLocation, objLocation, urgencyLevel)

    def send(self, message):
        print(message)
        payload = {}
        payload['message'] = message 
        payload['originatingTime'] = self.originatingTime[1:-2]
        self.action_socket.send_multipart(['pyshop-plan'.encode(), json.dumps(payload).encode('utf-8')])
        return

    def process(self, name, itemHelp, engagement, levelHelp, userLocation, taskLocation, objLocation, urgencyLevel):
        print("processing parameters")

        result = psiConditions(name, itemHelp, engagement, levelHelp, userLocation, taskLocation, objLocation, urgencyLevel)    
        
        return result
        
if __name__ == '__main__':
    conn = PyShopServer()
    conn.run_connection()