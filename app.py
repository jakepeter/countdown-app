from flask import Flask, render_template, request
from datetime import datetime, date

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    birth_date_str = request.form['birth_date']
    birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()

    today = date.today()

    # 生きた日数
    age_in_days = (today - birth_date).days

    # 100歳までの日数
    hundred_years = birth_date.replace(year=birth_date.year + 100)
    remaining_days = (hundred_years - today).days

    # 100歳までの残り秒数（残り日数×86400秒）
    remaining_seconds = remaining_days * 86400

    return render_template('result.html',
                           birth_date=birth_date_str,
                           today=today.strftime('%Y-%m-%d'),
                           age_in_days=age_in_days,
                           remaining_seconds=remaining_seconds)

if __name__ == '__main__':
    app.run(debug=True)
