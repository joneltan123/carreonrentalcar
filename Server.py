import pymysql
from app import app
from db_config import mysql
from flask import flash, render_template, request, redirect, url_for, session, json
import os
import requests
from werkzeug.utils import secure_filename
#====================================================
import logging

# Set up logging if the current file is the main application file.
# This ensures the logging is set up only once, even if this module gets imported elsewhere.
if __name__ == "__main__":
    logging.basicConfig(filename='error.log', level=logging.ERROR)

@app.errorhandler(500)
def internal_server_error(error):
    app.logger.error('Server Error: %s', error)
    return "500 error", 500

@app.errorhandler(404)
def not_found_error(error):
    app.logger.error('Not Found: %s', error)
    return "404 error", 404

#===================================================================================== View Ongoing Customer
@app.route('/admin_booking_ongoing', methods=['GET', 'POST'])
def admin_booking_ongoing():
    if 'Admin_UserName' not in session or 'AdminFirstName' not in session:
        return "<h1><center>Error: admin_booking_ongoing</center><br>⚠️Admin credentials are incomplete. Access Denied.⚠️<a href='/login_admin_view'>Log-In</a></h1>"
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        if request.method == 'POST':
            search_query = request.form.get('Search')
            sql_query = "SELECT * FROM tbl_customer_info WHERE Status = 'Ongoing' AND (Car_Name LIKE %s OR First_Name LIKE %s OR Last_Name LIKE %s OR Date_of_pickup LIKE %s OR Date_of_return LIKE %s);"
            cursor.execute(sql_query, (f"%{search_query}%", f"%{search_query}%", f"%{search_query}%", f"%{search_query}%", f"%{search_query}%"))
            flash('You search for "{}"'.format(search_query))
        else:
            cursor.execute("SELECT * FROM tbl_customer_info WHERE Status = 'Ongoing';")

        rows = cursor.fetchall()
        return render_template('admin_booking_ongoing.html', rows=rows)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

#===================================================================================== View Customer Info Ongoing Booking Page
@app.route('/view_ongoing_cust_info/<string:id>')
def view_ongoing_cust_info(id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM tbl_customer_info WHERE id=%s", id)
        row = cursor.fetchone()
        if row:
            return render_template('view_customerInfo_ongoingB.html', row=row)

        else:
            return 'Error loading #{id}'.format(id=id)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

#===================================================================================== View ALL Customer Completed Booking Page
@app.route('/admin_booking_completed', methods=['GET', 'POST'])
def admin_booking_completed():
    if 'Admin_UserName' not in session or 'AdminFirstName' not in session:
        return "<h1><center>Error: admin_booking_completed</center><br>⚠️Admin credentials are incomplete. Access Denied.⚠️<a href='/login_admin_view'>Log-In</a></h1>"
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        if request.method == 'POST':
            search_query = request.form.get('Search')
            sql_query = "SELECT * FROM tbl_customer_info WHERE Status = 'Completed' AND (Car_Name LIKE %s OR First_Name LIKE %s OR Last_Name LIKE %s);"
            cursor.execute(sql_query, (f"%{search_query}%", f"%{search_query}%", f"%{search_query}%"))
            flash('You search for "{}"'.format(search_query))
        else:
            cursor.execute("SELECT * FROM tbl_customer_info WHERE Status = 'Completed';")

        rows = cursor.fetchall()
        return render_template('admin_booking_completed.html', rows=rows)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

#====================================================== View Customer Info Completed Booked Page
@app.route('/view_completed_cust_info/<string:id>')
def view_completed_cust_info(id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM tbl_customer_info WHERE id=%s", id)
        row = cursor.fetchone()
        if row:
            return render_template('view_customerInfo_completedB.html', row=row)
        else:
            return 'Error loading #{id}'.format(id=id)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

#=================================================================View Admin Extend Rent Date
@app.route('/view_extend_rent_date/<string:id>')
def view_extend_rent_date(id):
    if 'Admin_UserName' not in session or 'AdminFirstName' not in session:
        return "<h1><center>Error: view_extend_rent_date</center><br>⚠️Admin credentials are incomplete. Access Denied.⚠️<a href='/login_admin_view'>Log-In</a></h1>"
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM tbl_customer_info WHERE id=%s", id)
        row = cursor.fetchone()
        if row:
            return render_template('extend_rental_date.html', row=row)
        else:
            return 'Error loading #{id}'.format(id=id)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

#==================================================================View Admin Extend Distance
@app.route('/view_extend_distance/<string:id>')
def view_extend_distance(id):
    if 'Admin_UserName' not in session or 'AdminFirstName' not in session:
        return "<h1><center>Error: view_extend_distance</center><br>⚠️Admin credentials are incomplete. Access Denied.⚠️<a href='/login_admin_view'>Log-In</a></h1>"
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM tbl_customer_info WHERE id=%s", id)
        row = cursor.fetchone()
        if row:
            return render_template('extend_distance.html', row=row)
        else:
            return 'Error loading #{id}'.format(id=id)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

#========================================= POST Method to Save Changes in Extend Rent Date
@app.route('/update_extend_rent_date', methods=['POST'])
def update_extend_rent_date():
    conn = None
    cursor = None
    try:
        # GET USER INPUTS
        strid = request.form['txtuserid']
        strreturn = request.form['txtreturn']
        strNoofDays = request.form['txtNoofDays']
        strAmounttoPay = request.form['txtAmount2Pay']
        strTotalAmounttoPay = request.form['txtTotalAmount2Pay']
        strpickup = request.form['txtpickup']
        strcarname = request.form['txtCarname']

        # Check if the return date is still available
        conn = mysql.connect()
        cursor = conn.cursor()

        # Query the tbl_customer_info table to check for date range overlap
        check_sql = """
            SELECT id FROM tbl_customer_info
            WHERE Car_Name = %s AND Status = 'Ongoing'
            AND (
                (Date_of_pickup <= %s AND Date_of_return >= %s)
                OR (Date_of_pickup > %s AND Date_of_pickup <= %s)
            )
        """
        check_data = (strcarname, strreturn, strreturn, strpickup, strreturn)
        cursor.execute(check_sql, check_data)
        result = cursor.fetchone()

        if result:
            # The return date is not available
            flash('⚠️Check the return date. {} will not be available.'.format(strreturn))
            return redirect('/admin_booking_ongoing')
        else:
            # The return date is available, proceed with the update
            update_sql = """
                UPDATE tbl_customer_info 
                SET Date_of_return=%s, No_of_Days=%s, Amount_to_Pay=%s, Total_Amount_to_Pay=%s 
                WHERE id=%s
            """
            update_data = (strreturn, strNoofDays, strAmounttoPay, strTotalAmounttoPay, strid)
            cursor.execute(update_sql, update_data)
            conn.commit()
            flash(u'\u2705' 'Extending Rental Date for ID# {} has been successfully saved in record.'.format(strid))
            return redirect('/admin_booking_ongoing')
    except Exception as e:
        print(e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

#===================================================================POST Method to Save Changes in Extend Distance
@app.route('/update_extend_distance', methods=['POST'])
def update_extend_distance():
    conn = None
    cursor = None
    try:
        # GET USER INPUTS
        strid = request.form['txtuserid']
        strcarparday = request.form['txtcar_per_day']
        strAmount2pay = request.form['txtAmount2Pay']
        strTotalAmounttoPay = request.form['txtTotalAmount2Pay']

        if request.method == 'POST':
            # SAVE RECORD TO DATABASE
            sql = "UPDATE tbl_customer_info SET \
                   Car_per_days=%s, Amount_to_Pay=%s, Total_Amount_to_Pay=%s \
                   WHERE id=%s"
            data = (strcarparday, strAmount2pay, strTotalAmounttoPay, strid)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            flash(u'\u2705''Record with ID {} has been successfully extend the location distance to rent.'.format(strid))
            return redirect('/admin_booking_ongoing')
        else:
            return 'Error while updating user'
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

#===========================Move Ongoing Booking Customer in Completed Customer
@app.route('/completed_cust_info/<string:id>')
def completed_cust_info(id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("UPDATE tbl_customer_info SET status = 'Completed' WHERE id = %s", (id,))
        conn.commit()
        flash(u'\u2705 Record with ID {} has been successfully transferred to Booking Completed!'.format(id))
        return redirect('/admin_booking_ongoing')
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

#===================================================View Admin Log-In Page
@app.route('/login_admin_view')
def login_admin_view():
    return render_template('admin_login_form.html')

#====================================================POST admin Log-In
@app.route('/AdminLogin', methods =['GET', 'POST'])
def AdminLogin():

    msg = ''
    if request.method == 'POST' and 'admin_username' in request.form and 'admin_password' in request.form:
        username = request.form['admin_username']
        password = request.form['admin_password']
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute('SELECT * FROM adminlogin_info WHERE Admin_UserName = % s AND Admin_Password = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['Admin_UserName'] = account['Admin_UserName']
            session['AdminFirstName'] = account['AdminFirstName']
            session['AdminLastName'] = account['AdminLastName']
            session['AdminPosition'] = account['AdminPosition']

            msg = 'Logged in successfully !'
            return redirect(url_for('admin_booking_ongoing', msg = msg))
        else:
            flash('! Something wrong in your username and password. Please check again your information to login.')

    return redirect('/login_admin_view')

#==============================================For Admin Log Out
@app.route('/AdminLogout')
def AdminLogout():
    session.pop('loggedin', None)
    session.pop('Admin_UserName', None)
    session.pop('AdminFirstName', None)
    session.pop('AdminLastName', None)
    session.pop('AdminPosition', None)

    return redirect(url_for('AdminLogin'))

#===========================================View All Car-List
@app.route('/car_list')
def car_list():
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM car_list")
        rows_car_list = cursor.fetchall()

        cursor.execute("SELECT * FROM tbl_customer_info WHERE Status = 'Ongoing'")
        rows_customer_info = cursor.fetchall()

        return render_template('rentcar_list.html', rows_car_list=rows_car_list, rows_customer_info=rows_customer_info)
    except Exception as e:
        print(e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

#============================================ Customer View_Profile
@app.route('/View_Profile')
def View_Profile():
    if 'UserName' not in session or 'CustomerID' not in session:
        return "<h1><center>Error: View_Profile</center><br>⚠️Admin credentials are incomplete. Access Denied.⚠️<a href='/Customer_LogIn'>Log-In</a></h1>"
    else:
        return render_template('View_profile.html')

#=================================== View Customer Register Form
@app.route('/Register_Customer')
def Register_Customer():
    sitekey = "6LcJ1qooAAAAANaAGE3m-VmoWNZ3GSubX29epKbM"# <<----| ReCaptcha Site Key
    return render_template("register_customer.html", sitekey=sitekey)

#========================================== Select Valid Id Picture Fulder Path
UPLOAD_FOLDER_ValidID = 'static/Customer_ValidIdPicture'
app.config['UPLOAD_FOLDER_ValidID'] = UPLOAD_FOLDER_ValidID

#========================================== ReCaptcha Validation
def is_human(captcha_response):
    """ Validating reCAPTCHA response from Google server
        Returns True if captcha test passed for submitted form else returns False.
    """
    secret = "6LcJ1qooAAAAAN4AUdYenHS-b8DmAoGSJesNpobk"# <<----| ReCaptcha Secret Key
    payload = {'response': captcha_response, 'secret': secret}
    response = requests.post("https://www.google.com/recaptcha/api/siteverify", data=payload)
    response_text = json.loads(response.text)
    return response_text['success']

#======================== ============POST Contact Validation And Save Register
@app.route("/contact/", methods=["GET", "POST"])
def contact():

    if request.method == "POST":
        strCusFName = request.form['txtRCusFName']
        strCusLName = request.form['txtRCusLName']
        strGender = request.form['cboRCGender']
        strAge = request.form['txtRCAge']
        strAddress = request.form['txtRAddress']
        strEmailAdd = request.form['txtREmailAdd']
        strMobileNo = request.form['txtRMobileNo']
        strusername = request.form['txtRusername']
        strpassword = request.form['txtRpassword']
        captcha_response = request.form['g-recaptcha-response']

        if is_human(captcha_response):
            # Check if the 'imageUpload' file input field exists in the request
            if 'imageUpload' not in request.files:
                return "No file part"

            file = request.files['imageUpload']

            # Check if the file is empty
            if file.filename == '':
                return "No selected file"

            # Check if the file is allowed (e.g., only image files)
            allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}

            if not '.' in file.filename or file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
                return "Invalid file type"

            # Generate a unique filename for the uploaded file
            filename = secure_filename(file.filename)
            file_count = 1
            while os.path.exists(os.path.join(app.config['UPLOAD_FOLDER_ValidID'], filename)):
                # File with the same name exists, add (1), (2), etc., to the filename
                filename = f"{os.path.splitext(file.filename)[0]}({file_count}){os.path.splitext(file.filename)[1]}"
                file_count += 1

            # Save the uploaded file with the unique filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER_ValidID'], filename))
            # Process request here
            # SAVE RECORD TO DATABASE
            sql = "INSERT INTO tbl_register_customer_info \
                            (FirstName, LastName, Gender, Age, Address, EmailAddress, MobileNumber, UserName, Password, Valid_Id_Image) \
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            data = (
            strCusFName, strCusLName, strGender, strAge, strAddress, strEmailAdd, strMobileNo, strusername, strpassword,
            filename)
            try:
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute(sql, data)
                conn.commit()
            except Exception as e:
                flash(f'Error occurred: {e}')
                conn.rollback()
            finally:
                cursor.close()
                conn.close()
            return redirect('/Customer_LogIn')
        else:
            # Log invalid attempts
            flash('Sorry! Please try again and Check "I am not a robot." for Validation.')
            return redirect(url_for('Register_Customer'))

#============================================  View Customer Log In
@app.route('/Customer_LogIn')
def Customer_LogIn():
    return render_template('customer_login.html')

#============================================  POST Customer Log In
@app.route('/loginn', methods =['GET', 'POST'])
def loginn():

    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute('SELECT * FROM tbl_register_customer_info WHERE UserName = % s AND Password = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['CustomerID'] = account['CustomerID']
            session['FirstName'] = account['FirstName']
            session['LastName'] = account['LastName']
            session['Gender'] = account['Gender']
            session['Age'] = account['Age']
            session['Address'] = account['Address']
            session['EmailAddress'] = account['EmailAddress']
            session['MobileNumber'] = account['MobileNumber']
            session['UserName'] = account['UserName']
            session['Valid_Id_Image'] = account['Valid_Id_Image']
            msg = 'Logged in successfully !'
            return redirect(url_for('car_list', msg = msg))
        else:
            flash('! Something wrong in your username and password. Please check again your information to login.')

    return redirect('/Customer_LogIn')

#============================================ POST Customer logout
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('CustomerID', None)
    session.pop('FirstName', None)
    session.pop('LastName', None)
    session.pop('Gender', None)
    session.pop('Age', None)
    session.pop('Address', None)
    session.pop('EmailAddress', None)
    session.pop('MobileNumber', None)
    session.pop('UserName', None)
    session.pop('Valid_Id_Image', None)
    return redirect(url_for('loginn'))

#===============================================  View Home Page
@app.route('/')
def home_page():
    return render_template('Home_Page.html')

#========================================  View Rental Form
@app.route('/view_rent_forms/<string:id>')
def view_rent_forms(id):
    if 'UserName' not in session or 'CustomerID' not in session:
        return "<h1><center>Error: view_rent_forms</center><br>⚠️Admin credentials are incomplete. Access Denied.⚠️<a href='/Customer_LogIn'>Log-In</a></h1>"
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        # Modify the SQL query to select from tbl_customer_info
        cursor.execute("""
            SELECT car_list.*, tbl_customer_info.*
            FROM car_list
            INNER JOIN tbl_customer_info ON car_list.CarNo = tbl_customer_info.CarNo
            WHERE car_list.CarNo = %s AND  tbl_customer_info.Status = 'Ongoing';
        """, id)

        # Fetch all rows
        rows = cursor.fetchall()

        if rows:
            return render_template('Car_Rental_Form.html', rows=rows)
        else:
            cursor.execute("SELECT * FROM car_list WHERE CarNo=%s", id)

            # Fetch all rows
            rows = cursor.fetchall()

            if rows:
                return render_template('Car_Rental_Form.html', rows=rows)
    except Exception as e:
        print(e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# =====================================  POST METHOD to Save New Customer Record
@app.route('/save_rental_Info', methods=['POST'])
def save_rental_Info():
    conn = None
    cursor = None
    try:
        #GET USER INPUTS txtCarName Id_Image
        strstatus = 'Ongoing'
        strCustomerID = request.form['txtCustomerID']
        strCarName = request.form['txtCarName']
        strCarNo = request.form['txtCarNo']
        strIdImage = request.form['txtvalid_IdImage']
        strCusLName = request.form['txtCusLName']
        strCusFName = request.form['txtCusFName']
        strGender = request.form['cboCGender']
        strAge = request.form['txtCAge']
        strAddress = request.form['txtAddress']
        strEmailAdd = request.form['txtEmailAdd']
        strMobileNo = request.form['txtMobileNo']
        strPUpDate = request.form['txtPUpDate']
        strturnDate = request.form['returnDate']
        strPUpTime = request.form['txtPUpTime']
        strNoDayRent = request.form['txtNoDayRent']
        strcarPDay = request.form["cbocarPDay"]
        strPayPalId = request.form['txtpaypal_id']
        strDownPayment = request.form['txtPayPalDownPayment']

        dblAmountPay = (float(strcarPDay) * float(strNoDayRent))
        dblTotaltoPay = (float(dblAmountPay) - float(strDownPayment))

        if request.method == 'POST':
            #SAVE RECORD TO DATABASE
            sql = "INSERT INTO tbl_customer_info \
                     (id, Car_Name, CarNo, Last_Name, First_Name, Gender, Age, Address, Email_Address, Mobile_Number, Date_of_pickup, Date_of_return, Time_of_pickup, No_of_Days, Car_per_days, Transaction_ID, Amount_to_Pay, Down_Payment, Total_Amount_to_Pay, Status, Id_Image) \
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s , %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            data = (strCustomerID, strCarName, strCarNo, strCusLName, strCusFName, strGender, strAge,
                    strAddress, strEmailAdd, strMobileNo, strPUpDate, strturnDate, strPUpTime, strNoDayRent, strcarPDay, strPayPalId, dblAmountPay, strDownPayment, dblTotaltoPay, strstatus, strIdImage)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            return redirect('/car_list')
        else:
            return 'Error while adding user'
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

#=========================================  View Add Car Page
@app.route('/View_Admin_AddCar')
def View_Admin_AddCar():
    if 'Admin_UserName' not in session or 'AdminFirstName' not in session:
        return "<h1><center>Error: View_Admin_AddCar</center><br>⚠️Admin credentials are incomplete. Access Denied.⚠️<a href='/login_admin_view'>Log-In</a></h1>"
    else:
        return render_template('AddCar_carlist.html')

#========================================= Select Folder Path
UPLOAD_FOLDER_CAR_IMAGE = 'static/image'
app.config['UPLOAD_FOLDER_CAR_IMAGE'] = UPLOAD_FOLDER_CAR_IMAGE

#========================================= POST Add Car
@app.route('/save_addCar', methods=['GET', 'POST'])
def save_addCar():
    if request.method == 'POST':
        # Check if the 'imageUpload' file input field exists in the request
        if 'imageUpload' not in request.files:
            return "No file part"

        file = request.files['imageUpload']

        # Check if the file is empty
        if file.filename == '':
            return "No selected file"

        # Check if the file is allowed (e.g., only image files)
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}

        if not '.' in file.filename or file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
            return "Invalid file type"

        # Generate a unique filename for the uploaded file
        filename = secure_filename(file.filename)
        file_count = 1
        while os.path.exists(os.path.join(app.config['UPLOAD_FOLDER_CAR_IMAGE'], filename)):
            # File with the same name exists, add (1), (2), etc., to the filename
            filename = f"{os.path.splitext(file.filename)[0]}({file_count}){os.path.splitext(file.filename)[1]}"
            file_count += 1

        # Save the uploaded file with the unique filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER_CAR_IMAGE'], filename))

        strCarName = request.form['txtaddCarName']
        strCarPriceNoPromo = request.form['txtaddCarPriceNoPromo']
        CarPriceWithPromo = request.form['txtaddCarPriceWithPromo']

        # SAVE RECORD TO DATABASE
        sql = "INSERT INTO car_list \
                (Car_Name, Car_Price_NoPromo, Car_Price_WithPromo, Image) \
                VALUES (%s, %s, %s, %s)"
        data = (strCarName, strCarPriceNoPromo, CarPriceWithPromo, filename)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        flash(u'\u2705' '{} as been successfully add in car list.'.format(strCarName))
        return redirect('View_Admin_CarList')

#========================================  Admin View ALL Car List
@app.route('/View_Admin_CarList', methods=['GET', 'POST'])
def View_Admin_CarList():
    if 'Admin_UserName' not in session or 'AdminFirstName' not in session:
        return "<h1><center>Error: View_Admin_CarList</center><br>⚠️Admin credentials are incomplete. Access Denied.⚠️<a href='/login_admin_view'>Log-In</a></h1>"
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        if request.method == 'POST':
            search_query = request.form.get('Search')
            sql_query = "SELECT * FROM car_list WHERE Car_Name LIKE %s;"
            cursor.execute(sql_query, (f"%{search_query}%"))
            flash('You search for "{}"'.format(search_query))
        else:
            cursor.execute("SELECT * FROM car_list")

        rows = cursor.fetchall()
        return render_template('admin_view_carlist.html', rows=rows)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

#========================================  Admin View Car Info
@app.route('/View_Admin_CarInfo/<string:id>')
def View_Admin_CarInfo(id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM car_list WHERE CarNo=%s", id)
        row = cursor.fetchone()
        if row:
            return render_template('View_Admin_CarInfo.html', row=row)

        else:
            return 'Error loading #{id}'.format(id=id)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

#========================================  Admin View Edit Car Info
@app.route('/View_Edit_CarInfo/<string:id>')
def View_Edit_CarInfo(id):
    if 'Admin_UserName' not in session or 'AdminFirstName' not in session:
        return "<h1><center>Error: View_Edit_CarInfo</center><br>⚠️Admin credentials are incomplete. Access Denied.⚠️<a href='/login_admin_view'>Log-In</a></h1>"
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM car_list WHERE CarNo=%s", id)
        row = cursor.fetchone()
        if row:
            return render_template('Edit_Car_Info.html', row=row)

        else:
            return 'Error loading #{id}'.format(id=id)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

#========================================  Admin POST Edit Car Price
@app.route('/editcarprice', methods=['POST'])
def editcarprice():
    conn = None
    cursor = None
    try:
        # GET USER INPUTS
        strCarNo = request.form['txtCarNo']
        streditCarName = request.form['txteditCarName']
        streditCarPriceNoPromo = request.form['txteditCarPriceNoPromo']
        streditCarPriceWithPromo = request.form['txteditCarPriceWithPromo']


        if request.method == 'POST':
            # SAVE RECORD TO DATABASE
            sql = "UPDATE car_list SET \
                   Car_Price_NoPromo=%s, Car_Price_WithPromo=%s \
                   WHERE CarNo=%s"
            data = (streditCarPriceNoPromo, streditCarPriceWithPromo, strCarNo)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            flash('Car "{}" as been successfully change the Price!'.format(streditCarName))
            return redirect('/View_Admin_CarList')
        else:
            return 'Error while updating user'
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


#========================================  Admin Delete Car and Car Picture
@app.route('/delete_cars/<string:id>')
def delete_cars(id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT Image FROM car_list WHERE CarNo=%s", (id,))
        image_name = cursor.fetchone()[0]  # Retrieve the image name

        cursor.execute("DELETE FROM car_list WHERE CarNo=%s", (id,))
        conn.commit()

        # Delete the image file
        image_path = os.path.join(app.root_path, 'static/image', image_name)
        if os.path.exists(image_path):
            os.remove(image_path)
            flash('Car {} as been delete'.format(id))
        else:
            flash('Car # {} has been deleted, but its image was not found'.format(id))

        return redirect('/View_Admin_CarList')
    except Exception as e:
        print(e)
        flash('Error occurred during deletion')
        return redirect('/View_Admin_CarList')
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

#======================================== Change Admin Username And pass
@app.route('/changeadmin', methods=['POST'])
def changeadmin():
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        # GET USER INPUTS
        streoldpassword = request.form['oldpassword']
        strchangeusername = request.form['changeusername']
        strchangepassword = request.form['changepassword']

        if request.method == 'POST':
            # UPDATE RECORD IN DATABASE
            cursor.execute("SELECT * FROM adminlogin_info WHERE Admin_Password=%s", (streoldpassword,))
            result = cursor.fetchone()
            if result:
                # If the password is found in the database
                sql = "UPDATE adminlogin_info SET Admin_UserName=%s, Admin_Password=%s WHERE Admin_Password=%s"
                data = (strchangeusername, strchangepassword, streoldpassword)
                cursor.execute(sql, data)
                conn.commit()
                flash('Admin credentials have been successfully updated!')
                return redirect('/AdminLogout')  # Redirect to the logout route
            else:
                # If the password is not found in the database
                flash('Your old password is wrong.')
                return redirect('/View_Admin_CarList')  # You might want to redirect to the same route to try again
        else:
            return 'Error while updating user'
    except mysql.connector.Error as e:
        print(e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

#======================================== Add Admin
@app.route('/add_admin', methods=['POST'])
def add_admin():
    conn = None
    cursor = None
    try:
        #GET USER INPUTS
        straddadminFname = request.form['addadminFname']
        straddadminLname = request.form['addadminLname']
        straddadminusername = request.form['addadminusername']
        straddadminpassword = request.form['addadminpassword']
        stradminposition = request.form['adminposition']

        if request.method == 'POST':
            #SAVE RECORD TO DATABASE
            sql = "INSERT INTO adminlogin_info \
                   (AdminFirstName, AdminLastName, Admin_UserName, Admin_Password, AdminPosition) \
                    VALUES(%s, %s, %s, %s, %s)"
            data = (straddadminFname, straddadminLname, straddadminusername, straddadminpassword, stradminposition)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            flash('Admin with username "{}" as been successfully add admin list'.format(straddadminusername))
            return redirect('/AdminLogout')  # Redirect to the logout route
        else:
            return 'Error while adding admin'
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()



if __name__ == "__main__":
    app.run()

