from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_mail import Mail
from apscheduler.schedulers.background import BackgroundScheduler
from fundtables import distribute_funds_and_notify  # Import the function

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root' 
app.config['MYSQL_PASSWORD'] = 'keerthi2005@'  
app.config['MYSQL_DB'] = 'sahyogdb'  

app.config['MAIL_SERVER'] = 'smtp.gmail.com'  
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'keerthivnair2005@example.com'  
app.config['MAIL_PASSWORD'] = 'keerthi2005@'  
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False  

mysql = MySQL(app)
mail = Mail(app)


scheduler = BackgroundScheduler()
scheduler.add_job(lambda: distribute_funds_and_notify(mysql, mail), 'interval', hours=24)
scheduler.start()


@app.route('/distribute_funds', methods=['POST'])
def distribute_funds():
    result = distribute_funds_and_notify(mysql, mail)
    return jsonify(result), 200

if __name__ == '__main__':
    app.run(debug=True)
