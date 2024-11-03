from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
from MySQLdb import Error
from locationtables import get_location_id  # Import the function to get LocationID
import os
from werkzeug.utils import secure_filename
import requests

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Replace with your MySQL username
app.config['MYSQL_PASSWORD'] = 'keerthi2005@'  # Replace with your MySQL password
app.config['MYSQL_DB'] = 'sahyogdb'  # Replace with your database name
app.config['UPLOAD_FOLDER'] = r'C:\react-js\dis-management\files'

# Initialize MySQL
mysql = MySQL(app)

# Individual routes for each view
@app.route('/donation_donator', methods=['GET'])
def donation_donator():
    try:
        mycursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        mycursor.execute("""
            SELECT Donations.DonationID, Donor.DonorID, Donor.Name, Donations.Amount
            FROM Donations
            JOIN Donor ON Donor.DonorID = Donations.DonorID;
        """)
        result = mycursor.fetchall()
        mycursor.close()
        return jsonify(result)
    except Error as e:
        print(f"Error fetching donation_donator view: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/volunteers_camp', methods=['GET'])
def volunteers_camp():
    try:
        mycursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        mycursor.execute("""
            SELECT COUNT(Volunteers.VolunteerID) AS VolunteerCount, Camp.CampID
            FROM Volunteers
            JOIN Camp ON Camp.VolunteerID = Volunteers.VolunteerID
            GROUP BY Camp.CampID;
        """)
        result = mycursor.fetchall()
        mycursor.close()
        return jsonify(result)
    except Error as e:
        print(f"Error fetching volunteers_camp view: {e}")
        return jsonify({"error": str(e)}), 500

# Define the rest of the individual views in a similar way...

# Route for combined views
@app.route('/combined_views', methods=['GET'])
def combined_views():
    mycursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    combined_data = {}

    try:
        # Fetch all views together
        mycursor.execute("""
            SELECT Donations.DonationID, Donor.DonorID, Donor.Name, Donations.Amount
            FROM Donations
            JOIN Donor ON Donor.DonorID = Donations.DonorID;
        """)
        combined_data['donation_donator'] = mycursor.fetchall()

        mycursor.execute("""
            SELECT COUNT(Volunteers.VolunteerID) AS VolunteerCount, Camp.CampID
            FROM Volunteers
            JOIN Camp ON Camp.VolunteerID = Volunteers.VolunteerID
            GROUP BY Camp.CampID;
        """)
        combined_data['volunteers_camp'] = mycursor.fetchall()

        # Continue adding the other views similarly
        # ...

        return jsonify(combined_data), 200

    except Error as e:
        print(f"Error fetching views: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        mycursor.close()
@app.route('/add_volunteer_details', methods=['POST'])
def add_volunteer_details():
    data = request.form
    username = data.get('VolunteerName')
    password = data.get('Password')
    location_name = data.get('LocationName')
    license_file = request.files.get('license')

    # Step 1: Fetch VolunteerID by calling /get_volunteer_id
    response = requests.post('http://localhost:5000/get_volunteer_id', json={'VolunteerName': username, 'Password': password})
    if response.status_code == 404:
        return jsonify({'error': 'Invalid username or password.'}), 401

    volunteer_id = response.json().get('VolunteerID')

    # Step 2: Convert location_name to location_id using get_location_id function
    location_id = get_location_id(location_name)
    if location_id is None:
        return jsonify({'error': 'Invalid location name.'}), 400

    # Step 3: Save the license file
    filename = secure_filename(license_file.filename)
    license_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    license_file.save(license_file_path)

    # Step 4: Insert data into vol_details
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('''
            INSERT INTO vol_details (VolunteerID, LocationID, License)
            VALUES (%s, %s, %s)
        ''', (volunteer_id, location_id, filename))
        mysql.connection.commit()
        cursor.close()

        return jsonify({'success': True, 'message': 'Volunteer details added successfully.'})
    except Error as e:
        print(f"Error adding volunteer details: {e}")
        return jsonify({'error': 'Could not add volunteer details.'}), 500


if __name__ == '__main__':
    app.run(debug=True)
