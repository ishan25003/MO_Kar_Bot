from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    incoming_msg = request.values.get('Body', '').strip().lower()
    print(f"User said: {incoming_msg}")

    resp = MessagingResponse()
    msg = resp.message()

    # Define basic greetings
    greetings = ['hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening']

    if any(greet in incoming_msg for greet in greetings):
        welcome_text = (
            "👋 Hello! Welcome to Material Organisation(Karwar)!\n"
            "I’m your virtual assistant Vibhu 🤖.\n"
            "How can I help you today?"
        )
        msg.body(welcome_text)
    else:
        # AI reply via OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": incoming_msg}]
        )
        reply = response['choices'][0]['message']['content']
        msg.body(reply)

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)