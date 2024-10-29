from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Ashmi@2004'
app.config['MYSQL_DB'] = 'sahyogdb'

# Initialize MySQL
mysql = MySQL(app)

# Route to create the 'Camp' table
@app.route('/create_camp_table', methods=['GET'])
def create_camp_table():
    cursor = mysql.connection.cursor()
    cursor.execute('''
       CREATE TABLE IF NOT EXISTS Camp (
    CampID INT AUTO_INCREMENT PRIMARY KEY,
    CampName VARCHAR(255) NOT NULL,
    Capacity INT NOT NULL,
    VolunteerReq INT NOT NULL,
    VolunteerAvail INT NOT NULL,
    FundReq VARCHAR(50),
    FundAvail VARCHAR(50),
    VolunteersRoutedBySahyog INT,
    VolunteerID INT,
    LocationID INT,
    FOREIGN KEY (VolunteerID) REFERENCES Volunteers(VolunteerID),
    FOREIGN KEY (LocationID) REFERENCES Location(LocationID)
);

    ''')
    mysql.connection.commit()
    cursor.close()
    return 'Camp table created successfully!'



# Insert a new camp into the database
@app.route('/add_camp', methods=['POST'])
def add_camp():
    data = request.json
    cursor = mysql.connection.cursor()
    query = '''
        INSERT INTO Camp (CampName, Capacity, VolunteerReq, VolunteerAvail, FundReq, FundAvail, Volunteersroutedbysahyog)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    '''
    values = (data['CampName'], data['Capacity'], data['VolunteerReq'], data['VolunteerAvail'], data['FundReq'], data['FundAvail'], data['Volunteersroutedbysahyog'])
    cursor.execute(query, values)
    mysql.connection.commit()
    cursor.close()
    return jsonify(message='Camp added successfully!')

# Retrieve all camps from the database
@app.route('/get_camps', methods=['GET'])
def get_camps():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM Camp")
    camps = cursor.fetchall()
    cursor.close()
    return jsonify(camps)

# Retrieve a specific camp by ID
@app.route('/get_camp/<int:id>', methods=['GET'])
def get_camp(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM Camp WHERE CampID = %s", [id])
    camp = cursor.fetchone()
    cursor.close()
    if camp:
        return jsonify(camp)
    return jsonify(message="Camp not found"), 404

# Update a camp by ID
@app.route('/update_camp/<int:id>', methods=['PUT'])
def update_camp(id):
    data = request.json
    cursor = mysql.connection.cursor()
    query = '''
        UPDATE Camp
        SET CampName = %s, Capacity = %s, VolunteerReq = %s, VolunteerAvail = %s, FundReq = %s, FundAvail = %s, Volunteersroutedbysahyog = %s
        WHERE CampID = %s
    '''
    values = (data['CampName'], data['Capacity'], data['VolunteerReq'], data['VolunteerAvail'], data['FundReq'], data['FundAvail'], data['Volunteersroutedbysahyog'], id)
    cursor.execute(query, values)
    mysql.connection.commit()
    cursor.close()
    return jsonify(message='Camp updated successfully!')

# Delete a camp by ID
@app.route('/delete_camp/<int:id>', methods=['DELETE'])
def delete_camp(id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM Camp WHERE CampID = %s", [id])
    mysql.connection.commit()
    cursor.close()
    return jsonify(message='Camp deleted successfully!')

if __name__ == '_main_':
    app.run(debug=True)