# Address	 Resolution	Protocol

Nodes	 on	 the	 same	 subnet	 communicate	 using	 MAC	 addresses	 and	 the	 Address	 Resolution	
Protocol aka ARP,	 is	 used	 to	 resolve	 IP	 addresses	 into	 MAC	 addresses.	 When	 a host	 A	 needs	 to	
communicate	to	host	B	on	the	same	subnet,	host	A	sends	packets	using	host	B’s	MAC	address.	

### What

This is a simplified	version	of the	ARP	protocol.

### Start
(assuming your OS is Linux)

1. Get VirtualBox:
https://www.virtualbox.org/wiki/Linux_Downloads

2. Get Mininet VM image:
https://github.com/mininet/mininet/wiki/Mininet-VM-Images

3. After Booting your VM:

Create a new VM.
Pick the .vmdk file as the virtual hard disk of the VM.

4. Enabling Port Forwarding:

Select your VM, go to settings, then network, then advanced, finally port forwarding.
Now add a rule(the green +) with TCP host port 2222 and guest port 22.
Save and close the window.

5. SSH into the VM(open 4 windows since our subnet is made of 4 nodes). Also you will be asked for the password:

`ssh -Y -l <user name> -p 2222 localhost`

### Testing

1. In each window start node A, B, C and D. Please note that each node's MAC address, listening port and IP address were hardcoded.
2. To print the ARP table(which will be empty in the beginning): `arp -a`
3. To fill node A's ARP table:
`telnet	localhost	8000`
`pingmac 10.0.100.3`
`pingmac 10.0.100.4`
`pingmac 10.0.100.5`
4. To check if the table is now filled, type again: `arp -a`
