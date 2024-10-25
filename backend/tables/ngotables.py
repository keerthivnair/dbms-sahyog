from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
import requests
import string
import random

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Replace with your MySQL username
app.config['MYSQL_PASSWORD'] = 'keerthi2005@'  # Replace with your MySQL password
app.config['MYSQL_DB'] = 'sahyogdb'  # Replace with your MySQL database name

# Initialize MySQL
mysql = MySQL(app)

# Route to create the NGO table
@app.route('/create_ngo_table', methods=['GET'])
def create_ngo_table():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS NGO (
                NGOID INT AUTO_INCREMENT PRIMARY KEY,
                LicenseNumber VARCHAR(255),
                NGOName VARCHAR(255) NOT NULL,
                ChairmanName VARCHAR(255),
                YearOfEstablishment YEAR,
                Email VARCHAR(255),
                PhoneNumber VARCHAR(15),
                AmountDonated DECIMAL(10, 2),
                Priority INT,
                Volunteers INT,
                Password VARCHAR(255)
            );
        ''')
        mysql.connection.commit()
        cursor.close()
        return 'NGO table created successfully!'
    except MySQLdb.Error as e:
        return f"Error creating NGO table: {e}"

# Function to generate a random password
def generate_password(length=8):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(length))

# Route to insert a new NGO
@app.route('/add_ngo', methods=['POST'])
def add_ngo():
    try:
        details = request.json
        # Check for duplicate email
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM NGO WHERE Email = %s", (details['Email'],))
        if cursor.fetchone() is not None:
            return jsonify({'error': 'Email already registered! Please log in.'}), 400
        
        # Generate random password
        password = generate_password()

        # Insert the new NGO into the database
        cursor.execute('''
            INSERT INTO NGO (LicenseNumber, NGOName, ChairmanName, YearOfEstablishment, Email, PhoneNumber, AmountDonated, Priority, Volunteers, Password)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (details['LicenseNumber'], details['NGOName'], details['ChairmanName'],
              details['YearOfEstablishment'], details['Email'], details['PhoneNumber'],
              details['AmountDonated'], details['Priority'], details['Volunteers'], password))
        
        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': 'NGO added successfully!', 'Password': password}), 201
    except MySQLdb.Error as e:
        return jsonify({'error': f"Error adding NGO: {e}"}), 400

# Route to update an existing NGO by ID
@app.route('/update_ngo/<int:id>', methods=['PUT'])
def update_ngo(id):
    try:
        cursor = mysql.connection.cursor()
        details = request.json
        query = '''
            UPDATE NGO
            SET LicenseNumber = %s, NGOName = %s, ChairmanName = %s, YearOfEstablishment = %s,
                Email = %s, PhoneNumber = %s, AmountDonated = %s, Priority = %s, Volunteers = %s
            WHERE NGOID = %s
        '''
        cursor.execute(query, (details['LicenseNumber'], details['NGOName'], details['ChairmanName'],
                               details['YearOfEstablishment'], details['Email'], details['PhoneNumber'],
                               details['AmountDonated'], details['Priority'], details['Volunteers'], id))
        mysql.connection.commit()
        cursor.close()
        return f"NGO with ID {id} updated successfully!"
    except MySQLdb.Error as e:
        return f"Error updating NGO: {e}"

# Route to delete an NGO by ID
@app.route('/delete_ngo/<int:id>', methods=['DELETE'])
def delete_ngo(id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM NGO WHERE NGOID = %s', (id,))
        mysql.connection.commit()
        cursor.close()
        return f"NGO with ID {id} deleted successfully!"
    except MySQLdb.Error as e:
        return f"Error deleting NGO: {e}"

# Route to fetch all NGOs
@app.route('/get_ngos', methods=['GET'])
def get_ngos():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM NGO')
        ngos = cursor.fetchall()
        cursor.close()
        return jsonify(ngos)
    except MySQLdb.Error as e:
        return f"Error fetching NGOs: {e}"

if __name__ == '__main__':
    app.run(debug=True)
