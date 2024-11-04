# Import necessary libraries and modules
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
from flask_cors import CORS
from flask_mail import Mail, Message
from datetime import datetime, date
import MySQLdb

# Initialize the Flask app
app = Flask(__name__)
CORS(app)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  
app.config['MYSQL_PASSWORD'] = 'keerthi2005@'  
app.config['MYSQL_DB'] = 'sahyogdb'  

# Email Configuration
app.config['MAIL_SERVER'] = 'smtp.gamil.com'  
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'keerthivnair2005@example.com'  
app.config['MAIL_PASSWORD'] = 'keerthi2005@'  
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

# Initialize MySQL and Mail
mysql = MySQL(app)
mail = Mail(app)

# Route to create necessary tables (Report, Funds, NGOContribution, DistributionFunds)
@app.route('/create_additional_tables', methods=['GET'])
def create_additional_tables():
    try:
        cursor = mysql.connection.cursor()

        # SQL query to create the Funds table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Funds (
                FundID INT AUTO_INCREMENT PRIMARY KEY,
                FundAmount DECIMAL(10, 2),
                IndividualDonorID INT,  -- Nullable foreign key
                CompanyDonorID INT,     -- Nullable foreign key
                FundDate DATE,
                FOREIGN KEY (IndividualDonorID) REFERENCES IndividualDonor(IndividualDonorID),
                FOREIGN KEY (CompanyDonorID) REFERENCES CompanyDonor(CompanyDonorID),
                CHECK (IndividualDonorID IS NOT NULL OR CompanyDonorID IS NOT NULL)
            );
        ''')

        # SQL query to create the NGOContribution table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS NGOContribution (
                ContributionID INT AUTO_INCREMENT PRIMARY KEY,
                NGOID INT,
                ContributionAmount DECIMAL(10, 2),
                ContributionDate DATE,
                FOREIGN KEY (NGOID) REFERENCES NGO(NGOID)
            );
        ''')

        # SQL query to create the DistributionFunds table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS DistributionFunds (
                DistributionID INT AUTO_INCREMENT PRIMARY KEY,
                NGOCount INT,
                TotalDistributionAmount DECIMAL(10, 2),
                DistributionDate DATE
            );
        ''')

        mysql.connection.commit()
        return "Tables created successfully.", 200

    except Exception as e:
        mysql.connection.rollback()
        return str(e), 500

# Route to add funds from an individual donor
@app.route('/add_funds_individual', methods=['POST'])
def add_funds_individual():
    try:
        data = request.get_json()
        
        fund_amount = data.get('FundAmount')
        fund_date = data.get('FundDate', date.today())
        individual_donor_id = data.get('IndividualDonorID')

        if not individual_donor_id:
            return jsonify({"error": "IndividualDonorID must be provided for individual donations."}), 400

        cursor = mysql.connection.cursor()
        cursor.execute('''
            INSERT INTO Funds (FundAmount, FundDate, IndividualDonorID)
            VALUES (%s, %s, %s)
        ''', (fund_amount, fund_date, individual_donor_id))

        mysql.connection.commit()
        return jsonify({"message": "Funds from individual donor added successfully!"}), 201

    except MySQLdb.Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


# Route to add funds from a company donor
@app.route('/add_funds_company', methods=['POST'])
def add_funds_company():
    try:
        data = request.get_json()
        
        fund_amount = data.get('FundAmount')
        fund_date = data.get('FundDate', date.today())
        company_donor_id = data.get('CompanyDonorID')

        if not company_donor_id:
            return jsonify({"error": "CompanyDonorID must be provided for company donations."}), 400

        cursor = mysql.connection.cursor()
        cursor.execute('''
            INSERT INTO Funds (FundAmount, FundDate, CompanyDonorID)
            VALUES (%s, %s, %s)
        ''', (fund_amount, fund_date, company_donor_id))

        mysql.connection.commit()
        return jsonify({"message": "Funds from company donor added successfully!"}), 201

    except MySQLdb.Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
