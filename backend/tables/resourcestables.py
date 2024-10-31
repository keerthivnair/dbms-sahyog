from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Replace with your MySQL username
app.config['MYSQL_PASSWORD'] = 'keerthi2005@'  # Replace with your MySQL password
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
                QuantityAvail INT
            );
        ''')
        mysql.connection.commit()
        cursor.close()
        return 'Resources table created successfully!'
    except MySQLdb.Error as e:
        return f"Error creating Resources table: {e}"
    
# Route to get the id of a particular location id
@app.route('/get_resource_id', methods=['POST']) 
def get_resource_id():
    data = request.json 
    resource_name = data.get('resource_name')  # Get resource_name from the request data
    if not resource_name:
        return jsonify({'error': 'Resource name is required!'}), 400
    
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT ResourceID FROM resources WHERE ResourceName = %s;', (resource_name,))
        resource_id = cursor.fetchone()  # Fetch the result
        cursor.close()
        
        if resource_id:
            return jsonify({'ResourceID': resource_id[0]}), 200  # Return the ResourceID
        else:
            return jsonify({'message': 'Resource not found.'}), 404  # Handle case when resource is not found
    except MySQLdb.Error as e:
        return jsonify({'error': f"Error retrieving resource ID: {e}"}), 400


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
            'QuantityAvail': row[2]
        })
    cursor.close()
    return jsonify(resources)

# Route to update a resource
@app.route('/update_resource/<resource_name>', methods=['PUT'])
def update_resource(resource_name):
    data = request.json
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('''
            UPDATE Resources
            SET QuantityAvail = %s
            WHERE ResourceName = %s
        ''', ( data['QuantityAvail'], resource_name))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Resource updated successfully!'})
    except MySQLdb.Error as e:
        return jsonify({'error': f"Error updating resource: {e}"}), 400

# Route to delete a resource
@app.route('/delete_resource/<resource_name>', methods=['DELETE'])
def delete_resource(resource_name):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM Resources WHERE ResourceName = %s;', (resource_name,))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Resource deleted successfully!'})
    except MySQLdb.Error as e:
        return jsonify({'error': f"Error deleting resource: {e}"}), 400

if __name__ == '_main_':
    app.run(debug=True)