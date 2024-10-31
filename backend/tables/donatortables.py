from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'keerthi2005@'
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
    CREATE TABLE IF NOT EXISTS IndividualDonor (
    DonorID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    ContactNumber VARCHAR(15),
    Email VARCHAR(255),
    Address VARCHAR(255),
    Password VARCHAR(255),
    ResourceID,
    FundID,
    FOREIGN KEY(ResourceID) REFERENCES resources(ResourceID)
    FOREIGN KEY(FundID) REFERENCES funds(FundID)
);

    CREATE TABLE IF NOT EXISTS CompanyDonor (
    DonorID INT AUTO_INCREMENT PRIMARY KEY,
    CompanyName VARCHAR(255) NOT NULL,
    ContactPerson VARCHAR(255), -- Specific for company donors
    ContactNumber VARCHAR(15),
    Email VARCHAR(255),
    Address VARCHAR(255),
    Password VARCHAR(255),
);

            )
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

    # Check if donor is already registered
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM Donor WHERE Name = %s AND Password = %s', (data['Name'], data['Password']))
    existing_donor = cursor.fetchone()
    cursor.close()
    
    if existing_donor:
        return jsonify({'error': 'Already registered! Please login.'}), 400
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('''
            INSERT INTO Donor (Name, ContactNumber, Email, Address, ResourceID, Password)
            VALUES (%s, %s, %s, %s, %s, %s);
        ''', (data['Name'], data['ContactNumber'], data['Email'], data['Address'], data['ResourceID'], data['Password']))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Donor added successfully!'}), 201
    except MySQLdb.Error as e:
        return jsonify({'error': f"Error adding donor: {e}"}), 400
       

# Route to update a donor
@app.route('/update_donor/<name>/<password>', methods=['PUT'])
def update_donor(name,password):
    data = request.json
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('''
            UPDATE Donor
            SET Name = %s, ContactNumber = %s, Email = %s, Address = %s
            WHERE Name = %s AND Password=%s;
        ''', (data['Name'], data['ContactNumber'], data['Email'], data['Address'], name,password,))
        mysql.connection.commit()
        cursor.close()
        return 'Donor updated successfully!'
    except MySQLdb.Error as e:
        return f"Error updating donor: {e}"

# Route to delete a donor
@app.route('/delete_donor/<name>/<password>', methods=['DELETE'])
def delete_donor(name,password):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('''
            DELETE FROM Donor WHERE Name = %s AND Password=%s;
        ''', (name,password,))
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

if __name__ == '__main__':
    app.run(debug=True)