from re import T
from flask import Flask, json, render_template
from flask_httpauth import HTTPBasicAuth

import utils
import subprocess
import encoder
import os
import json


def get_sample():
    sample = ['01000000', '00000100', '00000111', '00100000', '00000000', '00000000', '00000000', '01100000', '11010000', '00000001', '00000001', '11001000', '00000000', '00100011', '00000001', '00000000', '01001011', '10000000', '00000000', '00011000', '00000001', '10000000', '00000000', '00000000', '01000000', '00011000', '00111011', '00']

    return sample


# Globs
host = "192.168.0.106"
port = "5050"
api = Flask(__name__, template_folder="html", static_folder="static")
auth = HTTPBasicAuth()

def deleteTempFile():
    #os.system("rm -rf temp_signal.json")
    pass

@api.route("/", methods=['GET', 'POST'])
def homePage():
    return render_template('homepage.html') 

@api.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('homepage.html')  , 404

@auth.verify_password
def authenticate(username, password):
    if username and password:
        if username == "username" and password == "password":
            return True
        else:
            return False
    return False


def make_a_temp():
    temp_file = open('temp_signal.json', "w")
    #temp_file.truncate(0)
    return temp_file 
@api.route('/on', methods=['GET'])
@auth.login_required
def respond_turn_ac_on():
    chunks = get_sample()
    binary = ""
    
    
    chunks = utils.turn_ac_on(chunks)
    chunks = utils.perform_checksum(chunks)

    for i in chunks:
        binary+=i
    signal = encoder.encode(binary)
    signal = [int(e) for e in signal.split(', ')]
    jsonDict = {
        "command": signal
    }
    
    
    tempF = make_a_temp()
    tempF.write((json.dumps(jsonDict)))
    tempF.close()

    if os.path.exists("temp_signal.json"):
        print("Gonna send command ON ")
        print("python irrp.py -p -g17 -fir-codes command -f temp_signal.json")
        try:
            execution = subprocess.check_output("python3 /home/renessmey/develop/transmit/irrp.py -p -g17 -fir-codes command -f temp_signal.json", shell=True)
            response = {
                "error": False,
                "msg": ["command has executed sucessfully."]
            }

            #temp_file.truncate(0)
            #temp_file.close()
        except subprocess.CalledProcessError as error:
            response = {
                "error": True,
                "msg": [error.returncode, error.output]
            }
    deleteTempFile()
    print(chunks)
    return response
        
@api.route('/off', methods=['GET'])
@auth.login_required
def respond_turn_ac_off():
    chunks = get_sample()
    binary = ""
    
    
    chunks =utils.turn_ac_off(chunks)
    chunks =utils.perform_checksum(chunks)
    for i in chunks:
        binary+=i
    signal = encoder.encode(binary)
    signal = [int(e) for e in signal.split(', ')]
    jsonDict = {
        "command":  signal
    }
   
    
    tempF = make_a_temp()
    tempF.write((json.dumps(jsonDict)))
    tempF.close()

    if os.path.exists("temp_signal.json"):
        print("Gonna send command ON ")
        #print("python irrp.py -p -g17 -fir-codes command -f temp_signal.json")
        try:
            execution = subprocess.check_output(["python3 /home/renessmey/develop/transmit/irrp.py -p -g17 -fir-codes command -f temp_signal.json"], shell=True)
            response = {
                "error": False,
                "msg": ["command has executed sucessfully."]
            }
        except subprocess.CalledProcessError as error:
            response = {
                "error": True,
                "msg": [error.returncode, error.output]
            }
    deleteTempFile()
    return response

@api.route('/temp/<int:temp>', methods=['GET'])
@auth.login_required
def temperature_change(temp):
    chunkie = get_sample()
    msg = f"Command Executed temp set to {temp} "
    if not (temp >=16 and temp <= 30):
        print("Going to set default 16 temperature")
        msg = f"Command Executed temp set to 16"
        
    binary = ""
    
    
    chunkie =utils.change_temperature(chunkie, temp)
    
    chunkie =utils.perform_checksum(chunkie)
    
    for i in chunkie:
        binary+=i
    signal = encoder.encode(binary)
    signal = [int(e) for e in signal.split(', ')]
    jsonDict = {
        "command":  signal
    }
    
    
    tempF = make_a_temp()
    tempF.write((json.dumps(jsonDict)))
    tempF.close()
    if os.path.exists("temp_signal.json"):
        print("Gonna send command ON ")
        #print("python irrp.py -p -g17 -fir-codes command -f temp_signal.json")
        try:
            execution = subprocess.check_output(["python3 /home/renessmey/develop/transmit/irrp.py -p -g17 -fir-codes command -f temp_signal.json"], shell=True)
            response = {
                "error": False,
                "msg": [msg]
            }
        except subprocess.CalledProcessError as error:
            response = {
                "error": True,
                "msg": [error.returncode, error.output.decode("utf-8")]
            }
    deleteTempFile()
    return response

@api.route('/debug', methods=['GET'])
@auth.login_required
def debug():
    chunks = get_sample()
    msg = f"Command Executed temp set to   "
    
        
    binary = ""
    
    chunks =utils.turn_ac_on(chunks)
    
    chunks[16]="01111111"
    
    chunks = utils.perform_checksum(chunks)
    
    for i in chunks:
        binary+=i
    signal = encoder.encode(binary)
    signal = [int(e) for e in signal.split(', ')]
    jsonDict = {
        "command":  signal
    }
    
    
    tempF = make_a_temp()
    tempF.write((json.dumps(jsonDict)))
    tempF.close()
    if os.path.exists("temp_signal.json"):
        print("Gonna send command ON ")
        #print("python irrp.py -p -g17 -fir-codes command -f temp_signal.json")
        try:
            execution = subprocess.check_output(["python3 /home/renessmey/develop/transmit/irrp.py -p -g17 -fir-codes command -f temp_signal.json"], shell=True)
            response = {
                "error": False,
                "msg": [msg]
            }
        except subprocess.CalledProcessError as error:
            response = {
                "error": True,
                "msg": [error.returncode, error.output.decode("utf-8")]
            }
    deleteTempFile()
    print(chunks)
    
    return response

if __name__ == '__main__':
    api.run(host, port) 
