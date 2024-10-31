from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Replace with your MySQL username
app.config['MYSQL_PASSWORD'] = 'Ashmi@2004'  # Replace with your MySQL password
app.config['MYSQL_DB'] = 'sahyogdb'  # Replace with your MySQL database name

# Initialize MySQL
mysql = MySQL(app)

# Route to create the Report table
@app.route('/create_report_table', methods=['GET'])
def create_report_table():
    try:
        cursor = mysql.connection.cursor()
        # SQL query to create the Report table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Report (
    ReportID INT AUTO_INCREMENT PRIMARY KEY,
    ReportDate DATE,
    ReportDetails TEXT,
    ResourceID INT,
    DonationID INT,
    LocationID INT,
    DonorID INT,
    DisasterID INT,
    CampID INT,
    Volunteers_req INT,
    Volunteers_avail INT,
    FOREIGN KEY (ResourceID) REFERENCES Resources(ResourceID),
    FOREIGN KEY (DonationID) REFERENCES Donations(DonationID),
    FOREIGN KEY (LocationID) REFERENCES Location(LocationID),
    FOREIGN KEY (DonorID) REFERENCES Donor(DonorID),
    FOREIGN KEY (DisasterID) REFERENCES Disaster(DisasterID),
    FOREIGN KEY (CampID) REFERENCES Camp(CampID)
);
        ''')
        mysql.connection.commit()
        cursor.close()
        return 'Report table created successfully!'
    except MySQLdb.Error as e:
        return f"Error creating Report table: {e}"

# Route to add a new report
@app.route('/add_report', methods=['POST'])
def add_report():
    data = request.json
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('''
            INSERT INTO Report (ReportDate, ReportDetails)
            VALUES (%s, %s)
        ''', (data['ReportDate'], data['ReportDetails']))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Report added successfully!'}), 201
    except MySQLdb.Error as e:
        return jsonify({'error': f"Error adding report: {e}"}), 400

@app.route('/reports', methods=['GET'])
def get_reports():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM Report;')
    results = cursor.fetchall()
    reports = []
    for row in results:
        reports.append({
           'ReportID': row[0],
           'ReportDate': str(row[1]),  # Ensure the date is converted to string
           'ReportDetails': row[2]
        })
    cursor.close()
    return jsonify(reports)

# Route to update a report
@app.route('/update_report/<int:report_id>', methods=['PUT'])
def update_report(report_id):
    data = request.json
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('''
            UPDATE Report
            SET ReportDate = %s,
                ReportDetails = %s
            WHERE ReportID = %s
        ''', (data['ReportDate'], data['ReportDetails'], report_id))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Report updated successfully!'})
    except MySQLdb.Error as e:
        return jsonify({'error': f"Error updating report: {e}"}), 400

# Route to delete a report
@app.route('/delete_report/<int:report_id>', methods=['DELETE'])
def delete_report(report_id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM Report WHERE ReportID = %s;', (report_id,))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Report deleted successfully!'})
    except MySQLdb.Error as e:
        return jsonify({'error': f"Error deleting report: {e}"}), 400

if __name__ == '__main__':
    app.run(debug=True)