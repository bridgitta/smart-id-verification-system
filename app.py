import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS ids (
            id_number TEXT PRIMARY KEY,
            name TEXT,
            dob TEXT,
            father TEXT,
            mother TEXT,
            place TEXT,
            date_added TEXT
        )
    ''')
    conn.close()

init_db()

from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Use environment variable in production

# Database helper
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/verify', methods=['POST'])
def verify():
    id_number = request.form['id_number']
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM ids WHERE id_number = ?', (id_number,)).fetchone()
    conn.close()

    if user:
        return render_template('result.html', user=user)
    else:
        flash('Invalid ID card')
        return redirect(url_for('index'))

from flask import Flask, render_template, request, redirect, url_for, session, flash

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # ✅ Valid login
        if username == 'admin' and password == 'admin123':
            session['admin'] = True
            return redirect(url_for('dashboard'))
        
        # ❌ Invalid login
        flash("Invalid credentials. Please try again.", "danger")
        return redirect(url_for('admin_login'))  # ✅ This fixes your issue

    return render_template('admin_login.html')


@app.route('/dashboard')
def dashboard():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))

    show = request.args.get('show')
    records = []

    if show == '1':
        conn = get_db_connection()
        records = conn.execute('SELECT * FROM ids').fetchall()
        conn.close()

    return render_template('dashboard.html', records=records)


from datetime import datetime, timedelta

@app.route('/add', methods=['GET', 'POST'])
def add_record():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        id_number = request.form['id_number']
        name = request.form['name']
        dob = request.form['dob']
        father = request.form['father']
        mother = request.form['mother']
        place = request.form['place']
        date_added = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        try:
            dob_date = datetime.strptime(dob, '%Y-%m-%d')
            today = datetime.today()
            ten_years_ago = today - timedelta(days=365 * 10)

            if dob_date >= today:
                flash('Date of Birth cannot be today or in the future.')
                return redirect(url_for('add_record'))

            if dob_date > ten_years_ago:
                flash('Date of Birth must be at least 10 years ago.')
                return redirect(url_for('add_record'))

        except ValueError:
            flash('Invalid date format.')
            return redirect(url_for('add_record'))

        conn = get_db_connection()
        existing_record = conn.execute('SELECT * FROM ids WHERE id_number = ?', (id_number,)).fetchone()

        if existing_record:
            flash('ID number already exists. Please use a unique ID number.')
            conn.close()
            return redirect(url_for('add_record'))

        data = (id_number, name, dob, father, mother, place, date_added)
        conn.execute(
            'INSERT INTO ids (id_number, name, dob, father, mother, place, date_added) VALUES (?, ?, ?, ?, ?, ?, ?)',
            data
        )
        conn.commit()
        conn.close()

        flash('Record added successfully.')
        return redirect(url_for('dashboard', show=1))

    # 👇 Limit the calendar in the frontend too
    today = datetime.today()
    min_date = datetime(1900, 1, 1).strftime('%Y-%m-%d')  # Optional: set earliest possible DOB
    max_date = (today - timedelta(days=365 * 10)).strftime('%Y-%m-%d')  # Max allowed = 10 years ago

    return render_template('add_record.html', min_date=min_date, max_date=max_date)



@app.route('/report')
def report():
    search_id = request.args.get('search_id', '')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    if search_id:
        cursor.execute("SELECT * FROM records WHERE status='Validated' AND id_number LIKE ?", ('%' + search_id + '%',))
    else:
        cursor.execute("SELECT * FROM records WHERE status='Validated'")

    records = cursor.fetchall()
    total = len(records)

    conn.close()
    return render_template('report.html', records=records, total=total, search_id=search_id)


@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('index'))

@app.route('/print/<id_number>')
def print_record(id_number):
    if not session.get('admin'):
        return redirect(url_for('admin_login'))

    conn = get_db_connection()
    record = conn.execute('SELECT * FROM ids WHERE id_number = ?', (id_number,)).fetchone()
    conn.close()

    if not record:
        flash("Record not found.")
        return redirect(url_for('dashboard', show=1))

    return render_template('print_record.html', record=record)


if __name__ == '__main__':
    app.run(debug=True)
