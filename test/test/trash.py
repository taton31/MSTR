
import sqlite3 
class DB: 

    """
    # Можно выполнять кастомные запросы через cursor.execute
    a.cursor.execute(
            '''
            select * from users
            '''
        )   
    print(a.cursor.fetchall())
    """

    def __init__(self, path: str):
        self.connect = sqlite3.connect(path)
        self.connect.row_factory = sqlite3.Row
        self.cursor = self.connect.cursor()

    def insert_new_user(self, user_id: int):
        users = self.get_users()
        if (user_id,) in users: 
            return
        try:
            self.cursor.execute(
                '''
                insert into users (ID) values (:user_id);
                ''', 
                {"user_id": user_id}
            )   
            self.cursor.execute(
                '''
                insert into subscription (ID) values (:user_id);
                ''', 
                {"user_id": user_id}
            )   
            self.cursor.execute(
                '''
                insert into favorite (ID) values (:user_id);
                ''', 
                {"user_id": user_id}
            )   
        except sqlite3.DatabaseError as err:       
            print("Error: ", err)
        else:
            self.connect.commit()
        
    def get_users(self):
        try:
            self.cursor.execute(
                '''
                select ID from users
                '''
            )   
        except sqlite3.DatabaseError as err:       
            print("Error: ", err)
        else: 
            return self.cursor.fetchall()

    def insert_security (self, user_id: int, security: str):
        try:
            self.cursor.execute(
                '''
                UPDATE users SET security = :security WHERE ID = :user_id
                ''', 
                {"user_id": user_id, "security": security}
            )   
        except sqlite3.DatabaseError as err:       
            print("Error: ", err)
        else: 
            self.connect.commit()

    def insert_favorite (self, user_id: int, favorite: str):
        try:
            self.cursor.execute(
                '''
                UPDATE favorite SET favorite = :favorite WHERE ID = :user_id
                ''', 
                {"user_id": user_id, "favorite": favorite}
            )   
        except sqlite3.DatabaseError as err:       
            print("Error: ", err)
        else: 
            self.connect.commit()

    def insert_subscription (self, user_id: int, subscription: dict):
        try:
            self.cursor.execute(
                '''
                UPDATE subscription SET indicator_change = :indicator_change WHERE ID = :user_id;
                ''', 
                {"user_id": user_id, "indicator_change": subscription.get('indicator_change', 'Null')}
            )  
            self.cursor.execute(
                '''
                UPDATE subscription SET company_events = :company_events WHERE ID = :user_id;
                ''', 
                {"user_id": user_id, "company_events": subscription.get('company_events', 'Null')}
            )  
            self.cursor.execute(
                '''
                UPDATE subscription SET time_events = :time_events WHERE ID = :user_id;
                ''', 
                {"user_id": user_id, "time_events": subscription.get('time_events', 'Null')}
            )   
        except sqlite3.DatabaseError as err:       
            print("Error: ", err)
        else: 
            self.connect.commit()
        
    def concat_security (self, user_id: int, security: str):
        try:
            self.cursor.execute(
                '''
                select security from users WHERE ID = :user_id
                ''', 
                {"user_id": user_id}
            )   
            tmp = self.cursor.fetchall()[0][0]

            self.cursor.execute(
                '''
                UPDATE users SET security = :security WHERE ID = :user_id
                ''', 
                {"user_id": user_id, "security": f"{tmp};{security}"}
            )   
        except sqlite3.DatabaseError as err:       
            print("Error: ", err)
        else: 
            self.connect.commit()
    
    def concat_favorite (self, user_id: int, favorite: str):
        try:
            self.cursor.execute(
                '''
                select favorite from favorite WHERE ID = :user_id
                ''', 
                {"user_id": user_id}
            )   
            tmp = self.cursor.fetchall()[0][0]

            self.cursor.execute(
                '''
                UPDATE favorite SET favorite = :favorite WHERE ID = :user_id
                ''', 
                {"user_id": user_id, "favorite": f"{tmp};{favorite}"}
            )   
        except sqlite3.DatabaseError as err:       
            print("Error: ", err)
        else: 
            self.connect.commit()

    def concat_subscription (self, user_id: int, subscription: dict):
        try:
            self.cursor.execute(
                '''
                select indicator_change from subscription WHERE ID = :user_id
                ''', 
                {"user_id": user_id}
            )   
            tmp = self.cursor.fetchall()[0][0]

            self.cursor.execute(
                '''
                UPDATE favorite SET favorite = :favorite WHERE ID = :user_id
                ''', 
                {"user_id": user_id, "favorite": f"{tmp};{subscription.get('indicator_change', 'None')}"}
            )   

            
        except sqlite3.DatabaseError as err:       
            print("Error: ", err)
        else: 
            self.connect.commit()

    def get_security (self, user_id: int):
        try:
            self.cursor.execute(
                '''
                select security from users WHERE ID = :user_id
                ''', 
                {"user_id": user_id}
            )   
        except sqlite3.DatabaseError as err:       
            print("Error: ", err)
        else: 
            return self.cursor.fetchall()

    def get_favorite (self, user_id: int):
        try:
            self.cursor.execute(
                '''
                select favorite from favorite WHERE ID = :user_id
                ''', 
                {"user_id": user_id}
            )   
        except sqlite3.DatabaseError as err:       
            print("Error: ", err)
        else: 
            return self.cursor.fetchall()

    def get_subscription (self, user_id: int):
        try:
            self.cursor.execute(
                '''
                select indicator_change, company_events, time_events from subscription WHERE ID = :user_id;
                ''', 
                {"user_id": user_id}
            )   
        except sqlite3.DatabaseError as err:       
            print("Error: ", err)
        else: 
            return self.cursor.fetchall()

    """
    def get_all (self):
        try:
            self.cursor.executescript(
                '''
                select * from users;
                select * from subscription;
                select * from favorite;
                '''
            )   
        except sqlite3.DatabaseError as err:
            print("Error: ", err)
        else: 
            return self.cursor.fetchall()
    """

    def drop_user (self, user_id: int):
        try:
            self.cursor.execute(
                '''
                delete from users where ID = :user_id;
                ''',
                {"user_id": user_id}
            )   
            self.cursor.execute(
                '''
                delete from subscription where ID = :user_id;
                ''',
                {"user_id": user_id}
            )   
            self.cursor.execute(
                '''
                delete from favorite where ID = :user_id;
                ''',
                {"user_id": user_id}
            )   
        except sqlite3.DatabaseError as err:
            print("Error: ", err)
        else: 
            return self.cursor.fetchall()
    
    def drop_all_users(self):
        try:
            self.cursor.executescript(
                '''
                delete from users;
                delete from subscription;
                delete from favorite;
                '''
            )  
        except sqlite3.DatabaseError as err:
            print("Error: ", err)

    def __del__(self):
        self.cursor.close()
        self.connect.close()
        






import random
import time
def test():
    for i in range(100):
        b=random.randint(1,1111111111)
        random.randint()
        a.insert_new_user(b)
        a.insert_security(b, 'mos_div'+str(b))
        a.insert_favorite(b, 'fav'+str(b))
        a.insert_subscription(b, {"indicator_change": 'ind'+str(b), "company_events": 'comp'+str(b), "time_events": "time"+str(b)})
    a.insert_new_user(111)
    a.insert_security(111, 'mos_div'+str(111))
    a.insert_new_user(111)
    a.insert_security(111, 'mos_div'+str(111))


a = DB('database/bot_database.sqlite')
a.cursor.execute(
                '''
                select * from users LIMIT 1
                '''
            )   
z=a.cursor.fetchone()
print(z.keys())
exit()
a.drop_all_users()
start = time.time()
#test()
print(time.time()-start)
a.insert_new_user(1)
a.insert_security(1,"first")
print(a.get_security(1))
a.concat_security(1,"second")
z=a.get_security(1)
print(z)
z=z[0][0].split(';')
print(z)
exit()
start = time.time()
a.cursor.execute(
        '''
        select * from subscription
        '''
    )   
p=a.cursor.fetchall()
'''
print(p)
print(p[0])
print(p[0][1])
print(a.get_users())
z=a.get_subscription(1723464345)
print(a.get_favorite(1723464345))
print(a.get_security(1723464345))
print(a.get_subscription(1723464345))
print(time.time()-start)
'''

