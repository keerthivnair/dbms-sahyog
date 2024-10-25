from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
import requests

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Replace with your MySQL username
app.config['MYSQL_PASSWORD'] = 'Ashmi@2004'  # Replace with your MySQL password
app.config['MYSQL_DB'] = 'sahyogdb'  # Replace with your MySQL database name


#create a function to distibute the amont between among the ngo
#ngo_amount


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
    NGO_Amount DECIMAL(10, 2),
    Priority INT,
    VolunteerID INT,
    ReportID INT,
    FOREIGN KEY (ReportID) REFERENCES Report(ReportID),
    FOREIGN KEY (VolunteerID) REFERENCES Volunteers(VolunteerID)
);
        ''')
        mysql.connection.commit()
        cursor.close()
        return 'NGO table created successfully!'
    except MySQLdb.Error as e:
        return f"Error creating NGO table: {e}"

# Function to verify NGO license number
def verify_license(license_number):
    # Replace this URL with the actual government API endpoint for verification
    api_url = f"https://api.example.com/verify_ngo?license_number={license_number}"
    response = requests.get(api_url)
    
    if response.status_code == 200:
        return response.json().get('verified', False)  # Assuming the API returns a JSON with 'verified' key
    else:
        return False

# Route to insert a new NGO
@app.route('/add_ngo', methods=['POST'])
def add_ngo():
    try:
        details = request.json
        # Verify the license number before inserting
        if not verify_license(details['LicenseNumber']):
            return "License number is not verified!", 400
        
        cursor = mysql.connection.cursor()
        query = '''
            INSERT INTO NGO (LicenseNumber, NGOName, ChairmanName, YearOfEstablishment, Email, PhoneNumber, AmountDonated, Priority, Volunteers)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        cursor.execute(query, (details['LicenseNumber'], details['NGOName'], details['ChairmanName'],
                               details['YearOfEstablishment'], details['Email'], details['PhoneNumber'],
                               details['AmountDonated'], details['Priority'], details['Volunteers']))
        mysql.connection.commit()
        cursor.close()
        return 'NGO added successfully!', 201
    except MySQLdb.Error as e:
        return f"Error adding NGO: {e}"

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

if __name__ == '_main_':
    app.run(debug=True)