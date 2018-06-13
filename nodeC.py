#!/usr/bin/python
import socket  # for sockets

import sys  # for exit

import threading

from thread import *



# create an INET, STREAMing socket

try:

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

except socket.error:

    print 'Failed to create forwarder socket'

    sys.exit()



print 'forwarder Socket Created'



target=''

sender=''

source=''

protocol=''

host = ''

port = 8002 # my port

myinfo = ["C","10.0.100.4","08:00:27:58:68:98",port]

othersPorts = [8000,8001,8003]

ArpTable = []

ArpTable.append(myinfo)

for i in range(2,5):

    ArpTable.append([])





def getportfromIP(ip):

        portt = 0

        for info in range(0, len(ArpTable) - 1):

           # print ArpTable[info]  why print??

            if len(ArpTable[info]) > 0:

               # print ArpTable[info][1]

                if ArpTable[info][1] == ip:

                    portt = ArpTable[info][3]

        return portt





def getMACfromIP(ip):

        mac = 0

        for info in range(0,len(ArpTable)-1):

            #print ArpTable[info]

            if len(ArpTable[info]) > 0:

                # print ArpTable[info][1]

                 if ArpTable[info][1] == ip:

                     mac = ArpTable[info][2]

                     return mac



# Bind socket to local host and port

try:

    s.bind((host, port))

except socket.error, msg:

    print 'forwarder Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]

    sys.exit()



print 'Node C Socket bind complete'



# Start listening on socket

s.listen(10)

print 'Node C Socket now listening'





# Function for handling connections. This will be used to create threads

def clientthread(conn, addr):

    global target, source, sender, protocol

    # Sending message to connected client

    conn.send('Welcome to the node C. Type something and hit enter\n')

    # infinite loop so that function do not terminate and thread do not end.

    temp = True

    while temp:

    

       data = conn.recv(1024)

    

       if not data:

            break

       elif data.startswith("pingmac 10.0.100"): 

            targetIP = data.split(" ")[1]#retreives the targetIP

            targetport = getportfromIP(targetIP)#retreives the port number of the target ip

            mac = getMACfromIP(targetIP)

            if mac != 0: #then we already have the mac address so no need to send a broadcast message

                text="pingmac "+str(mac)

                sendToNodeSolo(mac,text)



                target = "Target MAC:"+mac+" Target IP:"+targetIP

                targetport = getportfromIP(targetIP)

            else : #in this case we don't have the node's mac address so we have to send a broadcast message to the network

                protocol = "Protocol: ARP Opcode: 1"

                source = "Source: " +myinfo[2]+" Destination: "+"FF:FF:FF:FF:FF:FF"

                sender = "SenderMAC: " + myinfo[2]+" SenderIP: "+myinfo[1]

                target = "TargetMAC: "+"00:00:00:00:00:00"+" TargetIP: "+targetIP



            broadcast = protocol +"\n" + source +"\n"+sender +"\n"+target

            reply = 'OK from node B, your request is being executed...' + data

            conn.sendall(reply)

            forwardToServer(broadcast,targetport)

       elif data=="pingmac received":

            print 'pingmac received' 

       elif data=='pingmac 08:00:27:58:68:98':

            ismymac=data.split(' ')[1]

            if ismymac==myinfo[2]:

                texty='pingmac received'

                conn.sendall(texty)

                

       elif data.startswith("Protocol:ARP Opcode:1"):#an arp request to get my mac addresse

            seplines=data.split("/n")

            sep=seplines.split(" ")

            ip=sep[16]

            if ip==myinfo[1]:

                 print 'received ARP from' + sep[6] +'replying'

                 mac = sep[6]  # get their mac

                 ip = sep[12]  # get their ip address

                 if ip == "10.0.100.3":

                     peerinfo = ['B', ip, mac, getportfromIP(ip)]

                 elif ip == "10.0.100.2":

                     peerinfo = ['A', ip, mac, getportfromIP(ip)]

                 elif ip == "10.0.100.5":

                     peerinfo = ['D', ip, mac, getportfromIP(ip)]



                 ArpTable.append(peerinfo)  # add their info in ArpTable

                 protocol = "Protocol: ARP Opcode: 2"

                 source = "Source: "+myinfo[2]+" Destination: "+sep[6]

                 sender = "SenderMAC: "+myinfo[2]+" SenderIP: "+myinfo[1]

                 target = "TargetMAC: "+sep[6]+" TargetIP: "+sep[12]



                 broadcast = protocol + "\n" + source + "\n" + sender + "\n" + target

                 sendToNodeSolo(mac,broadcast)

            print 'received ARP from' + sep[6] + 'ignoring'





       elif data.startswith("Protocol:ARP Opcode:2"): 

            seplines=data.split("/n")

            sep=seplines.split(" ")

            mac=sep[6]#get their mac

            ip=sep[12]#get their ip address


            if ip == "10.0.100.3":

                     peerinfo = ['B', ip, mac, getportfromIP(ip)]

            elif ip == "10.0.100.2":

                     peerinfo = ['A', ip, mac, getportfromIP(ip)]

            elif ip == "10.0.100.5":

                     peerinfo = ['D', ip, mac, getportfromIP(ip)]




            ArpTable.append(peerinfo)#add their info in ArpTable



       elif data.startswith("arp"):

             for j in range(len(ArpTable)):

				 print(" ".join(str(ArpTable[j])))

				 

				



       else:

            reply = "give a pingmac command please"

            conn.sendall(reply)

            temp = False

    # came out of loop

    conn.close()







def forwardToServer(broadcast, port):

    if port==0:

        for node in othersPorts:

     #       print node

            sendToNode(node,broadcast)

    else :

        sendToNode(port,broadcast)





def sendToNodeSolo(mac,text):

    socketClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    remote_ip = socket.gethostbyname("localhost")

   # print port

    socketClient.connect((remote_ip, port))

    try:

        # Set the whole string

        socketClient.send(text)

    except socket.error:

        print 'Send failed'

        sys.exit()

    socketClient.close()



def sendToNode(port,broadcast):

    socketClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    remote_ip = socket.gethostbyname("localhost")

    #print port

    socketClient.connect((remote_ip, port))

    try:

        # Set the whole string

        socketClient.sendall(broadcast)

    except socket.error:

        print 'Send failed'

        sys.exit()

    socketClient.close()

# now keep talking with the client





while 1:

    # wait to accept a connection - blocking call

    conn, addr = s.accept()

    print 'Connected with ' + addr[0] + ':' + str(addr[1])



    # start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.

    start_new_thread(clientthread, (conn, addr,))


