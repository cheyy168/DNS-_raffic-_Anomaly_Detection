# scripts/simulate_attack.py
import random, string, time
import socket

def random_subdomain(length=50):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))

for _ in range(50):
    sub = random_subdomain()
    domain = f"{sub}.lab.local"
    try:
        socket.gethostbyname(domain)  # triggers DNS query
    except:
        pass
    time.sleep(0.05)
