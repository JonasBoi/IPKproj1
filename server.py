import socket
import sys
import re


"""
    returns the answer to the request
"""
def parse_request(req):
    req = req.split(' ', 3)
    if len(req) != 3:
        return 400

    if req[0] == 'GET':
        req = op_get(req[1])
    elif req[0] == 'POST':
        req = op_post(req[1])
    else:
        return 405
    return req


"""
    resolves the GET request
"""
def op_get(arg):

    arg = arg.split('?', 2)
    if len(arg) != 2:
        return 400
    if arg[0] != '/resolve':
        return 400

    arg = arg[1].split('=', 3)
    if len(arg) != 3:
        return 400
    if arg[0] != 'name':
        return 400

    if arg[2] != 'A' and arg[2] != 'PTR':
        return 400
    else:
        req_type = arg[2]

    arg = arg[1]
    arg = arg.split('&', 2)
    if len(arg) != 2:
        return 400

    address = arg[0]
    if arg[1] != 'type':
        return 400

    if re.match('^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?).){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', address):
        vysledek = socket.gethostbyaddr(address)
        vysledek = vysledek[0]
    else:
        try:
            vysledek = socket.gethostbyname_ex(address)
            vysledek = vysledek[2]
            vysledek = vysledek[0]
        except (socket.error, socket.herror, socket.gaierror, socket.timeout):
            return 400

    return vysledek


"""
    resolves the POST request
"""
def op_post(arg):
    return arg


# kontrola poctu a spravnosti argumentu
if len(sys.argv) != 2:
    print('chybne argumenty')
    exit(1)

serPort = sys.argv[1].split('=', 2)
if serPort[0] != 'PORT':
    print('chybne argumenty')
    exit(1)

# ulozeni cisla portu
serPort = int(serPort[1])

"""
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind(('', serPort))
    sock.listen()

    conn, clientAddr = sock.accept()
    with conn:
        while True:
            mess = conn.recv(2048)
            if not mess:
                break
            mess = mess.decode()

            modifMess = parse_request(mess)
            modifMess = modifMess.encode()

            conn.sendall(modifMess)
"""


"""TESTOVACÍ HODNOTY"""
mess = 'GET /resolve?name=facebook.com&type=A HTTP/1.1'
modifMess = parse_request(mess)

if modifMess == 400:
    print('400 Bad request')
    exit(0)
if modifMess == 405:
    print('405 Method Not Allowed')
    exit(0)

print(modifMess)
