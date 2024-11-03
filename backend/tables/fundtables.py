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
                FOREIGN KEY (IndividualDonorID) REFERENCES IndividualDonor(DonorID),
                FOREIGN KEY (CompanyDonorID) REFERENCES CompanyDonor(DonorID),
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

# Route to add funds
@app.route('/add_funds', methods=['POST'])
def add_funds():
    try:
        data = request.get_json()

        fund_amount = data.get('FundAmount')
        fund_date = data.get('FundDate', date.today())
        individual_donor_id = data.get('IndividualDonorID')
        company_donor_id = data.get('CompanyDonorID')

        if not (individual_donor_id or company_donor_id):
            return jsonify({"error": "At least one donor ID must be provided."}), 400

        cursor = mysql.connection.cursor()
        cursor.execute('''
            INSERT INTO Funds (FundAmount, FundDate, IndividualDonorID, CompanyDonorID)
            VALUES (%s, %s, %s, %s)
        ''', (fund_amount, fund_date, individual_donor_id, company_donor_id))

        mysql.connection.commit()
        return jsonify({"message": "Funds added successfully!"}), 201

    except MySQLdb.Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

# Function to distribute funds and send notifications
def distribute_funds_and_notify():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute("SELECT SUM(FundAmount) AS total_funds FROM Funds")
        total_funds_result = cursor.fetchone()
        total_funds = total_funds_result['total_funds'] if total_funds_result['total_funds'] else 0

        cursor.execute('SELECT * FROM NGO ORDER BY YearOfEstablishment ASC')
        ngos = cursor.fetchall()

        MIN_AMOUNT_PER_NGO = 500
        eligible_ngos = []
        ngo_count = 0

        for ngo in ngos:
            if (ngo_count + 1) * MIN_AMOUNT_PER_NGO <= total_funds:
                eligible_ngos.append(ngo)
                ngo_count += 1
            else:
                break

        if eligible_ngos:
            amount_per_ngo = total_funds // ngo_count

            for ngo in eligible_ngos:
                ngo_id = ngo['NGOID']
                ngo_email = ngo['Email']  # Assuming you have an Email column in your NGO table

                # Insert distribution record
                cursor.execute('''
                    INSERT INTO NGOContribution (NGOID, ContributionAmount, ContributionDate)
                    VALUES (%s, %s, CURDATE())
                ''', (ngo_id, amount_per_ngo))

                # Send email notification
                msg = Message('Funds Distributed', recipients=[ngo_email])
                msg.body = f"Dear {ngo['NGOName']},\n\nYou have received a distribution of {amount_per_ngo} funds.\n\nBest regards,\nSahyog Team"
                mail.send(msg)

            # Log the distribution in DistributionFunds table
            cursor.execute('''
                INSERT INTO DistributionFunds (NGOCount, TotalDistributionAmount, DistributionDate)
                VALUES (%s, %s, CURDATE())
            ''', (ngo_count, total_funds))

            # Clear the Funds table after distribution
            cursor.execute('DELETE FROM Funds')
            mysql.connection.commit()

        return {"message": "Funds distributed and notifications sent successfully!"}

    except MySQLdb.Error as e:
        mysql.connection.rollback()
        return {"error": str(e)}
    finally:
        cursor.close()

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
