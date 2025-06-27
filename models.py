from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Student(db.Model):
    __tablename__ = 'students'  # Define the table name explicitly

    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(15), unique=True, nullable=False)
    address = db.Column(db.String(255), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)  # Updated to match the Rooms class

    # Optional: Add relationship for easy access
    room = db.relationship('Room', backref='students')


class Room(db.Model):
    __tablename__ = 'rooms'  # Define the table name explicitly

    id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.String(50), unique=True, nullable=False)
    bed_type = db.Column(db.String(50), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)

    # Optional: Add relationship for easy access
    payments = db.relationship('Payment', backref='room', lazy=True)


class Payment(db.Model):
    __tablename__ = 'payments'  # Define the table name explicitly

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    payment_date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), nullable=False)

    # Optional: Add relationship for easy access
    student = db.relationship('Student', backref='payments')


class Visitor(db.Model):
    __tablename__ = 'visitors'  # Define the table name explicitly

    id = db.Column(db.Integer, primary_key=True)
    visitor_name = db.Column(db.String(100), nullable=False)
    visit_date = db.Column(db.Date, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    relationship = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)

    # Optional: Add relationship for easy access
    student = db.relationship('Student', backref='visitors')
