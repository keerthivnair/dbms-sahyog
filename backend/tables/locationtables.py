from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Ashmi@2004'
app.config['MYSQL_DB'] = 'sahyogdb'

# Initialize MySQL
mysql = MySQL(app)

# Route to create the Location table
@app.route('/create_location_table', methods=['GET'])
def create_location_table():
    try:
        cursor = mysql.connection.cursor()
        # SQL query to create the Location table
        cursor.execute('''
           CREATE TABLE IF NOT EXISTS Location (
    LocationID INT AUTO_INCREMENT PRIMARY KEY,
    LocationName VARCHAR(255)
);
        ''')
        mysql.connection.commit()
        cursor.close()
        return 'Location table created successfully!'
    except MySQLdb.Error as e:
        return f"Error creating Location table: {e}"

# Route to add a new location
@app.route('/add_location', methods=['POST'])
def add_location():
    data = request.json
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('''
            INSERT INTO Location (LocationName)
            VALUES (%s);
        ''', (data['LocationName'],))
        mysql.connection.commit()
        cursor.close()
        return 'Location added successfully!'
    except MySQLdb.Error as e:
        return f"Error adding location: {e}"

# Route to update a location
@app.route('/update_location/<int:location_id>', methods=['PUT'])
def update_location(location_id):
    data = request.json
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('''
            UPDATE Location
            SET LocationName = %s
            WHERE LocationID = %s;
        ''', (data['LocationName'], location_id))
        mysql.connection.commit()
        cursor.close()
        return 'Location updated successfully!'
    except MySQLdb.Error as e:
        return f"Error updating location: {e}"

# Route to delete a location
@app.route('/delete_location/<int:location_id>', methods=['DELETE'])
def delete_location(location_id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('''
            DELETE FROM Location WHERE LocationID = %s;
        ''', (location_id,))
        mysql.connection.commit()
        cursor.close()
        return 'Location deleted successfully!'
    except MySQLdb.Error as e:
        return f"Error deleting location: {e}"

# Route to get all locations
@app.route('/get_locations', methods=['GET'])
def get_locations():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Location')
        locations = cursor.fetchall()
        cursor.close()
        return jsonify(locations)
    except MySQLdb.Error as e:
        return f"Error fetching locations: {e}"

if __name__ == '_main_':
    app.run(debug=True)