import io
import pandas as pd
import flask_login
from flask import Blueprint, render_template, request, flash, redirect, url_for, send_file
from .models import User, Customer, Student
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect Password, Try Again', category='error')
        else:
            flash('email does not exist', category='error')

    # data=request.form
    # print(data)
    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already in use.', category='error')

        elif len(email) < 4:
            flash('Email must be greater than 4 characters', category='error')
        elif len(firstName) < 2:
            flash('Email must be greater than 1 characters', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match', category='error')
        elif len(password1) < 7:
            flash('Password must be atleast 7 characters', category='error')
        else:
            new_user = User(email=email, firstName=firstName,
                            password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account Created.', category='success')
            return redirect(url_for('views.home'))

    return render_template("signup.html", user=current_user)


@auth.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    return "<p>This is the Home Page</p>"


@auth.route('/hourbasic', methods=['GET', 'POST'])
@login_required
def hourBasic():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    if request.method == 'POST':
        name = request.form.get('name')
        time = request.form.get('time')
        price = request.form.get('price')
        category = request.form.get('category')
        payment_type = request.form.get('payment')
        current_datetime = datetime.now()

        if name == "":
            flash('Name can not be empty', category='error')
        elif time == "":
            flash('Time can not be empty', category='error')
        elif price == "":
            flash('Price can not be empty', category='error')
        elif category == "" or category is None:
            flash('Category can not be empty', category='error')
        elif payment_type == "" or payment_type is None:
            flash('Payment Type can not be empty', category='error')
        else:
            new_customer = Customer(name=name, time=time, price=price, category=category, payment=payment_type)
            db.session.add(new_customer)
            db.session.commit()

            bill_number = new_customer.id

            flash('Bill Created', category='success')
            return render_template('displayinfo.html', name=name, time=time, price=price, category=category,
                                   payment=payment_type, current_datetime=current_datetime,
                                   user=current_user, bill_number=bill_number)
    return render_template("hourbasic.html", user=current_user)


@auth.route('/admission', methods=['GET', 'POST'])
@login_required
def admission():
    if request.method == 'POST':
        name = request.form.get('name')
        days = request.form.get('days')
        totalprice = request.form.get('totalprice')
        remainprice = request.form.get('remainprice')
        paidprice = request.form.get('paidprice')
        category = request.form.get('category')
        payment = request.form.get('payment')
        course = request.form.get('course')
        current_datetime = datetime.now()

        if name == "":
            flash('Name can not be empty', category='error')
        elif days == "":
            flash('Days can not be empty', category='error')
        elif totalprice=="":
            flash('Total Price can not be empty', category='error')
        elif paidprice == "":
            flash('Paid Price can not be empty', category='error')
        elif category=="" or category is None:
            flash('Category can not be empty', category='error')
        elif payment=="" or payment is None:
            flash('Payment can not be empty', category='error')
        elif course=="" or course is None:
            flash('Course can not be empty', category='error')
        else:
            new_student = Student(name=name, days=days, totalprice=totalprice, remainprice=remainprice, paidprice=paidprice,
                                  category=category,
                                  payment=payment, course=course)
            db.session.add(new_student)
            db.session.commit()

            bill_number = new_student.id

            flash('Student Registered', category='success')
            return render_template('admissiondisplayinfo.html', name=name, days=days, totalprice=totalprice,
                                   remainprice=remainprice, paidprice=paidprice,
                                   category=category, payment=payment, course=course, current_datetime=current_datetime,
                                   user=current_user, bill_number=bill_number)
    return render_template("admission.html", user=current_user)


@auth.route('/registeredlist', methods=['GET', 'POST'])
@login_required
def registeredList():
    search_query = request.form.get('search')  # Get the search query from the form
    if search_query:
        students = Student.query.filter(Student.name.ilike(f'%{search_query}%')).all()
    else:
        students = Student.query.all()
    return render_template("registeredlist.html", students=students, user=current_user, search_query=search_query)


@auth.route('/hourbasiclist', methods=['GET', 'POST'])
@login_required
def hourbasicList():
    search_query = request.form.get('search')  # Get the search query from the form
    if search_query:
        customer = Customer.query.filter(Customer.name.ilike(f'%{search_query}%')).all()
    else:
        customer = Customer.query.all()
    return render_template("hourbasiclist.html", customer=customer, user=current_user, search_query=search_query)

#
# @auth.route('/download_hourbasic', methods=['GET', 'POST'])
# def download_hourbasic():
#     # Get the current date
#     today = datetime.today().strftime('%Y-%m-%d')
#
#     # Query the database to get the entries for today
#     customers = Customer.query.filter(Customer.date == today).all()
#
#     # Create a DataFrame from the data
#     data = {
#         'Bill No.': [customer.id for customer in customers],
#         'Name': [customer.name for customer in customers],
#         'Time': [customer.time for customer in customers],
#         'Price': [customer.price for customer in customers],
#         'Payment': [customer.payment for customer in customers],
#         'Category': [customer.category for customer in customers]
#     }
#     df = pd.DataFrame(data)
#
#     # Create a BytesIO buffer and save the DataFrame as an Excel file
#     output = io.BytesIO()
#     writer = pd.ExcelWriter(output, engine='xlsxwriter')
#     df.to_excel(writer, index=False, sheet_name='Hour Basic List')
#     writer.save()
#     output.seek(0)
#
#     # Send the file to the user
#     return send_file(output, attachment_filename=f'Hour_Basic_List_{today}.xlsx', as_attachment=True)
