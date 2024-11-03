from flask import Flask, request, jsonify ,session
from flask_mysqldb import MySQL
import MySQLdb.cursors
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'keerthi2005@'
app.config['MYSQL_DB'] = 'sahyogdb'

# Initialize MySQL
mysql = MySQL(app)

# Route to create the Donor tables
@app.route('/create_donor_tables', methods=['GET'])
def create_donor_tables():
    try:
        cursor = mysql.connection.cursor()
        # SQL query to create the IndividualDonor and CompanyDonor tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS IndividualDonor (
                DonorID INT AUTO_INCREMENT PRIMARY KEY,
                Name VARCHAR(255) NOT NULL,
                ContactNumber VARCHAR(15),
                Email VARCHAR(255),
                Address VARCHAR(255),
                Password VARCHAR(255)
               );    
                       
            CREATE TABLE IF NOT EXISTS CompanyDonor (
                DonorID INT AUTO_INCREMENT PRIMARY KEY,
                CompanyName VARCHAR(255) NOT NULL,
                ContactPerson VARCHAR(255),
                ContactNumber VARCHAR(15),
                Email VARCHAR(255),
                Address VARCHAR(255),
                Password VARCHAR(255),
                );
        ''')
        mysql.connection.commit()
        cursor.close()
        return 'Donor tables created successfully!'
    except MySQLdb.Error as e:
        return f"Error creating Donor tables: {e}"
    
# Route to login as an individual donor using name and password
@app.route('/login_individual', methods=['POST'])
def login_individual():
    data = request.json
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM IndividualDonor WHERE Name = %s AND Password = %s', 
                   (data['Name'], data['Password']))  # Change DonorID to Name
    individual = cursor.fetchone()
    cursor.close()
    if individual:
        session['donor_id'] = individual[0]
        session['donor_type'] = 'individual'
        return jsonify({'message': 'Login successful!'}), 200
    else:
        return jsonify({'error': 'Invalid name or password'}), 400

# Route to login as a company donor
@app.route('/login_company', methods=['POST'])
def login_company():
    data = request.json
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM CompanyDonor WHERE DonorID = %s AND Password = %s', 
                   (data['Name'], data['Password']))
    company = cursor.fetchone()
    cursor.close()
    if company:
        session['donor_id'] = company[0]
        session['donor_type'] = 'company'
        return jsonify({'message': 'Login successful!'}), 200
    else:
        return jsonify({'error': 'Invalid DonorID or password'}), 400

# Route to add funds as an individual donor
@app.route('/add_funds_individual', methods=['POST'])
def add_funds_individual():
    if 'donor_id' in session and session.get('donor_type') == 'individual':
        data = request.json
        cursor = mysql.connection.cursor()
        # Add to funds table
        cursor.execute('INSERT INTO funds (FundAmount, DonorID) VALUES (%s, %s)', 
                       (data['FundAmount'], session['donor_id']))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Funds added successfully for individual donor!'}), 201
    else:
        return jsonify({'error': 'Unauthorized access'}), 403

# Route to add funds as a company donor
@app.route('/add_funds_company', methods=['POST'])
def add_funds_company():
    if 'donor_id' in session and session.get('donor_type') == 'company':
        data = request.json
        cursor = mysql.connection.cursor()
        # Add to funds table
        cursor.execute('INSERT INTO funds (FundAmount, DonorID) VALUES (%s, %s)', 
                       (data['FundAmount'], session['donor_id']))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Funds added successfully for company donor!'}), 201
    else:
        return jsonify({'error': 'Unauthorized access'}), 403


# Route to add an individual donor
@app.route('/add_individual_donor', methods=['POST'])
def add_individual_donor():
    data = request.json

    # Check if donor is already registered
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM IndividualDonor WHERE Name = %s AND Password = %s', (data['Name'], data['Password']))
    existing_donor = cursor.fetchone()
    cursor.close()
    
    if existing_donor:
        return jsonify({'error': 'Already registered! Please login.'}), 400

    try:
        cursor = mysql.connection.cursor()
        cursor.execute('''
            INSERT INTO IndividualDonor (Name, ContactNumber, Email, Address, Password)
            VALUES (%s, %s, %s, %s, %s);
        ''', (data['Name'], data['ContactNumber'], data['Email'], data['Address'], data['Password']))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Individual donor added successfully!'}), 201
    except MySQLdb.Error as e:
        return jsonify({'error': f"Error adding individual donor: {e}"}), 400

# Route to add a company donor
@app.route('/add_company_donor', methods=['POST'])
def add_company_donor():
    data = request.json

    # Check if donor is already registered
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM CompanyDonor WHERE CompanyName = %s AND Password = %s', (data['CompanyName'], data['Password']))
    existing_donor = cursor.fetchone()
    cursor.close()
    
    if existing_donor:
        return jsonify({'error': 'Already registered! Please login.'}), 400

    try:
        cursor = mysql.connection.cursor()
        cursor.execute('''
            INSERT INTO CompanyDonor (CompanyName, ContactPerson, ContactNumber, Email, Address, Password)
            VALUES (%s, %s, %s, %s, %s, %s);
        ''', (data['CompanyName'], data['ContactPerson'], data['ContactNumber'], data['Email'], data['Address'], data['Password']))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Company donor added successfully!'}), 201
    except MySQLdb.Error as e:
        return jsonify({'error': f"Error adding company donor: {e}"}), 400

# Route to update an individual donor
@app.route('/update_individual_donor/<name>/<password>', methods=['PUT'])
def update_individual_donor(name, password):
    data = request.json
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('''
            UPDATE IndividualDonor
            SET Name = %s, ContactNumber = %s, Email = %s, Address = %s
            WHERE Name = %s AND Password = %s;
        ''', (data['Name'], data['ContactNumber'], data['Email'], data['Address'], name, password))
        mysql.connection.commit()
        cursor.close()
        return 'Individual donor updated successfully!'
    except MySQLdb.Error as e:
        return f"Error updating individual donor: {e}"

# Route to update a company donor
@app.route('/update_company_donor/<company_name>/<password>', methods=['PUT'])
def update_company_donor(company_name, password):
    data = request.json
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('''
            UPDATE CompanyDonor
            SET CompanyName = %s, ContactPerson = %s, ContactNumber = %s, Email = %s, Address = %s
            WHERE CompanyName = %s AND Password = %s;
        ''', (data['CompanyName'], data['ContactPerson'], data['ContactNumber'], data['Email'], data['Address'], company_name, password))
        mysql.connection.commit()
        cursor.close()
        return 'Company donor updated successfully!'
    except MySQLdb.Error as e:
        return f"Error updating company donor: {e}"

# Route to delete an individual donor
@app.route('/delete_individual_donor/<name>/<password>', methods=['DELETE'])
def delete_individual_donor(name, password):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('''
            DELETE FROM IndividualDonor WHERE Name = %s AND Password = %s;
        ''', (name, password))
        mysql.connection.commit()
        cursor.close()
        return 'Individual donor deleted successfully!'
    except MySQLdb.Error as e:
        return f"Error deleting individual donor: {e}"

# Route to delete a company donor
@app.route('/delete_company_donor/<company_name>/<password>', methods=['DELETE'])
def delete_company_donor(company_name, password):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('''
            DELETE FROM CompanyDonor WHERE CompanyName = %s AND Password = %s;
        ''', (company_name, password))
        mysql.connection.commit()
        cursor.close()
        return 'Company donor deleted successfully!'
    except MySQLdb.Error as e:
        return f"Error deleting company donor: {e}"

# Route to get all individual donors
@app.route('/get_individual_donors', methods=['GET'])
def get_individual_donors():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM IndividualDonor')
        donors = cursor.fetchall()
        cursor.close()
        return jsonify(donors)
    except MySQLdb.Error as e:
        return f"Error fetching individual donors: {e}"

# Route to get all company donors
@app.route('/get_company_donors', methods=['GET'])
def get_company_donors():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM CompanyDonor')
        donors = cursor.fetchall()
        cursor.close()
        return jsonify(donors)
    except MySQLdb.Error as e:
        return f"Error fetching company donors: {e}"

if __name__ == '__main__':
    app.run(debug=True)
