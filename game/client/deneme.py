from tkinter import * 



board = Tk()
board.title("S0S")

# Variable that holds if user selected S or O.
choice = StringVar()

s = Radiobutton(board, text='S', variable=choice, value='S')
o = Radiobutton(board, text='O', variable=choice, value='O')
s.grid(row=3, column=0)
o.grid(row=4, column=0)

board.mainloop()