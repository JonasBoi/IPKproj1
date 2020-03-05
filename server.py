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
    req = req.split(' ')

    if req[0] == 'GET':
        if len(req) != 3:
            return 400
        if req[2] != 'HTTP/1.1':
            return 400
        req = op_get(req[1])
    elif req[0] == 'POST':
        req.__delitem__(0)
        req = op_post(" ".join(req))
    else:
        return 405
    return req


"""
    resolves the GET request-----------------
"""
def op_get(arg):

    """check the request syntax"""
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
        # store type request
        req_type = arg[2]

    arg = arg[1]
    arg = arg.split('&', 2)
    if len(arg) != 2:
        return 400

    # store address
    address = arg[0]
    if arg[1] != 'type':
        return 400
    """----------------------------------------------
        get host based on the type of request
    """
    req_answer = 400
    # PTR - REQ
    if re.match('^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?).){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', address):
        if req_type == 'PTR':
            try:
                req_answer = socket.gethostbyaddr(address)
            except (socket.error, socket.herror, socket.gaierror, socket.timeout):
                return 404
            req_answer = req_answer[0]
            try:
                req_answer = address + ':' + req_type + '=' + req_answer
            except (ValueError, TypeError):
                print("parse_error")
                return 99
        else:
            return 400
    # A - REQ
    elif req_type == 'A':
        try:
            req_answer = socket.gethostbyname_ex(address)
        except (socket.error, socket.herror, socket.gaierror, socket.timeout):
            return 404
        req_answer = req_answer[2]
        req_answer = req_answer[0]
        try:
            req_answer = address + ':' + req_type + '=' + req_answer
        except (ValueError, TypeError):
            print("parse_error")
            return 99

    return req_answer


"""
    resolves the POST request-------------------------
"""
def op_post(arg):
    arg = arg.split('\n')

    # check the "header"
    line = arg[0].split()
    if len(line) != 2:
        return 400
    if line[0] != '/dns-query' or line[1] != 'HTTP/1.1':
        return 400

    count = len(arg)
    i = 1
    while i < count:
        if i == count-1 and arg[i] == "":
            break

        line = arg[i].strip()
        line = line.split(':')
        if len(line) != 2:
            return 400

        address = line[0].strip()
        req_type = line[1].strip()

        if re.match('^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?).){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', address):
            if req_type == 'PTR':
                i += 1
                continue
                try:
                    req_answer = socket.gethostbyaddr(address)
                except (socket.error, socket.herror, socket.gaierror, socket.timeout):
                    return 404
                req_answer = req_answer[0]
                try:
                    req_answer = address + ':' + req_type + '=' + req_answer
                except (ValueError, TypeError):
                    print("parse_error")
                    return 99
            else:
                return 400
        # A - REQ
        elif req_type == 'A':
            i += 1
            continue

            try:
                req_answer = socket.gethostbyname_ex(address)
            except (socket.error, socket.herror, socket.gaierror, socket.timeout):
                return 404
            req_answer = req_answer[2]
            req_answer = req_answer[0]
            try:
                req_answer = address + ':' + req_type + '=' + req_answer
            except (ValueError, TypeError):
                print("parse_error")
                return 99
        i += 1

    return "OK"


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
messGet = "GET /resolve?name=17.142.160.59&type=PTR HTTP/1.1"
messPost = "POST /dns-query HTTP/1.1\n" \
           "www.fit.vutbr.cz:A\n" \
           "www.google.com:A\n" \
           "www.seznam.cz:A\n" \
           "147.229.14.131:PTR\n" \
           "ihned.cz:A\n"
modifMess = parse_request(messPost)

if modifMess == 400:
    print('400 Bad Request')
    exit(0)
if modifMess == 405:
    print('405 Method Not Allowed')
    exit(0)
if modifMess == 404:
    print('404 Not Found')
    exit(0)

print(modifMess)
