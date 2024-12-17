import sqlite3

try:
    sqliteConnection = sqlite3.connect('shantabai_login/db.sqlite3')
    cursor = sqliteConnection.cursor()
    command = input("Enter SQL command:")

    while(command != "z"):
        cursor.execute(command)
        result = cursor.fetchall()
        for row in result:
            print(row)
        
    cursor.close()

except sqlite3.Error as error:
    print('Error occured - ', error)

finally:
    if sqliteConnection:
        sqliteConnection.close()
