from sqlalchemy import create_engine, text
import os

db_connection_string = os.environ['DB_CONNECTION_STRING']

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
  result = conn.execute(text("select * from applications"))
  applications = []
  for row in result.all():
    applications.append(row._asdict()) 
    return applications