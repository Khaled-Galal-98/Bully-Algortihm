import sys
import re


def Read_config():
    fileName = 'config.txt'
    lineList = [line.rstrip('\n') for line in open(fileName)]

    number_of_machines = int(lineList[0])
    time_waited = int(lineList[1])

    ports = []
    priorties = []
    machinesdata = dict()
    for i in range(2,2+number_of_machines):
        priorty , port =  re.split(" ",lineList[i])
        ports.append(port)
        priorties.append(priorty)
        machinesdata[priorty] = port


    #print(number_of_machines , time_waited)
    #print(ports ,priorties)
    return number_of_machines, machinesdata , time_waited


def coordinator(machines):
    
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:%s" % "8801")
    while True:
        message = socket.recv()

        machineNo = int(message)

        port = machines[machineNo]

        socket.send("Recieved msg from client with id:" + str(machineNo))
    
    
    
    
def procces(machines, machineNo):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect ("tcp://127.0.0.1:%s" % str(machines[0]))
    while True:
        socket.send(machineNo)

        message = socket.recv()
        print(message)
    
machineNo = sys.argv[1]
number_of_machines,machinesdata,time_waited = Read_config()


if machineNo == 1:
    coordinator(machinesdata)
else:
    procces(machinesdata, machineNo)
