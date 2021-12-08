import PySimpleGUI as sg
import pymysql

conn = pymysql.connect(host='localhost',
                       user='root',
                       password='chy200412',
                       database='metadata')
cursor = conn.cursor()


def schema_update_charset(charset, schema_id, conn, cursor):
    sql = "UPDATE `schema` set character_set = '{}' where schema_id = {}".format(charset, schema_id)
    cursor.execute(sql)
    conn.commit()


def schema_update_collation(collation, schema_id, conn, cursor):
    sql = "UPDATE `schema` set collation = '{}' where schema_id = {}".format(collation, schema_id)
    cursor.execute(sql)
    conn.commit()


def table_update_name(table_name, table_id, conn, cursor):
    sql = "UPDATE `table` set table_name = '{}' where table_id = {}".format(table_name, table_id)
    cursor.execute(sql)
    conn.commit()


def table_update_collation(collation, table_id, conn, cursor):
    sql = "UPDATE `table` set collation = '{}' where table_id = {}".format(collation, table_id)
    cursor.execute(sql)
    conn.commit()


def filed_update_name(filed_name, filed_id, conn, cursor):
    sql = "UPDATE `filed` set filed_name = '{}' where filed_id = {}".format(filed_name, filed_id)
    cursor.execute(sql)
    conn.commit()


def filed_update_type(filed_type, filed_id, conn, cursor):
    sql = "UPDATE `filed` set type = '{}' where filed_id = {}".format(filed_type, filed_id)
    cursor.execute(sql)
    conn.commit()


def filed_update_length(filed_length, filed_id, conn, cursor):
    sql = "UPDATE `filed` set length = {} where filed_id = {}".format(filed_length, filed_id)
    cursor.execute(sql)
    conn.commit()


def filed_update_null(filed_null, filed_id, conn, cursor):
    sql = "UPDATE `filed` set `null` = '{}' where filed_id = {}".format(filed_null, filed_id)
    cursor.execute(sql)
    conn.commit()


def filed_update_default(filed_default, filed_id, conn, cursor):
    sql = "UPDATE `filed` set `default`  = '{}' where filed_id = {}".format(filed_default, filed_id)
    cursor.execute(sql)
    conn.commit()


def get_schema(cursor):
    sql = "select * from `schema`"
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def get_table(cursor):
    sql = "select * from `table`"
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def get_filed(cursor):
    sql = "select * from `filed`"
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def create_schema(db_name, charset, collation, conn, cursor):
    sql = "create database {} default character set {} default collate {}".format(db_name, charset,
                                                                                  collation)
    cursor.execute(sql)
    conn.commit()


layout = [[sg.Button('Function1'), sg.Button('Function2'), sg.Button('Function3')]]
window = sg.Window('Window Title', layout, enable_close_attempted_event=True)

while True:
    event, values = window.read()
    # See if user wants to quit or window was closed
    if event == sg.WINDOW_CLOSE_ATTEMPTED_EVENT and sg.popup_yes_no('Do you really want to exit?') == 'Yes':
        break
    # Output a message to the window
    if event == 'Function1':
        layout1 = [[sg.Input(key='win1_input')],
                   [sg.Button('修改字符集'), sg.Button('修改排序方式'), sg.Button('查看元数据'), sg.Button('新建数据库')],
                   [sg.Output(key='result', size=(200, 400))]]
        window1 = sg.Window('Window1', layout1, size=(400, 400))
        while True:
            ev1, val1 = window1.read()
            if ev1 == sg.WINDOW_CLOSED:
                break
            if ev1 == '修改字符集':
                window1['result'].update('')
                if val1['win1_input']:
                    win1_input = val1['win1_input']
                    charset, schema_id = win1_input.split(' ')
                    schema_update_charset(charset, schema_id, conn, cursor)
                    cursor.execute("select schema_name from `schema` where schema_id={}".format(schema_id))
                    schema_name = cursor.fetchone()
                    cursor.execute("alter database {} default character set {}".format(schema_name[0], charset))
                    conn.commit()
                    print("修改成功")
            if ev1 == '修改排序方式':
                window1['result'].update('')
                if val1['win1_input']:
                    win1_input = val1['win1_input']
                    collation, schema_id = win1_input.split(' ')
                    schema_update_collation(collation, schema_id, conn, cursor)
                    cursor.execute("select schema_name from `schema` where schema_id={}".format(schema_id))
                    schema_name = cursor.fetchone()
                    cursor.execute("alter database {} default collate {}".format(schema_name[0], collation))
                    print("修改成功")
            if ev1 == '查看元数据':
                window1['result'].update('')
                output = get_schema(cursor)
                print("schema_id      schema_name      character_set      collation\n")
                for i in output:
                    print(i)
            if ev1 == '新建数据库':
                window1['result'].update('')
                if val1['win1_input']:
                    win1_input = val1['win1_input']
                    db_name, charset, collation = win1_input.split(' ')
                    create_schema(db_name, charset, collation, conn, cursor)
                    cursor.execute("select max(schema_id) from `schema`")
                    result = cursor.fetchone()
                    schema_id = int(result[0]) + 1
                    cursor.execute(
                        "insert into `schema` values ({},'{}','{}','{}')".format(schema_id, db_name, charset,
                                                                                 collation))
                    conn.commit()
                    print("新建数据库成功")
    if event == 'Function2':
        layout2 = [[sg.Input(key='win2_input')],
                   [sg.Button('修改表名'), sg.Button('修改排序方式'), sg.Button('查看元数据')],
                   [sg.Output(key='result', size=(200, 400))]]
        window2 = sg.Window('Window2', layout2, size=(400, 400))
        while True:
            ev2, val2 = window2.read()
            if ev2 == sg.WINDOW_CLOSED:
                break
            if ev2 == "修改表名":
                window2['result'].update('')
                if val2['win2_input']:
                    win2_input = val2['win2_input']
                    table_name, table_id = win2_input.split(' ')
                    cursor.execute("select table_name from `table` where table_id = {}".format(table_id))
                    old_table_name = cursor.fetchone()
                    cursor.execute("select schema_name from `table` where table_id = {}".format(table_id))
                    schema_name = cursor.fetchone()
                    table_update_name(table_name, table_id, conn, cursor)
                    cursor.execute("use {}".format(schema_name[0]))
                    cursor.execute("alter table {} rename to {}".format(old_table_name[0], table_name))
                    conn.commit()
                    cursor.execute("use metadata")
                    print("修改成功")
            if ev2 == "修改排序方式":
                window2['result'].update('')
                if val2['win2_input']:
                    win2_input = val2['win2_input']
                    collation, table_id = win2_input.split(' ')
                    table_update_collation(collation, table_id, conn, cursor)
                    cursor.execute("select table_name from `table` where table_id = {}".format(table_id))
                    table_name = cursor.fetchone()
                    cursor.execute("select schema_name from `table` where table_id = {}".format(table_id))
                    schema_name = cursor.fetchone()
                    cursor.execute("use {}".format(schema_name[0]))
                    cursor.execute("alter table {} default collate {}".format(table_name[0], collation))
                    conn.commit()
                    cursor.execute("use metadata")
                    print("修改成功")
            if ev2 == "查看元数据":
                window2['result'].update('')
                output = get_table(cursor)
                print("table_id      table_name      schema_name      rows     collation\n")
                for i in output:
                    print(i)

    if event == 'Function3':
        layout3 = [[sg.Input(key='win3_input')],
                   [sg.Button('修改字段名'), sg.Button('修改字段类型'), sg.Button('修改字段长度'), sg.Button('修改非空属性'),
                    sg.Button('修改默认值')],
                   [sg.Button('查看元数据'), sg.Button('新建字段')],
                   [sg.Output(key='result', size=(200, 400))]]
        window3 = sg.Window('Window3', layout3, size=(600, 600))
        while True:
            ev3, val3 = window3.read()
            if ev3 == sg.WINDOW_CLOSED:
                break
            if ev3 == '修改字段名':
                window3['result'].update('')
                if val3['win3_input']:
                    win3_input = val3['win3_input']
                    filed_name, filed_id = win3_input.split(' ')
                    sql = "select schema_name,table_name,filed_name,type,length,`null` from filed where filed_id = {}".format(
                        filed_id)
                    cursor.execute(sql)
                    result = cursor.fetchone()
                    schema_name = result[0]
                    table_name = result[1]
                    old_filed_name = result[2]
                    filed_type = result[3]
                    filed_length = result[4]
                    null_flag = result[5]
                    if filed_length is None or filed_length == '':
                        sql = "alter table {} change {} {} {}".format(table_name, old_filed_name, filed_name,
                                                                      filed_type)
                    else:
                        sql = "alter table {} change {} {} {}({})".format(table_name, old_filed_name, filed_name,
                                                                          filed_type, filed_length)
                    if null_flag == 'NO':
                        sql = sql + " not null"
                    filed_update_name(filed_name, filed_id, conn, cursor)
                    cursor.execute("use {}".format(schema_name))
                    cursor.execute(sql)
                    conn.commit()
                    cursor.execute("use metadata")
                    print("修改成功")
            if ev3 == '修改字段类型':
                window3['result'].update('')
                if val3['win3_input']:
                    win3_input = val3['win3_input']
                    filed_type, filed_id = win3_input.split(' ')
                    sql = "select schema_name,table_name,filed_name,length,`null` from filed where filed_id = {}".format(
                        filed_id)
                    cursor.execute(sql)
                    result = cursor.fetchone()
                    schema_name = result[0]
                    table_name = result[1]
                    filed_name = result[2]
                    filed_length = result[3]
                    null_flag = result[4]
                    if filed_type == 'int':
                        sql = "alter table {} change {} {} {}".format(table_name, filed_name, filed_name,
                                                                      filed_type)
                    else:
                        sql = "alter table {} change {} {} {}({})".format(table_name, filed_name, filed_name,
                                                                          filed_type, filed_length)
                    if null_flag == 'NO':
                        sql = sql + " not null"
                    filed_update_type(filed_type, filed_id, conn, cursor)
                    cursor.execute("use {}".format(schema_name))
                    cursor.execute(sql)
                    conn.commit()
                    cursor.execute("use metadata")
                    print("修改成功")
            if ev3 == '修改字段长度':
                window3['result'].update('')
                if val3['win3_input']:
                    win3_input = val3['win3_input']
                    filed_length, filed_id = win3_input.split(' ')
                    sql = "select schema_name,table_name,filed_name,type,`null` from filed where filed_id = {}".format(
                        filed_id)
                    cursor.execute(sql)
                    result = cursor.fetchone()
                    schema_name = result[0]
                    table_name = result[1]
                    filed_name = result[2]
                    filed_type = result[3]
                    null_flag = result[4]
                    if filed_type == 'int':
                        print("int类型无法修改字段长度")
                    else:
                        sql = "alter table {} change {} {} {}({})".format(table_name, filed_name, filed_name,
                                                                          filed_type, filed_length)
                        if null_flag == 'NO':
                            sql = sql + " not null"
                        filed_update_length(filed_length, filed_id, conn, cursor)
                        cursor.execute("use {}".format(schema_name))
                        cursor.execute(sql)
                        conn.commit()
                        cursor.execute("use metadata")
                        print("修改成功")
            if ev3 == '修改非空属性':
                window3['result'].update('')
                if val3['win3_input']:
                    win3_input = val3['win3_input']
                    filed_null, filed_id = win3_input.split(' ')
                    filed_null = filed_null.upper()
                    sql = "select schema_name,table_name,filed_name,type,length from filed where filed_id = {}".format(
                        filed_id)
                    cursor.execute(sql)
                    result = cursor.fetchone()
                    schema_name = result[0]
                    table_name = result[1]
                    filed_name = result[2]
                    filed_type = result[3]
                    filed_length = result[4]
                    if filed_length is None or filed_length == '':
                        sql = "alter table {} change {} {} {}".format(table_name, filed_name, filed_name,
                                                                      filed_type)
                    else:
                        sql = "alter table {} change {} {} {}({})".format(table_name, filed_name, filed_name,
                                                                          filed_type, filed_length)
                    if filed_null == 'NO':
                        sql = sql + " not null"
                    print(sql)
                    filed_update_null(filed_null, filed_id, conn, cursor)
                    cursor.execute("use {}".format(schema_name))
                    cursor.execute(sql)
                    conn.commit()
                    cursor.execute("use metadata")
                    print("修改成功")
            if ev3 == '修改默认值':
                window3['result'].update('')
                if val3['win3_input']:
                    win3_input = val3['win3_input']
                    filed_default, filed_id = win3_input.split(' ')
                    sql = "select schema_name,table_name,filed_name,type,length,`null` from filed where filed_id = {}".format(
                        filed_id)
                    cursor.execute(sql)
                    result = cursor.fetchone()
                    schema_name = result[0]
                    table_name = result[1]
                    filed_name = result[2]
                    filed_type = result[3]
                    filed_length = result[4]
                    null_flag = result[5]
                    if filed_type == 'int':
                        sql = "alter table {} modify column {} {}".format(table_name, filed_name, filed_type)
                        if null_flag == 'NO':
                            sql = sql + " not null "
                        sql = sql + "default {}".format(filed_default)
                    else:
                        sql = "alter table {} modify column {} {}({})".format(table_name, filed_name, filed_type, filed_length)
                        if null_flag == 'NO':
                            sql = sql + " not null "
                        sql = sql + "default '{}'".format(filed_default)
                    filed_update_default(filed_default, filed_id, conn, cursor)
                    cursor.execute("use {}".format(schema_name))
                    cursor.execute(sql)
                    conn.commit()
                    cursor.execute("use metadata")
                    print("修改成功")
            if ev3 == '新建字段':
                layout = [
                    [sg.Text('Please enter filed_name, schema_name, table_name, type, length, null, default',
                             key="tip")],
                    [sg.Text('filed_name', size=(15, 1)), sg.InputText(key='filed_name'),
                     sg.Text('*', text_color='#FF6755', font=20)],
                    [sg.Text('schema_name', size=(15, 1)), sg.InputText(key='schema_name'),
                     sg.Text('*', text_color='#FF6755', font=20)],
                    [sg.Text('table_name', size=(15, 1)), sg.InputText(key='table_name'),
                     sg.Text('*', text_color='#FF6755', font=20)],
                    [sg.Text('filed_type', size=(15, 1)), sg.InputText(key='filed_type'),
                     sg.Text('*', text_color='#FF6755', font=20)],
                    [sg.Text('filed_length', size=(15, 1)), sg.InputText(key='filed_length')],
                    [sg.Text('field_null', size=(15, 1)), sg.InputText(key='filed_null'),
                     sg.Text('*', text_color='#FF6755', font=20)],
                    [sg.Text('filed_key', size=(15, 1)), sg.InputText(key='filed_key')],
                    [sg.Text('filed_default', size=(15, 1)), sg.InputText(key='filed_default')],
                    [sg.Submit(), sg.Cancel()]
                ]
                window4 = sg.Window('window4', layout)
                while True:
                    ev4, val4 = window4.read()
                    if ev4 == sg.WINDOW_CLOSED or ev4 == 'Cancel':
                        break
                    if ev4 == 'Submit':
                        window3['result'].update('')
                        filed_name = val4['filed_name']
                        schema_name = val4['schema_name']
                        table_name = val4['table_name']
                        filed_type = val4['filed_type']
                        filed_length = val4['filed_length']
                        filed_null = val4['filed_null'].upper()
                        filed_key = val4['filed_key']
                        filed_default = val4['filed_default']
                        table_name_list = []
                        cursor.execute("SELECT DISTINCT table_name from filed")
                        result = cursor.fetchall()
                        for i in result:
                            table_name_list.append(i[0])
                        print(table_name_list)
                        cursor.execute("select max(filed_id) from filed")
                        temp = cursor.fetchone()
                        filed_id = int(temp[0]) + 1
                        if filed_length:
                            sql = "insert into `filed` values ({0},'{1}','{2}','{3}','{4}',{5},'{6}','{7}','{8}')".format(
                                filed_id,
                                filed_name,
                                schema_name,
                                table_name,
                                filed_type,
                                filed_length,
                                filed_null,
                                filed_key,
                                filed_default)
                            # print(sql)
                        else:
                            if filed_default:
                                sql = "insert into `filed` (filed_id, filed_name, schema_name, table_name, `type`, `null`, `key`, `default`) values ({},'{}','{}','{}','{}','{}','{}',{})".format(
                                    filed_id,
                                    filed_name,
                                    schema_name,
                                    table_name,
                                    filed_type,
                                    filed_null,
                                    filed_key,
                                    filed_default)
                                # print(sql)
                            else:
                                sql = "insert into `filed` (filed_id, filed_name, schema_name, table_name, `type`, `null`, `key`) values ({},'{}','{}','{}','{}','{}','{}')".format(
                                    filed_id,
                                    filed_name,
                                    schema_name,
                                    table_name,
                                    filed_type,
                                    filed_null,
                                    filed_key)
                                # print(sql)
                        cursor.execute(sql)
                        conn.commit()
                        if table_name not in table_name_list:
                            print("table doesn't exist, try to create it")
                            if filed_length is None or filed_length == '':
                                sql = "create table {} ({} {}".format(table_name, filed_name, filed_type)
                                if filed_default:
                                    sql = sql + ' default {}'.format(filed_default)
                                if filed_null == 'NO':
                                    sql = sql + ' not null'
                            else:
                                sql = "create table {} ({} {}({})".format(table_name, filed_name, filed_type,
                                                                          filed_length)
                                if filed_default:
                                    sql = sql + " default '{}'".format(filed_default)
                                if filed_null == 'NO':
                                    sql = sql + ' not null'
                            sql = sql + ")"
                            print(sql)
                            cursor.execute("use {}".format(schema_name))
                            cursor.execute(sql)
                            conn.commit()
                            cursor.execute("use metadata")
                            print("新建表并成功添加字段")
                        else:
                            print("table has found")
                            if filed_length is None or filed_length == '':
                                sql = "alter table {} add {} {}".format(table_name, filed_name, filed_type)
                                if filed_default:
                                    sql = sql + ' default {}'.format(filed_default)
                            else:
                                sql = "alter table {} add {} {}({})".format(table_name, filed_name, filed_type,
                                                                            filed_length)
                                if filed_default:
                                    sql = sql + " default '{}'".format(filed_default)
                            if filed_null == 'NO':
                                sql = sql + ' not null'
                            print(sql)
                            cursor.execute("use {}".format(schema_name))
                            cursor.execute(sql)
                            conn.commit()
                            cursor.execute("use metadata")
                            print("添加字段成功")
                window4.close()
            if ev3 == '查看元数据':
                window3['result'].update('')
                output = get_filed(cursor)
                print(
                    "filed_id     filed_name     schema_name     table_name     type     length     null     key     default")
                for i in output:
                    print(i)
window.close()
conn.close()
