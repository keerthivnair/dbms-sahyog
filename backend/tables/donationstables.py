from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
from datetime import datetime

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Ashmi@2004'
app.config['MYSQL_DB'] = 'sahyogdb'

# Initialize MySQL
mysql = MySQL(app)

# Route to create the Donations table
@app.route('/create_donations_table', methods=['GET'])
def create_donations_table():
    try:
        cursor = mysql.connection.cursor()
        # SQL query to create the Donations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Donations (
    DonationID INT AUTO_INCREMENT PRIMARY KEY,
    Amount DECIMAL(10, 2),
    DonationDate DATE,
    DonorID INT,
    FOREIGN KEY (DonorID) REFERENCES Donor(DonorID)
);
        ''')
        mysql.connection.commit()
        cursor.close()
        return 'Donations table created successfully!'
    except MySQLdb.Error as e:
        return f"Error creating Donations table: {e}"

# Route to add a donation
@app.route('/add_donation', methods=['POST'])
def add_donation():
    data = request.json
    try:
        donation_date = datetime.strptime(data['DonationDate'], "%d/%m/%Y").strftime("%Y-%m-%d")
        cursor = mysql.connection.cursor()
        cursor.execute('''
            INSERT INTO Donations (Amount, DonationDate)
            VALUES (%s, %s);
        ''', (data['Amount'], donation_date))
        mysql.connection.commit()
        cursor.close()
        return 'Donation added successfully!'
    except MySQLdb.Error as e:
        return f"Error adding donation: {e}"
    except ValueError as ve:
        return f"Error in date format: {ve}"

# Route to update a donation
@app.route('/update_donation/<int:donation_id>', methods=['PUT'])
def update_donation(donation_id):
    data = request.json
    try:
        donation_date = datetime.strptime(data['DonationDate'], "%d/%m/%Y").strftime("%Y-%m-%d")
        cursor = mysql.connection.cursor()
        cursor.execute('''
            UPDATE Donations
            SET Amount = %s, DonationDate = %s
            WHERE DonationID = %s;
        ''', (data['Amount'], donation_date, donation_id))
        mysql.connection.commit()
        cursor.close()
        return 'Donation updated successfully!'
    except MySQLdb.Error as e:
        return f"Error updating donation: {e}"
    except ValueError as ve:
        return f"Error in date format: {ve}"

# Route to delete a donation
@app.route('/delete_donation/<int:donation_id>', methods=['DELETE'])
def delete_donation(donation_id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('''
            DELETE FROM Donations WHERE DonationID = %s;
        ''', (donation_id,))
        mysql.connection.commit()
        cursor.close()
        return 'Donation deleted successfully!'
    except MySQLdb.Error as e:
        return f"Error deleting donation: {e}"

# Route to get all donations
@app.route('/get_donations', methods=['GET'])
def get_donations():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Donations')
        donations = cursor.fetchall()
        cursor.close()
        return jsonify(donations)
    except MySQLdb.Error as e:
        return f"Error fetching donations: {e}"

if __name__ == '_main_':
    app.run(debug=True)