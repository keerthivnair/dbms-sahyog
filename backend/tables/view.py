from flask import Flask, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
from MySQLdb import Error  

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Replace with your MySQL username
app.config['MYSQL_PASSWORD'] = 'keerthi2005@'  # Replace with your MySQL password
app.config['MYSQL_DB'] = 'sahyogdb'  # Replace with your database name

# Initialize MySQL
mysql = MySQL(app)

# Route to fetch combined views in JSON format
@app.route('/combined_views', methods=['GET'])
def combined_views():
    mycursor = mysql.connection.cursor()
    combined_data = {}

    try:
        # Execute each view and collect results
        # View 1: Donation_Donator
        mycursor.execute("""
            SELECT Donations.DonationID, Donor.DonorID, Donor.Name, Donations.Amount
            FROM Donations
            JOIN Donor ON Donor.DonorID = Donations.DonorID;
        """)
        combined_data['donation_donator'] = mycursor.fetchall()

        # View 2: Volunteers_Camp
        mycursor.execute("""
            SELECT COUNT(Volunteers.VolunteerID) AS VolunteerCount, Camp.CampID
            FROM Volunteers
            JOIN Camp ON Camp.VolunteerID = Volunteers.VolunteerID
            GROUP BY Camp.CampID;
        """)
        combined_data['volunteers_camp'] = mycursor.fetchall()

        # View 3: Volunteer_Report
        mycursor.execute("""
            SELECT Camp.CampID, Report.Volunteers_avail, Report.Volunteer_req
            FROM Camp
            JOIN Report ON Camp.CampID = Report.CampID;
        """)
        combined_data['volunteer_report'] = mycursor.fetchall()

        # View 4: NGO_Donation
        mycursor.execute("""
            SELECT NGO.NGOID, NGO.NGOName, NGO.NGO_Amount, Donations.Amount
            FROM NGO
            JOIN Donations ON NGO.NGOID = Donations.DonorID
        """)
        combined_data['ngo_donation'] = mycursor.fetchall()

        # View 5: NGO_Resources
        mycursor.execute("""
            SELECT NGO.NGOID, NGO.NGOName, Resources.ResourceName, Resources.QuantityAvail
            FROM NGO
            JOIN Resources ON NGO.NGOID = Resources.CampID
        """)
        combined_data['ngo_resources'] = mycursor.fetchall()

        # View 6: Donor_Report
        mycursor.execute("""
            SELECT Donor.DonorID, Donor.Name, Report.ReportID, Report.ReportDetails
            FROM Donor
            JOIN Report ON Donor.DonorID = Report.DonorID
        """)
        combined_data['donor_report'] = mycursor.fetchall()

        # View 7: Camp_Report_Resources
        mycursor.execute("""
            SELECT Camp.CampID, Resources.QuantityReq, Resources.QuantityAvail
            FROM Camp
            JOIN Resources ON Camp.CampID = Resources.CampID
        """)
        combined_data['camp_report_resources'] = mycursor.fetchall()

        # View 8: Location_Camp
        mycursor.execute("""
            SELECT Camp.CampID, Camp.CampName, Location.LocationID, Location.LocationName
            FROM Camp
            JOIN Location ON Camp.LocationID = Location.LocationID
        """)
        combined_data['location_camp'] = mycursor.fetchall()

        # View 9: Report_Disaster
        mycursor.execute("""
            SELECT Disaster.DisasterID, Disaster.DisasterType, Report.LocationID
            FROM Disaster
            JOIN Report ON Report.DisasterID = Disaster.DisasterID
        """)
        combined_data['report_disaster'] = mycursor.fetchall()

        return jsonify(combined_data), 200

    except Error as e:
        print(f"Error fetching views: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        mycursor.close()

if __name__ == '__main__':
    app.run(debug=True)
