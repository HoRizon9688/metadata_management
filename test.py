import PySimpleGUI as sg
import pymysql

conn = pymysql.connect(host='localhost',
                       user='root',
                       password='chy200412',
                       database='metadata')
cursor = conn.cursor()

layout = [
    [sg.Text('Please enter filed_name, schema_name, table_name, type, length, null, default', key="tip")],
    [sg.Text('filed_name', size=(15, 1)), sg.InputText(key='filed_name'), sg.Text('*', text_color='#FF6755', font=20)],
    [sg.Text('schema_name', size=(15, 1)), sg.InputText(key='schema_name'),
     sg.Text('*', text_color='#FF6755', font=20)],
    [sg.Text('table_name', size=(15, 1)), sg.InputText(key='table_name'), sg.Text('*', text_color='#FF6755', font=20)],
    [sg.Text('filed_type', size=(15, 1)), sg.InputText(key='filed_type'), sg.Text('*', text_color='#FF6755', font=20)],
    [sg.Text('filed_length', size=(15, 1)), sg.InputText(key='filed_length')],
    [sg.Text('field_null', size=(15, 1)), sg.InputText(key='filed_null'), sg.Text('*', text_color='#FF6755', font=20)],
    [sg.Text('filed_key', size=(15, 1)), sg.InputText(key='filed_key')],
    [sg.Text('filed_default', size=(15, 1)), sg.InputText(key='filed_default')],
    [sg.Submit(), sg.Cancel()]
]

window = sg.Window('Simple data entry window', layout)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == 'Cancel':
        break
    if event == 'Submit':
        filed_name = values['filed_name']
        schema_name = values['schema_name']
        table_name = values['table_name']
        filed_type = values['filed_type']
        filed_length = values['filed_length']
        filed_null = values['filed_null'].upper()
        filed_key = values['filed_key']
        filed_default = values['filed_default']
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
            sql = "insert into `filed` values ({0},'{1}','{2}','{3}','{4}',{5},'{6}','{7}','{8}')".format(filed_id,
                                                                                                          filed_name,
                                                                                                          schema_name,
                                                                                                          table_name,
                                                                                                          filed_type,
                                                                                                          filed_length,
                                                                                                          filed_null,
                                                                                                          filed_key,
                                                                                                          filed_default)
            print(sql)
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
                print(sql)
            else:
                sql = "insert into `filed` (filed_id, filed_name, schema_name, table_name, `type`, `null`, `key`) values ({},'{}','{}','{}','{}','{}','{}')".format(
                    filed_id,
                    filed_name,
                    schema_name,
                    table_name,
                    filed_type,
                    filed_null,
                    filed_key)
                print(sql)
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
                sql = "create table {} ({} {}({})".format(table_name, filed_name, filed_type, filed_length)
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
            print("finish")
        else:
            print("table has found")
            if filed_length is None or filed_length == '':
                sql = "alter table {} add {} {}".format(table_name, filed_name, filed_type)
                if filed_default:
                    sql = sql + ' default {}'.format(filed_default)
            else:
                sql = "alter table {} add {} {}({})".format(table_name, filed_name, filed_type, filed_length)
                if filed_default:
                    sql = sql + " default '{}'".format(filed_default)
            if filed_null == 'NO':
                sql = sql + ' not null'
            print(sql)
            cursor.execute("use {}".format(schema_name))
            cursor.execute(sql)
            conn.commit()
            cursor.execute("use metadata")
            print("finish")
window.close()
conn.close()
