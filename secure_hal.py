from flask import Flask, request, redirect
from twilio.twiml.messaging_response import Message, MessagingResponse
import re
import subprocess
import os

app = Flask(__name__)

# return list of all acceptable commands
def help_list():
    # TODO add more options
    resp_str = """
    STATUS
    SYN
    POWER OFF
    HELP
    """
    return resp_str

# get system info
def get_system_status():
    procs_count = len(inject_bash_cmd(['ps','uaxw']).splitlines())
    # TODO fill in with more data for system status 
    return str(procs_count) + " processes running"

# shut down machine and terminate program
def poweroff():
    reply = "poweroff failed"
    inject_bash_cmd('poweroff')
    return reply

# execute bash command and return output
def inject_bash_cmd(cmd_input):
    p = subprocess.Popen([cmd_input], stdout=subprocess.PIPE, shell=True)
    output = p.stdout.read()
    return output

# verify incoming SMS sender to prevent unauthorized shell injection
def validateMsg(recv_sms):
    # TODO flesh out with way of authenticating sender of SMS
    return True

# parse incoming message and execute respective function
def parseMsg(recv_sms):
    resp_msg = 'Unkown command. Text "HELP" for list of options'
    # for testing connection
    if recv_sms == 'SYN':
        resp_msg = 'ACK'
    elif recv_sms == 'HELP':
        resp_msg = help_list()
    elif recv_sms == 'STATUS':
        resp_msg = get_system_status()
    elif recv_sms == 'POWER OFF':
        resp_msg = poweroff()
    return resp_msg

# listen for incoming command messages and respond accordingly
@app.route("/", methods=['GET', 'POST'])
def sms():
    msg_body = request.form['Body']
    resp_msg = 'Unkown command. Text "HELP" for list of options'
    if validateMsg(msg_body):
        resp_msg = parseMsg(msg_body)

    resp = """
    <?xml version="1.0" encoding="UTF-8"?>
    <Response>
        <Message>
            {}
        </Message>
    </Response> """.format(str(resp_msg))
    print(resp)
    return str(resp)

if __name__ == "__main__":
    app.run()