from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
from MySQLdb import Error  

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'your_username'  # Add your MySQL username
app.config['MYSQL_PASSWORD'] = 'keerthi2005@'
app.config['MYSQL_DB'] = 'sahyogdb'

# Initialize MySQL
mysql = MySQL(app)

# Route to create the Donations table
@app.route('/create_donations_table', methods=['GET'])
def create_donations_table():
    mycursor = mysql.connection.cursor()
    try:
        mycursor.execute("""
            CREATE TABLE IF NOT EXISTS Bank_bill (
                BillID INT AUTO_INCREMENT PRIMARY KEY,
                BankName VARCHAR(255),
                AccountNo VARCHAR(17),
                IFSC VARCHAR(11),
                DonorID INT,  -- Specify datatype for DonorID
                Amount INT,         
                FOREIGN KEY (DonorID) REFERENCES Donor(DonorID)  -- Remove trailing comma
            )
        """)
        mysql.connection.commit()
        return 'Bank table created successfully!'
    except Error as e:
        print(f"Error creating Bank table: {e}")
        return jsonify({"error": str(e)}), 500  # Return error response
    finally:
        mycursor.close()  # Ensure cursor is closed

if __name__ == '__main__':  # Corrected __name__ check
    app.run(debug=True)
