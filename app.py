from flask import Flask, render_template, request
from datetime import datetime, date

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    birth_date_str = request.form['birth_date']
    
    # 入力は8桁の数字（例：19780804）として処理
    try:
        birth_date = datetime.strptime(birth_date_str, '%Y%m%d').date()
    except ValueError:
        return "入力形式が正しくありません。8桁の数字（例：19780804）で入力してください。"

    today = date.today()

    # 生きた日数
    age_in_days = (today - birth_date).days

    # 100歳までの日数
    try:
        hundred_years = birth_date.replace(year=birth_date.year + 100)
    except ValueError:
        # うるう年（2月29日など）の調整
        hundred_years = birth_date.replace(month=3, day=1, year=birth_date.year + 100)

    remaining_days = (hundred_years - today).days
    remaining_seconds = remaining_days * 86400

    return render_template('result.html',
                           birth_date=birth_date.strftime('%Y-%m-%d'),
                           today=today.strftime('%Y-%m-%d'),
                           age_in_days=age_in_days,
                           remaining_seconds=remaining_seconds)

if __name__ == '__main__':
    app.run(debug=True)
