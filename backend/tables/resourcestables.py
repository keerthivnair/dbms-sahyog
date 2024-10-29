from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Replace with your MySQL username
app.config['MYSQL_PASSWORD'] = 'Ashmi@2004'  # Replace with your MySQL password
app.config['MYSQL_DB'] = 'sahyogdb'  # Replace with your MySQL database name

# Initialize MySQL
mysql = MySQL(app)

# Route to create the Resources table
@app.route('/create_resources_table', methods=['GET'])
def create_resources_table():
    try:
        cursor = mysql.connection.cursor()
        # SQL query to create the Resources table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Resources (
    ResourceID INT AUTO_INCREMENT PRIMARY KEY,
    ResourceName VARCHAR(255),
    QuantityReq INT,
    QuantityAvail INT,
    CampID INT,
    FOREIGN KEY (CampID) REFERENCES Camp(CampID)
);
        ''')
        mysql.connection.commit()
        cursor.close()
        return 'Resources table created successfully!'
    except MySQLdb.Error as e:
        return f"Error creating Resources table: {e}"

# Route to add a new resource
@app.route('/add_resource', methods=['POST'])
def add_resource():
    data = request.json
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('''
            INSERT INTO Resources (ResourceName, QuantityReq, QuantityAvail)
            VALUES (%s, %s, %s)
        ''', (data['ResourceName'], data['QuantityReq'], data['QuantityAvail']))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Resource added successfully!'}), 201
    except MySQLdb.Error as e:
        return jsonify({'error': f"Error adding resource: {e}"}), 400

# Route to get all resources
@app.route('/resources', methods=['GET'])
def get_resources():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM Resources;')
    results = cursor.fetchall()
    resources = []
    for row in results:
        resources.append({
            'ResourceID': row[0],
            'ResourceName': row[1],
            'QuantityReq': row[2],
            'QuantityAvail': row[3]
        })
    cursor.close()
    return jsonify(resources)

# Route to update a resource
@app.route('/update_resource/<int:resource_id>', methods=['PUT'])
def update_resource(resource_id):
    data = request.json
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('''
            UPDATE Resources
            SET ResourceName = %s,
                QuantityReq = %s,
                QuantityAvail = %s
            WHERE ResourceID = %s
        ''', (data['ResourceName'], data['QuantityReq'], data['QuantityAvail'], resource_id))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Resource updated successfully!'})
    except MySQLdb.Error as e:
        return jsonify({'error': f"Error updating resource: {e}"}), 400

# Route to delete a resource
@app.route('/delete_resource/<int:resource_id>', methods=['DELETE'])
def delete_resource(resource_id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM Resources WHERE ResourceID = %s;', (resource_id,))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Resource deleted successfully!'})
    except MySQLdb.Error as e:
        return jsonify({'error': f"Error deleting resource: {e}"}), 400

if __name__ == '_main_':
    app.run(debug=True)