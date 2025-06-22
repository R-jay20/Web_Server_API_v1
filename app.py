from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import os

app = Flask(__name__)
CORS(app)

# MySQL connection configuration
db_config = {
    'host': 'gator3041.hostgator.com',
    'user': 'norsamel_admin',
    'password': 'oPu8GhjKbrp+',
    'database': 'norsamel_onlineledger'
}

def run_select_query(query):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)  # Return rows as dicts
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

@app.route('/query', methods=['GET'])
def handle_query():
    sql = request.args.get('mysql')

    if not sql or not sql.strip().lower().startswith("select"):
        return jsonify({'error': 'Only SELECT queries are allowed'}), 400

    try:
        results = run_select_query(sql)
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Allow external connections by binding to 0.0.0.0
    app.run(host='0.0.0.0', port=5000, debug=False)
