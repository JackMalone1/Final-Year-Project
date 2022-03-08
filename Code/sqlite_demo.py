import sqlite3
from employee import Employee

conn = sqlite3.connect("employee.db")

cursor = conn.cursor()

# cursor.execute("""CREATE TABLE  employees (
#                     first text,
#                     last text,
#                     pay integer
#                     )""")

employee = Employee("John", "Doe", 80000)
employee2 = Employee("Jane", "Doe", 90000)

# cursor.execute("INSERT INTO employees VALUES (?, ?, ?)", (employee.first, employee.last, employee.pay))
#
# conn.commit()
#
# cursor.execute("INSERT INTO employees VALUES (:first, :last, :pay)", {'first': employee2.first, 'last': employee2.last, 'pay': employee2.pay})
#
# conn.commit()

cursor.execute(
    "SELECT * FROM employees WHERE last=:last",
    {"last": "Doe"},
)
print(cursor.fetchall())

cursor.execute(
    "SELECT * FROM employees WHERE last=?", ("Schafer",)
)

print(cursor.fetchall())

conn.commit()

conn.close()
