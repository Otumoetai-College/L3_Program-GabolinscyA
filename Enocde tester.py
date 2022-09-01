from flask import Flask
from flask_bcrypt import Bcrypt
import os
computer_username = os.getlogin()

app = Flask(__name__)
bcrypt = Bcrypt(app)

username_file = open(
            "C:/Users/{}/Documents/L2_ASSIGNMENT_RPG/account_data_username.txt".format(computer_username), "r")
password_file = open(
            "C:/Users/{}/Documents/L2_ASSIGNMENT_RPG/account_data_password.txt".format(computer_username), "r")
username_file_r = username_file.read()
username_file.close()
inputted_username = input("whats ur username")
inputted_password = input("whats ur password")
password_encoder = inputted_username and inputted_password
while True:
    password_file_r = password_file.readline()
  #  password_file_r.replace('"\n"', '')
    if not password_file_r:
        break
    try:
        if bcrypt.check_password_hash(password_file_r, password_encoder):
            answer = bcrypt.check_password_hash(password_file_r, password_encoder)
        #if str(username_encoder) in username_file_r:
            print("yes")
    except:
        print("no")
