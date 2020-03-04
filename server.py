from socket import *
import sys

""" kontrola poctu a spravnosti argumentu """
if len(sys.argv) != 2:
    print('chybne argumenty')
    exit(1)

serPort = sys.argv[1].split('=', 2)
if serPort[0] != 'PORT':
    print('chybne argumenty')
    exit(1)

""" ulozeni cisla portu """
serPort = int(serPort[1])

serSocket = socket(AF_INET, SOCK_DGRAM)
serSocket.bind(('', serPort))

print('server running')
print('cislo portu: ', serPort)

while True:
    mess, clientAddr = serSocket.recvfrom(2048)
    modifMess = mess + b'kkt'
    serSocket.sendto(modifMess, clientAddr)
