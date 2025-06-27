import dbm
import mysql.connector
from mysql.connector import Error
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',  # Change if your DB is hosted elsewhere
            user='root',
            password='Sam@2004',  # Use your password
            database='hostel_management'  # Your database name
        )
        if connection.is_connected():
            print("Connected to MySQL database")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Sam@2004'
app.config['MYSQL_DB'] = 'hostel_management'

mysql = MySQL(app)

@app.route('/test_db')
def test_db():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT DATABASE();")
        database = cursor.fetchone()
        cursor.close()
        return f"Connected to database: {database[0]}"
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    default_username = 'Samartha'
    default_password = '2004'
    if username == default_username and password == default_password:
        session['loggedin'] = True
        return redirect(url_for('dashboard'))
    else:
        flash('Invalid credentials')
        return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM students")
        students = cur.fetchall()
        cur.execute("SELECT * FROM rooms")
        rooms = cur.fetchall()
        cur.execute("SELECT * FROM payments")
        payments = cur.fetchall()
        cur.execute("SELECT * FROM visitors")
        visitors = cur.fetchall()
        cur.close()
        return render_template('dashboard.html', students=students, rooms=rooms, payments=payments, visitors=visitors)
    return redirect(url_for('login'))

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        student_name = request.form['student_name']
        dob = request.form['dob']
        email = request.form['email']
        phone_number = request.form['phone_number']
        address = request.form['address']
        room_id = request.form['room_id']
        try:
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO students (student_name, dob, email, phone_number, address, room_id) VALUES (%s, %s, %s, %s, %s, %s)',
                        (student_name, dob, email, phone_number, address, room_id))
            mysql.connection.commit()
            cur.close()
            flash('Student added successfully!', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            flash(f"Error adding student: {str(e)}", 'danger')
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM rooms')
    rooms = cur.fetchall()
    cur.close()
    return render_template('add_student.html')

@app.route('/add_room', methods=['GET', 'POST'])
def add_room():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        room_id = request.form['room_id']
        bed_type = request.form['bed_type']
        capacity = request.form['capacity']
        try:
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO rooms (room_id, bed_type, capacity) VALUES (%s, %s, %s)',
                        (room_id, bed_type, capacity))
            mysql.connection.commit()
            cur.close()
            flash('Room added successfully!', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            flash(f"Error adding room: {str(e)}", 'danger')
    return render_template('add_room.html')

@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        student_id = request.form['student_id']
        amount = request.form['amount']
        payment_date = request.form['payment_date']
        try:
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO payments (student_id, amount, payment_date) VALUES (%s, %s, %s)',
                        (student_id, amount, payment_date))
            mysql.connection.commit()
            cur.close()
            flash('Payment recorded successfully!', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            flash(f"Error recording payment: {str(e)}", 'danger')
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM students')
    students = cur.fetchall()
    cur.close()
    return render_template('payment.html')

@app.route('/visitor', methods=['GET', 'POST'])
def visitor():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        visitor_name = request.form['visitor_name']
        visit_date = request.form['visit_date']
        student_id = request.form['student_id']
        try:
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO visitors (visitor_name, visit_date, student_id) VALUES (%s, %s, %s)',
                        (visitor_name, visit_date, student_id))
            mysql.connection.commit()
            cur.close()
            flash('Visitor recorded successfully!', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            flash(f"Error recording visitor: {str(e)}", 'danger')
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM students')
    students = cur.fetchall()
    cur.close()
    return render_template('visitor.html')


@app.route('/update_all')
def update_all():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    return render_template('update_all.html')

@app.route('/delete_all')
def delete_all():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    return render_template('delete_all.html')

@app.route('/update_student', methods=['GET', 'POST'])
def update_student():
    if request.method == 'POST':
        student_id = request.form['student_id']  # Assuming form field still called student_id for the input, but it refers to 'id' in DB
        new_name = request.form.get('new_name')
        new_dob = request.form.get('new_dob')
        new_email = request.form.get('new_email')
        new_phone_number = request.form.get('new_phone_number')
        new_address = request.form.get('new_address')
        new_room_id = request.form.get('new_room_id')

        cur = mysql.connection.cursor()

        updates = []
        values = []

        # Add values to the update query if they are provided
        if new_name:
            updates.append("student_name = %s")
            values.append(new_name)
        if new_dob:
            updates.append("dob = %s")
            values.append(new_dob)
        if new_email:
            updates.append("email = %s")
            values.append(new_email)
        if new_phone_number:
            updates.append("phone_number = %s")
            values.append(new_phone_number)
        if new_address:
            updates.append("address = %s")
            values.append(new_address)
        if new_room_id:
            updates.append("room_id = %s")
            values.append(new_room_id)

        if updates:
            sql = "UPDATE students SET " + ', '.join(updates) + " WHERE id = %s;"
            values.append(student_id)  # Append the student_id at the end for WHERE clause
            
            try:
                # Execute the update query with values
                cur.execute(sql, tuple(values))
                mysql.connection.commit()
                flash('Student updated successfully!', 'success')
            except Exception as e:
                print(f"SQL Error: {e}")
                flash(f"Error updating student: {str(e)}", 'danger')
            finally:
                cur.close()

        return redirect(url_for('dashboard'))
    return render_template('update_student.html')



@app.route('/update_room', methods=['GET', 'POST'])
def update_room():
    if request.method == 'POST':
        room_id = request.form['room_id']
        new_bed_type = request.form.get('new_bed_type')
        new_capacity = request.form.get('new_capacity')

        cur = mysql.connection.cursor()

        # Prepare SQL query
        updates = []
        if new_bed_type:
            updates.append("bed_type = %s")
        if new_capacity:
            updates.append("capacity = %s")

        if updates:
            sql = "UPDATE rooms SET " + ', '.join(updates) + " WHERE room_id = %s;"
            try:
                cur.execute(sql, (*[v for v in (new_bed_type, new_capacity, room_id) if v is not None],))
                mysql.connection.commit()
                flash('Room updated successfully!', 'success')
            except Exception as e:
                flash(f"Error updating room: {str(e)}", 'danger')
            finally:
                cur.close()

        return redirect(url_for('dashboard'))  # Redirect to avoid form resubmission

    return render_template('update_room.html')
@app.route('/update_payment', methods=['GET', 'POST'])
def update_payment():
    if request.method == 'POST':
        payment_id = request.form['payment_id']
        student_id = request.form.get('student_id')
        new_amount = request.form.get('amount')  # Updated to 'amount' to match the form
        new_date = request.form.get('payment_date')  # Updated to 'payment_date' to match the form

        cur = mysql.connection.cursor()

        # Build the list of updates
        updates = []
        params = []

        if new_amount:
            updates.append("amount = %s")
            params.append(new_amount)
        if student_id:
            updates.append("student_id = %s")
            params.append(student_id)
        if new_date:
            updates.append("payment_date = %s")  # Correct column name is payment_date
            params.append(new_date)

        # Only proceed if there are updates
        if updates:
            # Add the payment_id to the parameter list for the WHERE clause
            sql = "UPDATE payments SET " + ', '.join(updates) + " WHERE id = %s"
            params.append(payment_id)

            try:
                # Execute the query with the parameters
                cur.execute(sql, tuple(params))
                mysql.connection.commit()
                flash('Payment updated successfully!', 'success')
            except Exception as e:
                flash(f"Error updating payment: {str(e)}", 'danger')
            finally:
                cur.close()

        return redirect(url_for('dashboard'))

    return render_template('update_payment.html')




@app.route('/update_visitor', methods=['GET', 'POST'])
def update_visitor():
    if request.method == 'POST':
        visitor_id = request.form['visitor_id']
        visitor_name = request.form['visitor_name']
        visit_date = request.form['visit_date']

        cur = mysql.connection.cursor()

        # Prepare SQL query
        updates = []
        values = []

        if visitor_name:
            updates.append("visitor_name = %s")
            values.append(visitor_name)
        if visit_date:
            updates.append("visitor_date = %s")
            values.append(visit_date)
        
        # Add the visitor_id for the WHERE clause
        values.append(visitor_id)

        if updates:
            sql = "UPDATE visitors SET " + ', '.join(updates) + " WHERE id = %s;"
            try:
                cur.execute(sql, tuple(values))
                mysql.connection.commit()
                flash('Visitor information updated successfully!', 'success')
            except Exception as e:
                flash(f"Error updating visitor information: {str(e)}", 'danger')
            finally:
                cur.close()

        return redirect(url_for('dashboard'))  # Redirect to avoid form resubmission

    return render_template('update_visitor.html')

@app.route('/delete_student', methods=['GET', 'POST'])
def delete_student():
    if request.method == 'POST':
        student_id = request.form['student_id']

        cur = mysql.connection.cursor()

        # Prepare SQL query to delete the visitor
        sql = "DELETE FROM students WHERE id = %s;"
        try:
            cur.execute(sql, (student_id,))
            mysql.connection.commit()
            flash('Student deleted successfully!', 'success')
        except Exception as e:
            flash(f"Error deleting student: {str(e)}", 'danger')
        finally:
            cur.close()

        return redirect(url_for('dashboard'))  # Redirect to avoid form resubmission

    return render_template('delete_student.html')  # Make sure this matches your HTML file name



@app.route('/delete_room', methods=['GET', 'POST'])
def delete_room():
    if request.method == 'POST':
        room_id = request.form['room_id']

        cur = mysql.connection.cursor()

        # Prepare SQL query to delete the room
        sql = "DELETE FROM rooms WHERE room_id = %s;"
        try:
            cur.execute(sql, (room_id,))
            mysql.connection.commit()
            flash('Room deleted successfully!', 'success')
        except Exception as e:
            flash(f"Error deleting room: {str(e)}", 'danger')
        finally:
            cur.close()

        return redirect(url_for('dashboard'))  # Redirect to avoid form resubmission

    return render_template('delete_room.html')



@app.route('/delete_payment', methods=['GET', 'POST'])
def delete_payment():
    if request.method == 'POST':
        payment_id = request.form['payment_id']

        cur = mysql.connection.cursor()

        # Prepare SQL query to delete the visitor
        sql = "DELETE FROM payments WHERE id = %s;"
        try:
            cur.execute(sql, (payment_id,))
            mysql.connection.commit()
            flash('Payment deleted successfully!', 'success')
        except Exception as e:
            flash(f"Error deleting payments: {str(e)}", 'danger')
        finally:
            cur.close()

        return redirect(url_for('dashboard'))  # Redirect to avoid form resubmission

    return render_template('delete_payment.html')  # Make sure this matches your HTML file name




@app.route('/delete_visitor', methods=['GET', 'POST'])
def delete_visitor():
    if request.method == 'POST':
        visitor_id = request.form['visitor_id']

        cur = mysql.connection.cursor()

        # Prepare SQL query to delete the visitor
        sql = "DELETE FROM visitors WHERE id = %s;"
        try:
            cur.execute(sql, (visitor_id,))
            mysql.connection.commit()
            flash('Visitor deleted successfully!', 'success')
        except Exception as e:
            flash(f"Error deleting visitor: {str(e)}", 'danger')
        finally:
            cur.close()

        return redirect(url_for('dashboard'))  # Redirect to avoid form resubmission

    return render_template('delete_visitor.html')  # Make sure this matches your HTML file name



@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
