import PySimpleGUI as sg
import pymysql

conn = pymysql.connect(host='localhost',
                       user='root',
                       password='chy200412',
                       database='metadata')
cursor = conn.cursor()


def schema_update_charset(charset, schema_id, conn, cursor):
    sql = "UPDATE `schema` set character_set='{}' where schema_id = '{}'".format(charset, schema_id)
    cursor.execute(sql)
    conn.commit()


def schema_update_collation(collation, schema_id, conn, cursor):
    sql = "UPDATE `schema` set collation='{}' where schema_id = '{}'".format(collation, schema_id)
    cursor.execute(sql)
    conn.commit()

def get_schema(cursor):
    sql = "select * from `schema`"
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


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
                   [sg.Button('修改字符集'), sg.Button('修改排序方式'), sg.Button('查看元数据')],
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
                    print(charset, schema_id)
                    schema_update_charset(charset, schema_id, conn, cursor)
                    print("修改成功")
            if ev1 == '修改排序方式':
                window1['result'].update('')
                if val1['win1_input']:
                    win1_input = val1['win1_input']
                    collation, schema_id = win1_input.split(' ')
                    print(collation, schema_id)
                    schema_update_collation(collation, schema_id, conn, cursor)
                    print("修改成功")
            if ev1 == '查看元数据':
                window1['result'].update('')
                output = get_schema(cursor)
                print("schema_id      schema_name      character_set      collation")
                for i in output:
                    print("{:^20}{:^20}{:^20}{:^20}".format(i[0], i[1], i[2], i[3]))

    if event == 'Function2':
        layout2 = [[sg.Input(key='win1_input')],
                   [sg.Button('修改表名'), sg.Button('修改排序方式'), sg.Button('查看元数据')],
                   [sg.Output(key='result', size=(200, 400))]]
        window2 = sg.Window('Window2', layout2, size=(400, 400))
        while True:
            ev2, val2 = window2.read()
            if ev2 == sg.WINDOW_CLOSED:
                break
# Finish up by removing from the screen
window.close()