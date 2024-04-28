from flask import Flask, jsonify
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


def check_organization_exists(org_id):
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM Organization WHERE Organization_Id = %s", (org_id,))
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    return count > 0


@app.route('/add_organization')
def add_organization():
    try:
        with open('data.json', 'r') as f:
            data = json.load(f)

        added_count = 0

        for org_data in data:
            org_id = org_data.get('id')
            org_name = org_data.get('Name')
            org_type = org_data.get('OrganizationType')
            created_by = org_data.get('CreatedBy')
            creation_date = org_data.get('CreationDate')
            updated_on = org_data.get('UpdatedOn')
            updated_by = org_data.get('UpdatedBy')

            if not check_organization_exists(org_id):
                conn = connect_to_db()
                cur = conn.cursor()

                cur.execute("""
                    INSERT INTO Organization (Organization_Id, Organization_Name, Organization_Type, Created_by, Creation_Date, Updated_On, Updated_by)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (org_id, org_name, org_type, created_by, creation_date, updated_on, updated_by))

                conn.commit()

                cur.close()
                conn.close()

                added_count += 1

        return jsonify({'message': f'{added_count} organizations added successfully'})

    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True)