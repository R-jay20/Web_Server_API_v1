from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import os

app = Flask(__name__)
CORS(app)

# MySQL connection configuration from environment variables
db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USERNAME'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}
#print(type(db_config))

#'host': os.getenv('DB_HOST'),
#'user': os.getenv('DB_USERNAME'),
#'password': os.getenv('DB_PASSWORD'),
#'database': os.getenv('DB_NAME')

#'host': 'gator3041.hostgator.com',
#'user': 'norsamel_admin',
#'password': 'oPu8GhjKbrp+',
#'database': 'norsamel_onlineledger'

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

@app.route('/multi-query', methods=['POST'])
def handle_multi_query():
    data = request.get_json()
    queries = data.get('queries')

    if not queries or not isinstance(queries, list):
        return jsonify({'error': 'A list of SQL queries is required.'}), 400

    results = []

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        for query in queries:
            try:
                cursor.execute(query)
                conn.commit()
                results.append({'query': query, 'success': True})
            except Exception as qerr:
                conn.rollback()
                results.append({'query': query, 'success': False, 'error': str(qerr)})

        cursor.close()
        conn.close()
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # Allow external connections by binding to 0.0.0.0
    app.run(host='0.0.0.0', port=5000, debug=False)
