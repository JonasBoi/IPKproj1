import socket
import sys
import re

"""
    check program argv and return the port number
"""
def parse_argv(argv):
    # kontrola poctu a spravnosti argumentu
    if len(argv) != 2:
        print('chybne argumenty')
        exit(1)

    ser_port = argv[1].split('=', 2)
    if len(ser_port) != 2:
        print('chybne argumenty')
        exit(1)
    if ser_port[0] != 'PORT':
        print('chybne argumenty')
        exit(1)

    # ulozeni cisla portu
    try:
        serPort = int(ser_port[1])
    except (ValueError, TypeError):
        print('chybne argumenty')
        exit(1)
    return ser_port[1]


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

    req_answer = 400
    if re.match('^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?).){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', address):
        if req_type == 'PTR':
            req_answer = socket.gethostbyaddr(address)
            req_answer = req_answer[0]
        else:
            return 400
    elif req_type == 'A':
        try:
            req_answer = socket.gethostbyname_ex(address)
            req_answer = req_answer[2]
            req_answer = req_answer[0]
        except (socket.error, socket.herror, socket.gaierror, socket.timeout):
            return 400

    return req_answer


"""
    resolves the POST request
"""
def op_post(arg):
    return arg


"""
--------------
MAIN_MAIN_MAIN_MAIN_MAIN_MAIN_MAIN_MAIN_MAIN_MAIN_MAIN_MAIN_MAIN_MAIN_MAIN_MAIN_MAIN_MAIN_
--------------
"""

serPort = parse_argv(sys.argv)

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
mess = 'GET /resolve?name=apple.com&type=A HTTP/1.1'
modifMess = parse_request(mess)

if modifMess == 400:
    print('400 Bad request')
    exit(0)
if modifMess == 405:
    print('405 Method Not Allowed')
    exit(0)

print(modifMess)
