import mysql.connector

conn2 = mysql.connector.connect(host="localhost", user="root", passwd="", database="medicines")

if conn2.is_connected():
    print('Connected to MySQL')
else:
    print('Failed to connect to MySQL')

path = conn2.cursor()
path.execute("select * from meddata")
ans = path.fetchall()  # Brings the rows back as tuples

# DB Operations
Medicine_Types = {}

for row in ans:
    Name, Quantity, Price, Expiry = row
    Medicine_Types[Name] = {"Quantity": Quantity, "Price": Price, "Expiry Date": Expiry}

req = input("What drug are you looking for?: ")
print(Medicine_Types[req])

