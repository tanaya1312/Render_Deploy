from flask import Flask, jsonify
import psycopg2

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


@app.route('/organization_names', methods=['GET'])
def get_organization_names():
    try:
        conn = connect_to_db()

        cur = conn.cursor()

        cur.execute("SELECT Organization_Name FROM Organization")

        organization_names = cur.fetchall()

        cur.close()
        conn.close()

        organization_names_list = [name[0] for name in organization_names]

        return jsonify({'organization_names': organization_names_list})

    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True)
