from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
	client = OpenAI(
	    api_key="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",   # your real key
	    project="proj_1I8UTWozyVJnv8jgnBRIC4Nj",            # your project ID
	    organization="org-guKBg4cdSHH3wIpUhfVY5kwo"         # your org ID
)

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
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": """
                You are an assistant for the Indian Navy's logistics support team. Your job is to help vendors and suppliers with:

                - Gate-in procedures for item delivery
                - Updates on shipment status to Navy ships
                - Providing clear guidance on delivery documents and access
                - Maintaining a formal, respectful, and professional tone

                If the question is unrelated to logistics, politely ask the user to contact the designated officer.

                Reply in clear and concise English or Hindi as appropriate.
                """},
                {"role": "user", "content": incoming_msg}] ,
            temperature=0.5,
        max_tokens=300
        )
        reply = response['choices'][0]['message']['content']
        msg.body(reply)

    return str(resp)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
