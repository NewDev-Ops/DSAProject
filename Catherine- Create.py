import mysql.connector
new_medicines=[]
def create_medicine(name,quantity,price,expiry):
  new_medicines.append([name,quantity,price,expiry])
  try:
     conn=mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="medicines"
     )
     cursor=conn.cursor()
     sql = "INSERT INTO meddata  (Name,Quantity,Price,Expiry) VALUES (%s,%s,%s,%s)"
     values = (name,quantity,price,expiry)
     cursor.execute(sql,values)
     conn.commit()

     print(f"Successfully added medicine: {name}")
  except mysql.connector.Error as err:
     print(f"Something went wrong: {err}")
  finally:
     if conn.is_connected():
        conn.close()

create_medicine("Aspirin", 50, 2.0, "2025-10-15")
create_medicine("Ibuprofen", 75, 2.5, "2026-01-01")


