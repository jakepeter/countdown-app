from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    birth_date_str = request.form['birth_date']
    birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d')

    today = datetime.now()

    hundred_years_later = birth_date.replace(year=birth_date.year + 100)
    remaining_time = hundred_years_later - today

    age_in_days = (today - birth_date).days
    remaining_days = remaining_time.days
    remaining_hours = int(remaining_time.total_seconds() // 3600)
    remaining_seconds = int(remaining_time.total_seconds())

    return render_template('result.html',
                           birth_date=birth_date_str,
                           today=today.strftime('%Y-%m-%d'),
                           age_in_days=age_in_days,
                           remaining_days=remaining_days,
                           remaining_hours=remaining_hours,
                           remaining_seconds=remaining_seconds)

if __name__ == '__main__':
    app.run(debug=True)
