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

port = 8003 # my port

myinfo = ["D","10.0.100.5","00:24:1d:5c:5b:dc",port]

othersPorts = [8000,8001,8003]

ArpTable = []

ArpTable.append(myinfo)

for i in range(2,5):

    ArpTable.append([])





def getportfromIP(ip):

        portt = 0

        for info in range(0, len(ArpTable) - 1):

           # print ArpTable[info]  

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



print 'Node D Socket bind complete'



# Start listening on socket

s.listen(10)

print 'Node D Socket now listening'


            ismymac=data.split(' ')[1]

            if ismymac==myinfo[2]:

                texty='pingmac received'

                conn.sendall(texty)

                

       elif data.startswith("Protocol:ARP Opcode:1"):

            seplines=data.split("/n")

            sep=seplines.split(" ")

            ip=sep[16]

            if ip==myinfo[1]:

                 print 'received ARP from' + sep[6] +'replying'

                 mac = sep[6]  # get their mac

                 ip = sep[12]  # get their ip address

                 if ip == "10.0.100.3":

                     peerinfo = ['B', ip, mac, getportfromIP(ip)]

                 elif ip == "10.0.100.4":

                     peerinfo = ['C', ip, mac, getportfromIP(ip)]

                 elif ip == "10.0.100.2":

                     peerinfo = ['A', ip, mac, getportfromIP(ip)]



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

            elif ip == "10.0.100.4":

                     peerinfo = ['C', ip, mac, getportfromIP(ip)]

            elif ip == "10.0.100.2":

                     peerinfo = ['A', ip, mac, getportfromIP(ip)]




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


