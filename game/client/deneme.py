from tkinter import * 



board = Tk()
board.title("S0S")

# Variable that holds if user selected S or O.
choice = StringVar()

s = Radiobutton(board, text='S', font=(None, 20), variable=choice, value='S')
o = Radiobutton(board, text='O', font=(None, 20), variable=choice, value='O')
s.grid(row=3, column=0, padx=20, pady=20)
o.grid(row=4, column=0, padx=20, pady=20)

a=Button(board, text="Pick S", font=(None, 20), command = S, width="5", height="2")
a.grid(row=5, column=0, padx=5, pady=5)
b=Button(board, text="Pick S", font=(None, 20), command = S, width="5", height="2")
b.grid(row=6, column=0, padx=5, pady=5)
a["state"] = "disabled"

board.mainloop()