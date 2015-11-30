from Crypto.Hash import SHA256

from Crypto import Random
import os.path
import os
from Crypto.Cipher import DES


from bs4 import BeautifulSoup
import requests
import sys

URL_BASE = "http://localhost:8000"
URL_SIGNIN = "http://localhost:8000/signin/"

iv = b'\x15\xff\xf3\xdfL\xa3\x82\xb8'

class Report:
    def __init__(self, desc, full_desc, rep, private, timestamp):
        self.description = str(desc)
        self.full_description = full_desc
        self.reporter = rep
        self.is_private = private
        self.created_at = timestamp
        self.id = 0

    def __unicode__(self):
        return self.description

    def __repr__(self):
        return self.description

    def __str__(self):
        return self.description

    def full_summary(self):
        return "Description: %s\n\nFull Description: %s\n\nReporter: %s\n\nIs it Private?: %s\n\nCreated At: %s" % (self.description, self.full_description, self.reporter, self.is_private, self.created_at)




def encrypt_text(text, key):
    key_size8 = key[0:8]
    cipher = DES.new(key_size8, DES.MODE_CFB, iv)
    encrypted = cipher.encrypt(text)
    return encrypted

def decrypt_text(text, key):
    key_size8 = key[0:8]
    cipher = DES.new(key_size8, DES.MODE_CFB, iv)
    return cipher.decrypt(text)

def downloadFile():
    #include code to download the file here
    pass

def viewFiles():
    print('REPORTS:')
    for file in os.listdir(os.curdir):
        if file.endswith(".txt"):
            print(file)
            print('\n')
    while True:
       choice = raw_input('Which file would you like to open (enter q to quit): ')
       if choice is 'q':
          break
       elif not os.path.isfile(choice):
          print('THAT FILE DOES NOT EXIST')
       else:
          f = open(choice, 'r')
          contents = f.read()
          f.close()
          print('\n')
          print(choice)
          print(contents)
          print('\n')
          break


def decrypt_file(fileName, key):
    if not os.path.isfile(fileName):
        print('\nTHAT FILE IS NOT IN THE CURRENT DIRECTORY OR DOES NOT EXIST. PLEASE TRY AGAIN\n')
        return False
    output = ""
    f = open(fileName, 'rb')
    key_size8 = key[0:8]
    cipher = DES.new(key_size8, DES.MODE_CFB, iv)
    for line in f:
        output += cipher.decrypt(line)
        output += '\n'
        print '\n'
        print fileName
        print
        print output

def encrypt_file(fileName, key):
    if not os.path.isfile(fileName):
        print('\nTHAT FILE IS NOT IN THE CURRENT DIRECTORY OR DOES NOT EXIST. PLEASE TRY AGAIN\n')
        return False
    f = open(fileName, 'rb')
    f2 = open(fileName+'.enc', 'wb')
    key_size8 = key[0:8]
    cipher = DES.new(key_size8, DES.MODE_CFB, iv)
    for line in f:
	f2.write(cipher.encrypt(line))
        print '\n'
        print fileName+'.enc is encrypted and saved to the current directory'
        print

def logIn():
    print('Please Log In')
    user_name = raw_input('Username: ')
    password = raw_input('Password: ')

    # Start a session so we can have persistant cookies
 
    # Session() &gt;&gt; http://docs.python-requests.org/en/latest/api/#request-sessions
    client = requests.Session()
    
    # retrieve the CSRF token first, set cookie
    csrftoken = client.get(URL_SIGNIN).cookies['csrftoken']

    # This is the form data that the page sends when logging in
    login_data = {
      'user_name': user_name,
      'password': password,
      'csrfmiddlewaretoken' : csrftoken,
    }
    #print(login_data)
 
    # Authenticate
    response = client.post(URL_SIGNIN, data=login_data)
 
    # Try accessing a page that requires you to be logged in
    response = client.get('http://localhost:8000/reports/')

    html = response.text
    find_report_urls(html)
    make_reports()
    client.close()

def find_report_urls(html):
    soup = BeautifulSoup(html, 'html.parser')

    # clear reports if there was a previous login
    global report_urls
    report_urls = []

    # DON'T FUCK WITH THESE LINES AND/OR TEMPLATES/REPORTS/INDEX.HTML
    if (soup.find(id='reports') == None):
        return

    for rs in soup.find('ul', id="reports").find_all('a'):
        report_urls.append("%s%s" % (URL_BASE, rs['href']))


def make_reports():
    global user_reports
    user_reports = {}

    worker = requests.Session()
    if len(report_urls) == 0:
        print("\nNo Reports to Display\n")
        return

    i = 0
    for url in report_urls:
        html = worker.get(url).text
        report = make_report_object(html)
        report.id = i
        user_reports[i] = report
        i+=1

    worker.close()
  

def display_remote_reports():
    global user_reports
    while True:
        print("\n#  Description")
        for k, v in user_reports.iteritems():
            print("%s. %s" % (k, v.description))
        
        print("\nSelect an Option:")
        print("    a. View Report")
        print("    b. Download a Report")
        print("    Enter 'q' to quit")
        choice = raw_input("--->> ")

        if choice == 'a':
            view_report()
        elif choice == 'b':
            download_report()
        elif choice == 'q':
            break

# TODO: change to viewing the files in the report?
def view_report():
    global user_reports
    r_id = int(raw_input("Which Report? Enter Report #\n"))
    report = user_reports[r_id]
    os.system('clear')
    print(report.full_summary())

# TODO: change to downloading the files attached to the report?
def download_report():
    pass



def make_report_object(html):
    soup = BeautifulSoup(html, 'html.parser')
    desc = list(soup.find(id='descr').descendants)[0].strip()
    full_desc = list(soup.find(id='full descr').descendants)[0].strip()
    rep = list(soup.find(id='reporter').descendants)[0].strip()
    private = list(soup.find(id='is private').descendants)[0].strip()
    timestamp = list(soup.find(id='timestamp').descendants)[0].strip()
    return Report(desc, full_desc, rep, private, timestamp)




def mainMenu():
    while True:
        print('Please select one of the following options.')
        print('1. View/Download Articles')
	print('2. Encryt File')
        print('3. Decrypt File')
        print('4. Relog In')
        print('5. Display Remote Reports')
        print('0. Quit')
        choice = raw_input('Enter your choice: ')


        if choice == '1':
            os.system('clear')
            viewFiles()
	elif choice == '2':
	    os.system('clear')
	    filename = raw_input('Enter the name of the file you want to encrypt: ')
	    securekey = raw_input('Enter the key: ')
	    encrypt_file(filename, securekey)
        elif choice == '3':
            os.system('clear')
            filename = raw_input('Enter the name of the file you want to decrypt: ')
	    securekey = raw_input('Enter the key: ')
            decrypt_file(filename, securekey)
        elif choice == '3':
            os.system('clear')
            logIn()
        elif choice == '4':
            os.system('clear')
            display_remote_reports()
        elif choice == '0':
            sys.exit(0)
        else:
            print('PLEASE ENTER A VALID CHOICE\n')


if __name__ == "__main__":
    print('Secure Share v1.0')
    global report_urls
    global user_reports
    report_urls = []
    user_reports = {}
    logIn()
    mainMenu()
