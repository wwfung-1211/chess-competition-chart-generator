"""Database queries, ID counters, and saved bracket data."""
import sqlite3
from config import DATABASE_PATH, IDS_PATH, BRACKET_PATH

def genid(table):
    """Read a counter: school=0, player=1, match=2, round=3, year=4."""
    with open(IDS_PATH) as file:
        return file.readlines()[table]


def addid(table):
    with open(IDS_PATH) as file:
        counters = file.readlines()
    counters[table] = f"{int(counters[table].strip()) + 1}\n"
    with open(IDS_PATH, "w") as file:
        file.writelines(counters)


def sql(column, table):
    """Fetch the first column of an internal SELECT query as a list."""
    con = sqlite3.connect(DATABASE_PATH)
    try:
        return [row[0] for row in con.execute(f"SELECT {column} FROM {table}")]
    finally:
        con.close()


def sort(list,order): #bubble sort, order=1 DESC, order=0 ASC
    c=list
    a=len(c)
    if order==1: #DESC
        for k in range (a-1):
            for i in range (a-1-k):
                if int(c[i+1])>int(c[i]):
                    temp=c[i]
                    c[i]=c[i+1]
                    c[i+1]=temp
    else: #ASC
        for k in range (a-1):
            for i in range (a-1-k):
                if int(c[i+1])<int(c[i]):
                    temp=c[i]
                    c[i]=c[i+1]
                    c[i+1]=temp
    return c

def write(x):
    with open(BRACKET_PATH, "w") as file:
        for row in x:
            row_str = " ".join(str(x) for x in row)
            file.write(row_str + "\n")
        file.close()
def save():
    with open(BRACKET_PATH, "r") as file:
        rows = [line.split() for line in file.readlines()]
        nlist = [[str(x) for x in row] for row in rows]
    return nlist

def inputsql(round): #input the result of each round into the comp{year} database
    year = int(genid(4))
    con = sqlite3.connect(DATABASE_PATH)
    cur = con.cursor()
    nlist=save()
    newlist=nlist[round]
    print(newlist)
    for i in range(0,len(newlist),2):
        cid=genid(2)
        paid=newlist[i]
        pbid=newlist[i+1]
        if paid=="bye":
            result=0
        elif pbid=="bye":
            result=1
        else:
            result="NULL"
        check=cur.execute(f"SELECT cid FROM comp{year} WHERE PAID='{paid}' AND PBID = '{pbid}'")
        check=check.fetchone()
        if not check:
            cur.execute(f"""INSERT INTO comp{year} VALUES("{cid}","{paid}","{pbid}",{result},{round+1})""")
            con.commit()
            addid(2)
