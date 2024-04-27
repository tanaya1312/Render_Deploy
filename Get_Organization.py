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


# Route to get list of organizations
@app.route('/organizations', methods=['GET'])
def get_organizations():
    try:
        # Connect to the database
        conn = connect_to_db()

        # Create a cursor
        cur = conn.cursor()

        # Execute the query to fetch organizations
        cur.execute("SELECT * FROM Organization")

        # Fetch all organizations
        organizations = cur.fetchall()

        # Close cursor and connection
        cur.close()
        conn.close()

        # Convert the organizations to a list of dictionaries
        organizations_list = []
        for org in organizations:
            organizations_list.append({
                'id': org[0],
                'name': org[1],
                'type': org[2],
                'created_by': org[3],
                'creation_date': org[4].isoformat(),
                'updated_on': org[5].isoformat(),
                'updated_by': org[6]
            })

        # Return the organizations as JSON response
        return jsonify({'organizations': organizations_list})

    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True)
