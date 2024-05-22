from sqlalchemy import create_engine, text
from werkzeug.security import generate_password_hash, check_password_hash
import os

db_connection_string = os.environ['DB_CONNECTION_STRING2']

engine = create_engine(db_connection_string)


def load_jobs_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("select * from JOBS"))
    jobs = []
    for row in result.all():
      jobs.append(row._asdict())
  return jobs

def load_work_from_db(id):
  with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM JOBS WHERE id = :val"),
                          {'val': id})
    row = result.fetchone()
    if row:
      return row._asdict()
    else:
      return None


# def add_application_to_db(job_id, data):
#   with engine.connect() as conn:
#     query = text(
#       "INSERT INTO applications (job_id, full_name, email, linkedin_url, education, experience, resume_url) VALUES (:job_id, :full_name, :email, :linkedin_url, :education, :experience, :resume_url)"
#     )
#     conn.execute(query,
#              job_id=job_id,
#              full_name=data['full_name'],
#              email=data['email'],
#              # linkedin_url=data['linkedin_url'],
#              education=data['education'],
#              work_experience=data['experience'],
#              resume_url=data['resume_url'])

def add_application_to_db(job_id, data):
  with engine.connect() as conn:
      query = text("INSERT INTO applications (job_id, full_name, email, linkedin_url, education, work_experience, resume_url) VALUES (:job_id, :full_name, :email, :linkedin_url, :education, :work_experience, :resume_url)")

      params = {
          'job_id': job_id,
          'full_name': data['full_name'],
          'email': data['email'],
          'linkedin_url': data['linkedin_url'],
          'education': data['education'],
          'work_experience': data['work_experience'],
          'resume_url': data['resume_url']
      }

      result = conn.execute(query, params)
      # Commit the transaction
      conn.commit()
      return result

def load_applications_from_db():
  with engine.connect() as conn:
      result = conn.execute(text("SELECT * FROM applications"))
      applications = []
      for row in result.all():
          applications.append(row._asdict())
      print(applications)  # This will print the applications after they have been added to the list
      return applications

def add_user_to_db(email, password, role):
  hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
  with engine.connect() as conn:
      query = text("INSERT INTO users (email, password, role) VALUES (:email, :password, :role)")
      conn.execute(query, {'email': email, 'password': hashed_password, 'role': role})
      conn.commit()

def get_user_by_email(email):
  with engine.connect() as conn:
      result = conn.execute(text("SELECT * FROM users WHERE email = :email"), {'email': email})
      row = result.fetchone()
      return row._asdict() if row else None

def add_job_to_db(title, location, salary, currency, responsibilites, requirements):
  with engine.connect() as conn:
      query = text(
          "INSERT INTO JOBS (title, location, salary, currency, responsibilites, requirements) "
          "VALUES (:title, :location, :salary, :currency, :responsibilites, :requirements)"
      )
      conn.execute(query, {
          'title': title,
          'location': location,
          'salary': salary,
          'currency': currency,
          'responsibilites': responsibilites,
          'requirements': requirements
      })
      conn.commit()