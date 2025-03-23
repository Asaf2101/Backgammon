from Graphics import *
from State import *

class Environment:
    def __init__(self, state : State = None):
        if state == None:
            self.state = State()
        else:
            self.state = state
    
    def end_of_game(self):    # returns if game ended and who won
        white_checkers_out, black_checkers_out = self.state.checkers_out
        if white_checkers_out == 15:
            return 1
        elif black_checkers_out == 15:
            return -1
        return 0
    
    def is_end_of_game(self, state):   # returns if game ended for the provided state
        white_checkers_out, black_checkers_out = state.checkers_out
        if white_checkers_out == 15 or black_checkers_out == 15: return True
        else: return False

    def all_checkers_in_home(self, board, player):
        board = board
        white_checkers_eaten, black_checkers_eaten = self.state.checkers_eaten

        if player == -1:
            if black_checkers_eaten > 0: return False
            for i in range(6, 24):
                if board[i] < 0: return False
        else:
            if white_checkers_eaten > 0: return False
            for i in range(18):
                if board[i] > 0: return False

        return True
        
    def no_checkers_behind(self, player, dice_needed):
        if self.all_checkers_in_home(self.state.board, player) == False: return False
        board = self.state.board

        if player == -1:
            for i in range(dice_needed, 6):
                if board[i] < 0: return False
        else:
            for i in range(18, TRIANGLES_AMOUNT - dice_needed):
                if board[i] > 0: return False
        return True

    def roll_dice(self):
        state = self.state
        blocked = state.blocked
        if state.throw and blocked == 0:
            dice1, dice2 = random.randint(1, 6), random.randint(1, 6)
            state.dice = dice1, dice2
            state.throw = False
            # print('dice rolled:', dice1, dice2)
        elif blocked == 1:
            state.blocked = 2

    def switch_players(self):
        if self.state.player == -1:
            self.state.player = 1
        else:
            self.state.player = -1

    def move_action(self, action):   # returns after state and reward
        move1, move2 = action   
        reward1 = self.move(move1)
        reward2 = self.move(move2)
        reward = reward1 + reward2

        dice = self.state.dice
        if self.state.blocked == 0:             # blocked 0: rolls, regular action, in the end if double blocked = 1
            if dice[0] == dice[1]:              # blocked 1: no roll, immediately blocked = 2
                self.state.blocked = 1          # blocked 2: no roll, end turn with (-1) action, in the end blocked = 3
            else:                               # blocked 3: no roll, regular action, in the end blocked = 0
                self.state.throw = True

        elif self.state.blocked == 2:
            self.state.blocked = 3
            
        elif self.state.blocked == 3:
            self.state.throw = True
            self.state.blocked = 0

        # win / loss +- 10 and +- according to diff
        if self.end_of_game() == 1:
            reward -= 10 + 15 - self.state.checkers_out[1]
        elif self.end_of_game() == -1:
            reward += 10 + 15 - self.state.checkers_out[0]

        reward /= 10  # normalize reward value

        return self.state, reward

    def move(self, move):
        from_area, to_area = move
        board = self.state.board
        white_checkers_eaten, black_checkers_eaten = self.state.checkers_eaten
        white_checkers_out, black_checkers_out = self.state.checkers_out
        player = self.state.player

        if move == (-1, -1):
            return 0          # reward 0

        start_w_eaten, start_b_eaten = white_checkers_eaten, black_checkers_eaten
        start_w_out, start_b_out = white_checkers_out, black_checkers_out
        start_w_checkers_end_zone = sum(x for x in board[18:24] if x > 0)
        start_b_checkers_end_zone = abs(sum(x for x in board[0:6] if x < 0))
        start_b_ones = np.count_nonzero(board == -1)
        start_w_ones = np.count_nonzero(board == 1)
                
        if player == -1:
            if from_area == 24:
                black_checkers_eaten -= 1
                if board[to_area] == 1:
                    board[to_area] = -1
                    white_checkers_eaten += 1
                else:
                    board[to_area] -= 1
            elif to_area == 26:
                black_checkers_out += 1
                board[from_area] += 1
            else:
                if board[to_area] == 1:
                    board[to_area] = -1
                    white_checkers_eaten += 1
                    board[from_area] += 1
                else:
                    board[to_area] -= 1
                    board[from_area] += 1

        else:
            if from_area == 25:
                white_checkers_eaten -= 1
                if board[to_area] == -1:
                    board[to_area] = 1
                    black_checkers_eaten += 1
                else:
                    board[to_area] += 1
            elif to_area == 27:
                white_checkers_out += 1
                board[from_area] -= 1
            else:
                if board[to_area] == -1:
                    board[to_area] = 1
                    black_checkers_eaten += 1
                    board[from_area] -= 1
                else:
                    board[to_area] += 1
                    board[from_area] -= 1
        
        # calculate reward
        w_checkers_end_zone = sum(x for x in board[18:24] if x > 0)
        b_checkers_end_zone = abs(sum(x for x in board[0:6] if x < 0))
        b_ones, w_ones = np.count_nonzero(board == -1), np.count_nonzero(board == 1)
        reward = 0
        if player == -1:
            reward += white_checkers_eaten - start_w_eaten
            reward += 0.5 * (start_b_ones - b_ones)
        if player == 1:
            reward -= black_checkers_eaten - start_b_eaten
            reward -= 0.5 * (start_w_ones - w_ones)
        reward += black_checkers_out - start_b_out
        reward -= white_checkers_out - start_w_out
        if not self.all_checkers_in_home(board, player):
            reward += 0.5 * (b_checkers_end_zone - start_b_checkers_end_zone)
            reward -= 0.5 * (w_checkers_end_zone - start_w_checkers_end_zone)

        self.state.board = board
        self.state.checkers_eaten = white_checkers_eaten, black_checkers_eaten
        self.state.checkers_out = white_checkers_out, black_checkers_out

        return reward

    def legal_move(self, move):
        from_area, to_area = move
        board = self.state.board
        white_checkers_eaten, black_checkers_eaten = self.state.checkers_eaten
        dice1, dice2 = self.state.dice
        player = self.state.player

        if from_area == -1 and to_area == -1:
            return -1

        if player == -1:
            if from_area == 25 or from_area == 27 or to_area == 25 or to_area == 27 or to_area == 24 or from_area == 26: return False

            if black_checkers_eaten > 0:
                if from_area != 24 or not 17 < to_area < 24 or board[to_area] > 1: return False
                dice_needed = TRIANGLES_AMOUNT - to_area
            
            elif to_area == 26:
                if self.all_checkers_in_home(board, -1) == False: return False
                if from_area == 24 or board[from_area] > -1: return False
                dice_needed = from_area + 1
                if self.no_checkers_behind(player, dice_needed) == True:
                    dice_needed = list(range(dice_needed, 7))
            
            else:
                if from_area == 24 and black_checkers_eaten < 1: return False
                if board[from_area] > -1 or board[to_area] > 1: return False
                dice_needed = from_area - to_area

        else:
            if from_area == 24 or from_area == 26 or to_area == 24 or to_area == 26 or to_area == 25 or from_area == 27: return False

            if white_checkers_eaten > 0:
                if from_area != 25 or not -1 < to_area < 6 or board[to_area] < -1: return False
                dice_needed = to_area + 1

            elif to_area == 27:
                if self.all_checkers_in_home(board, 1) == False: return False
                if from_area == 25 or board[from_area] < 1: return False
                dice_needed = TRIANGLES_AMOUNT - from_area
                if self.no_checkers_behind(player, dice_needed) == True:
                    dice_needed = list(range(dice_needed, 7))

            else:
                if from_area == 25 and white_checkers_eaten < 1: return False
                if board[from_area] < 1 or board[to_area] < -1: return False
                dice_needed = to_area - from_area
        
        if type(dice_needed) is not list:
            if dice_needed == dice1 or dice_needed == dice2: return dice_needed
        else:
            if dice1 in dice_needed and dice2 in dice_needed: return dice_needed
            elif dice1 in dice_needed: return dice1
            elif dice2 in dice_needed: return dice2
        return False

    def legal_action(self, dice_first_move, dice_second_move):
        dice1, dice2 = self.state.dice

        if type(dice_first_move) is not list: dice_first_move = [dice_first_move]
        if type(dice_second_move) is not list: dice_second_move = [dice_second_move]

        return (dice1 in dice_first_move and dice2 in dice_second_move) or (dice1 in dice_second_move and dice2 in dice_first_move)



    def slow_get_all_first_moves(self):    # returns all first legal moves, if none then (-1, -1)
        moves = []
        for from_area in range(AREAS_AMOUNT):
            for to_area in range(AREAS_AMOUNT):
                if self.legal_move((from_area, to_area)) is not False:
                    moves.append((from_area, to_area))
        if len(moves) == 0:                                      # if no moves available
            moves.append((-1, -1))
        return moves

    def slow_get_all_actions(self):    # checks and returns all legal actions
        if self.state.blocked == 2:
            return [((-1, -1), (-1, -1))]
        
        first_moves = self.slow_get_all_first_moves()
        if len(first_moves) == 1 and first_moves[0] == (-1, -1):   # if there were no first moves available, there is no legal action 
            return [((-1, -1), (-1, -1))]
        
        actions = []

        for first_move in first_moves:
            added_action = False
            for from_area in range(AREAS_AMOUNT):
                for to_area in range(AREAS_AMOUNT):

                    temp_state : State = self.state.copy()   # create copy of current state
                    self.move(first_move)                    # play the first move, so that 'legal_move' check according to updated state
                    
                    dice_second_move = self.legal_move((from_area, to_area))  # check if second move is legal and get dice needed
                    self.state = temp_state                                   # return the state to the original one
                    
                    if dice_second_move is not False:                              # if second move is legal
                        dice_first_move = self.legal_move(first_move)              # get the dice needed for the first move
                        if self.legal_action(dice_first_move, dice_second_move):  # check if action is legal, add to list
                            actions.append((first_move, (from_area, to_area)))
                            added_action = True
            if added_action is False:          # if there wasn't a legal second move, the legal action only has the first move
                actions.append((first_move, (-1, -1)))
        
        return actions
        
    def old_get_indices(self, state : State, dice):  # returns the board indices legal to play from according to dice
        player = state.player
        board : np.ndarray = state.board
        
        if player == -1:
            indices = np.arange(len(board))
            valid_indices = np.where(
                (board < 0) & 
                (indices - dice >= 0) & 
                (indices - dice <= 23))[0]
            valid_indices = valid_indices[(board[valid_indices - dice] < 2)]
        else:
            indices = np.arange(len(board))
            valid_indices = np.where(
                (board > 0) & 
                (indices + dice >= 0) & 
                (indices + dice <= 23))[0]
            valid_indices = valid_indices[(board[valid_indices + dice] > -2)]
        
        return valid_indices

    
    
    # new get all actions logic

    def get_indices(self, board, dice, player):  # returns the board indices legal to play from according to dice
        player = player
        board : np.ndarray = board
        
        if player == -1:
            indices = np.arange(len(board))
            valid_indices = np.where(
                (board < 0) & 
                (indices - dice >= 0) & 
                (indices - dice <= 23))[0]
            valid_indices = valid_indices[(board[valid_indices - dice] < 2)]
        else:
            indices = np.arange(len(board))
            valid_indices = np.where(
                (board > 0) & 
                (indices + dice >= 0) & 
                (indices + dice <= 23))[0]
            valid_indices = valid_indices[(board[valid_indices + dice] > -2)]
        
        return valid_indices

    def can_eaten_play(self, state : State, dice):
        player = state.player
        board : np.ndarray = state.board

        if player == -1:
            return board[len(board) - dice] < 2
        else:
            return board[dice - 1] > -2

    def get_all_actions(self, state : State):
        player = state.player
        dice1, dice2 = state.dice
        white_checkers_eaten, black_checkers_eaten = state.checkers_eaten
        board : np.ndarray = state.board
        actions = []

        if self.state.blocked == 2:
            return [((-1, -1), (-1, -1))]
        
        if player == -1:
            if black_checkers_eaten == 0: return self.get_regular_board_actions(state)
            elif black_checkers_eaten > 1:
                half1 = (24, len(board) - dice1) if self.can_eaten_play(state, dice1) else (-1, -1)
                half2 = (24, len(board) - dice2) if self.can_eaten_play(state, dice2) else (-1, -1)
                return [(half1, half2)]
            elif black_checkers_eaten == 1:
                if not self.can_eaten_play(state, dice1) and not self.can_eaten_play(state, dice2):
                    return [((-1, -1), (-1, -1))]
                else:
                    if self.can_eaten_play(state, dice1):
                        half1 = (24, len(board) - dice1)
                        updated_board = board.copy()
                        updated_board[len(board) - dice1] -= 2
                        indices2 = self.get_indices(updated_board, dice2, player)
                        if indices2.size > 0:
                            actions.extend([(half1, (a, a - dice2)) for a in indices2])
                        else:
                            actions.append((half1, (-1, -1)))
                    if self.can_eaten_play(state, dice2):
                        half1 = (24, len(board) - dice2)
                        updated_board = board.copy()
                        updated_board[len(board) - dice2] -= 2
                        indices1 = self.get_indices(updated_board, dice1, player)
                        if indices1.size > 0:
                            actions.extend([(half1, (a, a - dice1)) for a in indices1])
                        else:
                            actions.append((half1, (-1, -1)))
                    return actions
        
        else:
            if white_checkers_eaten == 0: return self.get_regular_board_actions(state)
            elif white_checkers_eaten > 1:
                half1 = (25, dice1 - 1) if self.can_eaten_play(state, dice1) else (-1, -1)
                half2 = (25, dice2 - 1) if self.can_eaten_play(state, dice2) else (-1, -1)
                return[(half1, half2)]
            elif white_checkers_eaten == 1:
                if not self.can_eaten_play(state, dice1) and not self.can_eaten_play(state, dice2):
                    return [((-1, -1), (-1, -1))]
                else:
                    if self.can_eaten_play(state, dice1):
                        half1 = (25, dice1 - 1)
                        updated_board = board.copy()
                        updated_board[dice1 - 1] += 2
                        indices2 = self.get_indices(updated_board, dice2, player)
                        if indices2.size > 0:  # if there is a move with the other dice as well
                            actions.extend([(half1, (a, a + dice2)) for a in indices2])
                        else:
                            actions.append((half1, (-1, -1)))
                    if self.can_eaten_play(state, dice2):
                        half1 = (25, dice2 - 1)
                        updated_board = board.copy()
                        updated_board[dice2 - 1] += 2
                        indices1 = self.get_indices(updated_board, dice1, player)
                        if indices1.size > 0:
                            actions.extend([(half1, (a, a + dice1)) for a in indices1])
                        else:
                            actions.append((half1, (-1, -1)))
                    actions = list(set(actions))
                    return actions

    def last_checker_index(self, board, player):   # returns last checker index if all checkers in home
        if player == -1:
            indices = np.where(board < 0)[0]
            return indices[-1] if indices.size > 0 else None
        else:
            indices = np.where(board > 0)[0]
            return indices[0] if indices.size > 0 else None
    
    def get_checkers_out_move(self, board, dice, player):  # returns the valid checker out move for the dice if there is, assuming no checkers eaten
        player = player
        board : np.ndarray = board

        if player == -1:
            if self.all_checkers_in_home(board, player) == False: return None
            last_checker_index = self.last_checker_index(board, player)
            if last_checker_index is None: return None
            if dice - 1 > last_checker_index: dice = last_checker_index + 1
            index = dice - 1 if board[dice - 1] < 0 else None               # valid index to play checker out
            move = np.array([index, 26]) if index is not None else None
        else:
            if self.all_checkers_in_home(board, player) == False: return None
            last_checker_index = self.last_checker_index(board, player)
            if last_checker_index is None: return None
            if 24 - last_checker_index < dice: dice = 24 - last_checker_index
            index = 24 - dice if board[24 - dice] > 0 else None             # valid index to play checker out
            move = np.array([index, 27]) if index is not None else None
        return move

    def sum_checkers_on_board(self, board, player):
        return np.sum(np.abs(board[board * player > 0]))

    def get_regular_board_actions(self, state : State):
        player = state.player
        dice1, dice2 = state.dice
        board : np.ndarray = state.board

        indices1 = self.get_indices(board, dice1, player)
        indices2 = self.get_indices(board, dice2, player)
        indices_1_2 = self.get_indices(board, dice1 + dice2, player)

        # get same checker actions
        play1_2 = np.intersect1d(indices1, indices_1_2)
        play2_2 = np.intersect1d(indices2, indices_1_2)

        if player == -1:
            actions1_2 = [((a, a - dice1), (a - dice1, a - dice1 - dice2)) for a in play1_2]
            actions2_2 = [((a, a - dice2), (a - dice2, a - dice2 - dice1)) for a in play2_2]
        else:
            actions1_2 = [((a, a + dice1), (a + dice1, a + dice1 + dice2)) for a in play1_2]
            actions2_2 = [((a, a + dice2), (a + dice2, a + dice2 + dice1)) for a in play2_2]
        
        # get different checkers actions
        dice1_index, dice2_index = np.meshgrid(indices1, indices2)
        from_index_pairs = np.vstack([dice1_index.ravel(), dice2_index.ravel()]).T

        # if a pair is the same index and has less than 2 checkers it's invalid
        same_value_mask = from_index_pairs[:, 0] == from_index_pairs[:, 1]
        if player == -1:
            invalid_pairs_mask = same_value_mask & (board[from_index_pairs[:, 0]] > -2)
        else:
            invalid_pairs_mask = same_value_mask & (board[from_index_pairs[:, 0]] < 2)

        # all legal indecies pairs from where you can play the dice: dice1 on pair element[0], dice2 on pair element[1]
        valid_from_index_pairs = from_index_pairs[~invalid_pairs_mask]

        calc_end_index_arr = np.array([[dice1, dice2]])

        # end indecies according to start indeices if you play dice1 pair element[0], dice2 pair element[1]
        if player == -1:
            result_valid_pairs = valid_from_index_pairs - calc_end_index_arr
        else:
            result_valid_pairs = valid_from_index_pairs + calc_end_index_arr
        
        arr = np.concatenate((result_valid_pairs, valid_from_index_pairs), axis = 1)
        arr[:, [0,1,2,3]] = arr[:, [2,0,3,1]]
        actions = [((a,b),(c,d)) for (a,b,c,d) in arr]

        # -----------------------
        # get actions with checkers out moves
        move1_out = self.get_checkers_out_move(board, dice1, player)
        move2_out = self.get_checkers_out_move(board, dice2, player)

        if player == -1:
            moves_dice1 = np.column_stack((indices1, indices1 - dice1))
            moves_dice2 = np.column_stack((indices2, indices2 - dice2))
        else:
            moves_dice1 = np.column_stack((indices1, indices1 + dice1))
            moves_dice2 = np.column_stack((indices2, indices2 + dice2))

        # get action where both moves are out moves if possible
        if move1_out is not None and move2_out is not None:
            if move1_out[0] == move2_out[0]:
                if abs(board[move1_out[0]]) > 1:
                    both_out_action = np.hstack((move1_out, move2_out))
                elif self.sum_checkers_on_board(board, player) == 1:
                    both_out_action = np.hstack((move1_out, [-1, -1]))
                else: both_out_action = np.empty((0, 4), dtype = np.int64)
            else:
                both_out_action = np.hstack((move1_out, move2_out))
        else: both_out_action = np.empty((0, 4), dtype = np.int64)

        # check for actions where both moves are out moves but second out move unlocked after first one played
        if (move1_out is not None and move2_out is None) or (move1_out is not None and move2_out is not None and both_out_action.size == 0):
            board_new = board.copy()
            if player == -1:
                board_new[move1_out[0]] += 1
            else:
                board_new[move1_out[0]] -= 1
            out_move = self.get_checkers_out_move(board_new, dice2, player)
            if out_move is not None:
                action_out1 = np.concatenate([move1_out, out_move])
            else: action_out1 = np.empty((0, 4), dtype = np.int64)
        else: action_out1 = np.empty((0, 4), dtype = np.int64)
        if (move1_out is None and move2_out is not None) or (move1_out is not None and move2_out is not None and both_out_action.size == 0):
            board_new = board.copy()
            if player == -1:
                board_new[move2_out[0]] += 1
            else:
                board_new[move2_out[0]] -= 1
            out_move = self.get_checkers_out_move(board_new, dice1, player)
            if out_move is not None:
                action_out2 = np.concatenate([move2_out, out_move])
            else: action_out2 = np.empty((0, 4), dtype = np.int64)
        else: action_out2 = np.empty((0, 4), dtype = np.int64)
        
        both_out_actions = np.vstack((both_out_action, action_out1, action_out2))
        
        # get same checker actions where second move is out move, and
        # actions where one move is regular move and the other is out move (not necessarily same checker)
        
        # if move1_out is not None:
        if moves_dice2.shape[0] > 0:      # first dice2 move then move with dice1
            boards = np.tile(board, (moves_dice2.shape[0], 1))
            rows = np.arange(moves_dice2.shape[0])
            cols_from = moves_dice2[:, 0]
            cols_to = moves_dice2[:, 1]
            if player == -1:
                boards[rows, cols_from] += 1
                boards[rows, cols_to] -= 1
            else:
                boards[rows, cols_from] -= 1
                boards[rows, cols_to] += 1
            continuation_out_moves1 = [self.get_checkers_out_move(row, dice1, player) for row in boards]
            results = np.empty((len(continuation_out_moves1), 1), dtype=object)
            results[:, 0] = continuation_out_moves1
            filtered_results = np.array([[np.array([None, None]) if row[0] is None else row[0]] for row in results], dtype=object)
            if filtered_results.size > 0:
                filtered_results = np.vstack(filtered_results)
            else: filtered_results = np.empty((moves_dice2.shape[0], 2))
            continuation_out_actions1 = np.hstack((moves_dice2, filtered_results))
        else: continuation_out_actions1 = np.empty((0, 4))
        # else: continuation_out_actions1 = np.empty((0, 4))
        
        # if move2_out is not None:
        if moves_dice1.shape[0] > 0:      # first dice1 move then move with dice2
            boards = np.tile(board, (moves_dice1.shape[0], 1))
            rows = np.arange(moves_dice1.shape[0])
            cols_from = moves_dice1[:, 0]
            cols_to = moves_dice1[:, 1]
            if player == -1:
                boards[rows, cols_from] += 1
                boards[rows, cols_to] -= 1
            else:
                boards[rows, cols_from] -= 1
                boards[rows, cols_to] += 1
            continuation_out_moves2 = [self.get_checkers_out_move(row, dice2, player) for row in boards]
            results = np.empty((len(continuation_out_moves2), 1), dtype=object)
            results[:, 0] = continuation_out_moves2
            filtered_results = np.array([[np.array([None, None]) if row[0] is None else row[0]] for row in results], dtype=object)
            if filtered_results.size > 0:
                filtered_results = np.vstack(filtered_results)
            else: filtered_results = np.empty((moves_dice1.shape[0], 2))
            continuation_out_actions2 = np.hstack((moves_dice1, filtered_results))
        else: continuation_out_actions2 = np.empty((0, 4))
        # else: continuation_out_actions2 = np.empty((0, 4))

        continuation_out_actions = np.vstack((continuation_out_actions1, continuation_out_actions2))
        # remove actions that did not have out moves after first move
        not_none_mask = continuation_out_actions[:, 2] != None
        continuation_out_actions = continuation_out_actions[not_none_mask]

        moves_out_actions = np.vstack((both_out_actions, continuation_out_actions)).astype(np.int64)

        keys, inverse, counts = np.unique(moves_out_actions[:, :2], axis = 0, return_inverse = True, return_counts = True)
        keep_mask = ~((moves_out_actions[:, 2:] == -1).all(axis = -1) & (counts[inverse] > 1))
        moves_out_actions = moves_out_actions[keep_mask]

        moves_out_actions = np.unique(moves_out_actions, axis = 0)
        
        # get actions where first move is out move and there is not second move (out_moves)
        if move1_out is not None and moves_dice2.shape[0] == 0 and both_out_action.size == 0:
            half_out_action1 = np.concatenate((move1_out, [-1, -1]))
        else: half_out_action1 = np.empty((0, 4), dtype = np.int64)
        if move2_out is not None and moves_dice1.shape[0] == 0 and both_out_actions.size == 0:
            half_out_action2 = np.concatenate((move2_out, [-1, -1]))
        else: half_out_action2 = np.empty((0, 4), dtype = np.int64)

        first_moves = {tuple(action[:2]) for action in moves_out_actions}  # if there is not other action with this first move then add
        if half_out_action1.size > 0:
            if tuple(half_out_action1[:2]) not in first_moves: moves_out_actions = np.vstack((moves_out_actions, half_out_action1))
        if half_out_action2.size > 0:
            if tuple(half_out_action2[:2]) not in first_moves: moves_out_actions = np.vstack((moves_out_actions, half_out_action2))
        
        checkers_out_actions = [((a, b), (c, d)) for (a,b,c,d) in moves_out_actions]
        # ------------------

        # get one move actions
        if player == -1:
            if indices1.size > 0 and indices2.size == 0:
                one_move_actions = [((a, a - dice1), (-1, -1)) for a in indices1]
            elif indices2.size > 0 and indices1.size == 0:
                one_move_actions = [((a, a - dice2), (-1, -1)) for a in indices2]
            else: one_move_actions = []
        else:
            if indices1.size > 0 and indices2.size == 0:
                one_move_actions = [((a, a + dice1), (-1, -1)) for a in indices1]
            elif indices2.size > 0 and indices1.size == 0:
                one_move_actions = [((a, a + dice2), (-1, -1)) for a in indices2]
            else: one_move_actions = []

        final_actions = actions if actions else []
        if actions1_2: final_actions.extend(actions1_2)
        if actions2_2: final_actions.extend(actions2_2)
        if checkers_out_actions: final_actions.extend(checkers_out_actions)

        # remove ((a,b),(-1,-1)) actions if there is a continuation to the move
        filtered_final_actions = [
        action for action in final_actions 
        if action[1] != (-1, -1) or not any(other[0] == action[0] for other in final_actions if other is not action)
        ]

        # adding one move actions only if move does not have any continuation
        existing_first_moves = {action[0] for action in filtered_final_actions}
        filtered_final_actions.extend(action for action in one_move_actions if action[0] not in existing_first_moves)
        
        if not filtered_final_actions: filtered_final_actions = [((-1, -1), (-1, -1))]   # if no legal actions

        return filtered_final_actions


'''
win +10, lose -10
ate +1 each, eaten -1 each
checkers out +1 each, enemy checkers out - 1 each
checkers entered end zone +0.5*num, enemy checkers entered end zone -0.5*num
'''
