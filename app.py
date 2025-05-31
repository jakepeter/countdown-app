from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime, date

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # フラッシュメッセージ用に必要

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    birth_date_str = request.form['birth_date']

    # 日付の形式をチェック
    try:
        birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
    except ValueError:
        flash("誕生日は YYYY-MM-DD の形式で入力してください。")
        return redirect(url_for('index'))

    today = date.today()

    # 生きた日数
    age_in_days = (today - birth_date).days

    # 100歳までの日数
    try:
        hundred_years = birth_date.replace(year=birth_date.year + 100)
    except ValueError:
        # 2月29日の例外処理（うるう年で100年後に存在しない日）
        hundred_years = birth_date + (date(birth_date.year + 100, 3, 1) - date(birth_date.year, 3, 1))

    remaining_days = (hundred_years - today).days
    remaining_seconds = remaining_days * 86400

    return render_template('result.html',
                           birth_date=birth_date_str,
                           today=today.strftime('%Y-%m-%d'),
                           age_in_days=age_in_days,
                           remaining_seconds=remaining_seconds)

if __name__ == '__main__':
    app.run(debug=True)
