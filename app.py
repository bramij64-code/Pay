from flask import Flask, request, jsonify
import os
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Payment links
PAYMENT_LINKS = {
    10: "https://api.zapupi.com/instent-pay-WkFQVVBJNjkyYzBkZGRlMWFkYQ",
    20: "https://api.zapupi.com/instent-pay-WkFQVVBJNjkyYzBkZjdhOTI4Mg",
    50: "https://api.zapupi.com/instent-pay-WkFQVVBJNjkyYzBlMGU2YTI4Ng",
    100: "https://api.zapupi.com/instent-pay-WkFQVVBJNjkyYzBlM2M0OWQ2Yg"
}

@app.route('/')
def home():
    return jsonify({
        "message": "Tournament App API is running!",
        "endpoints": {
            "webhook": "/webhook/zapupi (POST)",
            "payment_links": "/payment-links"
        }
    })

@app.route('/payment-links')
def payment_links():
    return jsonify(PAYMENT_LINKS)

# Main webhook endpoint
@app.route('/webhook/zapupi', methods=['POST'])
def zapupi_webhook():
    try:
        # Get JSON data from Zapupi
        data = request.get_json()
        
        # If JSON is empty, try form data
        if not data:
            data = request.form.to_dict()
        
        logging.info(f"🔔 Webhook received: {data}")
        
        # Extract fields
        transaction_id = data.get('transaction_id', data.get('txn_id'))
        amount = data.get('amount', data.get('amt'))
        status = data.get('status', data.get('payment_status'))
        
        logging.info(f"📊 Parsed - Transaction: {transaction_id}, Amount: {amount}, Status: {status}")
        
        # Process payment status
        if status in ['success', 'completed', 'SUCCESS', 'paid']:
            logging.info(f"✅ Payment successful: {transaction_id}, Amount: {amount}")
            
            # TODO: Add your database logic here
            # update_transaction_status(transaction_id, 'completed')
            # update_user_balance(transaction_id, amount)
            
            response = {
                "status": "success",
                "message": "Payment verified and processed",
                "transaction_id": transaction_id,
                "amount": amount
            }
            
        elif status in ['failed', 'FAILED', 'error']:
            logging.warning(f"❌ Payment failed: {transaction_id}")
            # update_transaction_status(transaction_id, 'failed')
            
            response = {
                "status": "failed", 
                "message": "Payment failed",
                "transaction_id": transaction_id
            }
            
        else:
            logging.info(f"⚠️ Payment pending: {transaction_id}, Status: {status}")
            response = {
                "status": "pending",
                "message": "Payment is processing",
                "transaction_id": transaction_id
            }
        
        return jsonify(response), 200
        
    except Exception as e:
        logging.error(f"🚨 Webhook error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Webhook processing failed: {str(e)}"
        }), 400

# Health check for Render
@app.route('/health')
def health_check():
    return jsonify({"status": "healthy", "service": "tournament-app"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
