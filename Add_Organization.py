from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

# Database configuration
DB_NAME = "flaskdeployment"
DB_USER = "tanaya"
DB_PASSWORD = "qi3gRlLlJduD0REQurSeu72uJfpGkka4"
DB_HOST = "dpg-colrd88l5elc73bo6rag-a.singapore-postgres.render.com"
DB_PORT = "5432"

# Global variable to store the organization count
organization_count = 0


# Function to establish a connection to the database
def connect_to_db():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )


class Organization:
    def __init__(self, data):
        self.id = data.get('id')
        self.name = data.get('Name')
        self.type = data.get('OrganizationType')
        self.created_by = data.get('CreatedBy')
        self.creation_date = data.get('CreationDate')
        self.updated_on = data.get('UpdatedOn')
        self.updated_by = data.get('UpdatedBy')

    def get_not_filled_fields(self):
        not_filled_fields = []
        if not self.id:
            not_filled_fields.append('id')
        if not self.name:
            not_filled_fields.append('Name')
        if not self.type:
            not_filled_fields.append('OrganizationType')
        if not self.created_by:
            not_filled_fields.append('CreatedBy')
        if not self.creation_date:
            not_filled_fields.append('CreationDate')
        if not self.updated_on:
            not_filled_fields.append('UpdatedOn')
        if not self.updated_by:
            not_filled_fields.append('UpdatedBy')
        return not_filled_fields

    def is_valid(self):
        return all(
            [self.id, self.name, self.type, self.created_by, self.creation_date, self.updated_on, self.updated_by])


@app.route('/organization', methods=['POST'])
def add_organization():
    global organization_count

    try:
        # Connect to the database
        conn = connect_to_db()
        cur = conn.cursor()

        # Get data from the request body
        data = request.json
        organization = Organization(data)

        if not organization.is_valid():
            not_filled_fields = organization.get_not_filled_fields()
            error_message = "Organization with ID {} is missing required fields: {}".format(organization.id, ', '.join(
                not_filled_fields))
            return jsonify({'error': error_message}), 400

        # Insert data into the organization table
        cur.execute(
            'INSERT INTO Organization (Organization_Id, Organization_Name, Organization_Type, Created_by, Creation_Date, Updated_On, Updated_by) VALUES (%s, %s, %s, %s, %s, %s, %s)',
            (organization.id, organization.name, organization.type, organization.created_by, organization.creation_date,
             organization.updated_on, organization.updated_by)
        )
        conn.commit()

        # Increment organization count
        organization_count += 1

        # Close database connection
        cur.close()
        conn.close()

        return jsonify({'message': f'{organization_count} organizations added successfully'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
