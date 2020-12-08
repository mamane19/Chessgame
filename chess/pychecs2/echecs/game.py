# -*- coding: utf-8 -*-
"""
This file contains a class containing information about a chess game,
including a chess object (an instance of the Chess class).

"""
from pychecs2.echecs.chess_board import Chessboard

class NoPieceInPosition(Exception):
    pass
class WrongColorException(Exception):
    pass

class Game:
    """
    The class Game contains information about a chess game, i.e. a chessboard, then
    an active player (white or black). Methods are available to move the game forward and to interact
    with the user.

    Attributes:
        active_player (str): The color of the active player, 'white' or 'black'.
        chessboard (Chessboard): The chessboard on which the game takes place.

    """
    def __init__(self):
        # The player starting a game of chess is the white player.
        self.active_player = 'white'

        # Creation of an instance of the Chessboard class, which will be manipulated in the methods of the class.
        self.chess_board = Chessboard()

    def determine_winner(self):
        """
        Determines the color of the winning player, if there is one. To determine if a player is the winner,
        the king of the opponent's color must be absent from the chessboard.

        Returns:
            str: white' if the white player won, 'black' if the black player won, and 'none' if no
                player hasn't won yet.

        """
        if not self.chess_board.color_king_is_on_board('black'):
            return 'white'
        elif not self.chess_board.color_king_is_on_board('white'):
            return 'black'

        return 'aucun'

    def game_over(self):
        """
        Checks if the game is over. A game is over if a winner can be declared.

        Returns:
            bool: True if the game is over, and False otherwise.

        """
        return self.determine_winner() != 'aucun'
        #TODO: A supprimer
    def ask_positions(self):
        """
        Asks the user to enter the start and end positions to make a move. If the
        If the entered positions are valid (if the move is valid), both positions are returned. We must
        Ask again until the user gives valid positions.

        Returns:
            str, str: Two strings representing the two valid positions provided by the user.

        """
        #TODO: A supprimer (UNCERTAIN)
        while True:
            # On demande et valide la position source.
            while True:
                source = input("Enter source position: ")
                if self.chess_board.is_position_valid(source) and self.chess_board.get_piece_color_from_position(source) == self.active_player:
                    break

                print("Invalid Position.\n")
        #TODO: Maybe useful
            # On demande et valide la position cible.
            cible = input("Entre source position: ")
            if self.chess_board.is_move_valid(source, cible):
                return source, cible

            print("Invalid Move\n")

    def move(self, source, target):
        piece = self.chess_board.get_piece_from_position(source)
        if piece is None:
            raise NoPieceInPosition("No piece at this location!")
        elif piece.color != self.active_player:
            raise WrongColorException("This piece does not belong to the active player.")
        self.chess_board.move(source, target)
        self.next_player()



    def next_player(self):
        """
        Changes the active player: switches from white to black, or from black to white, depending on the color of the active player.

        """
        if self.active_player == 'white':
            self.active_player = 'black'
        else:
            self.active_player = 'white'
    #Keep the game going(faire quelques chose d'autre)
    def play(self):
        """
        Until the game is over, play the game. On each turn:
            - The chessboard is displayed.
            - Both positions are requested.
            - You make the move on the chessboard.
            - Move on to the next player.

        Once the game is over, we congratulate the winning player!

        """
        while not self.game_over():
            print(self.chess_board)
            print("\nIt is the turn of {} to play".format(self.active_player))
            source, cible = self.ask_positions()
            self.chess_board.move(source, cible)
            self.next_player()

        print(self.chess_board)
        print("\nGame Over! \nThe {} player  won".format(self.determine_winner()))
