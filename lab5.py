import socket
import sys
import select
from check import ip_checksum

HOST = ''
PORT = 8888


def rdt_send(data, ack, sock, addr):
	checksum = ip_checksum(data)
	to_send = checksum + chr(0+ack) + data
	sock.sendto(to_send.encode(), addr)


try :
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	print ("Socket created")
except socket.error as msg :
	print ("Failed to create socket. Error Code : " + str(msg[0]) + " Message " + msg[1])
	sys.exit()


try:
	s.bind((HOST, PORT))
except socket.error as msg:
	print ("Bind failed. Error Code : " + str(msg[0]) + " Message " + msg[1])
	sys.exit()
	
print ("Socket bind complete")
ack_val = 0

while 1:
	d = s.recvfrom(1024)
	data = d[0]
	addr = d[1]

	checksum = data[:2]
	sequence = data[2]
	message = data[3:]

	if not data: 
		break

	print(message)

	calcSum = ip_checkum(message)
	if calcSum == checksum:
		# rdt_send(message, ack_val, s,  addr)
		print(sequence)
		print(ack_val) 
		if sequence == chr(0 + ack_val):
			print(message)
			rdt_send(message, ack_val, s, addr)
			ack_val = 0 if ack_val == 1 else 1
	else:
		nak = 0 if ack_val == 1 else 1
		rdt_send("ACK", nak, s, addr)
	
	# reply = 'OK...' + data.decode()
	
	# s.sendto(reply.encode() , addr)
	# print ("Message[" + (addr[0]) + ":" + str(addr[1]) + "] - " + data.strip().decode())
	
s.close()
