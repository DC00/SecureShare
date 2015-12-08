from Crypto.Hash import SHA256

from Crypto import Random
import os.path
import os
from Crypto.Cipher import DES

from Crypto.Cipher import ARC4
import binascii
import base64

from bs4 import BeautifulSoup
import requests
import sys
import time

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
        self.file_text = ""
        self.id = -1

    def __unicode__(self):
        return self.description

    def __repr__(self):
        return self.description

    def __str__(self):
        return self.description

    def full_summary(self):
        return "Description: %s\nFull Description: %s\nReporter: %s\nIs it Private?: %s\nCreated At: %s\nFile Text: %s\n" % (self.description, self.full_description, self.reporter, self.is_private, self.created_at, self.file_text)


def encrypt_text(text, key):
    key_size8 = key[0:8]
    cipher = DES.new(key_size8, DES.MODE_CFB, iv)
    encrypted = cipher.encrypt(text)
    return encrypted

def decrypt_text(text, key):
    key_size8 = key[0:8]
    cipher = DES.new(key_size8, DES.MODE_CFB, iv)
    return cipher.decrypt(text)

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
    os.system('clear')
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


    login_was_successful = find_report_urls(html)
    if login_was_successful:
        print("Logged in Successfully!")
    else:
        print("Error while trying to log in. Please try again")


    # At this point, have all the urls of reports that the user has made/shared with them
    # Because Django is being a pussy ass little bitch the worker in make_reports() is
    # not being persisted in the client session
    global user_reports
    user_reports = {}

    # Indexing the user's files
    global user_files
    user_files = {}

    i = 1
    for url in report_urls:
        html = client.get(url).text
        report = make_report_object(html)
        report.id = i
        user_reports[report.id] = report
        tomato_soup = BeautifulSoup(html, 'html.parser')

        if (tomato_soup.find(id='no files')):
            report.file_text = "No uploaded files"
        else:
            for fs in tomato_soup.find(id='uploaded files').find_all('a'):
                path = "%s%s" % (URL_BASE, fs['href'])
                clams = client.get(path).text
                clam_chowder = BeautifulSoup(clams, 'html.parser')
                raw_text = clam_chowder.find(id='file text').text.strip()
                user_files[report.id] = raw_text
                report.file_text = raw_text
        i+=1

    client.close()

def find_report_urls(html):
    soup = BeautifulSoup(html, 'html.parser')
    # clear reports if there was a previous login
    global report_urls
    report_urls = []

    # DON'T FUCK WITH THESE LINES AND/OR TEMPLATES/REPORTS/INDEX.HTML
    if (soup.find(id='reports') == None):
        return False

    for rs in soup.find('ul', id="reports").find_all('a'):
        report_urls.append("%s%s" % (URL_BASE, rs['href']))

    return True
  

def display_remote_reports():
    global user_reports
    while True:
        print("#  Description")
        for k, v in user_reports.iteritems():
            print("%s. %s" % (k, v.description))
        print("\n0. Main Menu")
        report_choice = int(raw_input(">>>  "))
        if report_choice == 0:
            mainMenu()
        view_report(report_choice)


# TODO: change to viewing the files in the report?
def view_report(r_id):
    global user_reports
    global user_files
    report = user_reports[r_id]
    os.system('clear')
    print(report.full_summary())
    print("1. Download Report\n2. View Attached File\n3. Go Back\n4. Decrypt File\n5. Encrypt File\n0. Main Menu")
    input_key = str(raw_input(">>>  "))

    if input_key == '1':
        download_file(r_id, user_files[r_id])
    elif input_key == '2':
        view_file(r_id)
    elif input_key == '3':
        display_remote_reports()
    elif input_key == '4':
        decrypt_file_text(r_id, user_files[r_id])
    elif input_key == '5':
        encrypt_file_text(r_id, user_files[r_id])
    elif input_key == '0':
        mainMenu()


def encrypt_file_text(r_id, file_text):
    global user_files
    global user_reports
    key = str(raw_input("Please enter your password: "))
    print(file_text)
    print("###########################################################")
    encrypted_text = base64.b64encode(encrypt(file_text, key))
    print(encrypted_text)
    user_files[r_id] = encrypted_text
    user_reports[r_id].file_text = encrypted_text
    return encrypted_text


def decrypt_file_text(r_id, file_text):
    key = str(raw_input("Please enter your password: "))
    cipher = ARC4.new(key)
    decrypted_text = decrypt(base64.b64decode(file_text), key)
    print(file_text)
    print("\n###########################################################\n")
    print(decrypted_text.decode('utf-8'))
    return decrypted_text.decode("utf-8")


def decrypt(text, key):
    cipher = ARC4.new(key)
    decrypted_text = cipher.decrypt(text)
    return decrypted_text.decode("utf-8")

def encrypt(text, key):
    cipher = ARC4.new(key)
    encrypted_text = cipher.encrypt(text.encode('utf-8'))
    return encrypted_text


def download_file(r_id, file_text):
    filename = "downloaded_file_id-%s.txt" % (r_id)
    with open(filename, 'wb') as writer:
        writer.write(file_text)
    for i in range(101):
        time.sleep(0.02)
        sys.stdout.write("\r%d%%" % i)
        sys.stdout.flush()


def view_file(r_id):
    global user_files
    if user_files.get(r_id) == None:
        print("No uploaded files")
    else:
        print("\n%s\n" % (user_files[r_id]))


def make_report_object(html):
    soup = BeautifulSoup(html, 'html.parser')
    desc = list(soup.find(id='descr').descendants)[0].strip()
    full_desc = list(soup.find(id='full descr').descendants)[0].strip()
    rep = list(soup.find(id='reporter').descendants)[0].strip()
    private = list(soup.find(id='is private').descendants)[0].strip()
    timestamp = list(soup.find(id='timestamp').descendants)[0].strip()
    return Report(desc, full_desc, rep, private, timestamp)
    return Report(desc="haha", full_desc="haha", rep="haha", private=False, timestamp="now")




def mainMenu():
    while True:
        print('Please select one of the following options.')
        print('1. Display Remote Reports')
        print('2. Relog In')
        print('0. Quit')
        choice = raw_input('Enter your choice: ')

        if choice == '1':
            os.system('clear')
            display_remote_reports()
        elif choice == '2':
            os.system('clear')
            logIn()
        elif choice == '0':
            sys.exit(0)
        else:
            print('PLEASE ENTER A VALID CHOICE\n')

        # if choice == '1':
        #     os.system('clear')
        #     viewFiles()
        # elif choice == '2':
        #     os.system('clear')
        #     filename = raw_input('Enter the name of the file you want to encrypt: ')
        #     securekey = raw_input('Enter the key: ')
        #     encrypt_file(filename, securekey)
        # elif choice == '3':
        #     os.system('clear')
        #     filename = raw_input('Enter the name of the file you want to decrypt: ')
        #     securekey = raw_input('Enter the key: ')
        #     decrypt_file(filename, securekey)



if __name__ == "__main__":
    print('Secure Share v1.0')
    global report_urls
    global user_reports
    global user_files
    report_urls = []
    user_reports = {}
    logIn()
    mainMenu()
