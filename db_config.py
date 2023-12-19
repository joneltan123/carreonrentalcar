from app import app
from flaskext.mysql import MySQL

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'carreonr_carreonr'
app.config['MYSQL_DATABASE_PASSWORD'] = 'joneltan1234'
app.config['MYSQL_DATABASE_DB'] = 'carreonr_db_rental_car_system'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
