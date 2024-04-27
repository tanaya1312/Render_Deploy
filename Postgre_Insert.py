from flask import Flask, jsonify
import json
from datetime import datetime
import psycopg2

app = Flask(__name__)


class Organization:
    def _init_(self, data):
        self.id = data.get('id')
        self.name = data.get('Name')
        self.type = data.get('OrganizationType')
        self.created_by = data.get('CreatedBy')
        self.creation_date = self.format_date(data.get('CreationDate'))
        self.updated_on = self.format_date(data.get('UpdatedOn'))
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

    def format_date(self, date_str):
        return datetime.strptime(date_str, "%m/%d/%Y").strftime("%Y-%m-%d") if date_str else None


def connect_to_database():
    try:
        con = psycopg2.connect(
            host='dpg-colrd88l5elc73bo6rag-a.singapore-postgres.render.com',
            user='tanaya',
            password='qi3gRlLlJduD0REQurSeu72uJfpGkka4',
            database='flaskdeployment',
            port='5432'
        )
        return con
    except Exception as e:
        print("Cannot connect to PostgreSQL database:", e)
        return None


def close_database_connection(con):
    if con is not None:
        con.close()
        print("Connection to PostgreSQL database closed.")


@app.route('/')
def index():
    return "Welcome to the Flask App."


@app.route('/load_data')
def load_data():
    con = connect_to_database()
    if not con:
        return jsonify({'error': {'category': 'IO Error', 'type': 'database_connection_error',
                                  'message': 'Failed to load data. Unable to connect to the database.'}})

    try:
        cur = con.cursor()
        with open('data.json', 'r') as f:
            data = json.load(f)

        for item in data:
            organization = Organization(item)
            if not organization.is_valid():
                not_filled_fields = organization.get_not_filled_fields()
                error_message = "Organization with ID {} is missing required fields: {}".format(organization.id,
                                                                                                ', '.join(
                                                                                                    not_filled_fields))
                return jsonify(
                    {'error': {'category': 'Value Error', 'type': 'data_validation_error', 'message': error_message}})

            val = (
            organization.id, organization.name, organization.type, organization.created_by, organization.creation_date,
            organization.updated_on, organization.updated_by)
            sql = "INSERT INTO Organization(Organization_Id, Organization_Name, Organization_Type, Created_by, Creation_Date, Updated_On, Updated_by) VALUES(%s,%s,%s,%s,%s,%s,%s)"
            cur.execute(sql, val)
            con.commit()

        cur.close()
        close_database_connection(con)
        return "Data loaded successfully into the database."
    except Exception as e:
        error_message = "An error occurred: {}".format(str(e))
        return jsonify({'error': {'category': 'Runtime Error', 'type': 'internal_error', 'message': error_message}})


if __name__== '_main_':
    app.run(debug=True)