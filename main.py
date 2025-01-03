from flask import Flask, jsonify
import os
import requests
from dotenv import load_dotenv

# Carregar variáveis de ambiente em ambiente local
load_dotenv()

app = Flask(__name__)

def get_bnb_price():
    """
    Obtém o preço atual do BNB em USD utilizando a API da Binance.
    """
    url = "https://api.binance.com/api/v3/ticker/price"
    params = {"symbol": "BNBUSDT"}
    headers = {
        "X-MBX-APIKEY": os.getenv("BINANCE_API_KEY"),
        "User-Agent": "MyApp/1.0 (https://example.com)"
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        price = float(data["price"])
        return price
    except requests.exceptions.RequestException as req_error:
        print(f"HTTP Error fetching BNB price: {req_error}")
    except ValueError as parse_error:
        print(f"Error parsing response from Binance: {parse_error}")
    except Exception as e:
        print(f"Unexpected error fetching BNB price: {e}")
    return None

@app.route('/bnb-price', methods=['GET'])
def bnb_price():
    price = get_bnb_price()
    if price is not None:
        return jsonify({"bnb_price": price, "success": True})
    else:
        return jsonify({"message": "Failed to fetch BNB price", "success": False}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
