from flask import Flask, render_template, request
from datetime import datetime, timedelta
import pytz

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    birth_date_str = request.form['birth_date']
    
    # ユーザーの入力（日付8桁）を日付型に変換
    try:
        birth_date = datetime.strptime(birth_date_str, '%Y%m%d').date()
    except ValueError:
        return "日付の形式が正しくありません。例：19780804"

    # 日本時間の現在日時を取得
    jst = pytz.timezone('Asia/Tokyo')
    now_jst = datetime.now(jst)
    today = now_jst.date()

    # 生きた日数
    age_in_days = (today - birth_date).days

    # 100歳になる日
    try:
        hundred_years = birth_date.replace(year=birth_date.year + 100)
    except ValueError:
        # うるう年などで日付が無効な場合（例：2月29日）
        hundred_years = birth_date + timedelta(days=36525)  # おおよそ100年

    # 残り日数と秒数
    remaining_days = (hundred_years - today).days
    remaining_seconds = remaining_days * 86400

    return render_template('result.html',
                           birth_date=birth_date.strftime('%Y-%m-%d'),
                           today=today.strftime('%Y-%m-%d'),
                           age_in_days=age_in_days,
                           remaining_seconds=remaining_seconds)

if __name__ == '__main__':
    app.run(debug=True)
