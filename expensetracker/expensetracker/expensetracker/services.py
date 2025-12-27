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



        def getAllExpenses(self, uid):
              con=pymysql.connect(host='mysql-pythonprojects-python-apps1.b.aivencloud.com',port=22928,user='aditi',password='AVNS_DkXRQRjbF7hMmDla-e2',database='aditidb')
              curs = con.cursor()
            #   curs.execute(f"select * from expenses where userid='{uid}'")
              curs.execute("SELECT expense_date, category, description, amount, paymentmode FROM expenses WHERE userid=%s",(uid,) )
              data=curs.fetchall()
              con.close()
              return data

        def generateReports(self, uid, start_date=None, end_date=None, category=None):
            # Connect to database
            try:
                con=pymysql.connect(host='mysql-pythonprojects-python-apps1.b.aivencloud.com',port=22928,user='aditi',password='AVNS_DkXRQRjbF7hMmDla-e2',database='aditidb')
                curs = con.cursor()
                
                # Start building SQL query - always filter by userid
                query = "SELECT expense_date, category, description, amount, paymentmode FROM expenses WHERE userid=%s"
                params = [uid]
                
                # Add date filters if provided
                if start_date:
                    query += " AND expense_date >= %s"
                    params.append(start_date)
                
                if end_date:
                    query += " AND expense_date <= %s"
                    params.append(end_date)
                
                # Add category filter if provided
                if category:
                    query += " AND category = %s"
                    params.append(category)
                
                # Sort by date, newest first
                query += " ORDER BY expense_date DESC"
                
                # Execute query and get all results
                curs.execute(query, tuple(params))
                data = curs.fetchall()
                con.close()
                
                # Calculate total amount
                total_amount = 0
                for row in data:
                    total_amount = total_amount + float(row[3])
                
                # Calculate amount per category
                category_totals = {}
                for row in data:
                    cat = row[1]  # category is at index 1
                    amt = float(row[3])  # amount is at index 3
                    if cat in category_totals:
                        category_totals[cat] = category_totals[cat] + amt
                    else:
                        category_totals[cat] = amt
                
                # Return all data
                return {
                    'expenses': data,
                    'total_amount': total_amount,
                    'category_totals': category_totals,
                    'total_count': len(data)
                }
            except:
                # If error occurs, return empty data
                return {
                    'expenses': [],
                    'total_amount': 0,
                    'category_totals': {},
                    'total_count': 0
                }

        def deleteExpense(self, uid, expenseid):
            try:
                con=pymysql.connect(host='mysql-pythonprojects-python-apps1.b.aivencloud.com',port=22928,user='aditi',password='AVNS_DkXRQRjbF7hMmDla-e2',database='aditidb')
                curs = con.cursor()
                # Delete expense only if it belongs to the user
                curs.execute("DELETE FROM expenses WHERE expenseid=%s AND userid=%s", (expenseid, uid))
                cnt = curs.rowcount
                con.commit()
                con.close()
                if cnt > 0:
                    return "Expense deleted successfully"
                else:
                    return "Delete failed – Expense not found or unauthorized"
            except Exception as e:
                return f"Delete failed – Error: {str(e)}"

        




                  