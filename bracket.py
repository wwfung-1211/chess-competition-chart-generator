"""Render the competition bracket in a Tkinter window."""
from theme import CREAM, WINNER, LOSER, PENDING
import sqlite3
from storage import sql

#Define Output Interface (competition table)
def window(main, mainframe, comp):
    import tkinter as tk
    import math
    
    oyear=comp.get() #get the year of table to be viewed by user
    try:
        oyear=int(oyear[4:8])
        n= int(sql("COUNT(PAID)", f"comp{oyear} WHERE ROUND = 1")[0])*2
        nround = math.ceil(math.log(n, 2))  # no.of rounds required
        win = tk.Toplevel(main)
        win.title(f"Chess Competition{oyear}")
        win.geometry('500x500')
        cframe = tk.Frame(win)
        cframe.pack(fill="both", expand=True,side="top")
        title=tk.Label(cframe,text=f"Chess Competition {oyear}", font=("Georgia",20,"bold"), justify="left",bg=CREAM)
        title.pack(fill="x")
        canva = tk.Canvas(cframe,  bg=CREAM)
        try:
            oldn= int(sql("COUNT(PAID)", f"comp{oyear-1} WHERE ROUND = 1")[0])*2
            oldnround = math.ceil(math.log(oldn, 2))        
            seed=sql("PAID",f"comp{oyear-1} WHERE ROUND = {oldnround-1}")+sql("PBID",f"comp{oyear-1} WHERE ROUND = {nround-1}")
        except sqlite3.OperationalError:
            seed=[]
        rowt=0
        column=0
        n=0
        compid=1
        for k in range (nround):
            paid=sql("PAID",f"comp{oyear} WHERE ROUND = {k+1}")
            pbid=sql("PBID",f"comp{oyear} WHERE ROUND = {k+1}")
            if k>=1:
                texta= "─────────┐\n"
                for p in range((2**(k))-k):
                    texta+="                        │\n"
                texta +="                        │────────────\n"
                for p in range((2**(k))-k):
                    texta+="                        │\n"
                texta +="─────────┘"
            for j in range(0, len(paid)):
                import datetime
                today = datetime.date.today()
                try:
                    bda=sql("BDAY",f"player WHERE PID = {paid[j]}")[0]
                    bya=int(bda[0:4])
                    bdaa=int(bda[5:7])
                    bma=int(bda[8:10])
                    agea= int(today.year)-bya
                    if today.month==int(bma):
                        if today.day<int(bdaa):
                            agea-=1
                    if today.month<int(bma):
                        agea-=1
                except sqlite3.OperationalError:
                    agea=""
                try:
                    bdb=sql("BDAY",f"player WHERE PID = {pbid[j]}")[0]
                    byb=int(bdb[0:4])
                    bdbb=int(bdb[5:7])
                    bmb=int(bdb[8:10])
                    ageb= int(today.year)-byb
                    if today.month==int(bmb):
                        if today.day<int(bdbb):
                            ageb-=1
                    if today.month<int(bmb):
                        ageb-=1
                except sqlite3.OperationalError:
                    ageb=""
                resultcolour=sql("RESULT",f"comp{oyear} WHERE CID='{compid}\n'")
                if not resultcolour:
                    coloura=PENDING
                    colourb=PENDING
                elif resultcolour[0]==1:
                    coloura=WINNER
                    colourb=LOSER
                elif resultcolour[0]==0:
                    coloura=LOSER
                    colourb=WINNER
                else:
                    coloura=PENDING
                    colourb=PENDING
                compid=compid+1
                
                if paid[j] != "bye":
                    namea = sql("PNAME", f"player WHERE PID = '{paid[j]}'")
                    schoola = sql("SNAME", f"school,player WHERE player.sid=school.sid AND PID = '{paid[j]}'")
                    try:
                        namea = namea[0]
                        schoola = schoola[0]
                        if paid[j] in seed:
                            namea=namea+"*"
                    except IndexError:
                        break

                else:
                    namea = "bye"
                    schoola = ""
                
                if pbid[j] != "bye":
                    nameb = sql("PNAME", f"player WHERE PID = '{pbid[j]}'")
                    schoolb = sql("SNAME", f"school,player WHERE player.sid=school.sid AND PID = '{pbid[j]}'")
                    try:
                        nameb = nameb[0]
                        schoolb = schoolb[0]
                        if pbid[j] in seed:
                            nameb=nameb+"*"
                    except IndexError:
                        break
                else:
                    nameb = "bye"
                    schoolb = ""
                frame = tk.Frame(canva, borderwidth=1,padx=10,bg=f"{coloura}")
                canva.create_window((column*80, rowt* 50), window=frame, anchor="nw")
                text = tk.Label(frame, text=f"{namea} ({agea})\n{schoola}",bg=f"{coloura}", font=("Georgia", 12), width=18, fg='white')
                text.grid(row=0, column=0)
                
                #draw line
                canva.create_line(column*80+200, rowt*50+25, column*80+280, rowt*50+25, fill="black", width=2) 
                canva.create_line(column*80+280, rowt*50+25, column*80+280, (rowt+2**k)*50+25, fill="black", width=2)
                canva.create_line(column*80+280, ((rowt*50+25)+((rowt+2**k)*50+25))/2, column*80+440, ((rowt*50+25)+((rowt+2**k)*50+25))/2, fill="black", width=2) 
                rowt+=2**k
                canva.create_line(column*80+200, rowt*50+25, column*80+280, rowt*50+25, fill="black", width=2) 
                
                frame = tk.Frame(canva, padx=10,bg=f"{colourb}")
                canva.create_window((column*80, rowt* 50), window=frame, anchor="nw")
                text = tk.Label(frame, text=f"{nameb} ({ageb})\n{schoolb}",bg=f"{colourb}", font=("Georgia", 12), width=18, fg='white')
                text.grid(row=0, column=0)
                rowt+=2**k

            
            column+=4.5
            rowt=0.5*(2*n+1)
            n=2*n+1

        #display winner
        try:
            import datetime
            today = datetime.date.today()
            wid=sql("PAID",f"comp{oyear} WHERE ROUND={nround} AND RESULT=TRUE")[0]
            bdw=sql("BDAY",f"player WHERE PID = {wid}")[0]
            byw=int(bdw[0:4])
            bdww=int(bdw[5:7])
            bmw=int(bdw[8:10])
            agew= int(today.year)-byw
            if today.month==int(bmw):
                if today.day<int(bdww):
                    agew-=1
            if today.month<int(bmw):
                agew-=1
            wname=sql("PNAME",f"player WHERE PID={wid}")[0]
            wschool=sql("SNAME",f"player,school WHERE PID={wid} AND player.SID=school.SID")[0]
            frame = tk.Frame(canva, padx=10, bg=WINNER)
            canva.create_window((column*80, rowt* 50), window=frame, anchor="nw")
            text = tk.Label(frame, text=f"{wname} ({agew})\n{wschool}",bg=WINNER, font=("Georgia", 12), width=18, fg="white")
            text.grid(row=0, column=0)
        except IndexError:
            try:
                wid=sql("PBID",f"comp{oyear} WHERE ROUND={nround} AND RESULT=FALSE")[0]
                bdw=sql("BDAY",f"player WHERE PID = {wid}")[0]
                byw=int(bdw[0:4])
                bdww=int(bdw[5:7])
                bmw=int(bdw[8:10])
                agew= int(today.year)-byw
                if today.month==int(bmw):
                    if today.day<int(bdww):
                        agew-=1
                if today.month<int(bmw):
                    agew-=1
                wname=sql("PNAME",f"player WHERE PID={wid}")[0]
                wschool=sql("SNAME",f"player,school WHERE PID={wid} AND player.SID=school.SID")[0]
                frame = tk.Frame(canva, padx=10, bg=WINNER)
                canva.create_window((column*80, rowt* 50), window=frame, anchor="nw")
                text = tk.Label(frame, text=f"{wname}\n{wschool}",bg=WINNER, font=("Georgia", 12), width=18, fg="white")
                text.grid(row=0, column=0)
            except IndexError:
                pass


                
        scrollX = tk.Scrollbar(cframe, orient='horizontal')
        scrollX.pack(side='bottom', fill='x')
        scrollX.config(command=canva.xview)
        scrollY = tk.Scrollbar(cframe, orient='vertical')
        scrollY.pack(side='right', fill='y')
        scrollY.config(command=canva.yview)
        canva.config(xscrollcommand=scrollX.set, yscrollcommand=scrollY.set)
        cframe.update_idletasks()
        canva.configure(scrollregion=canva.bbox("all"))
        canva.pack(side="left",  fill="both", expand=True)
        end=tk.Label(win,text="(age) *Seed Players", font=("Georgia",12), justify="left",bg=CREAM)
        end.pack(fill="x", side="left")

    except ValueError:
        label = tk.Label(mainframe, text="Please choose a year", font=("Georgia",10),bg=CREAM)
        label.pack(pady=5)
        label.config(text="Please choose a year") 
