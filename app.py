from flask import Flask, render_template, request, Response
import sqlite3
import time
import os
import random
import cv2
import bodydetect
import json

app = Flask(__name__)
conn = sqlite3.connect('old_care.sqlite', check_same_thread=False)
cur_id = 0


class VideoCamera1(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        bodydetect.detect_fall(image)
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()


class VideoCamera2(object):
    def __init__(self):
        self.video = cv2.VideoCapture('./camera2.mp4')

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()


class VideoCamera3(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()


class VideoCamera4(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()


class VideoCamera5(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()


class camera(object):
    def __init__(self):
        self.frames = [open(f + '.jpg', 'rb').read() for f in ['1', '2', '3']]
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed1')
def video_feed1():
    return Response(gen(VideoCamera1()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def columns(table_name):
    if table_name == 'oldperson_info':
        return ['id', 'usernamee', 'gender', 'phone', 'id_card', 'birthday', 'checkin_date', 'checkout_date',
                'imgset_dir'
            , 'profile_photo', 'room_number', 'firstguardian_name', 'firstguardian_relationship', 'firstguardian_phone'
            , 'firstguardian_wechat', 'secondguardian_name', 'secondguardian_relationship', 'secondguardian_phone'
            , 'secondguardian_wechat', 'health_state', 'DESCRIPTION', 'ISACTIVE', 'CREATED', 'CREATEDBY', 'UPDATED'
            , 'UPDATEDBY', 'REMOVE']
    elif table_name == 'employee_info':
        return ['id', 'username', 'gender', 'phone', 'id_card', 'birthday', 'hire_date', 'resign_date', 'imgset_dir',
                'profile_photo', 'DESCRIPTION', 'ISACTIVE', 'CREATED', 'CREATEDBY', 'UPDATED', 'UPDATEDBY', 'REMOVE']
    elif table_name == 'volunteer_info':
        return ['id', 'name', 'gender', 'phone', 'id_card', 'birthday', 'checkin_date', 'checkout_date', 'imgset_dir'
            , 'profile_photo', 'DESCRIPTION', 'ISACTIVE', 'CREATED', 'CREATEDBY', 'UPDATED'
            , 'UPDATEDBY', 'REMOVE']
    elif table_name == 'event_info':
        return ['id', 'event_type', 'event_date', 'event_location', 'event_desc', 'oldperson_id']
    elif table_name == 'sys_user':
        return ['ID', 'UserName', 'Password', 'REAL_NAME', 'SEX', 'EMAIL', 'PHONE', 'MOBILE', 'DESCRIPTION', 'ISACTIVE',
                'CREATED', 'CREATEDBY', 'UPDATED', 'UPDATEDBY', 'REMOVE', 'DATAFILTER', 'theme', 'defaultpage',
                'logoimage', 'qqopenid', 'appversion', 'jsonauth']
    else:
        print("表名不对")
        return 0


def insert(conn, table_name, value):  # 通用表格插入操作
    cols = columns(table_name)
    if cols != 0:
        sql_insert = "INSERT INTO " + table_name + "("
        for k, v in value.items():
            if v:
                sql_insert += k
                sql_insert += ','
        sql_insert = sql_insert[:-1]
        sql_insert += ')VALUES('
        for k, v in value.items():
            if v:
                sql_insert += '\''
                sql_insert += v
                sql_insert += '\''
                sql_insert += ','
        sql_insert = sql_insert[:-1]
        sql_insert += ')'
        # print(sql_insert)
        conn.execute(sql_insert)
        conn.commit()


def delete(conn, table_name, where):
    sql_delete = "DELETE FROM " + table_name + " WHERE " + where + ";"
    conn.execute(sql_delete)
    conn.commit()
    # print(sql_delete)


def update(conn, table_name, set, where):
    sql_update = "UPDATE " + table_name + " SET " + set
    if where != "":
        sql_update = sql_update + " WHERE " + where
    sql_update = sql_update + ";"
    print(sql_update)
    conn.execute(sql_update)
    conn.commit()


def select(conn, table_name, where):
    cols = columns(table_name)
    if cols != 0:
        sql_select = "SELECT * FROM " + table_name
        if where != "":
            sql_select = sql_select + " WHERE " + where
        sql_select = sql_select + ";"
        print(sql_select)
        curs = conn.execute(sql_select)
        return list(curs)


def login(conn, name, password):
    # 用户登录
    where = 'UserName = \'' + name + '\' and Password = \'' + password + '\''
    table_name = 'sys_user'
    l1 = select(conn, table_name, where)
    if len(l1) == 0:
        return 0
    else:
        global cur_id
        cur_id = l1[0][0]
        print(cur_id)
        return 1


def zhuce(conn, info):
    # 用户注册
    table_name = 'sys_user'
    where = 'UserName = \'' + info['UserName'] + '\''
    l = select(conn, table_name, where)
    if len(l) == 0:
        t = time.strftime('%Y-%m-%d', time.localtime())
        value = info
        value['CREATED'] = str(t)
        insert(conn, table_name, value)
        return 1
    else:
        return 0


def person_info(conn, uid, info):
    # 完善个人信息
    table_name = 'sys_user'
    set = ''
    for k, v in info.items():
        if v:
            set = set + k + '= \'' + str(v) + '\','
    t = time.strftime('%Y-%m-%d', time.localtime())
    set = set + 'UPDATED = \'' + str(t) + '\''
    where = 'id = \'' + str(uid) + '\''
    update(conn, table_name, set, where)
    return 1


def zhuxiao(conn, name):
    # 用户注销
    table_name = 'sys_user'
    if name:
        where = 'UserName = \'' + name + '\''
        delete(conn, table_name, where)
        return 1
    else:
        return 0


def add_elder(conn, info):
    # 新增老人
    table_name = 'oldperson_info'
    where = 'username = \'' + info['username'] + '\''
    l = select(conn, table_name, where)
    if len(l) == 0:
        t = time.strftime('%Y-%m-%d', time.localtime())
        value = info
        value['CREATED'] = str(t)
        insert(conn, table_name, value)
        return 1
    else:
        return 0


def elder_info(conn, uid, info):
    # 完善个人信息
    table_name = 'oldperson_info'
    set = ''
    for k, v in info.items():
        if v:
            set = set + k + '= \'' + str(v) + '\','
    t = time.strftime('%Y-%m-%d', time.localtime())
    set = set + 'UPDATED = \'' + str(t) + '\''
    where = 'id = \'' + str(uid) + '\''
    update(conn, table_name, set, where)


def del_elder(conn, uid):
    table_name = 'oldperson_info'
    where = 'ID = \'' + str(uid) + '\''
    delete(conn, table_name, where)
    return 1


def add_employee(conn, info):
    table_name = 'employee_info'
    where = 'username = \'' + info['username'] + '\''
    l = select(conn, table_name, where)
    if len(l) == 0:
        t = time.strftime('%Y-%m-%d', time.localtime())
        value = info
        value['CREATED'] = str(t)
        insert(conn, table_name, value)
        return 1
    else:
        return 0


def emp_info(conn, uid, info):
    # 完善个人信息
    table_name = 'employee_info'
    set = ''
    for k, v in info.items():
        if v:
            set = set + k + '= \'' + str(v) + '\','
    t = time.strftime('%Y-%m-%d', time.localtime())
    set = set + 'UPDATED = \'' + str(t) + '\''
    where = 'id = \'' + str(uid) + '\''
    update(conn, table_name, set, where)
    return 1


def del_employee(conn, uid):
    table_name = 'employee_info'
    where = 'ID = \'' + str(uid) + '\''
    delete(conn, table_name, where)
    return 1


def add_volunteer(conn, info):
    table_name = 'volunteer_info'
    where = 'name = \'' + info['name'] + '\''
    l = select(conn, table_name, where)
    if len(l) == 0:
        t = time.strftime('%Y-%m-%d', time.localtime())
        value = info
        value['CREATED'] = str(t)
        insert(conn, table_name, value)
        return 1
    else:
        return 0


def vol_info(conn, uid, info):
    # 完善个人信息
    table_name = 'volunteer_info'
    set = ''
    for k, v in info.items():
        if v:
            set = set + k + '= \'' + str(v) + '\','
    t = time.strftime('%Y-%m-%d', time.localtime())
    set = set + 'UPDATED = \'' + str(t) + '\''
    where = 'id = \'' + str(uid) + '\''
    update(conn, table_name, set, where)
    return 1


def del_volunteer(conn, uid):
    table_name = 'volunteer_info'
    where = 'ID = \'' + str(uid) + '\''
    delete(conn, table_name, where)
    return 1


def sel_old(conn, id):
    table_name = 'oldperson_info'
    where = 'id = \'' + id + '\''
    s = select(conn, table_name, where)
    info = {'id': s[0][0], 'username': s[0][1], 'gender': s[0][2], 'phone': s[0][3], 'id_card': s[0][4],
            'birthday': s[0][5], 'checkin_date': s[0][6], 'checkout_date': s[0][7], 'imgset_dir': s[0][8],
            'profile_photo': s[0][9], 'room_number': s[0][10], 'firstguardian_name': s[0][11],
            'firstguardian_relationship': s[0][12], 'firstguardian_phone': s[0][13], 'firstguardian_wechat': s[0][14],
            'secondguardian_name': s[0][15], 'secondguardian_relationship': s[0][16], 'secondguardian_phone': s[0][17]
        , 'secondguardian_wechat': s[0][18], 'health_state': s[0][19], 'DESCRIPTION': s[0][20], 'ISACTIVE': s[0][21],
            'CREATED': s[0][22], 'CREATEDBY': s[0][23], 'UPDATED': s[0][24]
        , 'UPDATEDBY': s[0][25], 'REMOVE': s[0][26]}
    info = json.dumps(info)
    return info


def sel_emp(conn, id):
    table_name = 'employee_info'
    where = 'id = \'' + id + '\''
    s = select(conn, table_name, where)
    info = {'id': s[0][0], 'username': s[0][1], 'gender': s[0][2], 'phone': s[0][3], 'id_card': s[0][4],
            'birthday': s[0][5], 'hire_date': s[0][6], 'resign_date': s[0][7], 'imgset_dir': s[0][8],
            'profile_photo': s[0][9], 'DESCRIPTION': s[0][10], 'ISACTIVE': s[0][11],
            'CREATED': s[0][12], 'CREATEDBY': s[0][13], 'UPDATED': s[0][14]
        , 'UPDATEDBY': s[0][15], 'REMOVE': s[0][16]}
    info = json.dumps(info)
    return info


def sel_vol(conn, id):
    table_name = 'volunteer_info'
    where = 'id = \'' + id + '\''
    s = select(conn, table_name, where)
    info = {'id': s[0][0], 'name': s[0][1], 'gender': s[0][2], 'phone': s[0][3], 'id_card': s[0][4],
            'birthday': s[0][5], 'checkin_date': s[0][6], 'checkout_date': s[0][7], 'imgset_dir': s[0][8],
            'profile_photo': s[0][9], 'DESCRIPTION': s[0][10], 'ISACTIVE': s[0][11],
            'CREATED': s[0][12], 'CREATEDBY': s[0][13], 'UPDATED': s[0][14]
        , 'UPDATEDBY': s[0][15], 'REMOVE': s[0][16]}
    info = json.dumps(info)
    return info


@app.route('/')
def login1():
    return render_template('/htmls/login.html')


@app.route('/toregister', methods=['GET', 'POST'])
def toregister():
    return render_template('/htmls/register.html')


@app.route('/tomodifypassword')
def tomodifypassword():
    return render_template('/htmls/modify_password.html')


@app.route('/tologin1')
def tologin1():
    return render_template('/htmls/login.html')


@app.route('/toprofile', methods=['GET', 'POST'])
def toprofile():
    return render_template('/htmls/profile.html')


@app.route('/tomain', methods=['GET', 'POST'])
def tomain():
    return render_template('/htmls/index.html')


@app.route('/toselectevent', methods=['GET', 'POST'])
def toselectevent():
    return render_template('/htmls/select_event.html')


@app.route('/toaddold', methods=['GET', 'POST'])
def toaddold():
    return render_template('/htmls/add_old.html')


@app.route('/toselectold', methods=['GET', 'POST'])
def toselectold():
    return render_template('/htmls/select_old.html')


@app.route('/tomodifyold', methods=['GET', 'POST'])
def tomodifyold():
    table_name = 'oldperson_info'
    s = select(conn, table_name, "")
    info = []
    for x in s:
        info.append({'id': x[0], 'username': x[1], 'gender': x[2], 'roomnum': x[10]})
    info = json.dumps(info)
    return render_template('/htmls/modify_old.html', info=info)


@app.route('/toanalyzeold', methods=['GET', 'POST'])
def toanalyzeold():
    return render_template('/htmls/analyze_old.html')


@app.route('/toaddworker', methods=['GET', 'POST'])
def toaddworker():
    return render_template('/htmls/add_worker.html')


@app.route('/toselectworker', methods=['GET', 'POST'])
def toselectworker():
    return render_template('/htmls/select_worker.html')


@app.route('/tomodifyworker', methods=['GET', 'POST'])
def tomodifyworker():
    table_name = 'employee_info'
    s = select(conn, table_name, "")
    info = []
    for x in s:
        info.append({'id': x[0], 'username': x[1], 'gender': x[2], 'phone': x[3]})
    info = json.dumps(info)
    return render_template('/htmls/modify_worker.html', info=info)


@app.route('/toanalyzeworker', methods=['GET', 'POST'])
def toanalyzeworker():
    return render_template('/htmls/analyze_worker.html')


@app.route('/toaddvolunteer', methods=['GET', 'POST'])
def toaddvolunteer():
    return render_template('/htmls/add_volunteer.html')


@app.route('/toselectvolunteer', methods=['GET', 'POST'])
def toselectvolunteer():
    return render_template('/htmls/select_volunteer.html')


@app.route('/tomodifyvolunteer', methods=['GET', 'POST'])
def tomodifyvolunteer():
    table_name = 'volunteer_info'
    s = select(conn, table_name, "")
    info = []
    for x in s:
        info.append({'id': x[0], 'name': x[1], 'gender': x[2], 'phone': x[3]})
    info = json.dumps(info)
    return render_template('/htmls/modify_volunteer.html', info=info)


@app.route('/toanalyzevolunteer', methods=['GET', 'POST'])
def toanalyzevolunteer():
    return render_template('/htmls/analyze_volunteer.html')


@app.route('/tooldtable', methods=['GET', 'POST'])
def tooldtable():
    return render_template('/htmls/old_table.html')


@app.route('/toworkertable', methods=['GET', 'POST'])
def toworkertable():
    return render_template('/htmls/worker_table.html')


@app.route('/tovolunteertable', methods=['GET', 'POST'])
def tovolunteertable():
    return render_template('/htmls/volunteer_table.html')


@app.route('/toeventtable', methods=['GET', 'POST'])
def toeventtable():
    return render_template('/htmls/event_table.html')


@app.route('/tooldinfo', methods=['GET', 'POST'])
def tooldinfo():
    return render_template('/htmls/old_info.html')


@app.route('/tomanagertable', methods=['GET', 'POST'])
def tomanagertable():
    return render_template('/htmls/manager_table.html')


@app.route('/tomonitor1', methods=['GET', 'POST'])
def tomonitor1():
    return render_template('/htmls/monitor1.html')


@app.route('/tomonitor2', methods=['GET', 'POST'])
def tomonitor2():
    return render_template('/htmls/monitor2.html')


@app.route('/tomonitor3', methods=['GET', 'POST'])
def tomonitor3():
    return render_template('/htmls/monitor3.html')


@app.route('/tomonitor4', methods=['GET', 'POST'])
def tomonitor4():
    return render_template('/htmls/monitor4.html')


@app.route('/tomonitor5', methods=['GET', 'POST'])
def tomonitor5():
    return render_template('/htmls/monitor5.html')


@app.route('/login0', methods=['GET', 'POST'])
def login0():
    form = request.form
    username = form.get('username')
    password = form.get('password')
    if not username:
        content = "请输入用户名"
        return render_template('/htmls/login.html', content=content)
    if not password:
        content = "请输入密码"
        return render_template('/htmls/login.html', content=content)
    global conn
    if login(conn, username, password):
        content = "登录成功"
        return render_template('/htmls/index.html', content=content)
    else:
        content = "用户名或密码错误"
        return render_template('/htmls/login.html', content=content)


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = request.form
    username = form.get('username')
    password = form.get('password')

    if not username:
        content = "请输入用户名"
        return render_template('/htmls/register.html', content=content)
    if not password:
        content = "请输入密码"
        return render_template('/htmls/register.html', content=content)
    global conn
    info = {'UserName': username, 'Password': password, 'REAL_NAME': form.get('REAL_NAME'), 'SEX': form.get('SEX'),
            'EMAIL': form.get('EMAIL'), 'PHONE': form.get('PHONE'), 'MOBILE': form.get('MOBILE')}
    if zhuce(conn, info):
        content = "注册成功"
        return render_template('/htmls/login.html', content=content)
    else:
        content = "用户名已存在"
        return render_template('/htmls/login.html', content=content)


@app.route('/pinfo', methods=['GET', 'POST'])
def pinfo():
    form = request.form
    info = {'REAL_NAME': form.get('REAL_NAME'), 'SEX': form.get('SEX'), 'PHONE': form.get('PHONE'),
            'MOBILE': form.get('MOBILE'), 'DESCRIPTION': form.get('DESCRIPTION'), 'ISACTIVE': form.get('ISACTIVE')}
    uid = form.get('id')
    if person_info(conn, uid, info):
        content = "用户信息更新成功"
    else:
        content = ''
    return render_template('pinfo.html', content=content)


@app.route('/signoff', methods=['GET', 'POST'])
def signoff():
    form = request.form
    username = form.get('username')
    if not username:
        content = "请输入用户名"
        return render_template('signoff.html', content=content)
    global conn
    if zhuxiao(conn, username):
        content = "注销成功"
        return render_template('signoff.html', content=content)
    else:
        content = "用户名不存在"
        return render_template('signoff.html', content=content)


@app.route('/addo', methods=['GET', 'POST'])
def addo():
    # 新增老人
    form = request.form
    if not form.get('username'):
        print("noname")
        content = "请输入用户名"
        return render_template('/htmls/add_old.html', content=content)
    info = {'username': form.get('username'), 'gender': form.get('gender'), 'phone': form.get('phone'),
            'id_card': form.get('id_card'),
            'birthday': form.get('birthday'), 'checkin_date': form.get("checkin_date"),
            'checkout_date': form.get('checkout_date'), 'profile_photo':
                form.get('profile_photo'), 'room_number': form.get('room_number'), 'firstguardian_name':
                form.get('firstguardian_name'), 'firstguardian_relationship': form.get('firstguardian_relationship'),
            'firstguardian_phone': form.get('firstguardian_phone'), 'firstguardian_wechat':
                form.get('firstguardian_wechat'), 'secondguardian_name':
                form.get('secondguardian_name'), 'secondguardian_relationship': form.get('secondguardian_relationship'),
            'secondguardian_phone': form.get('secondguardian_phone'), 'secondguardian_wechat':
                form.get('secondguardian_wechat'), 'health_state': form.get('health_state'),
            'DESCRIPTION': form.get('DESCRIPTION'), 'ISACTIVE': form.get('ISACTIVE')}
    global conn
    if add_elder(conn, info):
        content = "增添成功"
        return render_template('/htmls/index.html', content=content)
    else:
        content = "用户名已存在"
        return render_template('/htmls/index.html', content=content)


@app.route('/oinfo', methods=['POST', 'GET'])
def oinfo():
    form = request.form
    uid = form.get('id')
    info = {'gender': form.get('gender'), 'phone': form.get('phone'), 'id_card': form.get('id_card'),
            'birthday': form.get('birthday'), 'checkin_date': form.get("checkin_date"),
            'checkout_date': form.get('checkout_date'), 'profile_photo':
                form.get('profile_photo'), 'room_number': form.get('room_number'), 'firstguardian_name':
                form.get('firstguardian_name'), 'firstguardian_relationship': form.get('firstguardian_relationship'),
            'firstguardian_phone': form.get('firstguardian_phone'), 'firstguardian_wechat':
                form.get('firstguardian_wechat'), 'secondguardian_name':
                form.get('secondguardian_name'), 'secondguardian_relationship': form.get('secondguardian_relationship'),
            'secondguardian_phone': form.get('secondguardian_phone'), 'secondguardian_wechat':
                form.get('secondguardian_wechat'), 'health_state': form.get('health_state'),
            'DESCRIPTION': form.get('DESCRIPTION'), 'ISACTIVE': form.get('ISACTIVE')}
    if elder_info(conn, uid, info):
        content = "老人信息更新成功"
    else:
        content = ''
    return render_template('./htmls/add_old.html', content=content)


@app.route('/delo', methods=['GET', 'POST'])
def delo():
    form = request.form
    uid = form.get('uid')
    print(uid)
    if not uid:
        content = "请输入ID"
        return render_template('delo.html', content=content)
    global conn
    if del_elder(conn, uid):
        content = "删除成功"
        table_name = 'oldperson_info'
        s = select(conn, table_name, "")
        info = []
        for x in s:
            info.append({'id': x[0], 'username': x[1], 'gender': x[2], 'roomnum': x[10]})
        info = json.dumps(info)
        return render_template('/htmls/modify_old.html', info=info)
    else:
        content = "该id不存在"
        return render_template('delo.html', content=content)


@app.route('/selo', methods=['GET', 'POST'])
def selo():
    form = request.form
    id = form.get('id')
    content = sel_old(conn, id)
    if content:
        return render_template('/htmls/old_info.html', info=content)
    else:
        content = '该用户不存在'
        return render_template('/htmls/select_old.html', info=content)


@app.route('/selv', methods=['GET', 'POST'])
def selv():
    form = request.form
    id = form.get('id')
    content = sel_vol(conn, id)
    if content:
        return render_template('/htmls/volunteer_info.html', content=content)
    else:
        content = '该用户不存在'
        return render_template('/htmls/select_volunteer.html', content=content)


@app.route('/sele', methods=['GET', 'POST'])
def sele():
    form = request.form
    id = form.get('id')
    content = sel_emp(conn, id)
    if content:
        return render_template('/htmls/worker_info.html', content=content)
    else:
        content = '该用户不存在'
        return render_template('/htmls/select_worker.html', content=content)


@app.route('/adde', methods=['GET', 'POST'])
def adde():
    # 新增员工
    form = request.form
    if not form.get('username'):
        content = "请输入用户名"
        return render_template('/htmls/add_worker.html', content=content)
    info = {'username': form.get('username'), 'gender': form.get('gender'), 'phone': form.get('phone'),
            'id_card': form.get('id_card'),
            'birthday': form.get('birthday'), 'hire_date': form.get("hire_date"),
            'resign_date': form.get('resign_date'), 'profile_photo':
                form.get('profile_photo'), 'DESCRIPTION': form.get('DESCRIPTION'), 'ISACTIVE': form.get('ISACTIVE')}
    global conn
    if add_employee(conn, info):
        content = "增添成功"
        return render_template('/htmls/index.html', content=content)
    else:
        content = "用户名已存在"
        return render_template('/htmls/index.html', content=content)


@app.route('/einfo', methods=['GET', 'POST'])
def einfo():
    form = request.form
    uid = form.get('id')
    info = {'gender': form.get('gender'), 'phone': form.get('phone'), 'id_card': form.get('id_card'),
            'birthday': form.get('birthday'), 'hire_date': form.get("hire_date"),
            'resign_date': form.get('resign_date'), 'imgset_dir': form.get('imgset_dir'), 'profile_photo':
                form.get('profile_photo'), 'DESCRIPTION': form.get('DESCRIPTION'), 'ISACTIVE': form.get('ISACTIVE')}
    if emp_info(conn, uid, info):
        content = "员工信息更新成功"
    else:
        content = ''
    return render_template('einfo.html', content=content)


@app.route('/dele', methods=['GET', 'POST'])
def dele():
    form = request.form
    uid = form.get('uid')
    print(uid)
    if not uid:
        content = "请输入ID"
        return render_template('dele.html', content=content)
    global conn
    if del_employee(conn, uid):
        content = "删除成功"
        table_name = 'employee_info'
        s = select(conn, table_name, "")
        info = []
        for x in s:
            info.append({'id': x[0], 'username': x[1], 'gender': x[2], 'phone': x[3]})
        info = json.dumps(info)
        return render_template('/htmls/modify_worker.html', info=info)
    else:
        content = "该id不存在"
        return render_template('dele.html', content=content)


@app.route('/addv', methods=['GET', 'POST'])
def addv():
    # 新增志愿者
    form = request.form
    if not form.get('name'):
        content = "请输入用户名"
        return render_template('/htmls/add_volunteer.html', content=content)
    info = {'name': form.get('name'), 'gender': form.get('gender'), 'phone': form.get('phone'),
            'id_card': form.get('id_card'),
            'birthday': form.get('birthday'), 'checkin_date': form.get("checkin_date"),
            'checkout_date': form.get('checkout_date'), 'imgset_dir':
                form.get('imgset_dir'), 'DESCRIPTION': form.get('DESCRIPTION'), 'ISACTIVE': form.get('ISACTIVE')}
    global conn
    if add_volunteer(conn, info):
        content = "增添成功"
        return render_template('/htmls/index.html', content=content)
    else:
        content = "用户名已存在"
        return render_template('/htmls/index.html', content=content)


@app.route('/vinfo', methods=['GET', 'POST'])
def vinfo():
    form = request.form
    uid = form.get('id')
    info = {'gender': form.get('gender'), 'phone': form.get('phone'), 'id_card': form.get('id_card'),
            'birthday': form.get('birthday'), 'checkin_date': form.get("checkin_date"),
            'checkout_date': form.get('checkout_date'), 'imgset_dir': form.get('imgset_dir'), 'profile_photo':
                form.get('profile_photo'), 'DESCRIPTION': form.get('DESCRIPTION'), 'ISACTIVE': form.get('ISACTIVE')}
    if vol_info(conn, uid, info):
        content = "志愿者信息更新成功"
    else:
        content = ''
    return render_template('vinfo.html', content=content)


@app.route('/delv', methods=['GET', 'POST'])
def delv():
    form = request.form
    uid = form.get('uid')
    print(uid)
    if not uid:
        content = "请输入ID"
        return render_template('delv.html', content=content)
    global conn
    if del_volunteer(conn, uid):
        content = "删除成功"
        table_name = 'volunteer_info'
        s = select(conn, table_name, "")
        info = []
        for x in s:
            info.append({'id': x[0], 'name': x[1], 'gender': x[2], 'phone': x[3]})
        info = json.dumps(info)
        return render_template('/htmls/modify_volunteer.html', info=info)
    else:
        content = "该id不存在"
        return render_template('delv.html', content=content)


@app.route('/reto', methods=['GET', 'POST'])
def reto():
    table_name = 'oldperson_info'
    s = select(conn, table_name, "")
    info = []
    for x in s:
        info.append({'id': x[0], 'username': x[1], 'gender': x[2], 'roomnum': x[10]})
    info = json.dumps(info)
    return render_template('/htmls/select_old.html', info=info)


@app.route('/rete', methods=['GET', 'POST'])
def rete():
    table_name = 'employee_info'
    s = select(conn, table_name, "")
    info = []
    for x in s:
        info.append({'id': x[0], 'username': x[1], 'gender': x[2], 'phone': x[3]})
    info = json.dumps(info)
    return render_template('/htmls/select_worker.html', info=info)


@app.route('/retv', methods=['GET', 'POST'])
def retv():
    table_name = 'volunteer_info'
    s = select(conn, table_name, "")
    info = []
    for x in s:
        info.append({'id': x[0], 'name': x[1], 'gender': x[2], 'phone': x[3]})
    info = json.dumps(info)
    return render_template('/htmls/select_volunteer.html', info=info)


@app.route('/retev', methods=['GET', 'POST'])
def retev():
    table_name = 'event_info'
    s = select(conn, table_name, "")
    info = []
    for x in s:
        info.append({'id': x[0], 'event_type': x[1], 'event_date': x[2], 'event_location': x[3], 'event_desc': x[4],
                     'oldperson_id': x[5]})
    info = json.dumps(info)
    return render_template('/htmls/select_event.html', info=info)


@app.route('/images', methods=['GET', 'POST'])
def images():
    f = request.files.get('file')
    form = request.form
    t0 = form.get('type')
    if t0:
        t = int(t0)
        uid = form.get('id')
        if t == 0:
            t1 = 'old'
            table_name = 'oldperson_info'
        elif t == 1:
            t1 = 'employee'
            table_name = 'employee_info'
        else:
            t1 = 'volunteer'
            table_name = 'volunteer_info'
        path = 'D:\\dasanxxq\\images\\'
        path += t1
        path += '\\'
        path += str(uid)
        if not os.path.exists(path):
            os.mkdir(path)
        path += '\\'
        path += str(random.randint(0, 999999))
        path += '.png'
        f.save(path)
        set = 'imgset_dir = \'' + path + '\''
        where = 'id = \'' + str(uid) + '\''
        update(conn, table_name, set, where)
    return render_template('images.html')


@app.route('/videos', methods=['GET', 'POST'])
def videos():
    f = request.files.get('file')
    path = 'D:\\dasanxxq\\videos'
    if not os.path.exists(path):
        os.mkdir(path)
    path += '\\'
    path += str(random.randint(0, 999999))
    path += '.avi'
    if f:
        f.save(path)
    return render_template('videos.html')


@app.route('/vindex', methods=['GET', 'POST'])
def vindex():
    return render_template('vindex.html')


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/fall', methods=['GET', 'POST'])
def fall():
    f = bodydetect.detect_fall('./pic/test.png')
    if f:
        content = '摔倒'
    else:
        content = '正常'
    return render_template('fall.html', content=content)


@app.route('/camera')
def camera():
    # cap = cv2.VideoCapture('person.mp4')
    cap = cv2.VideoCapture()
    count = 1
    while True:
        success, image = cap.read()
        if success:
            if count % 36 == 1:
                cv2.imwrite("picture/frame%d.jpg" % count, image)
                if cv2.waitKey(10) == 27:
                    break
            count += 1
        else:
            break
    cap.release()
    cv2.destroyAllWindows()
    pass


if __name__ == '__main__':
    db_path = 'old_care.sqlite'
    conn = sqlite3.connect(db_path, check_same_thread=False)
    sql_create = '''
        CREATE TABLE IF NOT EXISTS oldperson_info (
          ID INTEGER PRIMARY KEY,
          username TEXT,
          gender TEXT,
          phone TEXT,
          id_card TEXT,
          birthday TEXT,
          checkin_date TEXT,
          checkout_date TEXT,
          imgset_dir TEXT,
          profile_photo TEXT,
          room_number TEXT,
          firstguardian_name TEXT,
          firstguardian_relationship TEXT,
          firstguardian_phone TEXT,
          firstguardian_wechat TEXT,
          secondguardian_name TEXT,
          secondguardian_relationship TEXT,
          secondguardian_phone TEXT,
          secondguardian_wechat TEXT,
          health_state TEXT,
          DESCRIPTION TEXT,
          ISACTIVE TEXT,
          CREATED TEXT,
          CREATEDBY INTEGER,
          UPDATED TEXT,
          UPDATEDBY INTEGER,
          REMOVE TEXT
        )
        '''
    # 用 execute 执行一条 sql 语句
    conn.execute(sql_create)
    sql_create = '''
            CREATE TABLE IF NOT EXISTS employee_info (
            id INTEGER PRIMARY KEY,
            username TEXT,
            gender TEXT,
            phone TEXT,
            id_card TEXT,
            birthday TEXT,
            hire_date TEXT,
            resign_date TEXT,
            imgset_dir TEXT,
            profile_photo TEXT,
            DESCRIPTION TEXT,
            ISACTIVE TEXT,
            CREATED TEXT,
            CREATEDBY INTEGER,
            UPDATED TEXT,
            UPDATEDBY INTEGER,
            REMOVE TEXT
            )
            '''
    # 用 execute 执行一条 sql 语句
    conn.execute(sql_create)
    sql_create = '''
              CREATE TABLE IF NOT EXISTS volunteer_info (
                id INTEGER PRIMARY KEY,
                name TEXT,
                gender TEXT,
                phone TEXT,
                id_card TEXT,
                birthday TEXT,
                checkin_date TEXT,
                checkout_date TEXT,
                imgset_dir TEXT,
                profile_photo TEXT,
                DESCRIPTION TEXT,
                ISACTIVE TEXT,
                CREATED TEXT,
                CREATEDBY INTEGER,
                UPDATED TEXT,
                UPDATEDBY INTEGER,
                REMOVE TEXT
              )
              '''
    # 用 execute 执行一条 sql 语句
    conn.execute(sql_create)
    sql_create = '''
                 CREATE TABLE IF NOT EXISTS event_info (
                    id INTEGER PRIMARY KEY,
                    event_type INTEGER,
                    event_date TEXT,
                    event_location TEXT,
                    event_desc TEXT,
                    oldperson_id INTEGER
                 )
                 '''
    # 用 execute 执行一条 sql 语句
    conn.execute(sql_create)
    sql_create = '''
                     CREATE TABLE IF NOT EXISTS sys_user (
                        ID INTEGER PRIMARY KEY,
                        UserName TEXT,
                        Password TEXT,
                        REAL_NAME TEXT,
                        SEX TEXT,
                        EMAIL TEXT,
                        PHONE TEXT,
                        MOBILE TEXT,
                        DESCRIPTION TEXT,
                        ISACTIVE TEXT,
                        CREATED TEXT,
                        CREATEDBY INTEGER,
                        UPDATED TEXT,
                        UPDATEDBY INTEGER,
                        REMOVE TEXT,
                        DATAFILTER TEXT,
                        theme TEXT,
                        defaultpage TEXT,
                        logoimage TEXT,
                        qqopenid TEXT,
                        appversion TEXT,
                        jsonauth TEXT
                     )
                     '''
    # 用 execute 执行一条 sql 语句
    conn.execute(sql_create)
    app.run(debug=True)
