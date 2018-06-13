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

source=''
target=''
sender=''
protocol=''
host = ''

port = 8000 # my port

myinfo = ["A","10.0.100.2","08:00:27:26:03:93",port]


othersPorts = [8001,8002,8003]

ArpTable = []

ArpTable.append(myinfo)

#for i in range(2,5):

#    ArpTable.append([])





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
        if ip=='10.0.100.3':
           mac=ArpTable[0][2]
           print mac
        elif ip=='10.0.100.4':
           mac=ArpTable[0][2]
           print mac
        elif ip=='10.0.100.5':
             mac=Arptable[0][2]
             print mac   
     
        return mac


# Bind socket to local host and port

try:

    s.bind((host, port))

except socket.error, msg:

    print 'forwarder Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]

    sys.exit()



print 'Node A Socket bind complete'



# Start listening on socket

s.listen(10)

print 'Node A Socket now listening'





# Function for handling connections. This will be used to create threads

def clientthread(conn, addr):
    global protocol, source, sender, target
    # Sending message to connected client

    conn.send('Welcome to the node A. Type something and hit enter\n')  

    # infinite loop so that function do not terminate and thread do not end.

    temp = True

    while temp:

       # Receiving from client

       data = conn.recv(1024)


       if not data:

            break

       elif data.startswith("pingmac 10.0.100"): 

            targetIP = data.split()[1]#retreives the targetIP

            targetport = getportfromIP(targetIP)#retreives the port number of the target ip

            mac = getMACfromIP(targetIP)
            print 'heeeeeere'
            print mac
            if mac != 0: #then we already have the mac address so no need to send a broadcast message

                text="pingmac "+str(mac)

                sendToNodeSolo(mac,text)

                source = "Source:" + myinfo[2] + " Destination:	" + mac

                target = "Target MAC:"+mac+" Target IP:"+targetIP

                targetport = getportfromIP(targetIP)

            else : #in this case we don't have the node's mac address so we have to send a broadcast message to the network
                
                protocol = "Protocol: ARP Opcode: 1"

                source = "Source: " +myinfo[2]+" Destination: "+"FF:FF:FF:FF:FF:FF"

                sender = "SenderMAC: " + myinfo[2]+" SenderIP: "+myinfo[1]

                target = "TargetMAC: "+"00:00:00:00:00:00"+" TargetIP: "+targetIP



                broadcast = "ARP 1 "+myinfo[2]+" FF:FF:FF:FF:FF:FF "+myinfo[2]+" "+myinfo[1]+" 00:00:00:00:00:00 "+targetIP
                reply = 'OK from node A, your request is being executed...' + data

                conn.sendall(reply)

                forwardToServer(broadcast,targetport)

       elif data=='pingmac received':

              print 'pingmac received' 

       elif data=='pingmac 08:00:27:26:03:93':

            # ismymac=data.split(' ')[1]

#             if ismymac==myinfo[2]:

                texty='pingmac received'

             #   sendToNodeSolo(mac,texty)
                conn.sendall(texty)
                

       elif data.startswith("ARP 1"):

             seplines=data.split("/n")

             sep=data.split()

             ip=sep[7]

             if ip==myinfo[1]:

                 print 'received ARP from' + sep[4] +'replying'

                 mac = sep[4]  # get their mac

                 ip = sep[5]  # get their ip address

                 if ip == "10.0.100.3":

                     peerinfo = ['B', ip, mac, getportfromIP(ip)]

                 elif ip == "10.0.100.4":

                     peerinfo = ['C', ip, mac, getportfromIP(ip)]

                 elif ip == "10.0.100.5":

                     peerinfo = ['D', ip, mac, getportfromIP(ip)]



                 ArpTable.append(peerinfo)  # add their info in ArpTable

                 protocol = "Protocol: ARP Opcode: 2"

                 source = "Source: "+myinfo[2]+" Destination: "+sep[6]

                 sender = "SenderMAC: "+myinfo[2]+" SenderIP: "+myinfo[1]

                 target = "TargetMAC: "+sep[6]+" TargetIP: "+sep[12]#??? che pas comment split wesh



                 broadcast = "ARP 2 "+myinfo[2]+" "+sep[4]+" "+myinfo[2]+" "+myinfo[1]+" "+sep[4]+" "+targetIP 

                 sendToNodeSolo(mac,broadcast)

             print 'received ARP from' + sep[4] + 'ignoring'

       elif data.startswith("ARP 2"): 

            seplines=data.split("/n")

            sep=seplines.split(" ")

            mac=sep[6]#get their mac

            ip=sep[12]#get their ip address

            if ip=="10.0.100.3":

                peerinfo=['B',ip,mac,getportfromIP(ip)]

            elif ip=="10.0.100.4":

                peerinfo = ['C', ip, mac, getportfromIP(ip)]

            elif ip == "10.0.100.5":

                peerinfo = ['D', ip, mac, getportfromIP(ip)]

            ArpTable.append(peerinfo)#add their info in ArpTable



       elif data.startswith("arp"):

             for j in range(len(ArpTable)):

				 print(" ".join(str(ArpTable[j])))

				 

				



       else:

            rey = "give a pingmac command please"
            conn.sendall(rey)

            temp = False

 

    conn.close()





def forwardToServer(broadcast, port):

     if port==0:

        for node in othersPorts:



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


