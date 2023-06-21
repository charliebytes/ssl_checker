import ssl
import socket
import datetime
import csv
from cryptography import x509
from cryptography.hazmat.backends import default_backend

def check_certificate(domain):
    try:
        # Get the SSL certificate for the domain
        cert = ssl.get_server_certificate((domain, 443))
    except socket.error as e:
        print(f"Error connecting to {domain}: {e}")

    try:
        with ssl.create_default_context().wrap_socket(socket.socket(), server_hostname=domain) as s:
            cert = s.getpeercert()
    except Exception as e:
        return f"Error retrieving certificate for domain {domain}: {e}"
    
    cert_obj = x509.load_pem_x509_certificate(ssl.DER_cert_to_PEM_cert(cert), default_backend())
    expiry_date = cert_obj.not_valid_after
    current_datetime = datetime.datetime.utcnow()
    expiry_difference = expiry_date - current_datetime
    return domain, expiry_date, expiry_difference.days

try:
    with open("domain_list.txt", "r") as domain_file, open("ssl_expiry.csv", "w", newline="") as out_file:
        domains = domain_file.read().splitlines()
        writer = csv.writer(out_file)
        writer.writerow(["Domain", "Expiry Date", "Days to Expiry"])
        
        for domain in domains:
            result = check_certificate(domain)
            if isinstance(result, tuple):
                domain, expiry_date, days_to_expiry = result
                writer.writerow([domain, expiry_date.strftime("%Y-%m-%d"), days_to_expiry])
            else:
                writer.writerow([result])
except Exception as e:
    print(f"Error opening files: {e}")
