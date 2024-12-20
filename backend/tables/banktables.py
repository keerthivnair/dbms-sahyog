from flask import Flask, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
from MySQLdb import Error   # Import Error class

app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root' 
app.config['MYSQL_PASSWORD'] = 'keerthi2005@'  
app.config['MYSQL_DB'] = 'sahyogdb'  

                                                                      
mysql = MySQL(app)

# Route to create the BankBill table
@app.route('/create_bankbill_table', methods=['GET'])
def create_bankbill_table():
    mycursor = mysql.connection.cursor()
    try:
        mycursor.execute("""
           CREATE TABLE IF NOT EXISTS BankBill (
               BankBillID INT AUTO_INCREMENT PRIMARY KEY,
               BankName VARCHAR(255) NOT NULL,
               AccountNo VARCHAR(17) NOT NULL,
               IFSC VARCHAR(11) NOT NULL,
               BranchName VARCHAR(255),
               IndividualDonorID INT,
               CompanyDonorID INT
               Amount DECIMAL(10, 2),
               BillDate DATE,
               PaymentStatus ENUM('Paid', 'Unpaid') DEFAULT 'Unpaid',
               FOREIGN KEY (IndividualDonorID) REFERENCES IndividualDonor(IndividualDonorID)
               FOREIGN KEY (CompanyDonorID) REFERENCES CompanyDonor(CompanyDonorID)
           );
        """)
        mysql.connection.commit()
        return jsonify({"message": "BankBill table created successfully!"}), 200
    except Error as e:
        print(f"Error creating BankBill table: {e}")
        return jsonify({"error": str(e)}), 500  # Return error response
    finally:
        mycursor.close()  # Ensure cursor is closed

if __name__ == '__main__':
    app.run(debug=True)
