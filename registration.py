"""School registration, player registration, and enrollment windows."""
from theme import NAVY, CREAM, button as themed_button
import sqlite3
from config import DATABASE_PATH, COMPETITORS_PATH
from storage import genid, addid, sql

#Define Input Interface
#School Register
def sreg_window(main):
    import tkinter as tk
    import sqlite3
    con = sqlite3.connect(DATABASE_PATH)
    cur = con.cursor()
    sreg = tk.Toplevel(main)
    sreg.title("School Registration")
    sreg.geometry("500x500")
    sframe=tk.Frame(sreg,bg=CREAM)
    sframe.pack(fill="both",expand=True)
    global pslabeldestroy
    pslabeldestroy=False
    def get_text(): #when registration button is clicked
        sid=int(genid(0))
        sname= snamebox.get("1.0", "end-1c")
        checksid=cur.execute(f"SELECT SID FROM school WHERE SNAME ='{sname}'")
        checksid=checksid.fetchone()
        global pslabel
        global pslabeldestroy
        try:
            sname=int(sname)
            printtext="School name should not be a number"
        except ValueError:   
            if sname=="":
                printtext="This field should not be empty. Please enter again."
            elif "\n" in sname:
                printtext="School name should not be more than one line. "
            elif " "in sname:
                printtext="School name should not consist of spaces"
            elif checksid:
                printtext=f"School account was registered before. Your school account id code is {str(checksid[0])}."
            else:
                cur.execute(f"""INSERT INTO school VALUES("{sid}","{sname}")""")          
                con.commit()
                addid(0)
                printtext=f"Account is registered successfully. Your school ({sname}) account id code is :{sid}"
        if pslabeldestroy==True:
            pslabel.destroy()
        pslabel = tk.Label(sframe, text=printtext, font=("Georgia",10),bg=CREAM)
        pslabel.pack(pady=5)
        pslabel.config(text=printtext)
        pslabeldestroy=True
    label = tk.Label(sframe, text="Register a school account", font=("Georgia",15,"bold"), bg=CREAM)
    label.pack(pady=10)
    label = tk.Label(sframe, text="Insert your school name to register a school account (e.g. HYS,DBS)", bg=CREAM)
    label.pack(pady=5)
    snamebox = tk.Text(sframe, height=2, width=30,font=("Georgia",10))
    snamebox.pack(pady=5)
    button = themed_button(sframe, text="Register", command=get_text, font=("Georgia",10),padx=10,pady=5, bg=NAVY, fg="#fff")
    button.pack(pady=5)


#Player Registration   
def preg_window(main):
    import sqlite3
    import tkinter as tk
    con = sqlite3.connect(DATABASE_PATH)
    cur = con.cursor()
    preg = tk.Toplevel(main)
    preg.title("Player Registration")
    preg.geometry("500x500")
    pframe=tk.Frame(preg,bg=CREAM)
    pframe.pack(fill="both",expand=True)
    byear = tk.StringVar()
    byear.set('')
    bmList = [1,2,3,4,5,6,7,8,9,10,11,12]
    bmonth = tk.StringVar()
    bmonth.set('')
    bdList = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]
    bday = tk.StringVar()
    bday.set('')
    global pplabeldestroy 
    pplabeldestroy=False
    def get_text():#when register button is clicked
        pid= int(genid(1))
        import sqlite3
        con = sqlite3.connect(DATABASE_PATH)
        cur = con.cursor()
        global pplabel
        global pplabeldestroy 
        pname= pnamebox.get("1.0", "end-1c")
        sname=schoolname.get()
        by=byear.get()
        bm=bmonth.get()
        bd=bday.get()
        studentid=psidbox.get("1.0", "end-1c")

        checkstudent=cur.execute(f"SELECT player.PID FROM player,school WHERE player.SID=school.SID AND SNAME ='{sname}' AND STUDENTID='{studentid}'")
        checkstudent=checkstudent.fetchone()
        try:
            pname=int(pname)
            printtext="Player name should not be an integer"
            
        except ValueError: 
            try:
                by=int(by)
                bd=int(bd)
                bm=int(bm)
                age= int(today.year)-by
                if today.month==int(bm):
                    if today.day<int(bd):
                        age-=1
                if today.month<int(bm):
                    age-=1
                if bm in [4,6,9,11]:
                    maxday=30
                elif bm==2 and by%4==0:
                    maxday=29
                elif bm==2 and by%4!=0:
                    maxday=28
                else:
                    maxday=31        
                if pname=="":
                    printtext="Player name should not be empty. Please register again." 
                elif "\n" in pname:
                    printtext="Player name should contain 1 line only"
                elif sname=="":
                    printtext="School name should not be empty. Please register again." 
                elif studentid=="":
                    printtext="Student id should not be empty. Please register again." 
                elif "\n" in studentid:
                    printtext="Student id should contain 1 line only"
                elif " " in studentid:
                    printtext="Student id should not contain spaces"
                elif bd>maxday:
                    printtext="Date is invalid. Insert your day of birth (e.g.11)"
                elif age >=22 or age<13:
                    printtext="Participants should age between 13-21."
                elif checkstudent:
                    printtext=f"Player account was registered before. Your player account id code is {str(checkstudent[0])}."
                else:
                    ssid=cur.execute(f"SELECT SID FROM school WHERE SNAME ='{sname}'")
                    ssid=ssid.fetchone()
                    if bm<10:
                        bm=str("0")+str(bm)
                    if bd<10:
                        bd=str("0")+str(bd)
                    bdaystring=str(by)+"-"+str(bm)+"-"+str(bd)
                    cur.execute(f"""INSERT INTO player VALUES("{pid}","{studentid}","{pname}","{bdaystring}","{ssid[0]}",NULL,NULL)""") 
                    con.commit()
                    addid(1)
                    printtext=f"Your player ({pname}) account id code is :{pid}"
            except ValueError:
                printtext="Date of birth should not be empty. Please register again."
        if pplabeldestroy==True:
            pplabel.destroy()
        pplabel = tk.Label(pframe, text=printtext, font=("Georgia",10),bg=CREAM)
        pplabel.pack(pady=5)
        pplabel.config(text=printtext)
        pplabeldestroy= True
    import datetime
    today = datetime.date.today()
    snameList = sql("SNAME","school")
    schoolname = tk.StringVar()
    schoolname.set('')
    byList=[]
    for i in range(13,23):
        byList.append(today.year-i)
    label = tk.Label(pframe, text="Register a player account", font=("Georgia",15,"bold"), bg=CREAM)
    label.pack(pady=10)
    label = tk.Label(pframe, text="Insert your name to register a player account (e.g. Chris Wong)", bg=CREAM)
    label.pack(pady=5)
    pnamebox = tk.Text(pframe, height=2, width=30,font=("Georgia",10))
    pnamebox.pack(pady=5)
    label = tk.Label(pframe, text="Choose your school", bg=CREAM)
    label.pack(pady=5)
    smenu = tk.OptionMenu(pframe,schoolname, *snameList)
    smenu.pack()
    label = tk.Label(pframe, text="Enter your date of birth", bg=CREAM)
    label.pack(pady=5)
    menuframe=tk.Frame(pframe, bg=CREAM)
    menuframe.pack()
    smenu = tk.OptionMenu(menuframe,byear, *byList)
    smenu.pack(side="left")
    smenu= tk.OptionMenu(menuframe,bmonth, *bmList)
    smenu.pack(side="left")
    smenu = tk.OptionMenu(menuframe,bday, *bdList)
    smenu.pack(side="left")
    label = tk.Label(pframe, text="Insert your student id at school (e.g. s119001)", bg=CREAM)
    label.pack(pady=5)
    psidbox = tk.Text(pframe, height=2, width=30,font=("Georgia",10))
    psidbox.pack(pady=5)
    button = themed_button(pframe, text="Register", command=get_text, font=("Georgia",10),padx=10,pady=5, bg=NAVY, fg="#fff")
    button.pack(pady=5)


#Competition Enrollment
def creg_window(main):
    year = int(genid(4))
    import tkinter as tk
    con = sqlite3.connect(DATABASE_PATH)
    cur = con.cursor()
    creg = tk.Toplevel(main)
    creg.title("Competition enrollment")
    creg.geometry("500x500")
    cframe=tk.Frame(creg,bg=CREAM)
    cframe.pack(fill="both",expand=True)
    global pclabeldestroy
    pclabeldestroy=False
    def get_text(): #when enrollment button is clicked
        global pclabel
        global pclabeldestroy 
        with open(COMPETITORS_PATH, "r") as file:
            clist = [line.strip() for line in file]
        
        cpid= cpidbox.get("1.0", "end-1c")
        try:
            by=int(sql("SUBSTR(BDAY, 1, 4) ",f"player WHERE PID={cpid}")[0])
            bm=int(sql("SUBSTR(BDAY, 6, 2) ",f"player WHERE PID={cpid}")[0])
            bd=int(sql("SUBSTR(BDAY, 9, 2) ",f"player WHERE PID={cpid}")[0])  
            import datetime
            today = datetime.date.today()
            age= today.year-by
            if today.month==int(bm):
                if today.day<int(bd):
                    age-=1
            if today.month<int(bm):
                age-=1
            if age>21 or age<13:
                printtext="Player should age 13-21 to enroll this competition"
            elif cpid in clist:
                printtext="Player has already enrolled in this competition."
            else:
                sid=cur.execute(f"SELECT SID FROM player WHERE PID ='{cpid}'")
                sid=sid.fetchone()[0]
                csid=cur.execute(f"SELECT COUNT(SID) FROM player WHERE SID ='{sid}' AND ENROLL = TRUE")
                csid=csid.fetchone()[0]
                if csid==2:
                    printtext="A school can only enroll for two players."
                else:
                    clist.append(cpid)
                    cur.execute(f"UPDATE player SET ENROLL = TRUE WHERE PID={cpid}")
                    printtext= f"{cpid} has successfully enrolled in Chess Competition {year}"
                    con.commit()

        except sqlite3.OperationalError:
            printtext="Player id should not be null "
        except IndexError:
            printtext="Please input a valid player id. The input should consists of 1 line only"
        with open(COMPETITORS_PATH, "w") as file:
            file.writelines(f"{item}\n" for item in clist)
        file.close()
        if pclabeldestroy==True:
            pclabel.destroy()
        pclabel = tk.Label(cframe, text=printtext, font=("Georgia",10),bg=CREAM)
        pclabel.pack(pady=5)
        pclabel.config(text=printtext)
        pclabeldestroy= True

    label = tk.Label(cframe, text="Enroll the competition", font=("Georgia",15,"bold"), bg=CREAM)
    label.pack(pady=10)
    label = tk.Label(cframe, text="Insert your player id to enroll Chess Competition. \n Please make sure the age of the player is between 13-21", bg=CREAM)
    label.pack(pady=5)
    cpidbox = tk.Text(cframe, height=2, width=30,font=("Georgia",10))
    cpidbox.pack(pady=5)
    button = themed_button(cframe, text="Enroll", command=get_text, font=("Georgia",10),padx=10,pady=5, bg=NAVY, fg="#fff")
    button.pack(pady=5)

