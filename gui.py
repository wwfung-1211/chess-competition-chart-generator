"""Build and run the user platform."""
from theme import NAVY, CREAM, button as themed_button, apply_theme
from storage import genid, sql
from registration import sreg_window, preg_window, creg_window
from bracket import window


def run():
    year = int(genid(4))
    #User Platform Window
    import tkinter as tk
    import sqlite3
    main = tk.Tk()
    apply_theme(main)
    main.title(f"Chess Competition")
    main.geometry('500x500')
    compList = sql("name","sqlite_master WHERE type = 'table' AND NAME LIKE 'comp%'")
    enroll=True
    if sql("CID",f"comp{year}") == []:
        compList.remove(f"comp{year}")
    else:
        enroll=False
    comp = tk.StringVar()
    comp.set('')
    
    frame=tk.Frame(main,bg=NAVY)
    frame.pack(fill="both",expand = True)
    mainframe=tk.Frame(frame,bg=CREAM)
    mainframe.pack(pady=20, anchor="center")
    title=tk.Label(mainframe,text="Chess Competition Platform", padx=10, pady=10,font=("Georgia",20,"bold"), bg=CREAM)
    title.pack(anchor="center", pady=(20, 20))
    sreg=themed_button(mainframe,text="Register a school account", command=lambda: sreg_window(main),font=("Georgia",10), padx=10, pady=5, bg=NAVY, fg="#fff")
    sreg.pack(anchor="center", pady=(0, 20))
    preg=themed_button(mainframe,text="Register a player account",command=lambda: preg_window(main),font=("Georgia",10), padx=10, pady=5, bg=NAVY, fg="#fff")
    preg.pack(anchor="center", pady=(0, 20))
    if enroll == True:
        creg=themed_button(mainframe,text=f"Enroll for the competition {year}",command=lambda: creg_window(main),font=("Georgia",10), padx=10, bg=NAVY, fg="#fff")
        creg.pack(anchor="center", pady=(0, 20))
    try:
        label=tk.Label(mainframe,text="Year of the competition chart", padx=10, pady=5,font=("Georgia",10), bg=CREAM)
        smenu = tk.OptionMenu(mainframe,comp, *compList)
        label.pack(anchor="center", pady=(10, 5))
        smenu.pack(pady=(0, 12))
        creg=themed_button(mainframe,text="Check",command=lambda: window(main, mainframe, comp),font=("Georgia",10), padx=10, bg=NAVY, fg="#fff")
        creg.pack(anchor="center", pady=(0, 20))
    except TypeError:
        pass
    main.mainloop()
