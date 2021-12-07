import pymysql

conn = pymysql.connect(host='localhost',
                       user='root',
                       password='chy200412',
                       database='metadata')
cursor = conn.cursor()

def get_schema(cursor):
    sql = "select * from `schema`"
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

output = get_schema(cursor)
print(output)

charset = input()
sql = "UPDATE `schema` set character_set='{}'".format(charset)
cursor.execute(sql)
conn.commit()
output = get_schema(cursor)
print(output)