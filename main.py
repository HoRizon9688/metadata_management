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
window = sg.Window('Window Title', layout)

while True:
    event, values = window.read()
    # See if user wants to quit or window was closed
    if event == sg.WINDOW_CLOSED:
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
                    sg.Button('修改键类型'), sg.Button('修改默认值')],
                   [sg.Button('查看元数据'), sg.Button('新建字段'), sg.Button('新建表')],
                   [sg.Output(key='result', size=(200, 400))]]
        window3 = sg.Window('Window2', layout3, size=(600, 600))
        while True:
            ev3, val3 = window3.read()
            if ev3 == sg.WINDOW_CLOSED:
                break
            if ev3 == '修改字段名':
                window3['result'].update('')
                if val3['win3_input']:
                    win3_input = val3['win3_input']
                    filed_name, filed_id = win3_input.split(' ')
                    sql = "select schema_name,table_name,filed_name,type,length,`null` from filed where filed_id = {}".format(filed_id)
                    cursor.execute(sql)
                    result = cursor.fetchone()
                    schema_name = result[0]
                    table_name = result[1]
                    old_filed_name = result[2]
                    filed_type = result[3]
                    filed_length = result[4]
                    null_flag = result[5]
                    if filed_length is None:
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

            if ev3 == '查看元数据':
                window3['result'].update('')
                output = get_filed(cursor)
                print(
                    "filed_id     filed_name     schema_name     table_name     type     length     null     key     default")
                for i in output:
                    print(i)

# Finish up by removing from the screen
window.close()
conn.close()
