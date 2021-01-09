from tkinter import * 

def initialize(control):
    root = Tk()  
    # Code to add widget will go here…….. 
    for i in range(control.game.col):
        for j in range(control.game.row):
            w = Label(root, text = control.game.board[i][j], width = "40", height = "15")  
            w.grid(row = i, column=j)  
    root.mainloop()