# Author: Elizabeth Mayer
# Date: 5/30/2020
# Description: Implementation of GessGame. See rules at https://www.chessvariants.com/crossover.dir/gess.html


class Board:
    """
    purpose: to create the initial board object and keep track of the changes
    responsibilities: tracks whose turn it is and the state
    communicates with(why): Interacts with GessGame to help it keep track of the board udpates
    """

    def __init__(self):
        """ 
        purpose: Creates the initial board object with the predetermined starting spots
        parameters: N/A
        return: the board with the initial spots
        """""
        self._board = []
        self.initial_board()

    def initial_board(self):
        """
        purpose: Creates the initial board with the predetermined starting spots
        parameters: N/A
        return: the board with the initial spots
        """
        count = 1

        top_row = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t"]
        self._board.append(top_row)

        for i in range(20):
            list_i = [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "]
            self._board.append(list_i)
            count += 1

        white_starting = [[19, 2], [19, 4], [19, 6], [19, 7], [19, 8], [19, 9], [19, 10], [19, 11], [19, 12], [19, 13], [19, 15], [19, 17],
                          [18, 1], [18, 2], [18, 3], [18, 5], [18, 7], [18, 8], [18, 9], [18, 10], [18, 12], [18, 14], [18, 16], [18, 17], [18, 18],
                          [17, 2], [17, 4], [17, 6], [17, 7], [17, 8], [17, 9], [17, 10], [17, 11], [17, 12], [17, 13], [17, 15], [17, 17],
                          [14, 2], [14, 5], [14, 8], [14, 11], [14, 14], [14, 17]]
        black_starting = [[2, 2], [2, 4], [2, 6], [2, 7], [2, 8], [2, 9], [2, 10], [2, 11], [2, 12], [2, 13], [2, 15], [2, 17],
                          [3, 1], [3, 2], [3, 3], [3, 5], [3, 7], [3, 8], [3, 9], [3, 10], [3, 12], [3, 14], [3, 16], [3, 17], [3, 18],
                          [4, 2], [4, 4], [4, 6], [4, 7], [4, 8], [4, 9], [4, 10], [4, 11], [4, 12], [4, 13], [4, 15], [4, 17],
                          [7, 2], [7, 5], [7, 8], [7, 11], [7, 14], [7, 17]]

        for sublist in black_starting:
            self._board[sublist[0]][sublist[1]] = "b"

        for sublist in white_starting:
            self._board[sublist[0]][sublist[1]] = "w"

    def print(self):
        """
         purpose: prints the board
         parameters: N/A
         return: the board printed line by line
         """
        for item in self._board:
            print(item)

    def get_board(self):
        """
         purpose: access to the board
         parameters: N/A
         return: the board itself
         """
        return self._board


class GessGame:
    """
    purpose: serves as the first class for tracking the gameplay
    responsibilities: makes sure moves are legal, tracks whose turn it is and the state, has composition of Board class
    communicates with(why): Board (composition, GessGame has a board so it must be able to communicate with it
    to get the initial board and to print)
    """

    def __init__(self):
        """
        purpose: create initial game object with the new board, an unfinished game state and whose turn it is
        and whose turn it isn't
        parameters: N/A
        return: a new GessGame Object
        """
        self._game_state = "UNFINISHED"
        self._turn = "b"
        self._not_turn = "w"
        self._board = Board()  # Composition of the board, since the game HAS a board
        self._temp_board = self._board

    def print(self):
        """
        purpose: utilizes the print method from the Board class for testing purposes
        parameters: N/A
        return: the board
        """
        self._board.print()

    def get_turn(self):
        return self._turn

    def get_game_state(self):
        """
        purpose: gets the game state
        parameters: N/A
        return: the current game state
        """
        return self._game_state

    def resign_game(self):
        """
        purpose: checks current player and allows them to resign
        parameters: N/A
        return: an updated game state
        """
        if self._turn == "b":
            self._game_state = "WHITE_WON"
        else:
            self._game_state = "BLACK_WON"

    def make_move(self, move_from, move_to):
        """
        purpose: strings that represent the center square of the piece being moved
        and the desired new location of the center square. checks if move is legal, checks to see if game is won,
        updates the board, update game state(if needed), update turn"
        parameters: move_from, move_to
        return: True or False
        """

        board = self._board.get_board()
        footprint_current = self.find_footprint(move_from)  # [c, n, s, e, w, ne, nw, se, sw]
        footprint_future = self.find_footprint(move_to)  # [c, n, s, e, w, ne, nw, se, sw]

        from_trans = footprint_current[0]
        to_trans = footprint_future[0]

        row_from = from_trans[0]
        col_from = from_trans[1]
        row_to = to_trans[0]
        col_to = to_trans[1]

        row_dir = (row_to - row_from)
        col_dir = (col_to - col_from)

        items_in_cur_footprint = self.items_in_footprint(footprint_current, board)

        if self._game_state != "UNFINISHED":
            return False

        if self.check_if_move_is_in_bounds(row_from, col_from) is False:
            return False

        elif self.check_for_others_stone_in_piece(footprint_current, board) is False:
            return False

        elif self.check_for_any_tokens(items_in_cur_footprint) is False:
            return False

        elif self.check_if_move_is_in_bounds(row_to, col_to) is False:
            return False

        elif self.check_if_no_center_more_than_three(row_from, col_from, row_dir, col_dir, board) is False:
            return False

        elif row_dir > 0:  # going in NX direction
            if self.check_nx_path_for_footprint(col_dir, items_in_cur_footprint, footprint_current, footprint_future) is False:
                return False

        elif row_dir < 0:  # going in SX direction
            if self.check_sx_path_for_footprint(col_dir, items_in_cur_footprint, footprint_current, footprint_future) is False:
                return False

        elif col_dir > 0:  # going in the E direction
            if self.check_e_path_for_footprint(items_in_cur_footprint, footprint_current, footprint_future) is False:
                return False

        elif col_dir < 0:  # going in the W direction
            if self.check_w_path_for_footprint(items_in_cur_footprint, footprint_current, footprint_future) is False:
                return False

        # checking to make sure that current player's move won't leave them with no rings
        if self.find_rings_for_illegal_move(footprint_current, footprint_future, self._turn) is False:
            return False
        else:
            self.update_board(footprint_current, footprint_future, board)  # since move is legal, update the board

        # checking if the update left the other player with no rings, and update board accordingly
        if self.find_rings(self._not_turn, board) is not True:
            if self._turn == 'b':
                self._game_state = "BLACK_WON"
            else:
                self._game_state = "WHITE_WON"

        # update whose turn it is
        self.update_turn()

        return True  # required to return True after move finished

    def update_board(self, footprint_current, footprint_future, board):
        """
        purpose: update the board with the new footprint
        parameters: footprint_current, footprint_future, board
        return: an updated board
        """
        new_status = []
        i = 0
        for item in footprint_current:  # updating board
            new_item = board[item[0]][item[1]]
            new_status.append(new_item)  # adds current item in current location to a list
            board[item[0]][item[1]] = " "  # removes item from location

        for item in footprint_future:  # special case for handling edges
            if item[0] == 1 or item[0] == 20:  # clears if spot is on first/last row
                board[item[0]][item[1]] = " "
            elif item[1] == 0 or item[1] == 19:  # clears if spot is on first/last col
                board[item[0]][item[1]] = " "
            else:
                board[item[0]][item[1]] = new_status[i]  # takes future location and update it with the correct item
            i += 1

    def update_turn(self):
        """
        purpose: update whose turn it is and whose turn it isn't
        parameters: N/A
        return: updated object with whose turn it is and isn't
        """

        if self._turn == "b":
            self._turn = "w"
            self._not_turn = "b"
        else:
            self._turn = "b"
            self._not_turn = "w"

    def find_rings_for_illegal_move(self, footprint_current, footprint_future, turn):
        """
        purpose: check to see if the desired move would leave the player with no rings
        parameters: footprint_current, footprint_future, turn, board
        return: False or none
        """
        board = self._board.get_board()
        temp_board = [item.copy() for item in board]

        self.update_board(footprint_current, footprint_future, temp_board)

        if self.find_rings(turn, temp_board) is not True:
            return False

    def find_rings(self, turn, board):
        """""
        purpose: finds rings on board for given player
        parameters: turn, board
        return: True or False
        """

        for row in range(3, 19):
            for col in range(2, 18):
                if board[row][col] == " ":  # making sure the center of the piece is empty

                    n = [row + 1, col]
                    s = [row - 1, col]
                    e = [row, col + 1]
                    w = [row, col - 1]
                    ne = [row + 1, col + 1]
                    nw = [row + 1, col - 1]
                    se = [row - 1, col + 1]
                    sw = [row - 1, col - 1]

                    ring = [n, s, e, w, ne, nw, se, sw]
                    items_in_footprint = set()

                    for item in ring:
                        item_in_square = board[item[0]][item[1]]
                        items_in_footprint.add(item_in_square)

                    if len(items_in_footprint) == 1:  # makes sure all items are the same
                        if items_in_footprint == {turn}:  # makes sure the items are the correct players
                            return True
        #
        # return False

    def check_for_others_stone_in_piece(self, footprint_current, board):
        """
        purpose: verify that the footprint does not contain other player's stones
        parameters: footprint_current, board
        return: None or False
        """

        # checking to see if the move_from has others player stones in footprint or none of their stones
        for item in footprint_current:
            if board[item[0]][item[1]] == self._not_turn:
                return False

    def items_in_footprint(self, footprint_current, board):
        """
        purpose: determining what item is in each square of the footprint (e.g. 'b', 'w', or ' ')
        parameters: footprint_current, board
        return: a list of what item is in each square of the footprint in a [c, n, s, e, w, ne, nw, se, sw]
        configuration
        """
        items_in_footprint = []

        for item in footprint_current:
            item_in_square = board[item[0]][item[1]]
            items_in_footprint.append(item_in_square)

        return items_in_footprint

    def check_for_any_tokens(self, items_in_cur_footprint):
        """
        purpose: verify there is at least 1 of the player's token in the footprint
        parameters: items_in_cur_footprint
        return: None or False
        """

        if self._turn not in items_in_cur_footprint:
            return False

    def check_if_move_is_in_bounds(self, row, col):
        """
        purpose: verify that the move does not place the center of the footprint out of bounds
        parameters: row, column
        return: None or False
        """

        if row < 2 or row > 19:  # piece will be out of bounds cuz in row 1 or 20
            return False
        elif col < 1 or col > 18:  # piece will be out of bound cuz in col a (col = 0) or t (col = 19)
            return False

    def check_if_no_center_more_than_three(self, row_from, col_from, row_dir, col_dir, board):
        """
        purpose: verify that if there is no center token, they are not moving more than 3 spaces
        parameters: row_from, col_from, row_dir, col_dir, board
        return: None or False
        """
        if board[row_from][col_from] != self._turn:  # verifying that move isn't more than 3 spaces
            if abs(row_dir) > 3 or abs(col_dir) > 3:
                return False

    def translate(self, a_move):
        """
        purpose: to translate the input of alpha-numeric (e.g. 'a6') to a numeric useable row and column
        parameters: a_move
        return: [row, col]
        """
        alpha_to_num = [['a', 0], ['b', 1], ['c', 2], ['d', 3], ['e', 4], ['f', 5], ['g', 6], ['h', 7], ['i', 8], ['j', 9], ['k', 10], [
            'l', 11], ['m', 12], ['n', 13], ['o', 14], ['p', 15], ['q', 16], ['r', 17], ['s', 18], ['t', 19]]

        row = int(a_move[1:])
        col = (a_move[0])

        for sublist in alpha_to_num:
            if col == sublist[0]:
                col = sublist[1]

        return [row, col]

    def find_footprint(self, a_move):
        """
        purpose: finds the footprint given the center coordinate
        parameters: a_move
        return: the footprint of the move
        """
        a_move_trans = self.translate(a_move)

        row = a_move_trans[0]
        col = a_move_trans[1]

        c = [row, col]
        e = [row, col + 1]
        w = [row, col - 1]
        n = [row + 1, col]
        s = [row - 1, col]
        ne = [row + 1, col + 1]
        nw = [row + 1, col - 1]
        sw = [row - 1, col - 1]
        se = [row - 1, col + 1]
        footprint = [c, n, s, e, w, ne, nw, se, sw]

        return footprint

    def check_nx_path_for_footprint(self, col_dir, items_in_cur_footprint, footprint_current, footprint_future):
        """""
        purpose: checks whether the player has the token in the correct place for the desired path and checkt whether
        the path is clear for the footprint to go from current to new if moving in a N, NE, or NW path
        parameters: col_dir, items_in_cur_footprint, footprint_current, footprint_future
        return: True or False
        """

        if col_dir == 0:  # going in N direction
            if items_in_cur_footprint[1] != self._turn:  # verifying a token is in the north spot to be able to move
                return False
            else:
                if self.a_square_path_clear_n(footprint_current[1], footprint_future[1]) is False:  # N square
                    return False
                elif self.a_square_path_clear_n(footprint_current[5], footprint_future[5]) is False:  # NE square
                    return False
                elif self.a_square_path_clear_n(footprint_current[6], footprint_future[6]) is False:  # NW square
                    return False
                else:
                    return

        elif col_dir > 0:  # going in NE direction
            if items_in_cur_footprint[5] != self._turn:  # verifying a token is in the northeast spot to be able to move
                return False
            else:
                if self.a_square_path_clear_ne(footprint_current[6], footprint_future[6]) is False:  # NW square
                    return False
                elif self.a_square_path_clear_ne(footprint_current[1], footprint_future[1]) is False:  # N square
                    return False
                elif self.a_square_path_clear_ne(footprint_current[5], footprint_future[5]) is False:  # NE square
                    return False
                elif self.a_square_path_clear_ne(footprint_current[3], footprint_future[3]) is False:  # E square
                    return False
                elif self.a_square_path_clear_ne(footprint_current[7], footprint_future[7]) is False:  # SE square
                    return False
                else:
                    return True

        elif col_dir < 0:  # going in NW direction
            if items_in_cur_footprint[6] != self._turn:  # verifying a token is in the northwest spot to be able to move
                return False
            else:
                if self.a_square_path_clear_nw(footprint_current[6], footprint_future[6]) is False:  # NW square
                    return False
                elif self.a_square_path_clear_nw(footprint_current[1], footprint_future[1]) is False:  # N square
                    return False
                elif self.a_square_path_clear_nw(footprint_current[5], footprint_future[5]) is False:  # NE square
                    return False
                elif self.a_square_path_clear_nw(footprint_current[4], footprint_future[4]) is False:  # W square
                    return False
                elif self.a_square_path_clear_nw(footprint_current[8], footprint_future[8]) is False:  # SW square
                    return False
                else:
                    return True

    def check_sx_path_for_footprint(self, col_dir, items_in_cur_footprint, footprint_current, footprint_future):
        """""
        purpose: checks whether the player has the token in the correct place for the desired path and check whether
        the path is clear for the footprint to go from current to new if moving in a S, SW, or SW path
        parameters: col_dir, items_in_cur_footprint, footprint_current, footprint_future
        return: True or False
        """

        if col_dir == 0:  # going in the S direction
            if items_in_cur_footprint[2] != self._turn:
                return False
            else:
                if self.a_square_path_clear_s(footprint_current[2], footprint_future[2]) is False:  # S square
                    return False
                elif self.a_square_path_clear_s(footprint_current[7], footprint_future[7]) is False:  # SE square
                    return False
                elif self.a_square_path_clear_s(footprint_current[8], footprint_future[8]) is False:  # SW square
                    return False
                else:
                    return True

        elif col_dir > 0:  # going in SE direction
            if items_in_cur_footprint[7] != self._turn:
                return False
            else:
                if self.a_square_path_clear_se(footprint_current[7], footprint_future[7]) is False:  # SE square
                    return False
                elif self.a_square_path_clear_se(footprint_current[2], footprint_future[2]) is False:  # S square
                    return False
                elif self.a_square_path_clear_se(footprint_current[8], footprint_future[8]) is False:  # SW square
                    return False
                elif self.a_square_path_clear_se(footprint_current[3], footprint_future[3]) is False:  # E square
                    return False
                elif self.a_square_path_clear_se(footprint_current[5], footprint_future[5]) is False:  # NE square
                    return False
                else:
                    return True

        elif col_dir < 0:  # going in SW direction
            if items_in_cur_footprint[8] != self._turn:
                return False
            else:
                if self.a_square_path_clear_sw(footprint_current[7], footprint_future[7]) is False:  # SE square
                    return False
                elif self.a_square_path_clear_sw(footprint_current[2], footprint_future[2]) is False:  # S square
                    return False
                elif self.a_square_path_clear_sw(footprint_current[8], footprint_future[8]) is False:  # SW square
                    return False
                elif self.a_square_path_clear_sw(footprint_current[4], footprint_future[4]) is False:  # W square
                    return False
                elif self.a_square_path_clear_sw(footprint_current[6], footprint_future[6]) is False:  # NW square
                    return False
                else:
                    return True

    def check_e_path_for_footprint(self, items_in_cur_footprint, footprint_current, footprint_future):
        """""
         purpose: checks whether the player has the token in the correct place for the desired path and check whether
         the path is clear for the footprint to go from current to new if moving in an East path
         parameters: col_dir, items_in_cur_footprint, footprint_current, footprint_future
         return: True or False
         """

        if items_in_cur_footprint[3] != self._turn:
            return False
        else:
            if self.a_square_path_clear_e(footprint_current[3], footprint_future[3]) is False:  # E square
                return False
            elif self.a_square_path_clear_e(footprint_current[5], footprint_future[5]) is False:  # NE square
                return False
            elif self.a_square_path_clear_e(footprint_current[7], footprint_future[7]) is False:  # SE square
                return False
            else:
                return True

    def check_w_path_for_footprint(self, items_in_cur_footprint, footprint_current, footprint_future):
        """""
         purpose: checks whether the player has the token in the correct place for the desired path and check whether
         the path is clear for the footprint to go from current to new if moving in an West path
         parameters: col_dir, items_in_cur_footprint, footprint_current, footprint_future
         return: True or False
         """

        if items_in_cur_footprint[4] != self._turn:
            return False
        else:
            if self.a_square_path_clear_w(footprint_current[4], footprint_future[4]) is False:  # W square
                return False
            elif self.a_square_path_clear_w(footprint_current[8], footprint_future[8]) is False:  # SW square
                return False
            elif self.a_square_path_clear_w(footprint_current[7], footprint_future[7]) is False:  # SE square
                return False
            else:
                return True

    def a_square_path_clear_n(self, curr_loc, future_loc):
        """""
        purpose: determines if square moving in north direction will run into anything prior to
        getting to desired location
        parameters: current location (list of row, col), future location (list of row, col)
        return: None or False
        """
        col_to = future_loc[1]
        row_from = curr_loc[0]
        row_to = future_loc[0]
        board = self._board.get_board()

        result = self.a_square_path_clear_n_helper(col_to, row_from, row_to, board)
        return result

    def a_square_path_clear_n_helper(self, col_to, row_from, row_to, board):
        """""
        purpose: helper function for determining if the path is clear moving east for a square
        parameters: col_to, row_from, row_to, board
        return: True or False
        """
        row_from_plus_one = row_from + 1

        if row_from_plus_one == row_to:
            return True

        if board[row_from_plus_one][col_to] != ' ':
            return False
        else:
            return self.a_square_path_clear_n_helper(col_to, row_from_plus_one, row_to, board)

    def a_square_path_clear_s(self, curr_loc, future_loc):
        """""
        purpose: determines if square moving in south direction will run into anything prior to
        getting to desired location
        parameters: current location (list of row, col), future location (list of row, col)
        return: True or False
        """
        col_to = future_loc[1]
        row_to = future_loc[0]
        row_from = curr_loc[0]
        board = self._board.get_board()

        result = self.a_square_path_clear_s_helper(col_to, row_from, row_to, board)
        return result

    def a_square_path_clear_s_helper(self, col_to, row_from, row_to, board):
        """""
        purpose: helper function for determining if the a squares's path is clear moving east for a square
        parameters: col_from, row_from, row_to, board
        return: None or False
        """

        row_from_minus_one = row_from - 1

        if row_from_minus_one == row_to:
            return True

        if board[row_from_minus_one][col_to] != ' ':
            return False
        else:
            return self.a_square_path_clear_s_helper(col_to, row_from_minus_one, row_to, board)

    def a_square_path_clear_e(self, curr_loc, future_loc):
        """""
        purpose: determines if square moving in east direction will run into anything prior to
        getting to desired location
        parameters: current location (list of row, col), future location (list of row, col)
        return: True or False
        """
        col_to = future_loc[1]
        col_from = curr_loc[1]
        row_from = future_loc[0]
        board = self._board.get_board()

        result = self.a_square_path_clear_e_helper(col_from, col_to, row_from, board)
        return result

    def a_square_path_clear_e_helper(self, col_from, col_to, row_from, board):
        """""
        purpose: helper function for determining if the a square's path is clear moving east for a square
        parameters: col_from, col_to, row_from, board
        return: True or False
        """
        col_from_minus_one = col_from + 1

        if col_from_minus_one == col_to:
            return True

        if board[row_from][col_from_minus_one] != ' ':
            return False
        else:
            return self.a_square_path_clear_e_helper(col_from_minus_one, col_to, row_from, board)

    def a_square_path_clear_w(self, curr_loc, future_loc):
        """""
        purpose: determines if square moving in west direction will run into anything prior to
        getting to desired location
        parameters: current location (list of row, col), future location (list of row, col)
        return: True or False
        """
        col_to = future_loc[1]
        col_from = curr_loc[1]
        row_from = future_loc[0]
        board = self._board.get_board()

        result = self.a_square_path_clear_w_helper(col_from, col_to, row_from, board)
        return result

    def a_square_path_clear_w_helper(self, col_from, col_to, row_from, board):
        """""
        purpose: helper function for determining if the square's path is clear moving west
        parameters: col_from, col_to, row_from, board
        return: None or False
        """
        col_from_plus_one = col_from - 1

        if col_from_plus_one == col_to:
            return True

        if board[row_from][col_from_plus_one] != ' ':
            return False
        else:
            return self.a_square_path_clear_w_helper(col_from_plus_one, col_to, row_from, board)

    def a_square_path_clear_nw(self, curr_loc, future_loc):
        """""
        purpose: determines if square moving in northwest direction will run into anything prior to
        getting to desired location
        parameters: current location (list of row, col), future location (list of row, col)
        return: True or False
        """

        col_to = future_loc[1]
        col_from = curr_loc[1]
        row_from = curr_loc[0]
        row_to = future_loc[0]
        board = self._board.get_board()

        result = self.a_square_path_clear_nw_helper(col_from, col_to, row_from, row_to, board)
        return result

    def a_square_path_clear_nw_helper(self, col_from, col_to, row_from, row_to, board):
        """""
        purpose: helper function for determining if the square's path is clear moving northwest
        parameters: col_from, col_to, row_from, row_to, board
        return: True or False
        """
        col_from_minus_one = col_from - 1
        row_from_plus_one = row_from + 1

        if col_from_minus_one == col_to and row_from_plus_one == row_to:
            return True

        if board[row_from_plus_one][col_from_minus_one] != ' ':
            return False
        else:
            return self.a_square_path_clear_nw_helper(col_from_minus_one, col_to, row_from_plus_one, row_to, board)

    def a_square_path_clear_ne(self, curr_loc, future_loc):
        """""
        purpose: determines if square moving in northeast direction will run into anything prior to
        getting to desired location
        parameters: current location (list of row, col), future location (list of row, col)
        return: True or False
        """
        col_to = future_loc[1]
        col_from = curr_loc[1]
        row_from = curr_loc[0]
        row_to = future_loc[0]
        board = self._board.get_board()

        result = self.a_square_path_clear_ne_helper(col_from, col_to, row_from, row_to, board)
        return result

    def a_square_path_clear_ne_helper(self, col_from, col_to, row_from, row_to, board):
        """""
        purpose: helper function for determining if the path is clear moving northwest
        parameters: col_from, col_to, row_from, row_to, board
        return: True or False
        """
        col_from_plus_one = col_from + 1
        row_from_plus_one = row_from + 1

        if col_from_plus_one == col_to and row_from_plus_one == row_to:
            return True

        if board[row_from_plus_one][col_from_plus_one] != ' ':
            return False
        else:
            return self.a_square_path_clear_ne_helper(col_from_plus_one, col_to, row_from_plus_one, row_to, board)

    def a_square_path_clear_sw(self, curr_loc, future_loc):
        """""
        purpose: determines if square moving in southwest direction will run into anything prior to
        getting to desired location
        parameters: current location (list of row, col), future location (list of row, col)
        return: True or False
        """
        col_to = future_loc[1]
        col_from = curr_loc[1]
        row_from = curr_loc[0]
        row_to = future_loc[0]
        board = self._board.get_board()

        result = self.a_square_path_clear_sw_helper(col_from, col_to, row_from, row_to, board)
        return result

    def a_square_path_clear_sw_helper(self, col_from, col_to, row_from, row_to, board):
        """""
        purpose: helper function for determining if the path is clear moving southwest
        parameters: col_from, col_to, row_from, row_to, board
        return: True or False
        """
        col_from_minus_one = col_from - 1
        row_from_minus_one = row_from - 1

        if col_from_minus_one == col_to and row_from_minus_one == row_to:
            return

        if board[row_from_minus_one][col_from_minus_one] != ' ':
            return False
        else:
            return self.a_square_path_clear_sw_helper(col_from_minus_one, col_to, row_from_minus_one, row_to, board)

    def a_square_path_clear_se(self, curr_loc, future_loc):

        """""
        purpose: determines if square moving in southeast direction will run into anything prior to
        getting to desired location
        parameters: current location (list of row, col), future location (list of row, col)
        return: True or False
        """
        col_to = future_loc[1]
        col_from = curr_loc[1]
        row_from = curr_loc[0]
        row_to = future_loc[0]
        board = self._board.get_board()

        result = self.a_square_path_clear_se_helper(col_from, col_to, row_from, row_to, board)

        return result

    def a_square_path_clear_se_helper(self, col_from, col_to, row_from, row_to, board):
        """""
        purpose: helper function for determining if the path is clear moving southeast
        parameters: col_from, col_to, row_from, row_to, board
        return: True or False
        """

        col_from_plus_one = col_from + 1
        row_from_minus_one = row_from - 1

        if col_from_plus_one == col_to and row_from_minus_one == row_to:
            return

        if board[row_from_minus_one][col_from_plus_one] != ' ':
            return False
        else:
            return self.a_square_path_clear_se_helper(col_from_plus_one, col_to, row_from_minus_one, row_to, board)


