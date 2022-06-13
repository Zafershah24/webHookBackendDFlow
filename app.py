


try:
    import urllib
    import json
    import os
    from flask import (Flask, request, make_response)
    from twilio.twiml.messaging_response import MessagingResponse

except Exception as e:

    print("Some modules are missing {}".format(e))


# Flask app should start in global layout
app = Flask(__name__)


# whenever you make request /webhook
# Following calls are made
# webhook ->
# -----------> Process requests
# ---------------------------->get_data()

@app.route("/")
def hello():
    return "Hello, World!"
@app.route("/sms", methods=['POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    msg = request.form.get('Body')
    # Create reply
    resp = MessagingResponse()
    resp.message("Hi How may  help you?")
    return str(resp)
@app.route('/webhook', methods=['POST'])
def webhook():

    if request.method == "POST":
        req = request.get_json(silent=True, force=True)
        res = processRequest(req)

        res = json.dumps(res, indent=4)
        r = make_response(res)
        r.headers['Content-Type'] = 'application/json'
        return r


def processRequest(req):

    # Get all the Query Parameter
    query_response = req["queryResult"]
    print(query_response)
    text = query_response.get('queryText', None)
    parameters = query_response.get('parameters', None)

    res = get_data()

    return res


def get_data():

    speech = "Hi How may  help you? "

    return {
        "fulfillmentText": speech,
    }


if _name_ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print ("Starting app on port %d" %(port))
    app.run(debug=True, port=port, host='0.0.0.0')