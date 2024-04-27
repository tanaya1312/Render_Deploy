from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

# Function to connect to PostgreSQL database
def connect_to_db():
    conn = psycopg2.connect(
        dbname="flaskdeployment",
        user="tanaya",
        password="qi3gRlLlJduD0REQurSeu72uJfpGkka4",
        host="dpg-colrd88l5elc73bo6rag-a.singapore-postgres.render.com",
        port="5432"
    )
    return conn


# Route to get list of organization names
@app.route('/organization_names', methods=['GET'])
def get_organization_names():
    try:
        # Connect to the database
        conn = connect_to_db()

        # Create a cursor
        cur = conn.cursor()

        # Execute the query to fetch organization names
        cur.execute("SELECT Organization_Name FROM Organization")

        # Fetch all organization names
        organization_names = cur.fetchall()

        # Close cursor and connection
        cur.close()
        conn.close()

        # Extract organization names from the result
        organization_names_list = [name[0] for name in organization_names]

        # Return the organization names as JSON response
        return jsonify({'organization_names': organization_names_list})

    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True)
