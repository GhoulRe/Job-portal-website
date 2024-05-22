import secrets
from flask import Flask, render_template, jsonify, request, redirect, url_for, flash, session
from database import load_jobs_from_db, load_work_from_db, add_application_to_db, load_applications_from_db, add_user_to_db, get_user_by_email, add_job_to_db
from werkzeug.security import check_password_hash

app = Flask(__name__)

def generate_secret_key(length=32):
    return secrets.token_hex(length)

secret_key = generate_secret_key()
app.secret_key = secret_key

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        if get_user_by_email(email):
            flash('Email already registered', 'danger')
        else:
            add_user_to_db(email, password, role)
            flash('Registration successful', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = get_user_by_email(email)
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['user_email'] = user['email']
            session['user_role'] = user['role']
            flash('Login successful', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template('login.html')


@app.route("/logout")
def logout():
    session.pop('user_id', None)
    session.pop('user_email', None)
    session.pop('user_role', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))


@app.route("/")
def home():
    if 'user_id' not in session:  # Check if user is not logged in
        return redirect(url_for('login'))  # Redirect to login page
    else:
        jobs = load_jobs_from_db()
        return render_template('home.html', jobs=jobs)
      
@app.route("/")
def hello_world():
  jobs = load_jobs_from_db()
  return render_template('home.html', jobs=jobs)

@app.route("/add_job", methods=['POST'])
def add_job():
    if 'user_id' not in session or session.get('user_role') != 'admin':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('login'))

    title = request.form['title']
    location = request.form['location']
    salary = request.form['salary']
    currency = request.form['currency']
    responsibilities = request.form['responsibilities']
    requirements = request.form['requirements']

    add_job_to_db(title, location, salary, currency, responsibilities, requirements)
    flash('Job added successfully!', 'success')
    return redirect(url_for('home'))


@app.route("/api/jobs")
def list_jobs():
  jobs = load_jobs_from_db()
  return jsonify(jobs)


@app.route("/applications")
def list_applications():
  applications = load_applications_from_db()
  return render_template('all_applications.html', applications=applications)


@app.route("/job/<id>")
def show_job(id):
  job = load_work_from_db(id)
  if not job:
    return "Not Found", 404
  return render_template('jobpage.html', job=job)


@app.route("/api/job/<id>")
def show_job_json(id):
  job = load_work_from_db(id)
  return jsonify(job)


@app.route("/job/<id>/apply", methods=['post'])
def apply_to_jobs(id):
  data = request.form
  job = load_work_from_db(id)
  add_application_to_db(id, data)
  return render_template('application_submitted.html',
                         application=data,
                         job=job)

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
