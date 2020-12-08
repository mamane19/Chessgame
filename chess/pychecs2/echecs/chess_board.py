# -*- coding: utf-8 -*-
"""
This file contains the Chessboard class, a class grouping together various pieces on a game board.

"""
from pychecs2.echecs.piece import Pawn, Rook, Bishop, Knight, Queen, King, USE_UNICODE


class Chessboard:
    """
    Chessboard class, implemented with a piece dictionary.

    Attributes:
        pieces_dictionary (dict): A dictionary whose keys are positions, according to the following format:
            A position is a two-character string.
            The first character is a letter between a and h, representing the column of the chessboard.
            The second character is a number between 1 and 8, representing the row of the chessboard.
        row_numbers (list): A list containing, in order, the numbers representing the rows.
        col_letters (list): A list containing, in order, the letters representing the columns.

    """
    def __init__(self):
        # The dictionary of pieces, initially empty, but then filled by the initialize_checkboard() method.
        self.pieces_dictionary = {}

        # These lists can be used in other methods, for example to validate a position.
        self.row_numbers = ['1', '2', '3', '4', '5', '6', '7', '8']
        self.col_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

        self.init_board()
        self.taken_pieces = []

    def is_position_valid(self, position):
        """
        Checks if a position is valid (in the chessboard). A position is a concatenation of a letter of
        column and a row number, e.g. 'a1' or 'h8'.

        Args:
            position (str): The position to validate.

        Returns:
            bool: True if the position is valid, False otherwise.

        """
        if len(position) != 2:
            return False

        if position[0] not in self.col_letters:
            return False

        if position[1] not in self.row_numbers:
            return False

        return True

    def get_piece_from_position(self, position):
        """
        Returns the piece that is located at a particular position, received as an argument. If no piece is
        located at this position, returns None.

        Args:
            position (str): The position where to retrieve the piece.

        Returns:
            Piece or None: A Piece instance if a piece was located at this position, and None otherwise.

        """
        if position not in self.pieces_dictionary:
            return None

        return self.pieces_dictionary[position]

    def get_piece_color_from_position(self, position):
        """
        Returns the color of the piece located at the position received as argument, and an empty string if no one is present.
        piece is at this location.

        Args:
            position (str): The position where to get the color of the piece.

        Returns:
            str: The color of the piece if there is one, and '' otherwise.

        """
        piece = self.get_piece_from_position(position)
        if piece is None:
            return ''

        return piece.color

    def rows_between(self, start_row, end_row):
        """
        Returns the list of rows that are located between the two rows received as argument, exclusively.
        Be careful to keep the right order.

        Args:
            start_range (str): The character representing the start row, for example '1'.
            end_range (str): The character representing the end row, e.g. '4'.

        Exemple:
            >>> chessboard.rows_between('1', '1')
            []
            >>> chessboard.rows_between('2', '3')
            []
            >>> chessboard.rows_between('2', '8')
            ['3', '4', '5', '6', '7']
            >>> chessboard.rows_between('8', '3')
            ['7', '6', '5', '4']

        Returns:
            list: A list of rows (in str) between the beginning and the end, in the right order.

        """
        start_index = self.row_numbers.index(start_row)
        end_index = self.row_numbers.index(end_row)
        if start_index <= end_index:
            direction = 1
        else:
            direction = -1

        return self.row_numbers[start_index+direction:end_index:direction]

    def col_between(self, start_col, end_col):
        """
        Returns the list of columns that are located between the two columns received as argument, exclusively.

        Args:
            start_column (str): The character representing the start column, for example 'a'.
            end_column (str): The character representing the end column, for example 'h'.

        Exemple:
            >>> chessboard.col_between('a', 'a')
            []
            >>> chessboard.col_between('b', 'c')
            []
            >>> chessboard.col_between('b', 'h')
            ['c', 'd', 'e', 'f', 'g']
            >>> chessboard.col_between('h', 'c')
            ['g', 'f', 'e', 'd']

        Indice:
            Utilisez self.lettres_colonnes pour obtenir une liste des colonnes valides.

        Returns:
            list: A list of the columns (in str) between the beginning and the end, in the right order.

        """
        start_index = self.col_letters.index(start_col)
        end_index = self.col_letters.index(end_col)
        if start_index <= end_index:
            direction = 1
        else:
            direction = -1

        return self.col_letters[start_index+direction:end_index:direction]

    def free_path_between_positions(self, source, target):
        """
        Checks if the path is clear between two positions, received as arguments. This method will be convenient
        to validate the movements: most pieces cannot "jump" over other pieces,
        so make sure there are no pieces in the way.

        There are four possibilities (to be determined in your code): Either the two positions are on the same
        row, either they are on the same column, either it is a diagonal, or we are in a
        situation where we cannot search for positions "between" the source and target positions. In all three
        first cases, we do the verification and return True or False depending on the presence of a piece or not.
        In the last situation, the positions received are considered invalid and False is always returned.

        Args:
            source_position (str): The source position.
            target_position (str): The target position.

        Warning:
            We don't check the source and target positions, since there may be pieces at this location.
            For example, if a rook "eats" an enemy pawn, there will be a rook on the source position and a pawn on the target position.
            on the target position.

        Returns:
            bool: True if no piece is located between the two positions, and False otherwise (or if the
                did not allow for verification).
        """
        source_col, target_col = source[0], target[0]
        source_row, target_row = source[1], target[1]

        # If the source and target columns are the same, we check if the field is free for each row.
        if source_col == target_col:
            for rangee in self.rows_between(source_row, target_row):
                if self.get_piece_from_position('{}{}'.format(source_col, rangee)) is not None:
                    return False

            return True

        # If the source and target rows are the same, we check if the field is free for each column.
        if source_row == target_row:
            for col in self.col_between(source_col, target_col):
                if self.get_piece_from_position('{}{}'.format(col, source_row)) is not None:
                    return False

            return True

        #  here, it's either a diagonal or something invalid.
        columns = self.col_between(source_col, target_col)
        rows = self.rows_between(source_row, target_row)
        if len(columns) != len(rows):
            # Error, it is neither a line nor a diagonal.
            return False

        i = 0
        while i < len(rows):
            if self.get_piece_from_position('{}{}'.format(columns[i], rows[i])) is not None:
                return False
            i += 1

        return True

    def is_move_valid(self, source, target):
        """
        Checks if a move would be valid in the current chessboard. Note that each type of
        piece moves in a different way, you will probably want to use polymorphism :-).

        Rules for a move to be valid:
            1. There must be a piece at the source position.
            2. The target position must be valid (in the chessboard).
            3. If the piece can't jump, the path must be free between the two positions.
            4. If there is a piece at the target position, it must be of a different color.
            5. The move must be valid for this particular piece.

        Args:
            source_position (str): The source position of the move.
            target_position (str): The target position of the move.

        Returns:
            bool: True if the move is valid, and False otherwise.
        """
        # Make sure that the source position contains a piece.
        piece = self.get_piece_from_position(source)

        if piece is None:
            return False

        # We make sure that the target position is valid (in the chessboard).
        if not self.is_position_valid(target):
            return False

        # If the selected piece cannot jump, it is checked whether the path
        # is free between the two positions.
        if not piece.can_jump:
            if not self.free_path_between_positions(source, target):
                return False

        piece_cible = self.get_piece_from_position(target)
        if piece_cible is not None:
            if piece_cible.color == piece.color:
                return False

            else:
                return piece.can_take_over(source, target)

        return piece.can_move_towards(source, target)

    def move(self, source, target):
        """
        Moves a piece from the source position to the target box. First checks
        if the move is valid, and does nothing (then returns False) in this box. If the move is valid,
        it is performed (in the current chessboard) and the True value is returned.

        Args:
            source_position (str): The source position.
            target_position (str): The target position.

        Returns:
            bool: True if the move was valid and was performed, and False otherwise.

        """

        if not self.is_move_valid(source, target):
            raise MoveException("Invalid Move!")
        # if there are no pieces at the target position, it is added to the list of taken pieces.
        if self.get_piece_from_position(target) is not None:
            self.taken_pieces.append(self.pieces_dictionary[target])


        self.pieces_dictionary[target] = self.pieces_dictionary[source]
        del self.pieces_dictionary[source]


    def color_king_is_on_board(self, color):
        """
        Checks if a king of the color received in argument is present on the chessboard.

        Args:
            color (str): The color (white or black) of the king to look for.

        Returns:
            bool: True if a king of this color is in the chessboard, and False otherwise.

        """
        for piece in self.pieces_dictionary.values():
            if isinstance(piece, King):
                if piece.color == color:
                    return True

        return False

    def init_board(self):
        """
        Initializes the chessboard to its initial content. To make your tests during the development,
        we suggest you to make a simpler chessboard, by modifying the attribute
        dictionary_pieces of your Chess instance.

        """
        self.pieces_dictionary = {
            'a1': Rook('white'),
            'b1': Knight('white'),
            'c1': Bishop('white'),
            'd1': Queen('white'),
            'e1': King('white'),
            'f1': Bishop('white'),
            'g1': Knight('white'),
            'h1': Rook('white'),
            'a2': Pawn('white'),
            'b2': Pawn('white'),
            'c2': Pawn('white'),
            'd2': Pawn('white'),
            'e2': Pawn('white'),
            'f2': Pawn('white'),
            'g2': Pawn('white'),
            'h2': Pawn('white'),
            'a7': Pawn('black'),
            'b7': Pawn('black'),
            'c7': Pawn('black'),
            'd7': Pawn('black'),
            'e7': Pawn('black'),
            'f7': Pawn('black'),
            'g7': Pawn('black'),
            'h7': Pawn('black'),
            'a8': Rook('black'),
            'b8': Knight('black'),
            'c8': Bishop('black'),
            'd8': Queen('black'),
            'e8': King('black'),
            'f8': Bishop('black'),
            'g8': Knight('black'),
            'h8': Rook('black'),
        }

    def __repr__(self):
        """
        Displays the chessboard on the screen. Uses Unicode codes, if the constant USE_UNICODE is set to True in
        the piece module. Otherwise, use only standard characters.

        """
        string = ""
        if USE_UNICODE:
            string += '  \u250c' + '\u2500\u2500\u2500\u252c' * 7 + '\u2500\u2500\u2500\u2510\n'
        else:
            string += '  +' + '----+' * 8 + '\n'

        for row in range(7, -1, -1):
            if USE_UNICODE:
                string += '{} \u2502 '.format(self.row_numbers[row])
            else:
                string += '{} | '.format(self.row_numbers[row])
            for col in range(8):
                piece = self.pieces_dictionary.get('{}{}'.format(self.col_letters[col], self.row_numbers[row]))
                if piece is not None:
                    if USE_UNICODE:
                        string += str(piece) + ' \u2502 '
                    else:
                        string += str(piece) + ' | '
                else:
                    if USE_UNICODE:
                        string += '  \u2502 '
                    else:
                        string += '   | '

            if row != 0:
                if USE_UNICODE:
                    string += '\n  \u251c' + '\u2500\u2500\u2500\u253c' * 7 + '\u2500\u2500\u2500\u2524\n'
                else:
                    string += '\n  +' + '----+' * 8 + '\n'

        if USE_UNICODE:
            string += '\n  \u2514' + '\u2500\u2500\u2500\u2534' * 7 + '\u2500\u2500\u2500\u2518\n'
        else:
            string += '\n  +' + '----+' * 8 + '\n'

        string += '    '
        for col in range(8):
            if USE_UNICODE:
                string += self.col_letters[col] + '   '
            else:
                string += self.col_letters[col] + '    '
        string += '\n'
        return string

class MoveException(Exception):
    pass