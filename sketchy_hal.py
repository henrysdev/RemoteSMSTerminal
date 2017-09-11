from flask import Flask, request, redirect
from twilio.twiml.messaging_response import Message, MessagingResponse
import re
import subprocess
import os

app = Flask(__name__)

# execute bash command and return response
def inject_bash_cmd(cmd_input):
    p = subprocess.Popen([cmd_input], stdout=subprocess.PIPE, shell=True)
    output = p.stdout.read()
    return output

# denote bash command by starting line with >
def parseMsg(recv_sms):
    resp_msg = 'Unkown command. Text "HELP" for format example'
    if re.match(r">(.+)", recv_sms):
        bash_cmd = recv_sms[1:]
        resp_msg = inject_bash_cmd(bash_cmd)
    return resp_msg

# listen for incoming messages and respond accordingly
@app.route("/", methods=['GET', 'POST'])
def sms():
    msg_body = request.form['Body']
    resp_msg = parseMsg(msg_body)

    resp = """
    <?xml version="1.0" encoding="UTF-8"?>
    <Response>
        <Message>
            {}
        </Message>
    </Response> """.format(str(resp_msg))
    return str(resp)

if __name__ == "__main__":
    app.run()