import socket
import ssl
import datetime
from cryptography import x509
from cryptography.hazmat.backends import default_backend

# Prompt the user for the file with the list of domains
file_name = input("Enter the name of the file containing the domain list: ")

# Open the file containing the list of domains
try:
    with open(f'{file_name}', 'r') as domain_file:
        # Read the list of domains from the file, excluding comments and blank lines
        domains = [line.strip() for line in domain_file if not line.strip().startswith('//') and not line.strip().startswith('/*') and line.strip()]
except Exception as e:
    # If there's an error opening the domain list file, print an error message
    print(f"Error opening domain list file: {e}")
    exit(1)

# Open a file to write the output to
try:
    with open('ssl_expiry.txt', 'w') as out_file:

        # Write the headings
        now = datetime.datetime.now()
        header = 'SSL certificates for domains checked on '
        timestamp = now.strftime("%Y-%m-%d %H:%M")
        separator = '\n---------------------------------------------------'
        print(f'{header:<40} {timestamp} {separator}')
        out_file.write(f'{header:<40} {timestamp} {separator}\n')

        # Loop through each domain
        for domain in domains:
            # Create a flag to indicate if the certificate was successfully retrieved
            success = False
            
            try:
                # Establish a socket connection to the domain on port 443
                sock = socket.create_connection((domain, 443))
                # Wrap the socket with an SSL context
                context = ssl.create_default_context()
                with context.wrap_socket(sock, server_hostname=domain) as sslsock:
                    # Get the SSL certificate from the server
                    cert = sslsock.getpeercert(binary_form=True)
                
                # Load the SSL certificate into a cryptography object
                cert_obj = x509.load_der_x509_certificate(cert, default_backend())

                # Get the expiration date of the SSL certificate
                expiry_date = cert_obj.not_valid_after

                # Get the current date and time
                current_datetime = datetime.datetime.utcnow()

                # Calculate the difference between the current date and the expiration date
                expiry_difference = expiry_date - current_datetime
                
                # Set the flag to indicate success
                success = True
            except Exception as e:
                error_message = str(e)
                # Remove the string from the start of the error message
                if error_message.startswith("[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed:"):
                    error_message = error_message[len("[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed:"):]
                # Remove the string from the end of the error message
                error_message = error_message.split(" (_ssl.c:1002)")[0]
                print(f'{domain:<40} # ERROR  #{error_message}')
                out_file.write(f'{domain:<40} # ERROR  #{error_message}\n')

            if success:
                # If the difference is negative, the SSL certificate has expired, so add an exclamation
                if expiry_difference.days < 0:
                    output = f'{domain:<40} {expiry_date.strftime("%Y-%m-%d")} !expired\n'
                # If the difference is less than 30 days, add an asterisk
                elif expiry_difference.days < 30:
                    output = f'{domain:<40} {expiry_date.strftime("%Y-%m-%d")} *30 days\n'
                # Otherwise, just write the domain name and expiration date
                else:
                    output = f'{domain:<40} {expiry_date.strftime("%Y-%m-%d")}\n'
                    
                print(output, end='')
                out_file.write(output)
except Exception as e:
    print(f'Error opening output file: {e}')
