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
    target_age_str = request.form.get('target_age', '100')  # デフォルト100歳

    # ユーザーの入力（日付8桁）を日付型に変換
    try:
        birth_date = datetime.strptime(birth_date_str, '%Y%m%d').date()
    except ValueError:
        return "日付の形式が正しくありません。例：19780804"

    # 何歳まで生きるか（数字）を取得
    try:
        target_age = int(target_age_str)
        if not (1 <= target_age <= 150):
            return "年齢は1〜150の範囲で入力してください。"
    except ValueError:
        return "年齢は数字で入力してください。"

    # 日本時間の現在日時を取得（offset-aware）
    jst = pytz.timezone('Asia/Tokyo')
    now_jst = datetime.now(jst)
    today = now_jst.date()

    # 生きた日数
    age_in_days = (today - birth_date).days

    # 目標年齢になる日付（offset-naiveなdate）
    try:
        target_date = birth_date.replace(year=birth_date.year + target_age)
    except ValueError:
        # うるう年対応（例：2月29日）
        target_date = birth_date + timedelta(days=365 * target_age + target_age // 4)

    # offset-naiveなdatetimeを作成（目標日の午前0時）
    target_naive = datetime.combine(target_date, datetime.min.time())

    # JSTのタイムゾーン情報を付与（offset-awareに変換）
    target_aware = jst.localize(target_naive)

    # 残り時間の差分を計算（offset-aware同士）
    remaining_timedelta = target_aware - now_jst
    if remaining_timedelta.total_seconds() < 0:
        remaining_timedelta = timedelta(0)

    remaining_seconds = int(remaining_timedelta.total_seconds())
    remaining_days = remaining_timedelta.days

    return render_template('result.html',
                           birth_date=birth_date.strftime('%Y-%m-%d'),
                           today=today.strftime('%Y-%m-%d'),
                           age_in_days=age_in_days,
                           remaining_seconds=remaining_seconds,
                           remaining_days=remaining_days,
                           target_age=target_age)

if __name__ == '__main__':
    app.run(debug=True)
