# SSL Certificate Expiry Checker

This is a simple Python script that takes a list of domains as input and checks the expiry dates of their SSL certificates. The domains are read from a file and the script writes the results to a file named ssl_expiry.txt.

## How it Works
The script uses the `ssl` and `datetime` libraries from the Python standard library, as well as the `cryptography` library to check the expiry dates of the SSL certificates.

- The user is prompted to enter the name of the file that contains the list of domains.
- The script then opens the file and reads the list of domains into a list.
- For each domain, the script retrieves its SSL certificate using the `ssl.get_server_certificate()` function and loads it into a `x509` object from the `cryptography` library.
- The expiration date of the SSL certificate is extracted using the `not_valid_after` attribute of the `x509` object.
- The script calculates the difference between the current date and the expiration date of the certificate, and writes the results to the output file. If the certificate has already expired, the domain name is followed by an exclamation mark. If the certificate expires within 30 days, it is followed by an asterisk.

## How to Use
1. Install the required libraries: `ssl`, `datetime`, and `cryptography`.
2. Place your list of domains in a text file, with each domain on a separate line.
3. Run the script by entering the following command in your terminal: `python ssl_certificate_expiry.py`
4. When prompted, enter the name of the file containing the list of domains.
5. The script will echo the results to the terminal.
6. The script will write the results to a file named `ssl_expiry.txt` in the same directory.

## Output Format
The output file will contain a table with the following columns:

- Domain: The domain name.
- Expiry Date: The expiration date of the SSL certificate in the format `YYYY-MM-DD`.
- (optional) `!expired`: If the certificate has already expired, this column will contain the string `!expired`.
- (optional) `*30 days`: If the certificate expires within 30 days, this column will contain the string `*30 days`.
