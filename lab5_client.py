import socket	#for sockets
import sys	#for exit
import select
from check import ip_checksum


def rdt_send(data, ack, sock, addr):
	checksum = ip_checksum(data)
	to_send = checksum + chr(0+ack) + data
	sock.sendto(to_send.encode(), addr)


try:
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
	print("Failed to create socket")
	sys.exit()

host = 'localhost';
port = 8888;

ack_seq = 0

inputs = [mySocket]
output = []

timeout = 10

readbale, writeable, exceptional = select.select( inputs, outputs, inputs, timeout)

while(1) :
	msg = input('Enter message to send : ')
	
	ack_rcvd = False
	while not ack_rcvd:
		# s.sendto(msg.encode(), (host, port))
		rdt_send(msg, ack_seq, inputs[0], (host, port))
		
		for tempSock in readable:
			try:
				d = tempSock.recvfrom(1024)
				reply = d[0]
				addr = d[1]
		
				checksum = reply[:2]
				ack_seq = reply[2]
				message = reply[3:]
			
				print(message)

				calcSum = ip_checksum(message)
				if calcSum == checksum and ack_seq == str(seq):
					ack_rcvd = True

		
	
			except socket.error as msg:
				print ("Error Code : " + str(msg[0]) + " Message " + msg[1].decode())
				sys.exit()
