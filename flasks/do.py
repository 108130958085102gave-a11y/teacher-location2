from datetime import datetime
from flask import Flask, jsonify, render_template, request, session # type: ignore


app = Flask(__name__)
app.secret_key = 'school_location_secret_key'


# データベース（メモリ上）
teachers_db = {
    'sato': {
        'pass': 'pass123',
        'name': '佐藤 健一',
        'subject': '数学',
        'room': '1F-職員室',
        'status': '在室',
        'note': '15時以降質問受付けます',
        'floor': 1,
    },
    'suzuki': {
        'pass': 'pass123',
        'name': '鈴木 美咲',
        'subject': '英語',
        'room': '2F-2A教室',
        'status': '授業中',
        'note': '2A 英語コミⅠ',
        'floor': 2,
    },
    'takahashi': {
        'pass': 'pass123',
        'name': '高橋 誠',
        'subject': '国語',
        'room': '1F-職員室',
        'status': '在室',
        'note': '明日の講習準備中',
        'floor': 1,
    },
    'tanaka': {
        'pass': 'pass123',
        'name': '田中 恵子',
        'subject': '理科(化学)',
        'room': '3F-理科実験室',
        'status': '在室',
        'note': '実験室にいます',
        'floor': 3,
    },
    'ito': {
        'pass': 'pass123',
        'name': '伊藤 雄太',
        'subject': '体育',
        'room': '1F-体育館',
        'status': '授業中',
        'note': '体育館でバスケ指導',
        'floor': 1,
    },
    'watanabe': {
        'pass': 'pass123',
        'name': '渡辺 裕子',
        'subject': '社会(日本史)',
        'room': '2F-進路指導室',
        'status': '離席',
        'note': '16:00面談予定',
        'floor': 2,
    },
    'kobayashi': {
        'pass': 'pass123',
        'name': '小林 隆',
        'subject': '情報',
        'room': '3F-PC教室',
        'status': '在室',
        'note': 'PC室キー開放中',
        'floor': 3,
    },
    'kato': {
        'pass': 'pass123',
        'name': '加藤 直樹',
        'subject': '数学',
        'room': '校外',
        'status': '出張',
        'note': '県立教育センター出張',
        'floor': 1,
    },
    'yamamoto': {
        'pass': 'pass123',
        'name': '山本 さくら',
        'subject': '音楽',
        'room': '3F-音楽室',
        'status': '授業中',
        'note': '合唱練習指導',
        'floor': 3,
    },
    'nakamura': {
        'pass': 'pass123',
        'name': '中村 慎太郎',
        'subject': '美術',
        'room': '1F-美術室',
        'status': '在室',
        'note': '作品点検中',
        'floor': 1,
    },
}


room_database = [
    # --- 教室棟２階 ---
    {
        'id': '1F-H科',
        'name': 'H科',
        'floor': 1,
        'x': 68,       # 左からの位置
        'y': 25,       # 上からの位置
        'width': 100,  # 部屋の横幅
        'height': 120, # 部屋の縦幅
    },
    {
        'id': '1F-G科',
        'name': 'G科',
        'floor': 1,
        'x': 316,
        'y': 25,
        'width': 88,
        'height': 120,
    },
    {
        'id': '1F-F科',
        'name': 'F科',
        'floor': 1,
        'x': 406,
        'y': 25,
        'width': 88,
        'height': 120,
    },
    {
        'id': '1F-I科',
        'name': 'I科',
        'floor': 1,
        'x': 496,
        'y': 25,
        'width': 88,
        'height': 120,
    },
    {
        'id': '1F-M科',
        'name': 'M科',
        'floor': 1,
        'x': 585,
        'y': 25,
        'width': 88,
        'height': 120,
    },
    {
        'id': '1F-学年職員室',
        'name': '学年職員室',
        'floor': 1,
        'x': 837,
        'y': 25,
        'width': 145,
        'height': 300,
    },
    {
        'id': '1F-選択教室',
        'name': '選択教室',
        'floor': 1,
        'x': 15,
        'y': 25,
        'width': 52,
        'height': 300,
    },
   
    # --- 2階・3階データ（省略せずに既存のものを下に続けてください）---


# --- 東実習棟2階 ---
    {
        'id': '2F-コンピュータ1',
        'name': 'コンピュータ❶',
        'floor': 2,
        'x': 0,
        'y': 0,
        'width': 117,
        'height': 350,
    },
    {
        'id': '2F-情報科学実習室',
        'name': '情報科学実習室',
        'floor': 2,
        'x': 196,
        'y': 0,
        'width': 258,
        'height': 138,
    },
    {
        'id': '2F-コンピュータ制御実習室',
        'name': 'コンピュータ制御実習室',
        'floor': 2,
        'x': 454,
        'y': 0,
        'width': 171,
        'height': 138,
    },
    {
        'id': '2F-映像作成室',
        'name': '映像作成室',
        'floor': 2,
        'x': 625,
        'y': 0,
        'width': 105,
        'height': 138,
    },
    {
        'id': '2F-CAD実習室',
        'name': 'CAD実習室',
        'floor': 2,
        'x': 859,
        'y': 0,
        'width': 141,
        'height': 350,
    },
    {
        'id': '2F-コンピュータ2',
        'name': 'コンピュータ❷',
        'floor': 2,
        'x': 187,
        'y': 227,
        'width': 267,
        'height': 123,
    },
    {
        'id': '2F-コンピュータ3',
        'name': 'コンピュータ❸',
        'floor': 2,
        'x': 454,
        'y': 227,
        'width': 185,
        'height': 123,
    },
    {
        'id': '2F-総合準備室',
        'name': '総合準備室',
        'floor': 2,
        'x': 639,
        'y': 227,
        'width': 130,
        'height': 123,
    },
    {
        'id': '2F-デジタル技術実習室',
        'name': 'デジタル技術実習室',
        'floor': 2,
        'x': 769,
        'y': 227,
        'width': 90,
        'height': 123,
    },
   # --- 東実習棟3階 ---
    {
        'id': '3F-工作工事実習室1',
        'name': '工作工事実習室❶',
        'floor': 3,
        'x': 26,
        'y': 0,
        'width': 112,
        'height': 150,
    },
    {
        'id': '3F-電気機器実習室',
        'name': '電気機器実習室',
        'floor': 3,
        'x': 199,
        'y': 0,
        'width': 252,
        'height': 138,
    },
    {
        'id': '3F-コンピュータ室4',
        'name': 'コンピュータ室❹',
        'floor': 3,
        'x': 451,
        'y': 0,
        'width': 272,
        'height': 138,
    },
    {
        'id': '3F-ネットワーク1',
        'name': 'ネットワーク❶',
        'floor': 3,
        'x': 846,
        'y': 0,
        'width': 128,
        'height': 200,
    },
    {
        'id': '3F-工作工事実習室2',
        'name': '工作工事実習室❷',
        'floor': 3,
        'x': 26,
        'y': 150,
        'width': 112,
        'height': 200,
    },
    {
        'id': '3F-計測実習室1',
        'name': '計測実習室❶',
        'floor': 3,
        'x': 138,
        'y': 225,
        'width': 204,
        'height': 125,
    },
    {
        'id': '3F-計測実習室2',
        'name': '計測実習室❷',
        'floor': 3,
        'x': 342,
        'y': 225,
        'width': 177,
        'height': 125,
    },
    {
        'id': '3F-CADCAM実習室',
        'name': 'CAD CAM実習室',
        'floor': 3,
        'x': 519,
        'y': 225,
        'width': 172,
        'height': 125,
    },
    {
        'id': '3F-デザイン実習室',
        'name': 'デザイン実習室',
        'floor': 3,
        'x': 691,
        'y': 225,
        'width': 155,
        'height': 125,
    },
    {
        'id': '3F-ネットワーク2',
        'name': 'ネットワーク❷',
        'floor': 3,
        'x': 846,
        'y': 200,
        'width': 128,
        'height': 150,
    },
  # --- 管理棟1階
    {
        'id': '管理1F-校長室',
        'name': '校長室',
        'floor': 4,
        'x': 15,
        'y': 6,
        'width': 118,
        'height': 142,
    },
    {
        'id': '管理1F-応接室',
        'name': '応接室',
        'floor': 4,
        'x': 134,
        'y': 6,
        'width': 91,
        'height': 142,
    },
    {
        'id': '管理1F-事務室',
        'name': '事務室',
        'floor': 4,
        'x': 15,
        'y': 206,
        'width': 151,
        'height': 133,
    },
    {
        'id': '管理1F-倉庫',
        'name': '倉庫',
        'floor': 4,
        'x': 168,
        'y': 206,
        'width': 39,
        'height': 133,
    },
    {
        'id': '管理1F-進路指導室',
        'name': '進路指導室',
        'floor': 4,
        'x': 286,
        'y': 206,
        'width': 126,
        'height': 133,
    },
    {
        'id': '管理1F-教材室',
        'name': '教材室',
        'floor': 4,
        'x': 414,
        'y': 206,
        'width': 41,
        'height': 133,
    },
    {
        'id': '管理1F-印刷室',
        'name': '印刷室',
        'floor': 4,
        'x': 456,
        'y': 206,
        'width': 107,
        'height': 133,
    },
    {
        'id': '管理1F-職員室',
        'name': '職員室',
        'floor': 4,
        'x': 565,
        'y': 206,
        'width': 247,
        'height': 133,
    },
    {
        'id': '管理1F-保健室',
        'name': '保健室',
        'floor': 4,
        'x': 813,
        'y': 206,
        'width': 101,
        'height': 133,
    },


    # --- 管理棟2階
    {
        'id': '管理2F-図書室',
        'name': '図書室',
        'floor': 5,
        'x': 16,
        'y': 6,
        'width': 213,
        'height': 200,
    },
    {
        'id': '管理2F-司書室',
        'name': '司書室',
        'floor': 5,
        'x': 123,
        'y': 210,
        'width': 106,
        'height': 133,
    },
    {
        'id': '管理2F-第2食物準備室',
        'name': '第2食物準備室',
        'floor': 5,
        'x': 310,
        'y': 210,
        'width': 63,
        'height': 133,
    },
    {
        'id': '管理2F-第2食物実習室',
        'name': '第2食物実習室',
        'floor': 5,
        'x': 375,
        'y': 210,
        'width': 184,
        'height': 133,
    },
    {
        'id': '管理2F-理科実験準備室',
        'name': '理科実験準備室',
        'floor': 5,
        'x': 561,
        'y': 210,
        'width': 86,
        'height': 133,
    },
    {
        'id': '管理2F-理科実験室',
        'name': '理科実験室',
        'floor': 5,
        'x': 649,
        'y': 210,
        'width': 161,
        'height': 133,
    },
    {
        'id': '管理2F-生徒会室',
        'name': '生徒会室',
        'floor': 5,
        'x': 812,
        'y': 210,
        'width': 98,
        'height': 133,
    },
]
@app.route('/')
def index():
  return render_template('index.html')


# API: 教員一覧・部屋一覧データ取得（パスワードは除外して送信）
@app.route('/api/data', methods=['GET'])
def get_data():
  safe_teachers = {
      tid: {k: v for k, v in info.items() if k != 'pass'}
      for tid, info in teachers_db.items()
  }
  return jsonify({
      'teachers': safe_teachers,
      'rooms': room_database,
      'currentUser': session.get('user'),
  })


# API: ログイン処理
@app.route('/api/login', methods=['POST'])
def login():
  data = request.json
  role = data.get('role')

  if role == 'student':
    student_id = data.get('student_id', '').strip()
    name = f'{student_id}（生徒）' if student_id else '生徒ユーザー'
    session['user'] = {'role': 'student', 'id': student_id or 'student', 'name': name}
    return jsonify({'success': True, 'user': session['user']})

  elif role == 'teacher':
    teacher_id = data.get('teacher_id', '').strip()
    password = data.get('password', '').strip()
    teacher = teachers_db.get(teacher_id)

    if teacher and teacher['pass'] == password:
      session['user'] = {
          'role': 'teacher',
          'id': teacher_id,
          'name': teacher['name'],
      }
      return jsonify({'success': True, 'user': session['user']})
    else:
      return (
          jsonify({
              'success': False,
              'message': 'IDまたはパスワードが正しくありません。',
          }),
          401,
      )


# API: ログアウト処理
@app.route('/api/logout', methods=['POST'])
def logout():
  session.clear()
  return jsonify({'success': True})


# API: ステータス更新処理
@app.route('/api/update', methods=['POST'])
def update():
  user = session.get('user')
  if not user or user.get('role') != 'teacher':
    return (
        jsonify({'success': False, 'message': '権限がありません。'}),
        403,
    )

  data = request.json
  teacher_id = user.get('id')
  teacher = teachers_db.get(teacher_id)

  if teacher:
    teacher['status'] = data.get('status', teacher['status'])
    new_room = data.get('room', teacher['room'])
    teacher['room'] = new_room
    teacher['note'] = data.get('note', '')

    room_info = next((r for r in room_database if r['id'] == new_room), None)
    if room_info:
      teacher['floor'] = room_info['floor']
    elif new_room == '校外':
      teacher['floor'] = 1

    return jsonify({'success': True, 'teacher': teacher})

  return jsonify({'success': False, 'message': '教員が見つかりません。'}), 404


# API: パスワード変更処理（新規追加）
@app.route('/api/change_password', methods=['POST'])
def change_password():
  user = session.get('user')
  if not user or user.get('role') != 'teacher':
    return jsonify({'success': False, 'message': '権限がありません。'}), 403

  data = request.json
  current_pass = data.get('current_password', '').strip()
  new_pass = data.get('new_password', '').strip()

  if not new_pass:
    return jsonify({'success': False, 'message': '新しいパスワードを入力してください。'}), 400

  teacher_id = user.get('id')
  teacher = teachers_db.get(teacher_id)

  if not teacher:
    return jsonify({'success': False, 'message': '教員が見つかりません。'}), 404

  if teacher['pass'] != current_pass:
    return jsonify({'success': False, 'message': '現在のパスワードが正しくありません。'}), 401

  teacher['pass'] = new_pass
  return jsonify({'success': True, 'message': 'パスワードを変更しました。'})


if __name__ == '__main__':
  app.run(debug=True, port=5000)