from flask import Flask, render_template, jsonify

app = Flask(__name__)

JOBS = [
    {
        'ID': 1,
        'Title': 'Data Analyst',
        'Location': 'Bengaluru, India',
        'Salary': 'Rs. 10,00,000'
    },
    {
        'ID': 2,
        'Title': 'Frontend Engineer',
        'Location': 'Remote',
    },
    {
        'ID': 3,
        'Title': 'Backend Engineer',
        'Location': 'San Fransisco, USA  ',
        'Salary': '$120,000'
    },
    {
        'ID': 4,
        'Title': 'Data Analyst',
        'Location': 'Bengaluru, India',
        'Salary': 'Rs. 10,00,000'
    },
    {
        'ID': 4,
        'Title': 'Data Scientist',
        'Location': 'Delhi, India',
        'Salary': 'Rs. 15,00,000'
    },
]


@app.route("/")
def hello_world():
  return render_template('home.html', jobs=JOBS)


@app.route("/api/jobs")
def list_jobs():
  return jsonify(JOBS)


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
