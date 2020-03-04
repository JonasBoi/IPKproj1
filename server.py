from socket import *
import sys

"""
    returns the answer to the request
"""
def parse_request(req):
    req = req.split(' ', 3)
    if req[0] == 'GET':
        req = op_get(req[1])
    elif req[0] == 'POST':
        req = op_post(req[1])
    else:
        print('405 Method Not Allowed')
        exit(1)
    return req


"""
    resolves the GET request
"""
def op_get(arg):
    return arg


"""
    resolves the POST request
"""
def op_post(arg):
    return arg


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

print('cislo portu: ', serPort)

while True:
    "mess, clientAddr = serSocket.recvfrom(2048)"
    mess = 'GET /resolve?name=apple.com&type=A HTTP/1.1'
    modifMess = parse_request(mess)
    "serSocket.sendto(modifMess, clientAddr)"
    print(modifMess)
    break
