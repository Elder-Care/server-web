from flask import Flask, render_template, request, Response
import sqlite3
import time
import os
import random
import cv2
import bodydetect


app = Flask(__name__)
conn = sqlite3.connect('old_care.sqlite', check_same_thread=False)
cur_id = 0


class camera(object):#摄像机
    def __init__(self):
        self.frames = [open(f + '.jpg', 'rb').read() for f in ['1', '2', '3']]
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()


def columns(table_name):#获取表格列名
    if table_name == 'oldperson_info':
        return ['id', 'usernamee', 'gender', 'phone', 'id_card', 'birthday', 'checkin_date', 'checkout_date', 'imgset_dir'
            , 'profile_photo', 'room_number', 'firstguardian_name', 'firstguardian_relationship', 'firstguardian_phone'
            , 'firstguardian_wechat', 'secondguardian_name', 'secondguardian_relationship', ' secondguardian_phone'
            , 'secondguardian_wechat', 'health_state', 'DESCRIPTION', 'ISACTIVE', 'CREATED', 'CREATEDBY', 'UPDATED'
                , 'UPDATEDBY', 'REMOVE']
    elif table_name == 'employee_info':
        return['id', 'username', 'gender', 'phone', 'id_card', 'birthday', 'hire_date', 'resign_date', 'imgset_dir',
               'profile_photo', 'DESCRIPTION', 'ISACTIVE', 'CREATED', 'CREATEDBY', 'UPDATED', 'UPDATEDBY', 'REMOVE']
    elif table_name == 'volunteer_info':
        return['id', 'name', 'gender', 'phone', 'id_card', 'birthday', 'checkin_date', 'checkout_date', 'imgset_dir'
            , 'profile_photo', 'DESCRIPTION', 'ISACTIVE', 'CREATED', 'CREATEDBY', 'UPDATED'
                , 'UPDATEDBY', 'REMOVE']
    elif table_name == 'event_info':
        return['id', 'event_type', 'event_date', 'event_location', 'event_desc', 'oldperson_id']
    elif table_name == 'sys_user':
        return['ID', 'UserName', 'Password', 'REAL_NAME', 'SEX', 'EMAIL', 'PHONE', 'MOBILE', 'DESCRIPTION', 'ISACTIVE',
               'CREATED', 'CREATEDBY', 'UPDATED', 'UPDATEDBY', 'REMOVE', 'DATAFILTER', 'theme', 'defaultpage',
               'logoimage', 'qqopenid', 'appversion', 'jsonauth']
    else:
        print("表名不对")
        return 0


def insert(conn, table_name, value):#通用表格插入操作
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


def delete(conn, table_name, where):#通用表格删除操作
    sql_delete = "DELETE FROM " + table_name + " WHERE " + where + ";"
    conn.execute(sql_delete)
    conn.commit()
    #print(sql_delete)


def update(conn, table_name, set, where):#通用表格更新操作
    sql_update = "UPDATE " + table_name + " SET " + set
    if where != "":
        sql_update = sql_update + " WHERE " + where
    sql_update = sql_update + ";"
    print(sql_update)
    conn.execute(sql_update)
    conn.commit()


def select(conn, table_name, where):#通用表格查询操作
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


def zhuce(conn, name, password):
    #用户注册
    table_name = 'sys_user'
    where = 'UserName = \'' + name + '\''
    l = select(conn, table_name, where)
    if len(l) == 0:
        t = time.strftime('%Y-%m-%d', time.localtime())
        value = {'UserName': name, 'Password': password, 'CREATED': t}
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
    #新增老人
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
    # 完善老人信息
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
    #删除老人
    table_name = 'oldperson_info'
    where = 'ID = \'' + str(uid) + '\''
    delete(conn, table_name, where)
    return 1


def add_employee(conn, info):
    #新增员工
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
    # 完善员工信息
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
    #删除员工
    table_name = 'employee_info'
    where = 'ID = \'' + str(uid) + '\''
    delete(conn, table_name, where)
    return 1


def add_volunteer(conn, info):
    #新增志愿者
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
    # 完善志愿者信息
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
    #删除志愿者
    table_name = 'volunteer_info'
    where = 'ID = \'' + str(uid) + '\''
    delete(conn, table_name, where)
    return 1


@app.route('/')
def login1():
    #初始登录界面
    return render_template('login.html')


@app.route('/login0', methods=['GET', 'POST'])
def login0():
    #登录
    form = request.form
    username = form.get('username')
    password = form.get('password')
    if not username:
        content = "请输入用户名"
        return render_template('login.html', content=content)
    if not password:
        content = "请输入密码"
        return render_template('login.html', content=content)
    global conn
    if login(conn, username, password):
        content = "登录成功"
        return render_template('login.html', content=content)
    else:
        content = "用户名或密码错误"
        return render_template('login.html', content=content)


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    #注册
    form = request.form
    username = form.get('username')
    password = form.get('password')
    if not username:
        content = "请输入用户名"
        return render_template('signin.html', content=content)
    if not password:
        content = "请输入密码"
        return render_template('signin.html', content=content)
    global conn
    if zhuce(conn, username, password):
        content = "注册成功"
        return render_template('login.html', content=content)
    else:
        content = "用户名已存在"
        return render_template('signin.html', content=content)


@app.route('/pinfo', methods=['GET', 'POST'])
def pinfo():
    #个人信息
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
    #注销
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
    #新增老人
    form = request.form
    if not form.get('username'):
        content = "请输入用户名"
        return render_template('addo.html', content=content)
    info = {'username':form.get('username'), 'gender': form.get('gender'), 'phone': form.get('phone'), 'id_card': form.get('id_card'),
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
        return render_template('addo.html', content=content)
    else:
        content = "用户名已存在"
        return render_template('addo.html', content=content)


@app.route('/oinfo', methods=['POST', 'GET'])
def oinfo():
    #老人信息
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
    return render_template('oinfo.html', content=content)


@app.route('/delo', methods=['GET', 'POST'])
def delo():
    #删除老人
    form = request.form
    uid = form.get('uid')
    print(uid)
    if not uid:
        content = "请输入ID"
        return render_template('delo.html', content=content)
    global conn
    if del_elder(conn, uid):
        content = "删除成功"
        return render_template('delo.html', content=content)
    else:
        content = "该id不存在"
        return render_template('delo.html', content=content)


@app.route('/adde', methods=['GET', 'POST'])
def adde():
    #新增员工
    form = request.form
    if not form.get('username'):
        content = "请输入用户名"
        return render_template('adde.html', content=content)
    info = {'username':form.get('username'), 'gender': form.get('gender'), 'phone': form.get('phone'), 'id_card': form.get('id_card'),
            'birthday': form.get('birthday'), 'hire_date': form.get("hire_date"),
            'resign_date': form.get('resign_date'), 'profile_photo':
                form.get('profile_photo'), 'DESCRIPTION': form.get('DESCRIPTION'), 'ISACTIVE': form.get('ISACTIVE')}
    global conn
    if add_employee(conn, info):
        content = "增添成功"
        return render_template('adde.html', content=content)
    else:
        content = "用户名已存在"
        return render_template('adde.html', content=content)


@app.route('/einfo', methods=['GET', 'POST'])
def einfo():
    #员工信息
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
    #删除员工
    form = request.form
    uid = form.get('uid')
    print(uid)
    if not uid:
        content = "请输入ID"
        return render_template('dele.html', content=content)
    global conn
    if del_employee(conn, uid):
        content = "删除成功"
        return render_template('dele.html', content=content)
    else:
        content = "该id不存在"
        return render_template('dele.html', content=content)


@app.route('/addv', methods=['GET', 'POST'])
def addv():
    #新增志愿者
    form = request.form
    if not form.get('username'):
        content = "请输入用户名"
        return render_template('addv.html', content=content)
    info = {'name':form.get('username'), 'gender': form.get('gender'), 'phone': form.get('phone'), 'id_card': form.get('id_card'),
            'birthday': form.get('birthday'), 'checkin_date': form.get("checkin_date"),
            'checkout_date': form.get('checkout_date'), 'profile_photo':
                form.get('profile_photo'), 'DESCRIPTION': form.get('DESCRIPTION'), 'ISACTIVE': form.get('ISACTIVE')}
    global conn
    if add_volunteer(conn, info):
        content = "增添成功"
        return render_template('addv.html', content=content)
    else:
        content = "用户名已存在"
        return render_template('addv.html', content=content)


@app.route('/vinfo', methods=['GET', 'POST'])
def vinfo():
    #志愿者信息
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
    #删除志愿者
    form = request.form
    uid = form.get('uid')
    print(uid)
    if not uid:
        content = "请输入ID"
        return render_template('delv.html', content=content)
    global conn
    if del_volunteer(conn, uid):
        content = "删除成功"
        return render_template('delv.html', content=content)
    else:
        content = "该id不存在"
        return render_template('delv.html', content=content)


@app.route('/images', methods=['GET', 'POST'])
def images():
    #上传图片（老人、员工和志愿者照片）
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
    #上传视频文件
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

#这三个用不到，尝试获取视频流，但没有成功
@app.route('/vindex', methods=['GET', 'POST'])
def vindex():
    return render_template('vindex.html')


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(camera()),
                mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/fall', methods=['GET', 'POST'])
def fall():
    #读取指定图片进行摔倒检测
    f = bodydetect.detect_fall('D:\\dasanxxq\\fallimage\\fall-02-cam0-rgb-001.png')
    if f:
        content = '摔倒'
    else:
        content = '正常'
    return render_template('fall.html', content=content)


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
