from flask import Flask, request, jsonify
import psycopg2
import json

app = Flask(__name__)


def connect_to_db():
    conn = psycopg2.connect(
        dbname="flaskdeployment",
        user="tanaya",
        password="qi3gRlLlJduD0REQurSeu72uJfpGkka4",
        host="dpg-colrd88l5elc73bo6rag-a.singapore-postgres.render.com",
        port="5432"
    )
    return conn


# Route to add a new organization
@app.route('/add_organization', methods=['POST'])
def add_organization():
    try:
        # Read data from data.json file
        with open('data.json', 'r') as f:
            data = json.load(f)

        # Extract organization data
        org_name = data.get('Name')
        org_type = data.get('OrganizationType')
        created_by = data.get('CreatedBy')
        creation_date = data.get('CreationDate')
        updated_on = data.get('UpdatedOn')
        updated_by = data.get('UpdatedBy')

        # Connect to the database
        conn = connect_to_db()

        # Create a cursor
        cur = conn.cursor()

        # Execute the insertion query
        cur.execute("""
            INSERT INTO Organization (Organization_Name, Organization_Type, Created_by, Creation_Date, Updated_On, Updated_by)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (org_name, org_type, created_by, creation_date, updated_on, updated_by))

        # Commit the transaction
        conn.commit()

        # Close cursor and connection
        cur.close()
        conn.close()

        return jsonify({'message': 'Organization added successfully'})

    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True)
