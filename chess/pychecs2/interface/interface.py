"""
This file allows to understand how to inherit a tkinter widget, to draw
a chessboard in a Canvas, then determine which box has been selected.

"""

import pickle, webbrowser
from tkinter import NSEW, Canvas, Label, Tk, messagebox, Menu, Button

# Exemple d'importation de la classe Partie.
from pychecs2.echecs.game import Game, NoPieceInPosition, WrongColorException
from pychecs2.echecs.chess_board import MoveException


class CanvasChessboard(Canvas):
    """
    Class inheriting a Canvas, and displaying a chessboard that resizes automatically when
    the window is stretched.

    """

    def __init__(self, parent, n_pixels_per_box, game):
        # Number of rows and columns
        self.n_rows = 8
        self.n_columns = 8

        # Name of rows and columns
        self.row_numbers = ["1", "2", "3", "4", "5", "6", "7", "8"]
        self.col_letters = ["a", "b", "c", "d", "e", "f", "g", "h"]

        self.boxes_list = []

        #Selected Position
        self.selected_position = None

        # Game
        self.game = game

        # Number of pixels per box, variable.
        self.n_pixels_per_box = n_pixels_per_box

        # Calling the constructor of the base class (Canvas).
        # Width and height are determined according to the number of boxes.
        super().__init__(
            parent,
            width=self.n_rows * n_pixels_per_box,
            height=self.n_columns * self.n_pixels_per_box,
        )

        # Dictionary containing the pieces. 
        self.pieces = {
            "a1": "TB",
            "b1": "CB",
            "c1": "FB",
            "d1": "DB",
            "e1": "RB",
            "f1": "FB",
            "g1": "CB",
            "h1": "TB",
            "a2": "PB",
            "b2": "PB",
            "c2": "PB",
            "d2": "PB",
            "e2": "PB",
            "f2": "PB",
            "g2": "PB",
            "h2": "PB",
            "a7": "PN",
            "b7": "PN",
            "c7": "PN",
            "d7": "PN",
            "e7": "PN",
            "f7": "PN",
            "g7": "PN",
            "h7": "PN",
            "a8": "TN",
            "b8": "CN",
            "c8": "FN",
            "d8": "DN",
            "e8": "RN",
            "f8": "FN",
            "g8": "CN",
            "h8": "TN",
        }

        # Variable that allows to switch between 2 themes via sms()
        self.theme = 0
        # List that will store the performed movements
        self.moves_done = []

        # We make sure that resizing the canvas resizes its content. This event is also
        # generated when creating the window, we don't have to draw the boxes and pieces in the
        # builder.
        self.bind("<Configure>", self.resize)

    def change_theme(self):
        if self.theme == 1:
            theme = 0
            self.draw_boxes(theme)

        else:
            theme = 0
            self.draw_boxes(theme)
        self.refresh()

    def draw_boxes(self, theme):
        """
        Method that draws the boxes on the chessboard.
        """

        for i in range(self.n_rows):
            for j in range(self.n_columns):
                row_start = i * self.n_pixels_per_box
                row_end = row_start + self.n_pixels_per_box
                col_start = j * self.n_pixels_per_box
                col_end = col_start + self.n_pixels_per_box
                color = ""
                # We determine the color.
                if (i + j) % 2 == 0:
                    if theme == 0:
                        color = "white"
                    elif theme != 0:
                        color = "aqua"
                else:
                    if theme == 0:
                        color = "gray"
                    elif theme != 0:
                        color = "dark Gray"

                # We draw the rectangle. We use the attribute "tags" to be able to retrieve the elements
                # afterwards.
                self.create_rectangle(
                    col_start, row_start, col_end, row_end, fill=color, tags="box"
                )

    def draw_pieces(self):
        # Caractères  représentant les pièces. Vous avez besoin de la police d'écriture DejaVu.
        piece_chars = {
            "PB": "\u2659",
            "PN": "\u265f",
            "TB": "\u2656",
            "TN": "\u265c",
            "CB": "\u2658",
            "CN": "\u265e",
            "FB": "\u2657",
            "FN": "\u265d",
            "RB": "\u2654",
            "RN": "\u265a",
            "DB": "\u2655",
            "DN": "\u265b",
        }

        # For any pair position, piece:
        for position, piece in self.game.chess_board.pieces_dictionary.items():
            # We draw the piece in the canvas, in the center of the box. We use the attribute "tags" to be in
            # ability to retrieve the elements in the canvas.
            coordonnee_y = (
                self.n_rows - self.row_numbers.index(position[1]) - 1
            ) * self.n_pixels_per_box + self.n_pixels_per_box // 2
            coordonnee_x = (
                self.col_letters.index(position[0]) * self.n_pixels_per_box
                + self.n_pixels_per_box // 2
            )
            self.create_text(
                coordonnee_x,
                coordonnee_y,
                text=piece,
                font=("Deja Vu", self.n_pixels_per_box // 2),
                tags="piece",
            )

    def resize(self, event):
        # We receive in the "event" the new dimension in the attributes width and height. We want a checkerboard
        # box, then only the smaller of these two values is retained.
        nouvelle_taille = min(event.width, event.height)

        # Calculation of the new dimension of the boxes.
        self.n_pixels_per_box = nouvelle_taille // self.n_rows

        # We delete the old boxes and add the new ones.
        self.delete("box")
        self.draw_boxes(self.theme)

        # We delete the old pieces and add the new ones.
        self.delete("piece")
        self.draw_pieces()

    def refresh(self):
        """
        Allows you to redraw the window after each call of the function.
        """
        self.delete("box")
        self.draw_boxes(self.theme)

        self.delete("piece")
        self.draw_pieces()

    def options(self):
        """
        Function to create the menu that will be called when creating the window.
        Each menu item allows to perform a function determined below.
        Adding lambda prevents the menu from performing the commands of the menu creation.
        """
        self.barre_tache = Menu(master=self)
        self.infos = Menu(self.barre_tache, tearoff=0)
        self.infos.add_command(
            label="instructions", command=lambda: self.instructions()
        )
        self.infos.add_command(
            label="Done moves", command=lambda: self.moves_done()
        )
        self.barre_tache.add_cascade(label="Options", menu=self.infos)

    def instructions(self):
        # a link is opened where the user can learn about the rules of the game
        webbrowser.open(
            "https://www.chess.com/learn-how-to-play-chess"
        )

    def exit_game(self):
        # Allows to save_game before exiting (from the menu)
        confirm_exit = messagebox.askquestion(
            "Quit the game.",
            "Would you like to save before leaving the game?",
            icon="warning",
        )
        if confirm_exit == "yes":
            self.save_game()
            self.quit()
        else:
            self.quit()

    def save_game(self):
        # Allows to save_game the dictionary of pieces
        with open("Save", "wb") as f:
            pickle.dump(self.game.chess_board.pieces_dictionary, f)

    def load_game(self):
        """
        Function load_game of the menu which allows to recover the last backup.
        Then, update the chessboard and reset the counter to zero.
        """
        with open("Save", "rb") as f:
            self.game.chess_board.pieces_dictionary = pickle.load(f)
        self.game.chess_board.pieces_prises = []
        self.refresh()
        self.counter_start()

    def restart(self):
        """
        Exactly the same principle as the load_game function.
        We don't create a new window, but rather a backup of a starting equipment.
        """
        with open("NewGameSave", "rb") as f:
            self.game.chess_board.pieces_dictionary = pickle.load(f)
        self.game.chess_board.pieces_prises = []
        self.moves_done = []
        self.refresh()
        self.counter_start()

    def moves_done(self):
        """
        Creation of a new window that displays the movements made by the players.
        The icon of the piece is displayed followed by its movement.
        """
        root = Tk()
        root.title("Moves list")
        move_txt = ""
        for moves in self.moves_done:
            move_txt += moves
        phrase = Label(root, text=move_txt, fg="green")
        phrase.pack()
        root.mainloop()

    def sms(self):
        """
        This dialog box will be called when the window is created.
        The yes/no option will allow us to change the theme to 0 or 1.
        This theme will change the colors according to the draw_boxs() function.
        """
        confirm_exit = messagebox.askyesno(
            "Bienvenue",
            "Ready to loose? \n"
            "You have {} seconds to make your move!\n".format(start_time)
            + "click option for more details \n Before we start, do you want another theme?",
        )

        if confirm_exit is True:
            self.theme = 1
            self.refresh()
        else:
            self.theme = 0

    def counter_start(self):
        # Reset the counter to its initial value
        global game_time
        game_time = start_time


# limit time to play
start_time = 20
game_time = start_time


class Window(Tk):
    position1 = ""
    position2 = ""

    def __init__(self):
        super().__init__()

        # Name of the window.
        self.title("Chess Board")

        self.game = Game()

        # Tip for the automatic resizing of the window elements.
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Creation of the chess canvas.
        self.canvas_board = CanvasChessboard(self, 60, self.game)
        self.canvas_board.grid(sticky=NSEW)

        self.canvas_board.options()
        self.config(menu=self.canvas_board.barre_tache)
        self.canvas_board.sms()

        # Added an information label.
        self.info = Label(self)
        self.info.grid()
        self.info["foreground"] = "black"
        self.info["text"] = "You can start !"
        self.msg_active_player = Label(self)
        self.msg_active_player.grid()
        self.msg_active_player["foreground"] = "black"
        self.msg_active_player["text"] = (
            "It's the turn of : " + self.game.active_player.upper()
        )
        self.message_timer = Label(self)
        self.message_timer.grid()
        self.message_timer["foreground"] = "red"
        self.counter()
        self.boxes()
        self.msg_taken_pieces = Label(self)
        self.msg_taken_pieces.grid()
        self.msg_taken_pieces["foreground"] = "red"

        # A click on the CanvasChecker is linked to a method.
        self.canvas_board.bind("<Button-1>", self.select)
        # def boutons(self):
        self.new_game = Button(
            self, text="Restart", command=self.canvas_board.restart
        )
        self.new_game.grid(row=3, column=0, padx=10, pady=10)

        self.save = Button(
            self, text="Save", command=self.canvas_board.save_game
        )
        self.save.grid(row=3, column=1, padx=10, pady=10)

        self.load = Button(
            self,
            text="Resume the previous game",
            command=self.canvas_board.load_game,
        )
        self.load.grid(row=4, column=0, padx=10, pady=10)

        self.exit = Button(self, text="Exit", command=self.canvas_board.exit_game)
        self.exit.grid(row=5, column=0, padx=10, pady=10)
        self.c_theme = Button(
            self, text="Change Theme", command=self.canvas_board.change_theme
        )
        self.c_theme.grid(row=4, column=1, padx=10, pady=10)

    def boxes(self):
        # Creation of all possible positions to use it in the function
        # box_destination()
        inverse_row_numbers = self.canvas_board.row_numbers[::-1]
        for i in self.canvas_board.col_letters:
            for j in inverse_row_numbers:
                self.canvas_board.boxes_list.append(i + j)

    def counter(self):
        """
        Recursive function that decrement the global variable game_time.
        After a delay of one second, the function calls itself.
        If the number of seconds reaches 0, a message is displayed and ends the game.
        """
        global game_time
        game_time -= 1
        self.message_timer["text"] = game_time
        self.message_timer.after(1000, self.counter)
        if game_time == 0:
            messagebox.showinfo(
                title="Checkmate!",
                message="Checkmate! \n Press Ok for more details!",
            )
            self.info[
                "text"
            ] = "Game Over, the player {} has exhausted allotted time. ".format(
                self.game.active_player
            )
            self.msg_active_player["text"] = "The allotted time has been exceeded"
            self.message_timer.destroy()
            self.canvas_board.destroy()

    def charge_taken_pieces_to_str(self):
        """
        Update of the labels pieces eaten.
        (We have added the label of the active player)
        """
        self.msg_taken_pieces["text"] = self.game.chess_board.taken_pieces
        self.msg_active_player["text"] = (
            "It's player  " + self.game.active_player.upper() + " turn"
        )

    def dest_box(self, source):
        """
        Using the list of all the positions to pass these positions in a for loop
        and in the function of the chess class: is_move_valid(). If the move returns
        True, we add it to a list that we browse to draw the boxes.
        """
        possible_positions_list = []
        for i in self.canvas_board.boxes_list:
            if self.game.chess_board.is_move_valid(source, i) is True:
                possible_positions_list.append(i)
        for j in possible_positions_list:
            row = 8 - (int(j[1]))
            col = int(ord(j[0]) - 97)
            row_start = row * self.canvas_board.n_pixels_per_box
            row_end = row_start + self.canvas_board.n_pixels_per_box
            col_start = col * self.canvas_board.n_pixels_per_box
            col_end = col_start + self.canvas_board.n_pixels_per_box
            self.canvas_board.create_rectangle(
                col_start,
                row_start,
                col_end,
                row_end,
                fill="yellow",
                width=3,
                tags="boxs_debut",
            )

    def source_box(self, row, column, color):
        # This code is similar to what was provided in the draw_boxs() function.
        row_start = row * self.canvas_board.n_pixels_per_box
        row_end = row_start + self.canvas_board.n_pixels_per_box
        col_start = column * self.canvas_board.n_pixels_per_box
        col_end = col_start + self.canvas_board.n_pixels_per_box
        self.canvas_board.create_rectangle(
            col_start,
            row_start,
            col_end,
            row_end,
            outline=color,
            width=3,
            tags="indications",
        )

    def select(self, event):
        # The row/column number is found by dividing the y/x positions by the number of pixels per box
        row = event.y // self.canvas_board.n_pixels_per_box
        col = event.x // self.canvas_board.n_pixels_per_box
        position = "{}{}".format(
            self.canvas_board.col_letters[col],
            int(self.canvas_board.row_numbers[self.canvas_board.n_rows - row - 1]),
        )

        try:
            if not self.canvas_board.selected_position:
                # source position == selected_position
                self.canvas_board.selected_position = position
                # When a box is selected, its outline is drawn. Same thing for the valid boxes.
                self.source_box(row, col, "blue")
                self.dest_box(self.canvas_board.selected_position)
            else:

                self.game.move(
                    self.canvas_board.selected_position, position
                ) 

                # Creation of the list of the movements performed if a move has taken place (to be displayed from
                # the Information menu
                piece = self.game.chess_board.pieces_dictionary[position]
                self.canvas_board.moves_done += "{} : {} at the position {}.\n".format(
                    piece, self.canvas_board.selected_position, position
                )

                # Since a move has been made, the counter is reset to zero (and then the label is updated).
                self.canvas_board.counter_start()
                self.charge_taken_pieces_to_str()

                """
                The following section (followed by the except) allows you to update the labels according to
                of the events that took place. 
                A message is displayed if the function game_over() returns True, then the program 
                ends. 
                """
                self.canvas_board.selected_position = None
                self.canvas_board.refresh()
                self.info["foreground"] = "black"
                self.info["text"] = "The piece has been moved"
                if self.game.game_over():
                    self.message_timer.destroy()
                    self.info["foreground"] = "black"
                    self.info["text"] = (
                        "Game Over, the winner is the"
                        + self.game.determine_winner() + "player"
                    )
                    messagebox.showinfo(
                        title="Checkmate!",
                        message="Press OK for more details!",
                    )
                    self.canvas_board.destroy()

        except (NoPieceInPosition, WrongColorException, MoveException) as e:
            self.info["foreground"] = "red"
            self.info["text"] = e
            self.canvas_board.selected_position = None
            self.canvas_board.refresh()
