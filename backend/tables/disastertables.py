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

# Route to create the Disaster table
@app.route('/create_disaster_table', methods=['GET'])
def create_disaster_table():
    try:
        cursor = mysql.connection.cursor()
        # SQL query to create the Disaster table

        #change the primary key*****
        cursor.execute('''
           CREATE TABLE IF NOT EXISTS Disaster (
    DisasterID INT AUTO_INCREMENT PRIMARY KEY,
    DisasterType VARCHAR(255),
    SeverityLevel INT,
    StartDate DATE,
    EndDate DATE
);
        ''')
        mysql.connection.commit()
        cursor.close()
        return 'Disaster table created successfully!'
    except MySQLdb.Error as e:
        return f"Error creating Disaster table: {e}"

# Route to insert a disaster record
@app.route('/add_disaster', methods=['POST'])
def add_disaster():
    data = request.json
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('''
            INSERT INTO Disaster (DisasterType, SeverityLevel, StartDate, EndDate)
            VALUES (%s, %s, %s, %s);
        ''', (data['DisasterType'], data['SeverityLevel'], data['StartDate'], data['EndDate']))
        mysql.connection.commit()
        cursor.close()
        return 'Disaster record added successfully!'
    except MySQLdb.Error as e:
        return f"Error adding disaster record: {e}"

# Route to retrieve all disaster records
@app.route('/get_disasters', methods=['GET'])
def get_disasters():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Disaster;')
        disasters = cursor.fetchall()
        cursor.close()
        return jsonify(disasters)
    except MySQLdb.Error as e:
        return f"Error fetching disaster records: {e}"

# Route to update a disaster record by ID
@app.route('/update_disaster/<int:id>', methods=['PUT'])
def update_disaster(id):
    data = request.json
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('''
            UPDATE Disaster
            SET DisasterType = %s, SeverityLevel = %s, StartDate = %s, EndDate = %s
            WHERE DisasterID = %s;
        ''', (data['DisasterType'], data['SeverityLevel'], data['StartDate'], data['EndDate'], id))
        mysql.connection.commit()
        cursor.close()
        return 'Disaster record updated successfully!'
    except MySQLdb.Error as e:
        return f"Error updating disaster record: {e}"

# Route to delete a disaster record by ID
@app.route('/delete_disaster/<int:id>', methods=['DELETE'])
def delete_disaster(id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM Disaster WHERE DisasterID = %s;', (id,))
        mysql.connection.commit()
        cursor.close()
        return 'Disaster record deleted successfully!'
    except MySQLdb.Error as e:
        return f"Error deleting disaster record: {e}"

if __name__ == '_main_':
    app.run(debug=True)