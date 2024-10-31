from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Replace with your MySQL username
app.config['MYSQL_PASSWORD'] = 'keerthi2005@'  # Replace with your MySQL password
app.config['MYSQL_DB'] = 'sahyogdb'  # Replace with your MySQL database name

# Initialize MySQL
mysql = MySQL(app)

# Route to create the Volunteers table
@app.route('/create_volunteers_table', methods=['GET'])
def create_volunteers_table():
    try:
        cursor = mysql.connection.cursor()
        # SQL query to create the Volunteers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Volunteers (
                VolunteerID INT AUTO_INCREMENT PRIMARY KEY,
                VolunteerName VARCHAR(255) NOT NULL,
                VolunteerEmail VARCHAR(255),
                Gender ENUM('Male', 'Female', 'Other'),
                Age INT,
                PlaceOfStay VARCHAR(255),
                LanguagesKnown VARCHAR(255),
                PreviousExperience TEXT,
                Height DECIMAL(5, 2),  -- In meters
                Weight DECIMAL(5, 2),  -- In kilograms
                BMI DECIMAL(5, 2) GENERATED ALWAYS AS (Weight / (Height * Height)) STORED,  -- Calculated BMI field
                EducationalQualification VARCHAR(255),
                Password int not null
            );
        ''')
        mysql.connection.commit()
        cursor.close()
        return 'Volunteers table created successfully!'
    except Exception as e:
        return f"Error creating Volunteers table: {e}"

# Route to add a new volunteer
@app.route('/add_volunteer', methods=['POST'])
def add_volunteer():
    data = request.json
    try:
        height = float(data['Height'])
        weight = float(data['Weight'])
        bmi = round(weight / (height ** 2), 2)

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM Volunteers WHERE VolunteerName = %s AND Password = %s",(data['VolunteerName'],data['Password']))
        existing_volunteer = cursor.fetchone()

        if existing_volunteer:
            cursor.close()
            return jsonify({'message': 'Volunteer already registered, please login.'})
        cursor.execute('''
            INSERT INTO Volunteers (VolunteerName, VolunteerEmail, Gender, Age, PlaceOfStay,
                                    LanguagesKnown, PreviousExperience, Height, Weight, EducationalQualification,Password)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)
        ''', (data['VolunteerName'], data['VolunteerEmail'], data['Gender'], data['Age'],
              data['PlaceOfStay'], data['LanguagesKnown'], data['PreviousExperience'],
              data['Height'], data['Weight'],data['EducationalQualification'], data['Password']))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Volunteer added successfully!'}), 201
    except Exception as e:
        return jsonify({'error': f"Error adding volunteer: {e}"}), 400

# Route to get all volunteers
@app.route('/volunteers', methods=['GET'])
def get_volunteers():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM Volunteers;')
    results = cursor.fetchall()
    volunteers = []
    for row in results:
        volunteers.append({
            'VolunteerID': row[0],
            'VolunteerName': row[1],
            'VolunteerEmail': row[2],
            'Gender': row[3],
            'Age': row[4],
            'PlaceOfStay': row[5],
            'LanguagesKnown': row[6],
            'PreviousExperience': row[7],
            'Height': row[8],
            'Weight': row[9],
            'BMI': row[10],
            'EducationalQualification': row[11],
            'Password': row[12]
        })
    cursor.close()
    return jsonify(volunteers)

@app.route('/volunteer/<username>/<password>',methods=['POST'])
def get_volunteer(username,password):
    try:
        cursor=mysql.connection.cursor()
        cursor.execute('SELECT * FROM Volunteers WHERE VolunteerName=%s AND Password=%s',(username,password))
        volunteer = cursor.fetchone()
        cursor.close()
        if volunteer:
            return jsonify({
                'VolunteerID': volunteer[0],
                'VolunteerName': volunteer[1],
                'VolunteerEmail': volunteer[2],
                'Gender': volunteer[3],
                'Age': volunteer[4],
                'PlaceOfStay': volunteer[5],
                'LanguagesKnown': volunteer[6],
                'PreviousExperience': volunteer[7],
                'Height': volunteer[8],
                'Weight': volunteer[9],
                'BMI': volunteer[10],
                'EducationalQualification': volunteer[11]
            })
        else:
            return jsonify({'message': 'Volunteer not found, please register.'}), 404
    except Exception as e:
             return jsonify({'error': f"Error retrieving volunteer: {e}"})

@app.route('/update_volunteer/<username>/<password>', methods=['PUT'])
def update_volunteer(username, password):
    data = request.json
    try:
        # Verify username and password
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM Volunteers WHERE VolunteerName = %s AND Password = %s', 
                       (username, password))
        volunteer = cursor.fetchone()
        
        if not volunteer:
            cursor.close()
            return jsonify({'message': 'Volunteer not found or incorrect credentials.'}), 404

        # Update volunteer if credentials match
        cursor.execute('''
            UPDATE Volunteers
            SET VolunteerName = %s,
                VolunteerEmail = %s,
                Gender = %s,
                Age = %s,
                PlaceOfStay = %s,
                LanguagesKnown = %s,
                PreviousExperience = %s,
                Height = %s,
                Weight = %s,
                EducationalQualification = %s
            WHERE VolunteerID = %s
        ''', (data['VolunteerName'], data['VolunteerEmail'], data['Gender'], data['Age'],
              data['PlaceOfStay'], data['LanguagesKnown'], data['PreviousExperience'],
              data['Height'], data['Weight'], data['EducationalQualification'], volunteer[0]))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Volunteer updated successfully!'})
    except Exception as e:
        return jsonify({'error': f"Error updating volunteer: {e}"}), 400
# Route to delete a volunteer

@app.route('/delete_volunteer/<username>/<password>', methods=['DELETE'])
def delete_volunteer(username, password):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM Volunteers WHERE VolunteerName = %s AND Password = %s', 
                       (username, password))
        volunteer = cursor.fetchone()

        if not volunteer:
            cursor.close()
            return jsonify({'message': 'Volunteer not found or incorrect credentials.'}), 404

        cursor.execute('DELETE FROM Volunteers WHERE VolunteerID = %s', (volunteer[0],))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Volunteer deleted successfully!'})
    except Exception as e:
        return jsonify({'error': f"Error deleting volunteer: {e}"}), 400
if __name__ == '__main__':
    app.run(debug=True)