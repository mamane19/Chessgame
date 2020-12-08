# -*- coding: utf-8 -*-
"""
File containing the base Piece class, as well as a child class for each of the type of pieces in the chess game.

"""
# TODO: If your system does not correctly display the unicode characters of the chess game,
# set this constant (global variable) to False.
USE_UNICODE = True


class Piece:
    """
    A basic class representing a piece of the chess game. It is this class which is inherited below to provide
    one class per type of piece (Pawn, Rook, etc.).

    Attributes:
        color (str): The color of the piece, either 'white' or 'black'.
        can_jump (bool): Whether or not the piece can "jump" over other pieces on a chessboard.

    Args:
        color (str): The color with which to create the piece.
        can_jump (bool): The value with which the attribute can_jump must be initialized.

    """
    def __init__(self, color, can_jump):
        # Validation if the received color is valid.
        assert color in ('white', 'black')

        # Creation of the attributes with the received values.
        self.color = color
        self.can_jump = can_jump

    def is_white(self):
        """
        Returns whether or not the room is white.

        Returns:
            bool: True if the coin is white, and False otherwise.

        """
        return self.color == 'white'

    def is_black(self):
        """
        Returns whether or not the piece is black.

        Returns:
            bool: True if the coin is black, and False otherwise.

        """
        return self.color == 'black'

    def can_move_towards(self, source, target):
        """
        Checks whether, according to the rules of chess, the piece can move from one position to another.

        A position is a two-character string.
            The first character is a letter between a and h, representing the column of the chessboard.
            The second character is a number between 1 and 8, representing the row of the chessboard.

        Args:
            source_position (str): The source position, following the above format. For example, 'a8', 'f3', etc.
            target_position (str): The target position, according to the above format. For example, 'b6', 'h1', etc.

        Warning:
            Since we are in the base class and not in one of the daughter classes, we don't know
            (again) how this piece moves. This method is thus to be redefined in each of the
            girls' classes.

        Warning:
            As the Piece class is independent of the chessboard (and therefore we don't know if a piece is "in the
            path"), we must ignore the content of the chessboard: we concentrate only on the rules of movement
            pieces.

        Returns:
            bool: True if the move is valid following the rules of the piece, and False otherwise.

        """
        # An exception is thrown (more on this later) indicating that this code has not been implemented.
        raise NotImplementedError

    def can_take_over(self, source, target):
        """
        Checks whether, according to the rules of chess, the piece can "eat" (make a capture) an enemy piece.
        For most pieces the rule is the same, so the method can_move_towards is called.

        If this is not the case for a certain piece, we can simply redefine this method to program
        the rule.

        Args:
            source_position (str): The source position, following the above format. For example, 'a8', 'f3', etc.
            target_position (str): The target position, according to the above format. For example, 'b6', 'h1', etc.

        Returns:
            bool: True if the take is valid according to the rules of the piece, and False otherwise.

        """
        return self.can_move_towards(source, target)


class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color, False)

    def can_move_towards(self, source, target):
        source_col, target_col = ord(source[0]), ord(target[0])
        source_row, target_row = int(source[1]), int(target[1])

        # A pawn moves in the same column.
        if target_col != source_col:
            return False

        # If the pawn has never moved, it may move two boxes. Otherwise, only one box.
        # Note that this is the only place where we refer to the size of the chessboard.
        # To make our classes of pieces truly independent of this size, we could
        # for example add an attribute n_deplacements, which will be incremented if the piece is
        # moves.
        diff = source_row - target_row
        if self.is_white():
            if source_row == 2:
                return diff in (-1, -2)
            else:
                return diff == -1

        else:
            if source_row == 7:
                return diff in (1, 2)
            else:
                return diff == 1

    def can_take_over(self, source, target):
        source_col, target_col = ord(source[0]), ord(target[0])
        source_row, target_row = int(source[1]), int(target[1])

        # The pawn makes a diagonal capture, of one box only, and the direction depends
        # of its color.
        if target_col not in (source_col - 1, source_col + 1):
            return False

        if self.is_white():
            return target_row == source_row + 1

        else:
            return target_row == source_row - 1

    def __repr__(self):
        """
        Redefines how a pawn is displayed on the screen. We use the constant USE_UNICODE
        to determine how to display the pawn.

        Returns:
            str: The string representing the pawn.

        """
        if self.is_white():
            if USE_UNICODE:
                return '\u2659'
            else:
                return 'PB'
        else:
            if USE_UNICODE:
                return '\u265f'
            else:
                return 'PN'


class Rook(Piece):
    def __init__(self, color):
        super().__init__(color, False)

    def can_move_towards(self, source, target):
        source_col, target_col = source[0], target[0]
        source_row, target_row = source[1], target[1]

        # A tower moves on the same row or line in any direction.
        if target_col != source_col and source_row != target_row:
            return False

        # On the other hand, it cannot stay there.
        if source_col == target_col and source_row == target_row:
            return False

        return True

    def __repr__(self):
        if self.is_white():
            if USE_UNICODE:
                return '\u2656'
            else:
                return 'TB'
        else:
            if USE_UNICODE:
                return '\u265c'
            else:
                return 'TN'


class Knight(Piece):
    def __init__(self, color):
        super().__init__(color, True)

    def can_move_towards(self, source, target):
        source_col, target_col = ord(source[0]), ord(target[0])
        source_row, target_row = int(source[1]), int(target[1])

        # A knight moves in an "L", so one of its coordinates varies by 1, and the other by 2.
        col_distance = abs(source_col - target_col)
        row_distance = abs(source_row - target_row)

        if col_distance == 1 and row_distance == 2:
            return True

        if col_distance == 2 and row_distance == 1:
            return True

        return False

    def __repr__(self):
        if self.is_white():
            if USE_UNICODE:
                return '\u2658'
            else:
                return 'CB'
        else:
            if USE_UNICODE:
                return '\u265e'
            else:
                return 'CN'


class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color, False)

    def can_move_towards(self, source, target):
        # A bishop moves diagonally, i.e. the distance between rows and columns must be the same.
        source_col, target_col = ord(source[0]), ord(target[0])
        source_row, target_row = int(source[1]), int(target[1])

        if abs(source_col - target_col) != abs(source_row - target_row):
            return False

        # Par contre, il ne peut pas faire de sur-place.
        if source_col == target_col and source_row == target_row:
            return False

        return True

    def __repr__(self):
        if self.is_white():
            if USE_UNICODE:
                return '\u2657'
            else:
                return 'FB'
        else:
            if USE_UNICODE:
                return '\u265d'
            else:
                return 'FN'


class King(Piece):
    def __init__(self, color):
        super().__init__(color, False)

    def can_move_towards(self, source, target):
        # A king can move one box, on a line, row or column.
        source_col, target_col = ord(source[0]), ord(target[0])
        source_row, target_row = int(source[1]), int(target[1])

        col_distance = abs(source_col - target_col)
        row_distance = abs(source_row - target_row)

        if row_distance != 1 and col_distance != 1:
            return False

        return True

    def __repr__(self):
        if self.is_white():
            if USE_UNICODE:
                return '\u2654'
            else:
                return 'RB'
        else:
            if USE_UNICODE:
                return '\u265a'
            else:
                return 'RN'


class Queen(Piece):
    def __init__(self, color):
        super().__init__(color, False)

    def can_move_towards(self, source, target):
        # A move for a queen is valid if it moves in a row, column or diagonally.
        # Note that we use the methods directly from a class, passing as first
        # argument the current object (self). It would have been "cleaner" to create new functions
        # common to Rook, Bishop and Queen classes to avoid making these calls from the class.
        return Rook.can_move_towards(self, source, target) or \
            Bishop.can_move_towards(self, source, target)

    def __repr__(self):
        if self.is_white():
            if USE_UNICODE:
                return '\u2655'
            else:
                return 'DB'
        else:
            if USE_UNICODE:
                return '\u265b'
            else:
                return 'DN'
