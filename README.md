# SSL Certificate Expiry Checker

This is a simple Python script that takes a list of domains as input and checks the expiry dates of their SSL certificates. The domains are read from a file and the script writes the results to the console and also to a file named `ssl_expiry.txt`.

## How it Works

The script uses the `ssl` and `datetime` libraries from the Python standard library, as well as the `cryptography` library to check the expiry dates of the SSL certificates.

- The script prompts the user for a filename, which should contain a list of domains to check.
- The script then opens the file and reads the list of domains into a list.
- For each domain, the script retrieves its SSL certificate using the `ssl.get_server_certificate()` function and loads it into a `x509` object from the `cryptography` library.
- The expiration date of the SSL certificate is extracted using the `not_valid_after` attribute of the `x509` object.
- The script calculates the difference between the current date and the expiration date of the certificate, and writes the results to the console and the output file named `ssl_expiry.txt`. If the certificate has already expired, the domain name is followed by `!expired`. If the certificate expires within 30 days, it is followed by `*30 days`.

## Requirements

This script requires Python 3.x and the following Python libraries:

- `ssl`
- `datetime`
- `cryptography`

## Installation

1. Ensure that Python 3 is installed on your system.
2. Install the required Python package with pip:

    ```bash
    pip install cryptography
    ```

## Usage

1. Install the required libraries: `ssl`, `datetime`, and `cryptography`.
2. Place your list of domains in a text file, with each domain on a separate line.
3. Run the script by entering the following command in your console: `python ssl_checker.py`
4. When prompted, enter the name of the file containing the list of domains.
5. The script will echo the results to the console.
6. The script will write the results to a file named `ssl_expiry.txt` in the same directory.

## Output
The output file and console will contain a table with the following columns:

- Domain: The domain name.
- Expiry Date: The expiration date of the SSL certificate in the format `YYYY-MM-DD`.
- (optional) If the certificate has already expired, this column will contain the string `!expired`.
- (optional) If the certificate expires within 30 days, this column will contain the string `*30 days`.

## Notes

This script does not handle all potential exceptions or errors that might occur during the SSL certificate retrieval process. If an error occurs while retrieving a certificate, the error message will be printed to the console and written to the output file. If the script cannot open the domain list file or the output file, it will print an error message and exit.

This script only checks SSL certificates on port 443. If your server uses a different port for SSL/TLS connections, you will need to modify the script.