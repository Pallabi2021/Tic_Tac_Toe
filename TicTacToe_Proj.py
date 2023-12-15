import random
import tkinter as tk
from tkinter import messagebox


def pos(n):
    return [(n - 1) // 3, (n - 1) % 3] #The pos function takes an integer n as input
                                       # (which represents the position number on the Tic-Tac-Toe board) and
                                       # returns the corresponding row and column as a list of two coordinates


def win(b, x): #checks if player 'x' wins or not acc to that returns True or False
    for i in range(3):
        if b[i][0] == b[i][1] == b[i][2] == x: #HORIZONTAL
            return True
        if b[0][i] == b[1][i] == b[2][i] == x: #VERTICAL
            return True
    if b[0][0] == b[1][1] == b[2][2] == x: #DIAGONAL
        return True
    if b[0][2] == b[1][1] == b[2][0] == x: #DIAGONAL
        return True
    return False


def is_draw(b): #checks if no empty position left on board that means draw
    for i in range(3):
        for j in range(3):
            if b[i][j] == "N":
                return False
    return True


class TTT: #
    def __init__(self, x): #constructor that initializes the game
        self.pc = x #when player chooses x comp chooses o and viceversa
        self.cc = "o" if x == "x" else "x"
        self.board = [["N" for _ in range(3)] for _ in range(3)]  #self.grid is 3x3 grid
        #[["N" for _ in range(3)] creates list of 3 eles initialized with "N". '_' is throwaway var used as loop var isnt req. O/p= ["N",  "N","N"]
        #for _ in range(3) creates 3 lists ie Final o/p= ["N", "N", "N"]
        #                                                ["N", "N", "N"]
        #                                                ["N", "N", "N"]

    def make_move(self, row, col): #Method is used to make a move by player
        if self.board[row][col] == "N": #if pos chosen by player empty then move is success ie True else False
            self.board[row][col] = self.pc
            return True
        else:
            return False

    def c_m(self): #Method is used to make a move by comp.It prioritizes winning the game or blocking the player from winning.
                   # If these are not possible, it tries to take corners or the center.
                   # If none of these options are available, it makes a random move.

        c = [] #a list that is currently empty that will store all the pos that are empty on board and are available to make move
        b = [row[:] for row in self.board] #creates copy of curr board 'b'. it helps in making poss moves without modifying actual board

        for i in range(3): #outer loop iterates over rows
            for j in range(3): #inner loop iterates over cols
                if self.board[i][j] == "N": #if the pos is empty then available for move so appended to list 'c'
                    c.append([i, j])

        #This part checks if player gonna win then blocks winning move
        for move in c: #iterates over each avail empty pos stored in c. 'move' is a list containing row n col indices of empty pos on board
            b[move[0]][move[1]] = self.cc #For each 'move' comp temporaily places player's choice(x or o) on copied board b to see if making this move will cause player to win
            if win(b, self.cc): #checks if curr move is a win condition for player
                self.board[move[0]][move[1]] = self.cc #if cond true then that means player will win so comp blocks the move on actual board
                return True  #comp made successful move to block player's winning move
            b[move[0]][move[1]] = "N"  #If curr move isnt win for player (cond is false)the temporary board b is reset back to its original state by setting the position at move back to 'N', indicating that the position is empty again


        #This part checks if comp can win on next move
        for move in c: #iterates over each avail empty pos stored in c. 'move' is a list containing row n col indices of empty pos on board
            b[move[0]][move[1]] = self.pc#For each 'move' comp temporaily places player's choice(x or o) on copied board b to see if making this move will cause comp to win
            if win(b, self.pc): #This condition checks if the current move results in a win for the computer
                self.board[move[0]][move[1]] = self.cc #if true then current move is a win for the comp so the actual game board (self.board) is updated with the computer's choice (self.cc)
                return True #True to indicate that the comp made a successful move and won the game
            b[move[0]][move[1]] = "N" #If curr move isnt win for comp(cond is false)the temporary board b is reset back to its original state by setting the position at move back to 'N', indicating that the position is empty again


        #Corners are often considered strategic positions in Tic-Tac-Toe as they create winning patterns compared to other positions.
        #The computer checks if any of the corner positions are empty and, if so, takes one of them as its move,
        #returning True to indicate a successful move
        corners = [[0, 0], [0, 2], [2, 0], [2, 2]] #list that contains the coordinates of all corner positions on the board.
        for move in corners: # It will go through all four corner positions one by one
            if move in c:   #checks if the curr corner move is in the list c that contains the coordinates of all available empty positions on the board. So, this condition checks if the current corner position is empty.
                self.board[move[0]][move[1]] = self.cc
                return True   # indicate that the computer has made a successful move in one of the corners

        #If the center position is empty ('N'), the computer chooses it, places its choice there, and returns True
        if self.board[1][1] == "N":
            self.board[1][1] = self.cc
            return True

        #If none of the previous conditions are met,
        #the computer chooses a random empty position from the list c, places its choice there, and returns True
        move = random.choice(c)
        self.board[move[0]][move[1]] = self.cc
        return True


class TicTacToeGUI(tk.Tk): #The TicTacToeGUI class inherits from tk.Tk and represents the graphical user interface for the Tic-Tac-Toe game
    def __init__(self): #def __init__(self):: This is the constructor method of the TicTacToeGUI class
        super().__init__() #calls the constructor of the superclass (tk.Tk) to initialize the tkinter part of the GUI to set up the tkinter window properly.
        self.title("Tic Tac Toe AI") #sets the title of the tkinter window to "Tic Tac Toe AI"
        self.geometry("350x350")    #sets the initial size of the tkinter window to a width of 300 pixels and a height of 400 pixels
        self.resizable(False, False) # disables the ability to resize the tkinter window ie both arguments False means window cannot be resized in either the horizontal or vertical direction
        self.board_buttons = [[None for _ in range(3)] for _ in range(3)] #creates a 3x3 matrix of None values, representing the buttons that will display the Tic-Tac-Toe board.
        self.ttt = None #used to hold an instance of the TTT class
        self.player_turn = None #used to keep track of whether it's the player's turn to make a move
        self.create_widgets()  #calls the create_widgets() method to set up the initial widgets (buttons) on the tkinter window

    def create_widgets(self): ## Create the initial widgets (labels and buttons) for the player to choose 'x' or 'o'
        label = tk.Label(self, text="Choose 'x' or 'o':", font=("Arial", 16)) #creates a 'Label' widget assigns it to the var 'label' displays the text "Choose 'x' or 'o':" with a font size of 16 pixels
        label.pack(pady=10) #uses the pack geometry manager to place the label widget on the window. The pady=30 argument adds 10 pixels of vertical padding to the widget,pushing it down from the top of the window.

        x_button = tk.Button(self, text="x", font=("Arial", 14),width=5, height=2, command=self.start_game_x)  #creates a 'Button' widget assigns it to the var x_button n displays the text "x" and uses the start_game_x method as its callback
        x_button.pack(pady=50) #uses the pack geometry manager to place the x_button widget on the window. The pady=50 argument adds 5 pixels of vertical padding to the widget, pushing it down from the previous widget (the label)

        o_button = tk.Button(self, text="o", font=("Arial", 14),width=5, height=2, command=self.start_game_o) # creates a Button widget assigns to var o_button n displays the text "o" and uses the start_game_o method as its callback.
        o_button.pack(pady=20) #uses the pack geometry manager to place the o_button widget on the window. adds 5 pixels of vertical padding to the widget, pushing it down from the previous widget (the "x" button)

    #The start_game_x method is called when the player selects to play as 'x'
    def start_game_x(self):
        self.ttt = TTT("x") #creates an instance of the TTT class passes "x" as an argument to the TTT constructor, indicating that the player will be 'x' and the computer will be 'o'
        self.player_turn = True #indicating that it's the player's turn to make a move
        self.destroy_widgets() #The buttons for selecting 'x' or 'o' are no longer needed once the game has started so remove the initial widgets (buttons) from the tkinter window
        self.create_board() #create the new widgets (buttons) for the Tic-Tac-Toe game board

    # The start_game_x method is called when the player selects to play as 'o'
    def start_game_o(self):
        self.ttt = TTT("o")
        self.player_turn = False ##indicating that it's the comp's turn to make a move
        self.destroy_widgets()
        self.create_board()
        self.computer_move()

    #this uimethod sets up the widgets (buttons) representing the Tic-Tac-Toe game board
    def create_board(self):
        for row in range(3):
            for col in range(3):
                #creates a Button widget for each cell in the Tic-Tac-Toe board
                self.board_buttons[row][col] = tk.Button(
                    self, text="", font=("Arial", 24), width=5, height=2,  #text="": This sets the initial text of each button to an empty string. Since the game has just started, all buttons are empty.
                    command=lambda r=row, c=col: self.on_click(r, c)       # This line sets the callback function that will be executed when the button is clicked.
                                                                           # The lambda function is used to pass the current row and column indices (r and c) as arguments to the self.on_click method
                                                                           # This way, each button is associated with its specific row and column, allowing the on_click method to handle the player's move on the correct cell
                )
                self.board_buttons[row][col].grid(row=row, column=col, padx=5, pady=5) #uses the grid geometry manager to place each button at its corresponding row and column on the tkinter window

    #method is responsible for removing the initial widgets (buttons) from the tkinter window when the player chooses to start the game as 'x' or 'o'
    def destroy_widgets(self):
        for widget in self.winfo_children(): #starts a loop that iterates over all the child widgets of the main tkinter window returns a list of all the child widgets contained within the window.
            widget.destroy() # calls the destroy() method on each child widget

    #method is called when the player clicks on one of the buttons representing the Tic-Tac-Toe board cells
    #handles the player's move and checks for a win, draw, or updates the computer's move.
    def on_click(self, row, col):
        if not self.player_turn: # if it's not the player's turn to make a move. If it's not the player's turn, the method returns immediately, and nothing happens
            return

        if self.ttt.make_move(row, col):  #The make_move method returns True if the move is valid and the cell is empty
            self.board_buttons[row][col].config(text=self.ttt.pc) #If the move is valid, this line updates the text of the button  at the specified row and col on the tkinter window to the player's choice (self.ttt.pc)
            self.player_turn = False #indicating that it's now the computer's turn to make a move. prevents the player from making another move until the computer has made its move.

            if win(self.ttt.board, self.ttt.pc): #This line checks if the player has won the game by calling the win function
                self.show_winner("Player")
            elif is_draw(self.ttt.board):
                self.show_draw()
            else:
                self.computer_move()

    def computer_move(self):
        self.ttt.c_m()
        for row in range(3):
            for col in range(3):
                if self.ttt.board[row][col] == self.ttt.cc:
                    self.board_buttons[row][col].config(text=self.ttt.cc)

        if win(self.ttt.board, self.ttt.cc):
            self.show_winner("Computer")
        elif is_draw(self.ttt.board):
            self.show_draw()
        else:
            self.player_turn = True

    def show_winner(self, winner):
        messagebox.showinfo("Game Over", f"{winner} wins!")
        self.destroy()

    def show_draw(self):
        messagebox.showinfo("Game Over", "It's a draw!")
        self.destroy()


if __name__ == "__main__":
    app = TicTacToeGUI()
    app.mainloop()
