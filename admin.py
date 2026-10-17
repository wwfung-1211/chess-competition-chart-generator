"""Admin actions extracted from the notebook; callable from the launcher."""
import sqlite3
import math
from config import ADMIN_PASSWORD, DATABASE_PATH, IDS_PATH, COMPETITORS_PATH, DATA_DIR
from storage import genid, addid, sql, sort, write, save, inputsql

compover = False


def generate_competition():
    global compover
    year = int(genid(4))
    #Admin: update participating players (admin should run this cell before generating table)
    pw=input("Input admin password to update results")
    for i in range(4):
        if pw!=ADMIN_PASSWORD:
            print (f"Password is incorrect. There is {4-i} try(s) left.")
            pw=input("Input admin password to update results")
        if pw==ADMIN_PASSWORD:
            import sqlite3
            con = sqlite3.connect(DATABASE_PATH)
            cur = con.cursor()
            with open(COMPETITORS_PATH, "r") as file:
                clist = [line.strip() for line in file]
            clist=sort(clist,0)
            if len(clist) < 2:
                print("At least two enrolled players are required.")
                con.close()
                return
            compover = False
    
            #generate competition table (Do not run this after table is generated)
            id=open(IDS_PATH,"r")
            id.seek(0)
            id= id.readlines()
            id[3] = str(1)+'\n'
            id[2] = str(1)+'\n'
            nid=open(IDS_PATH,"w")
            nid.writelines(id)
            nid.close()
            
            cur.execute(f"""DELETE FROM comp{year}""")
            con.commit()
            a=[]
            b=[]
            seedlist=sql("PID","player WHERE SEED = TRUE AND ENROLL= TRUE")
            sseedlist=sql("SID","player WHERE SEED = TRUE AND ENROLL= TRUE")
            import math
            import random
            n=len(clist) #no.of participants
            try:
                nround= math.ceil(math.log(n,2)) #no.of rounds required
            except ValueError:
                print("The enrollment has not started yet")
                break
            # find player that are in school with 2 players
            ptwo=sql("PID",f"player WHERE SID IN (SELECT SID FROM player WHERE ENROLL = TRUE GROUP BY SID HAVING COUNT(SID) = 2) AND ENROLL = TRUE ORDER BY SID ASC") 
            rand= random.randint(0,1)
            asp=0
            bsp=0
            for i in range(0,len(ptwo),2):
                if ptwo[i] in seedlist and ptwo[i+1] not in seedlist: #make sure the seed player are evenly distributed to a and b
                    if bsp>asp:
                        a.append(ptwo[i])
                        b.append(ptwo[i+1])
                        asp=asp+1
                    else:
                        b.append(ptwo[i])
                        a.append(ptwo[i+1])
                        bsp=bsp+1
                elif ptwo[i] not in seedlist and ptwo[i+1] in seedlist: 
                    if bsp>asp:
                        b.append(ptwo[i])
                        a.append(ptwo[i+1])
                        asp=asp+1
                    else:
                        a.append(ptwo[i])
                        b.append(ptwo[i+1])
                        bsp=bsp+1
                else:
                    b.append(ptwo[i])
                    a.append(ptwo[i+1])                              
                clist.remove(ptwo[i])
                clist.remove(ptwo[i+1])
            if len(a)>len(b):
                along=True
            else:
                along=False
            #remove the seed players already in the lists 
            r=0
            aseed=[]
            bseed=[]
            for i in range(len(sseedlist)):
                if seedlist[r] in a:
                    aseed.append(seedlist[r])
                    a.remove(seedlist[r])
                    seedlist.remove(seedlist[r])
                    r=r-1
                elif seedlist[r] in b:
                    bseed.append(seedlist[r])
                    b.remove(seedlist[r])
                    seedlist.remove(seedlist[r])
                    r=r-1
                r=r+1
            for i in range(len(seedlist)):
                clist.remove(seedlist[i])
            random.shuffle(clist)
            print (a,b,aseed,bseed,clist)
    
            for i in range (len(clist)):
                if i%2==0:
                    if along==True:
                        b.append(clist[i])
                    else:
                        a.append(clist[i])
                else:
                    if along==True:
                        a.append(clist[i])
                    else:
                        b.append(clist[i])
            random.shuffle(a)
            random.shuffle(b)
            random.shuffle(seedlist)
            for i in range(len(seedlist)):
                if len(aseed)>len(bseed):
                    bseed.append(seedlist[i])
                else:
                    aseed.append(seedlist[i])
            random.shuffle(aseed)
            random.shuffle(bseed)
            if len(aseed)>=1:
                a.insert(0,aseed[0])
            if len(aseed)>=2:
                a.append(aseed[1])
            if len(bseed)>=1:
                b.insert(0,bseed[0])
            if len(bseed)>=2:
                b.append(bseed[1])
          
            for i in range (2**(nround-1)-len(a)):
                a.insert(2*i,"bye")
    
            for i in range (2**(nround-1)-len(b)):
                b.insert(2*i,"bye")
    
            newlist=a+b
            nlist=[newlist]
            for i in range(nround-1):
                list=[]
                nlist.append(list)
            write(nlist)
    
            inputsql(0)
            break


def update_results():
    global compover
    year = int(genid(4))
    #Admin: Update results
    con = sqlite3.connect(DATABASE_PATH)
    cur = con.cursor()
    cid=input("Input competition id code the save the results")
    r=input("Input the winner side")
    
    while r!="A" and r!="B":
        print("Invalid input")
        r=input("Input the winner side")
    pw=input("Input admin password to update results")
    for i in range(4):
        if pw!=ADMIN_PASSWORD:
            print (f"Password is incorrect. There is {4-i} try(s) left.")
            pw=input("Input admin password to update results")
        if pw==ADMIN_PASSWORD:
            if r=="A":
                result="TRUE"
            elif r=="B":
                result="FALSE"
            cid=cid+"\n"
            cvalid=cur.execute(f"SELECT CID FROM comp{year} WHERE CID='{cid}'")
            cvalid=cvalid.fetchone()
            cnull=cur.execute(f"SELECT CID FROM comp{year} WHERE CID='{cid}' AND RESULT IS NULL")
            cnull=cnull.fetchone()
            if not cvalid:
                print("Competition id input is invalid")
            elif not cnull:
                print("Repeated result of the same competition is input")
            else:
                cur.execute(f"UPDATE comp{year} SET RESULT = {result} WHERE CID='{cid}'")
                print ("Result has been successfully updated")
                con.commit()
            break
    


def next_round():
    global compover
    year = int(genid(4))
    #Admin: Next round
    import sqlite3
    import math
    con = sqlite3.connect(DATABASE_PATH)
    cur = con.cursor()
    check=cur.execute(f"SELECT CID FROM comp{year} WHERE RESULT IS NULL ")
    check=check.fetchall()
    round=int(genid(3).strip())
    n= int(sql("COUNT(PAID)", f"comp{year} WHERE ROUND = 1")[0])*2
    if n == 0:
        print("Competition has not started.")
        return
    nround = math.ceil(math.log(n, 2))  # no.of rounds required
    nlist=save()
    pw=input("Input admin password to update results")
    for i in range(4):
        if pw!=ADMIN_PASSWORD:
            print (f"Password is incorrect. There is {4-i} try(s) left.")
            pw=input("Input admin password to update results")
        if pw==ADMIN_PASSWORD:
            if not check: 
                try:
                    r=sql("RESULT",f"comp{year} WHERE ROUND={round}")
                    a=sql("PAID",f"comp{year} WHERE ROUND={round}")
                    b=sql("PBID",f"comp{year} WHERE ROUND={round}")
                    for i in range(len(r)):
                        if r[i]==1:
                            if round==nround :
                                winner=a[i]
                            else:
                                nlist[round].append(a[i]) 
                        else:
                            if round==nround :
                                winner=b[i]
                            else:
                                nlist[round].append(b[i]) 
                    write(nlist)
                    inputsql(round)
                    addid(3) 
                    print (f"Round {round} has completed.")
                    compover=True
                except IndexError:
                    if compover==True:
                        cur = con.cursor()
                        print("The competition is over")
                        cur.execute(f"UPDATE player SET SEED = NULL")
                        cur.execute(f"UPDATE player SET ENROLL = NULL")
                        cur.execute(f"UPDATE player SET SEED = TRUE  WHERE PID IN (SELECT PAID FROM comp{year} WHERE ROUND = {nround-1}) OR PID IN (SELECT PBID FROM comp{year} WHERE ROUND = {nround-1})")
                        con.commit()
                        #add year
                        addid(4)
                        id=open(IDS_PATH,"r")
                        id.seek(0)
                        id= id.readlines()
                        id[2] = "1\n"        
                        id[3] = "1\n"
                        nid=open(IDS_PATH,"w")
                        nid.writelines(id)
                        nid.close()
                        #delete all data in text files
                        def deltxtdata(x):
                            k=open(DATA_DIR / f"{x}.txt","w")
                            k.writelines("")
                            k.close()
                        deltxtdata("competitorlist")
                        deltxtdata("list")
                        deltxtdata("array")
                        #create a new database
                        con = sqlite3.connect(DATABASE_PATH)
                        cur = con.cursor()
                        cur.execute(f"""
                            CREATE TABLE comp{year+1}(
                                CID CHAR PRIMARY KEY,
                                PAID CHAR,
                                PBID CHAR,
                                RESULT BOOLEAN,
                                ROUND INT,
                                FOREIGN KEY (PAID) REFERENCES player(PID),
                                FOREIGN KEY (PBID) REFERENCES player(PID)
                            );
                        """)
                        con.commit()
                        year=year+1
                        compover=False
                    else:
                        print("Competition has not started.")
            else:
                print(f"Round {round} has not completed.")
            break
        

