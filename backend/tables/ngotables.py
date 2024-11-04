from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
import requests
from flask_cors import CORS
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)
# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Replace with your MySQL username
app.config['MYSQL_PASSWORD'] = 'keerthi2005@'  # Replace with your MySQL password
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
    NGO_Amount DECIMAL(10, 2)
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
    form_url = 'https://ngodarpan.gov.in/index.php/search/'
    
    try:
        session = requests.Session()

        #Fetch form page to get the CSRF token
        response = session.get(form_url)
        response.raise_for_status

        #Load the form page into Beautiful Soup

        soup = BeautifulSoup(response.content,'html.parser')

        # Find the csrf Token

        csrf_token = None
        input_field=soup.find('input',{'name':'unique_id_search'})
        if input_field and 'value' in input_field.attrs:
            csrf_token = input_field['value']

        payload = {
            'unique_id_search': license_number,  # Adjust this field name according to the form's requirement
            'csrf_token': csrf_token,  # Include CSRF token if needed
        }

        post_response = session.post(form_url, data=payload)
        post_response.raise_for_status()

        # Parse the response to check the verification result
        verification_soup = BeautifulSoup(post_response.content, 'html.parser')
        verification_status = verification_soup.find('div', class_='result-status')  # Adjust this according to the actual HTML structure

        if verification_status and 'valid' in verification_status.text.lower():
            return True
        else:
            return False

    except requests.RequestException as e:
        print(f"Error during requests to {form_url}: {str(e)}")
        return False

# Route to verify NGO license number
@app.route('/verify_ngo', methods=['POST'])
def verify_ngo():
    try:
        details = request.json
        license_number = details.get('LicenseNumber')

        if verify_license(license_number):
            return jsonify({"verified": True, "message": "License number is verified."}), 200
        else:
            return jsonify({"verified": False, "message": "License number is not verified."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500




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
            INSERT INTO NGO (LicenseNumber, NGOName, ChairmanName, YearOfEstablishment, Email, PhoneNumber,NGO_Amount)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        '''
        cursor.execute(query, (details['LicenseNumber'], details['NGOName'], details['ChairmanName'],
                               details['YearOfEstablishment'], details['Email'], details['PhoneNumber'],
                               details['NGO_Amount']))
        mysql.connection.commit()
        cursor.close()
        return 'NGO added successfully!', 201
    except MySQLdb.Error as e:
        return f"Error adding NGO: {e}"

# Route to update an existing NGO by ID
@app.route('/update_ngo/<license_number>', methods=['PUT'])
def update_ngo(license_number):
    try:
        cursor = mysql.connection.cursor()
        details = request.json
        query = '''
            UPDATE NGO
            SET LicenseNumber = %s, NGOName = %s, ChairmanName = %s, YearOfEstablishment = %s,
                Email = %s, PhoneNumber = %s, AmountDonated = %s, Priority = %s, Volunteers = %s
            WHERE LicenseNumber = %s
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
@app.route('/delete_ngo/<license_number>', methods=['DELETE'])
def delete_ngo(license_number):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM NGO WHERE LicenseNumber = %s', (license_number,))
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