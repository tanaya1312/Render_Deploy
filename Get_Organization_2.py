from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)


class OrganizationService:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname="flaskdeployment",
            user="tanaya",
            password="qi3gRlLlJduD0REQurSeu72uJfpGkka4",
            host="dpg-colrd88l5elc73bo6rag-a.singapore-postgres.render.com",
            port="5432"
        )

    def get_organizations(self):
        try:
            cur = self.conn.cursor()

            cur.execute("SELECT * FROM Organization")

            organizations = cur.fetchall()

            cur.close()

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

            return organizations_list

        except Exception as e:
            return [{'error': str(e)}]

    def close_connection(self):
        self.conn.close()


organization_service = OrganizationService()


@app.route('/organizations', methods=['GET'])
def get_organizations():
    organizations = organization_service.get_organizations()
    return jsonify({'organizations': organizations})


if __name__ == '__main__':
    app.run(debug=True)
