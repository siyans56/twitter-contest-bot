from tkinter import *

def printtext():
    global E1
    string = E1.get()
    print(string)

'''
TODO:
- Lay out all the inputs I'd want (main window, setup window + tutorial)
- Lay out all the outputs I'd want to give (console? Log of whats being tweeted, etc.)
- See how to package as an executable
'''

#widget code...
top = Tk()
L1 = Label(top, text = "User Name")
L1.pack(side = RIGHT)
E1 = Entry(top, bd = 5)
E1.pack(side = LEFT)
w = Frame(top, bg="red", cursor = 'dot', height = 600, width = 600)
w.pack(side = LEFT)

B1 = Button(top, text = "Say Hello")


b = Button(top, text= 'okay',command = printtext)
b.pack(side = RIGHT)

# m1 = PanedWindow()
# m1.pack(fill=BOTH, expand=1)
#
# left = Label(m1, text="left pane")
# m1.add(left)
#
# m2 = PanedWindow(m1, orient=VERTICAL)
# m1.add(m2)
#
# bot = Label(m2, text="top pane")
# m2.add(bot)
#
# bottom = Label(m2, text="bottom pane")
# m2.add(bottom)


top.mainloop()


#Current Problems
#woot now we experiment
