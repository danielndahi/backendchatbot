from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import pandas as pd

app = Flask(__name__)

# Load the dataset 
dataset = pd.read_csv('tuesday.csv')
print(dataset)

@app.route("/")
def home():
    return "Welcome to the WhatsApp Bot!"


@app.route("/whatsapp", methods=['POST'])
def whatsapp_bot():
    incoming_msg = request.form.get('Body', '').lower()
    response = MessagingResponse()
    reply = process_query(incoming_msg)
    response.message(reply)
    return str(response)

def process_query(query):
    if 'price' in query:
        product_name = query.split('price of ')[-1]
        result = dataset[dataset['ProductName'].str.contains(product_name, case=False)]
        if not result.empty:
            return f"The price of {product_name} is {result.iloc[0]['Price']} {result.iloc[0]['Currency']}."
        else:
            return "Sorry, I couldn't find that product."
    return "Sorry, I didn't understand your query."

if __name__ == "__main__":
    app.run(debug=True)
