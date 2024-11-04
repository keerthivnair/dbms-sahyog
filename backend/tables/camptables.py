from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
from flask_cors import CORS
from locationtables import get_location_id  

app = Flask(__name__)
CORS(app)

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'keerthi2005@'
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
            Password varchar(100),
            LocationID INT,
            FOREIGN KEY(LocationID) REFERENCES Location(LocationID)
        );   
''')
    mysql.connection.commit()
    cursor.close()
    return 'Camp table created successfully!'

# Insert a new camp into the database with LocationID and duplicate check
@app.route('/add_camp', methods=['POST'])
def add_camp():
    data = request.json
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # Retrieve LocationID based on LocationName (assumed to be part of 'data')
    location_id = get_location_id(data['LocationID'])  # Ensure get_locations fetches the LocationID

    # Check for duplicate CampName and Password
    cursor.execute('SELECT * FROM Camp WHERE CampName = %s AND Password = %s', 
                   (data['CampName'], data['Password']))
    existing_camp = cursor.fetchone()
    if existing_camp:
        cursor.close()
        return jsonify(message='Camp already registered, please log in.')

    # Insert new camp if not a duplicate
    query = '''
        INSERT INTO Camp (CampName, Capacity, VolunteerReq, VolunteerAvail, FundReq, FundAvail, Password, LocationID)
        VALUES (%s, %s, %s, %s, %s, %s, %s,%s)
    '''
    values = (data['CampName'], data['Capacity'], data['VolunteerReq'], data['VolunteerAvail'],
              data['FundReq'], data['FundAvail'], data['Password'], location_id)
    cursor.execute(query, values)
    mysql.connection.commit()
    cursor.close()
    return jsonify(message='Camp added successfully!')

# Retrieve all camps
@app.route('/get_camps',methods=['GET'])
def get_camps():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Camp')
    camp=cursor.fetchall()
    cursor.close()
    if camp: 
        return jsonify(camp)
    return jsonify(message="Camp not found"), 404

# Retrieve a specific camp by CampName and Password
@app.route('/get_camp/<campname>/<password>', methods=['POST'])
def get_camp(campname, password):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Camp WHERE CampName = %s AND Password = %s', (campname, password))
    camp = cursor.fetchone()
    cursor.close()
    if camp:
        return jsonify(camp)
    return jsonify(message="Camp not found"), 404

# Update a camp by CampName and Password
@app.route('/update_camp/<campname>/<password>', methods=['POST'])
def update_camp(campname, password):
    data = request.json
    cursor = mysql.connection.cursor()

    # Verify CampName and Password
    cursor.execute('SELECT * FROM Camp WHERE CampName = %s AND Password = %s', (campname, password))
    camp = cursor.fetchone()
    if not camp:
        cursor.close()
        return jsonify(message="Camp not found or incorrect credentials."), 404

    # Update camp details
    query = '''
        UPDATE Camp
        SET Capacity = %s, VolunteerReq = %s, VolunteerAvail = %s, FundReq = %s, FundAvail = %s, Volunteersroutedbysahyog = %s
        WHERE CampName = %s AND Password = %s
    '''
    values = (data['Capacity'], data['VolunteerReq'], data['VolunteerAvail'], 
              data['FundReq'], data['FundAvail'], data['Volunteersroutedbysahyog'], 
              campname, password)
    cursor.execute(query, values)
    mysql.connection.commit()
    cursor.close()
    return jsonify(message='Camp updated successfully!')

# Delete a camp by CampName and Password
@app.route('/delete_camp/<campname>/<password>', methods=['POST'])
def delete_camp(campname, password):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM Camp WHERE CampName = %s AND Password = %s', (campname, password))
    camp = cursor.fetchone()

    if not camp:
        cursor.close()
        return jsonify(message='Camp not found or incorrect credentials.'), 404

    cursor.execute('DELETE FROM Camp WHERE CampName = %s AND Password = %s', (campname, password))
    mysql.connection.commit()
    cursor.close()
    return jsonify(message='Camp deleted successfully!')

@app.route('/describe_camp_table', methods=['GET'])
def describe_camp_table():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        # Query to get the structure of the Camp table
        cursor.execute('''
            SELECT COLUMN_NAME, COLUMN_TYPE, IS_NULLABLE, COLUMN_KEY, EXTRA
            FROM information_schema.COLUMNS
            WHERE TABLE_SCHEMA = %s AND TABLE_NAME = 'Camp';
        ''', (app.config['MYSQL_DB'],))
        
        # Fetch all the results
        camp_structure = cursor.fetchall()
        cursor.close()
        
        # Return the structure in JSON format
        return jsonify(camp_structure)
    except MySQLdb.Error as e:
        return f"Error describing Camp table: {e}"




if __name__ == '__main__':
    app.run(debug=True)
