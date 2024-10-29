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

# Route to create the Donor table
@app.route('/create_donor_table', methods=['GET'])
def create_donor_table():
    try:
        cursor = mysql.connection.cursor()
        # SQL query to create the Donor table
        cursor.execute('''
           CREATE TABLE IF NOT EXISTS Donor (
    DonorID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    ContactNumber VARCHAR(15),
    Email VARCHAR(255),
    Address VARCHAR(255),
    ResourceID INT,
    FOREIGN KEY (ResourceID) REFERENCES Resources(ResourceID)
);
        ''')
        mysql.connection.commit()
        cursor.close()
        return 'Donor table created successfully!'
    except MySQLdb.Error as e:
        return f"Error creating Donor table: {e}"

# Route to add a donor
@app.route('/add_donor', methods=['POST'])
def add_donor():
    data = request.json
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('''
            INSERT INTO Donor (Name, ContactNumber, Email, Address)
            VALUES (%s, %s, %s, %s);
        ''', (data['Name'], data['ContactNumber'], data['Email'], data['Address']))
        mysql.connection.commit()
        cursor.close()
        return 'Donor added successfully!'
    except MySQLdb.Error as e:
        return f"Error adding donor: {e}"

# Route to update a donor
@app.route('/update_donor/<int:donor_id>', methods=['PUT'])
def update_donor(donor_id):
    data = request.json
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('''
            UPDATE Donor
            SET Name = %s, ContactNumber = %s, Email = %s, Address = %s
            WHERE DonorID = %s;
        ''', (data['Name'], data['ContactNumber'], data['Email'], data['Address'], donor_id))
        mysql.connection.commit()
        cursor.close()
        return 'Donor updated successfully!'
    except MySQLdb.Error as e:
        return f"Error updating donor: {e}"

# Route to delete a donor
@app.route('/delete_donor/<int:donor_id>', methods=['DELETE'])
def delete_donor(donor_id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('''
            DELETE FROM Donor WHERE DonorID = %s;
        ''', (donor_id,))
        mysql.connection.commit()
        cursor.close()
        return 'Donor deleted successfully!'
    except MySQLdb.Error as e:
        return f"Error deleting donor: {e}"

# Route to get all donors
@app.route('/get_donors', methods=['GET'])
def get_donors():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Donor')
        donors = cursor.fetchall()
        cursor.close()
        return jsonify(donors)
    except MySQLdb.Error as e:
        return f"Error fetching donors: {e}"

if __name__ == '_main_':
    app.run(debug=True)