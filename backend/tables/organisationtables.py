from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors  

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Replace with your MySQL username
app.config['MYSQL_PASSWORD'] = 'Ashmi@2004'  # Replace with your MySQL password
app.config['MYSQL_DB'] = 'sahyogdb'  # Replace with your MySQL database name

# Initialize MySQL
mysql = MySQL(app)

# Route to create the Organisation table
@app.route('/create_organisation_table', methods=['GET'])
def create_organisation_table():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('''
    CREATE TABLE IF NOT EXISTS Organisation (
    OrganisationName VARCHAR(255),
    LicenseNumber VARCHAR(255) PRIMARY KEY,
    DateOfEstablishment DATE,
    Email VARCHAR(255),
    PhoneNumber VARCHAR(15),
    NumberOfEmployees INT,
    noofNGOsregistered INT,
    FOREIGN KEY (NGOID) REFERENCES NGO(NGOID),
    FOREIGN KEY (ReportID) REFERENCES Report(ReportID),
    FOREIGN KEY (CampID) REFERENCES Camp(CampID),
    FOREIGN KEY (VolunteerID) REFERENCES Volunteers(VolunteerID),
    FOREIGN KEY (DonationID) REFERENCES Donations(DonationID),
    FOREIGN KEY (DisasterID) REFERENCES Disaster(DisasterID)
);
        ''')
        mysql.connection.commit()
        cursor.close()
        return 'Organisation table created successfully!'
    except MySQLdb.Error as e:
        return f"Error creating Organisation table: {e}"

# Route to add a new organisation
@app.route('/add_organisation', methods=['POST'])
def add_organisation():
    data = request.json
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('''
            INSERT INTO Organisation (OrganisationName, LicenseNumber, DateOfEstablishment, Email, PhoneNumber, NumberOfEmployees, noofNGOsregistered)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (data['OrganisationName'], data['LicenseNumber'], data['DateOfEstablishment'], data['Email'], data['PhoneNumber'], data['NumberOfEmployees'], data['noofNGOsregistered']))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Organisation added successfully!'}), 201
    except MySQLdb.Error as e:
        return jsonify({'error': f"Error adding organisation: {e}"}), 400

# Route to get all organisations
@app.route('/organisations', methods=['GET'])
def get_organisations():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM Organisation;')
    results = cursor.fetchall()
    organisations = []
    for row in results:
        organisations.append({
            'OrganisationName': row[0],
            'LicenseNumber': row[1],
            'DateOfEstablishment': row[2],
            'Email': row[3],
            'PhoneNumber': row[4],
            'NumberOfEmployees': row[5],
            'noofNGOsregistered': row[6]
        })
    cursor.close()
    return jsonify(organisations)

# Route to update an organisation
@app.route('/update_organisation/<license_number>', methods=['PUT'])
def update_organisation(license_number):
    data = request.json
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('''
            UPDATE Organisation
            SET OrganisationName = %s,
                DateOfEstablishment = %s,
                Email = %s,
                PhoneNumber = %s,
                NumberOfEmployees = %s,
                noofNGOsregistered = %s
            WHERE LicenseNumber = %s
        ''', (data['OrganisationName'], data['DateOfEstablishment'], data['Email'], data['PhoneNumber'], data['NumberOfEmployees'], data['noofNGOsregistered'], license_number))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Organisation updated successfully!'})
    except MySQLdb.Error as e:
        return jsonify({'error': f"Error updating organisation: {e}"}), 400

# Route to delete an organisation
@app.route('/delete_organisation/<license_number>', methods=['DELETE'])
def delete_organisation(license_number):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM Organisation WHERE LicenseNumber = %s;', (license_number,))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Organisation deleted successfully!'})
    except MySQLdb.Error as e:
        return jsonify({'error': f"Error deleting organisation: {e}"}), 400

if __name__ == '_main_':
    app.run(debug=True)
