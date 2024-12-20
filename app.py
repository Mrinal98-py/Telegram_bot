from twilio.rest import Client
from flask import Flask
from googlesearch import search
import requests
from twilio.twiml.messaging_response import MessagingResponse

account_sid = 'AC6445a7a485be73b9d13b159a395a6d8c'
auth_token = '[AuthToken]'
client = Client(account_sid, auth_token)

message = client.messages.create(
  from_='whatsapp:+14155238886',
  content_sid='HXb5b62575e6e4ff6129ad7c8efe1f983e',
  content_variables='{"1":"12/1","2":"3pm"}',
  to='whatsapp:+918178140149'
)

print(message.sid)


app = Flask(__name__)

@app.route("/", methods=["POST"])

# chatbot logic
def bot():

	# user input
	user_msg = request.values.get('Body', '').lower()

	# creating object of MessagingResponse
	response = MessagingResponse()

	# User Query
	q = user_msg + "geeksforgeeks.org"

	# list to store urls
	result = []

	# searching and storing urls
	for i in search(q, num_results=3):
		result.append(i)

	# displaying result
	msg = response.message(f"--- Results for '{user_msg}' ---")
	for result in search_results:
		msg = response.message(result)

	return str(response)


if __name__ == "__main__":
	app.run()
