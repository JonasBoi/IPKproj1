import socket
import sys
import re


"""
    check program argv and return the port number
"""
def parse_argv(argv):
    ser_port = -1

    # kontrola poctu a spravnosti argumentu
    if len(argv) != 2:
        print('chybne argumenty')
        exit(1)

    # ulozeni cisla portu
    try:
        ser_port = int(argv[1])
    except (ValueError, TypeError):
        print('chybne argumenty')
        exit(1)

    if ser_port < 0 or ser_port > 65535:
        print('chybne argumenty')
        exit(1)

    return ser_port


"""
    returns the answer to the request
"""
def parse_request(req):
    req = req.split('\n')
    req_type = req[0].split()

    if req_type[0] == 'GET':
        if len(req_type) != 3:
            return 400
        if req_type[2] != 'HTTP/1.1':
            return 400
        req = op_get(req_type[1])

    elif req_type[0] == 'POST':

        if len(req_type) != 3:
            return 400
        if req_type[1] != '/dns-query' or req_type[2] != 'HTTP/1.1':
            return 400

        req.__delitem__(0)

        while 1:
            key = req[0].split()
            if key[0] == "Content-Type:":
                req.__delitem__(0)
                break

            req.__delitem__(0)

        req = op_post("\n".join(req))
        try:
            req = req.rstrip('\r\n')
        except:
            return 400

    else:
        return 405
    return req


"""
    resolves the GET request-----------------
"""
def op_get(arg):

    address = ""
    req_type = ""

    """check the request syntax"""
    arg = arg.split('?', 2)
    if len(arg) != 2:
        return 400
    if arg[0] != '/resolve':
        return 400

    arg = arg[1].split('=', 3)
    if len(arg) != 3:
        return 400

    if arg[0] == 'name':
        # store type request
        req_type = arg[2]
    elif arg[0] == 'type':
        address = arg[2]

    arg = arg[1]
    arg = arg.split('&', 2)
    if len(arg) != 2:
        return 400

    # store address
    if address == "":
        if arg[1] != 'type':
            return 400
        address = arg[0]
    else:
        req_type = arg[0]

    if req_type != 'A' and req_type != 'PTR':
        return 400

    # ----------------------------------------------
    # get host based on the type of request
    req_answer = 404
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
            return 404
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

    # initialise the answer
    req_answer = ""
    # checks if we got at least one result
    min_one_answer = False
    # checks if we got wrong req type or so
    syntax_bad = False
    # number of lines
    count = len(arg)
    i = 1
    while i < count:
        # ignore the blank lines
        if i == count-1 and arg[i] == "":
            if min_one_answer:
                i += 1
                continue
            else:
                if not syntax_bad:
                    return 404
                else:
                    return 400
        if i != count-1 and arg[i] == "":
            return 400

        # get rid of whitespaces and split the string
        line = arg[i].strip()
        line = line.split(':')
        if len(line) != 2:
            syntax_bad = True
            i += 1
            continue

        # get rid of whitespaces
        address = line[0].strip()
        req_type = line[1].strip()

        # badrequest
        if req_type != 'A' and req_type != 'PTR':
            syntax_bad = True
            i += 1
            continue

        # ----------------------------------------------
        # get host based on the type of request
        # PTR - REQ
        if re.match('^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?).){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', address):
            if req_type == 'PTR':
                try:
                    answer = socket.gethostbyaddr(address)
                except (socket.error, socket.herror, socket.gaierror, socket.timeout):
                    i += 1
                    continue
                answer = answer[0]
                try:
                    req_answer += address + ':' + req_type + '=' + answer + '\r\n'
                    min_one_answer = True
                except (ValueError, TypeError):
                    return 99
            else:
                i += 1
                continue
        # A - REQ
        elif req_type == 'A':
            try:
                answer = socket.gethostbyname_ex(address)
            except (socket.error, socket.herror, socket.gaierror, socket.timeout):
                i += 1
                continue
            answer = answer[2]
            answer = answer[0]
            try:
                req_answer += address + ':' + req_type + '=' + answer + '\r\n'
                min_one_answer = True
            except (ValueError, TypeError):
                print("parse_error")
                return 99
        i += 1

    """
    if we didnt get a single answer for the requests, we chceck if there
    was also a syntactic fault, if so, we return 400 because its a bigger fault
    """
    if not min_one_answer:
        if not syntax_bad:
            return 404
        else:
            return 400

    return req_answer


"""
    adds the header or uses the right error header
"""
def add_header(modif_mess):
    answer = "HTTP/1.1 200 OK\r\n"
    answer += "\r\n"

    if modif_mess == 400:
        answer = "HTTP/1.1 400 Bad Request\r\n"
    elif modif_mess == 405:
        answer = "HTTP/1.1 405 Method Not Allowed\r\n"
    elif modif_mess == 404:
        answer = "HTTP/1.1 404 Not Found\r\n"
    elif modif_mess == 99:
        print('parse error')
        exit(0)
    elif modif_mess == "":
        answer = "HTTP/1.1 404 Not Found\r\n"
    else:
        answer += modifMess + "\r\n"

    return answer


"""
--------------
MAIN_MAIN_MAIN_MAIN_MAIN_MAIN_MAIN_MAIN_MAIN_MAIN_MAIN_MAIN_MAIN_MAIN_MAIN_MAIN_MAIN_MAIN_
--------------
"""

serPort = parse_argv(sys.argv)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

    try:
        sock.bind(('localhost', serPort))
    except socket.error:
        print("bind failed")
        exit(1)
    sock.listen()

    while True:
        try:
            conn, clientAddr = sock.accept()
        except:
            exit(0)
        mess = conn.recv(2048)
        if not mess:
            break
        mess = mess.decode()

        modifMess = parse_request(mess)
        modifMess = add_header(modifMess)

        modifMess = modifMess.encode()

        conn.sendall(modifMess)
        conn.close()
