import whois
import socket

def get_domain_info(domain):
    try:
        w = whois.whois(domain)
        return {
            "domain_name": w.domain_name,
            "registrar": w.registrar,
            "creation_date": str(w.creation_date),
            "expiration_date": str(w.expiration_date)
        }
    except Exception as e:
        return {
            "error": str(e)
        }

def get_dns_info(domain):
    try:
        ip = socket.gethostbyname(domain)
        return {
            "ip_address": ip,
            "reverse_dns": get_reverse_dns(ip)
        }
    except socket.gaierror:
        return {
            "ip_address": "Non résolu",
            "reverse_dns": "Non disponible"
        }

def get_reverse_dns(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except Exception:
        return "Non disponible"