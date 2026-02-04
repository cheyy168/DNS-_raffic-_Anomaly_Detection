import random
import string
import time
import socket

DNS_SERVER = "127.0.0.1"   # Technitium DNS
DOMAIN = "lab.local"

def random_payload(length=40):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def send_query(domain):
    try:
        socket.gethostbyname(domain)
    except:
        pass

for i in range(100):
    payload = random_payload()
    fqdn = f"{payload}.{DOMAIN}"
    print(f"Sending: {fqdn}")
    send_query(fqdn)
    time.sleep(1)
