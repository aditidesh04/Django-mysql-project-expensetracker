import pymysql

class TrackerServices:
        def addnewuser(self,uid,ps,nm,mob,age,gen,occ,ct):
            try:
                con=pymysql.connect(host='mysql-pythonprojects-python-apps1.b.aivencloud.com',port=22928,user='aditi',password='AVNS_DkXRQRjbF7hMmDla-e2',database='aditidb')
                curs=con.cursor()
                curs.execute(f"insert into users values('{uid}','{ps}','{nm}','{mob}',{age},'{gen}','{occ}','{ct}')")
                con.commit()
                msg="success"
                con.close()
            except:
                 msg='failed'
            return msg
        
        def checkuser(self,uid,ps):
            try:
                con=pymysql.connect(host='mysql-pythonprojects-python-apps1.b.aivencloud.com',port=22928,user='aditi',password='AVNS_DkXRQRjbF7hMmDla-e2',database='aditidb')
                curs=con.cursor()
                curs.execute(f"select * from users where userid='{uid}' and password='{ps}'")
                data=curs.fetchone()
                if data:
                    msg='success'
                else:
                    msg='failed'
                con.close()
            except:
                msg='failed'
            return msg
        
        def addnewexpense(self,uid,dt,cat,desc,amt,pay):
            try:
                con=pymysql.connect(host='mysql-pythonprojects-python-apps1.b.aivencloud.com',port=22928,user='aditi',password='AVNS_DkXRQRjbF7hMmDla-e2',database='aditidb')
                curs=con.cursor()
                curs.execute(f"insert into expenses (userid,expense_date,category,description,amount,paymentmode) values('{uid}','{dt}','{cat}','{desc}',{amt},'{pay}')")
                con.commit()
                msg='Expense entry recorded successfully'
                con.close()
            except:
                msg='Expense entry failed'
            return msg

        def changeuserpassword(self,uid,opass,npass1,npass2):
              if npass1==npass2:
                    
                    con=pymysql.connect(host='mysql-pythonprojects-python-apps1.b.aivencloud.com',port=22928,user='aditi',password='AVNS_DkXRQRjbF7hMmDla-e2',database='aditidb')
                
                    curs=con.cursor()
                    cnt=curs.execute(f"update users set password='{npass1}' where userid='{uid}' and password='{opass}'")
                    con.commit()
                    if cnt>0:
                        status="Password changed successfully"
                    else:
                        status="Current password incorrect"
                    con.close()
              else:
                status="New passwords mismatched"
              return status
        
        
                
        def searchexpondate(self,uid,sdt):
            con=pymysql.connect(host='mysql-pythonprojects-python-apps1.b.aivencloud.com',port=22928,user='aditi',password='AVNS_DkXRQRjbF7hMmDla-e2',database='aditidb')
            curs=con.cursor()
            curs.execute(f"select * from expenses where userid='{uid}' and expense_date='{sdt}'")
            data=curs.fetchall()
            con.close()
            return data
        
        def modification(self, uid, sdt, category, desc, amount, paymentmode):
    # connect to DB
                con=pymysql.connect(host='mysql-pythonprojects-python-apps1.b.aivencloud.com',port=22928,user='aditi',password='AVNS_DkXRQRjbF7hMmDla-e2',database='aditidb')
                curs = con.cursor()

                # Update query
                sql = f"""
                    UPDATE expenses 
                    SET category='{category}', 
                        description='{desc}', 
                        amount='{amount}', 
                        paymentmode='{paymentmode}'
                    WHERE userid='{uid}' AND expense_date='{sdt}'
                """

                cnt = curs.execute(sql)
                con.commit()
                con.close()

                if cnt > 0:
                    return "Expense updated successfully"
                else:
                    return "Update failed – No matching record found"






                  