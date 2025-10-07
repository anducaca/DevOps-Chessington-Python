from chessington.engine.board import Board
from chessington.engine.data import Player, Square
from chessington.engine.pieces import Pawn, King, Knight, Bishop, Rook, Queen 


class TestPawns:

    @staticmethod
    def test_white_pawns_can_move_up_one_square():

        # Arrange
        board = Board.empty()
        pawn = Pawn(Player.WHITE)
        square = Square.at(1, 4)
        board.set_piece(square, pawn)

        # Act
        moves = pawn.get_available_moves(board)

        # Assert
        assert Square.at(2, 4) in moves

    @staticmethod
    def test_black_pawns_can_move_down_one_square():

        # Arrange
        board = Board.empty()
        pawn = Pawn(Player.BLACK)
        square = Square.at(6, 4)
        board.set_piece(square, pawn)

        # Act
        moves = pawn.get_available_moves(board)

        # Assert
        assert Square.at(5, 4) in moves

    @staticmethod
    def test_white_pawn_can_move_up_two_squares_if_not_moved():

        # Arrange
        board = Board.empty()
        pawn = Pawn(Player.WHITE)
        square = Square.at(1, 4)
        board.set_piece(square, pawn)

        # Act
        moves = pawn.get_available_moves(board)

        # Assert
        assert Square.at(3, 4) in moves

    @staticmethod
    def test_black_pawn_can_move_down_two_squares_if_not_moved():

        # Arrange
        board = Board.empty()
        pawn = Pawn(Player.BLACK)
        square = Square.at(6, 4)
        board.set_piece(square, pawn)

        # Act
        moves = pawn.get_available_moves(board)

        # Assert
        assert Square.at(4, 4) in moves

    @staticmethod
    def test_white_pawn_cannot_move_up_two_squares_if_already_moved():

        # Arrange
        board = Board.empty()
        pawn = Pawn(Player.WHITE)
        starting_square = Square.at(1, 4)
        board.set_piece(starting_square, pawn)

        intermediate_square = Square.at(2, 4)
        pawn.move_to(board, intermediate_square)

        # Act
        moves = pawn.get_available_moves(board)

        # Assert
        assert Square.at(3, 4) in moves
        assert Square.at(4, 4) not in moves

    @staticmethod
    def test_black_pawn_cannot_move_down_two_squares_if_already_moved():

        # Arrange
        board = Board.empty()
        pawn = Pawn(Player.BLACK)
        starting_square = Square.at(6, 4)
        board.set_piece(starting_square, pawn)

        intermediate_square = Square.at(5, 4)
        board.current_player = Player.BLACK
        pawn.move_to(board, intermediate_square)

        # Act
        moves = pawn.get_available_moves(board)

        # Assert
        assert Square.at(4, 4) in moves
        assert Square.at(3, 4) not in moves




class TestKing:
    @staticmethod
    def test_king_can_only_move_one_square_in_any_direction():
        # Arrange
        board = Board.empty()
        king = King(Player.WHITE)
        starting_square = Square.at(4, 4)
        board.set_piece(starting_square, king)

        # Act
        moves = king.get_available_moves(board)

        # Assert: all 8 adjacent squares should be valid
        expected_moves = [
            Square.at(3, 3), Square.at(3, 4), Square.at(3, 5),
            Square.at(4, 3),                 Square.at(4, 5),
            Square.at(5, 3), Square.at(5, 4), Square.at(5, 5)
        ]
        for sq in expected_moves:
            assert sq in moves

        # And the King must NOT be able to move two squares away
        forbidden_moves = [
            Square.at(2, 4), Square.at(6, 4),  # vertical two-step
            Square.at(4, 2), Square.at(4, 6),  # horizontal two-step
            Square.at(2, 2), Square.at(6, 6)   # diagonal two-step
        ]
        for sq in forbidden_moves:
            assert sq not in moves


class TestKnight:
    @staticmethod
    def test_knight_has_eight_moves_from_centre():
        # Arrange
        board = Board.empty()
        knight = Knight(Player.WHITE)
        start_square = Square.at(4, 4)
        board.set_piece(start_square, knight)

        # Act
        moves = knight.get_available_moves(board)

        # Assert: all 8 L-shaped moves should be available
        expected_moves = [
            Square.at(2, 3), Square.at(2, 5),
            Square.at(3, 2), Square.at(3, 6),
            Square.at(5, 2), Square.at(5, 6),
            Square.at(6, 3), Square.at(6, 5)
        ]
        assert set(moves) == set(expected_moves)

    @staticmethod
    def test_knight_moves_reduced_near_board_edge():
        # Arrange
        board = Board.empty()
        knight = Knight(Player.WHITE)
        start_square = Square.at(0, 0)  # top-left corner
        board.set_piece(start_square, knight)

        # Act
        moves = knight.get_available_moves(board)

        # Assert: only two valid moves from corner
        expected_moves = [Square.at(1, 2), Square.at(2, 1)]
        assert set(moves) == set(expected_moves)

    @staticmethod
    def test_knight_can_capture_enemy_but_not_friendly():
        # Arrange
        board = Board.empty()
        knight = Knight(Player.WHITE)
        start_square = Square.at(4, 4)
        board.set_piece(start_square, knight)

        enemy_piece = Pawn(Player.BLACK)
        friendly_piece = Pawn(Player.WHITE)

        enemy_square = Square.at(6, 5)   # valid knight move
        friendly_square = Square.at(2, 3)  # valid knight move

        board.set_piece(enemy_square, enemy_piece)
        board.set_piece(friendly_square, friendly_piece)

        # Act
        moves = knight.get_available_moves(board)

        # Assert: enemy square is included, friendly square is not
        assert enemy_square in moves
        assert friendly_square not in moves

class TestBishop:
    @staticmethod
    def test_bishop_moves_diagonally_from_centre():
        # Arrange
        board = Board.empty()
        bishop = Bishop(Player.WHITE)
        start_square = Square.at(4, 4)
        board.set_piece(start_square, bishop)

        # Act
        moves = bishop.get_available_moves(board)

        # Assert: bishop should move along all diagonals until edge
        expected_moves = []
        # top-left diagonal
        expected_moves += [Square.at(r, c) for r, c in zip(range(3, -1, -1), range(3, -1, -1))]
        # top-right diagonal
        expected_moves += [Square.at(r, c) for r, c in zip(range(3, -1, -1), range(5, 8))]
        # bottom-left diagonal
        expected_moves += [Square.at(r, c) for r, c in zip(range(5, 8), range(3, -1, -1))]
        # bottom-right diagonal
        expected_moves += [Square.at(r, c) for r, c in zip(range(5, 8), range(5, 8))]

        for sq in expected_moves:
            assert sq in moves

    @staticmethod
    def test_bishop_blocked_by_friendly_piece():
        # Arrange
        board = Board.empty()
        bishop = Bishop(Player.WHITE)
        start_square = Square.at(4, 4)
        board.set_piece(start_square, bishop)

        friendly = Pawn(Player.WHITE)
        block_square = Square.at(6, 6)
        board.set_piece(block_square, friendly)

        # Act
        moves = bishop.get_available_moves(board)

        # Assert: bishop cannot move past friendly piece
        assert block_square not in moves
        assert Square.at(7, 7) not in moves

    @staticmethod
    def test_bishop_can_capture_enemy_but_not_move_past():
        # Arrange
        board = Board.empty()
        bishop = Bishop(Player.WHITE)
        start_square = Square.at(4, 4)
        board.set_piece(start_square, bishop)

        enemy = Pawn(Player.BLACK)
        enemy_square = Square.at(6, 6)
        board.set_piece(enemy_square, enemy)

        # Act
        moves = bishop.get_available_moves(board)

        # Assert: bishop can capture enemy but not move beyond
        assert enemy_square in moves
        assert Square.at(7, 7) not in moves

class TestRook:
    @staticmethod
    def test_rook_moves_straight_lines_from_centre():
        # Arrange
        board = Board.empty()
        rook = Rook(Player.WHITE)
        start_square = Square.at(4, 4)
        board.set_piece(start_square, rook)

        # Act
        moves = rook.get_available_moves(board)

        # Assert: rook should move along all ranks and files until edge
        expected_moves = []
        # Up
        expected_moves += [Square.at(r, 4) for r in range(3, -1, -1)]
        # Down
        expected_moves += [Square.at(r, 4) for r in range(5, 8)]
        # Left
        expected_moves += [Square.at(4, c) for c in range(3, -1, -1)]
        # Right
        expected_moves += [Square.at(4, c) for c in range(5, 8)]

        for sq in expected_moves:
            assert sq in moves

    @staticmethod
    def test_rook_blocked_by_friendly_piece():
        # Arrange
        board = Board.empty()
        rook = Rook(Player.WHITE)
        start_square = Square.at(4, 4)
        board.set_piece(start_square, rook)

        friendly = Pawn(Player.WHITE)
        block_square = Square.at(4, 6)
        board.set_piece(block_square, friendly)

        # Act
        moves = rook.get_available_moves(board)

        # Assert: rook cannot move onto or past friendly piece
        assert block_square not in moves
        assert Square.at(4, 7) not in moves

    @staticmethod
    def test_rook_can_capture_enemy_but_not_move_past():
        # Arrange
        board = Board.empty()
        rook = Rook(Player.WHITE)
        start_square = Square.at(4, 4)
        board.set_piece(start_square, rook)

        enemy = Pawn(Player.BLACK)
        enemy_square = Square.at(4, 6)
        board.set_piece(enemy_square, enemy)

        # Act
        moves = rook.get_available_moves(board)

        # Assert: rook can capture enemy but not move beyond
        assert enemy_square in moves
        assert Square.at(4, 7) not in moves

class TestQueen:
    @staticmethod
    def test_queen_moves_like_rook_and_bishop():
        # Arrange
        board = Board.empty()
        queen = Queen(Player.WHITE)
        start_square = Square.at(4, 4)
        board.set_piece(start_square, queen)

        # Act
        moves = queen.get_available_moves(board)

        # Assert: queen should move along ranks, files, and diagonals
        expected_moves = []

        # Vertical up and down
        expected_moves += [Square.at(r, 4) for r in range(3, -1, -1)]
        expected_moves += [Square.at(r, 4) for r in range(5, 8)]

        # Horizontal left and right
        expected_moves += [Square.at(4, c) for c in range(3, -1, -1)]
        expected_moves += [Square.at(4, c) for c in range(5, 8)]

        # Diagonals
        expected_moves += [Square.at(r, c) for r, c in zip(range(3, -1, -1), range(3, -1, -1))]
        expected_moves += [Square.at(r, c) for r, c in zip(range(3, -1, -1), range(5, 8))]
        expected_moves += [Square.at(r, c) for r, c in zip(range(5, 8), range(3, -1, -1))]
        expected_moves += [Square.at(r, c) for r, c in zip(range(5, 8), range(5, 8))]

        for sq in expected_moves:
            assert sq in moves

    @staticmethod
    def test_queen_blocked_by_friendly_piece():
        # Arrange
        board = Board.empty()
        queen = Queen(Player.WHITE)
        start_square = Square.at(4, 4)
        board.set_piece(start_square, queen)

        friendly = Pawn(Player.WHITE)
        block_square = Square.at(4, 6)
        board.set_piece(block_square, friendly)

        # Act
        moves = queen.get_available_moves(board)

        # Assert: queen cannot move onto or past friendly piece
        assert block_square not in moves
        assert Square.at(4, 7) not in moves

    @staticmethod
    def test_queen_can_capture_enemy_but_not_move_past():
        # Arrange
        board = Board.empty()
        queen = Queen(Player.WHITE)
        start_square = Square.at(4, 4)
        board.set_piece(start_square, queen)

        enemy = Pawn(Player.BLACK)
        enemy_square = Square.at(6, 6)
        board.set_piece(enemy_square, enemy)

        # Act
        moves = queen.get_available_moves(board)

        # Assert: queen can capture enemy but not move beyond
        assert enemy_square in moves
        assert Square.at(7, 7) not in moves