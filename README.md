# Computer-Networks - ARP

Nodes	 on	 the	 same	 subnet	 communicate	 using	 MAC	 addresses	 and	 the	 Address	 Resolution	
Protocol aka ARP,	 is	 used	 to	 resolve	 IP	 addresses	 into	 MAC	 addresses.	 When	 a host	 A	 needs	 to	
communicate	to	host	B	on	the	same	subnet,	host	A	sends	packets	using	host	B’s	MAC	address.	

### WHAT

This is a simplified	version	of the	ARP	protocol.

### START
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

5. SSH into the VM(open 4 windows since our subnet is made of 4 nodes):
` ssh -Y -l <user name> -p 2222 localhost`

