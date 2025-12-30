import re
import socket

def check_email(email):
    result = {
        "format_valid": False,
        "domain_exists": False
    }

    regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    if re.match(regex, email):
        result["format_valid"] = True
        domain = email.split("@")[1]

        try:
            socket.gethostbyname(domain)
            result["domain_exists"] = True
        except socket.gaierror:
            pass

    return result
