import random
import numpy as np
from game_mod import GameState


# Define state representation
def get_state(game_state):
    # Create an 8x8 array to represent the board
    state = np.zeros((8, 8), dtype=np.int8)

    # Populate the array with the piece positions
    for row in range(8):
        for col in range(8):
            piece = game_state.get_piece(row, col)
            if piece is not None:
                # Use integer values to represent the pieces
                if piece.color == 'white':
                    if piece.type == 'king':
                        state[row, col] = 1
                    elif piece.type == 'queen':
                        state[row, col] = 2
                    elif piece.type == 'rook':
                        state[row, col] = 3
                    elif piece.type == 'bishop':
                        state[row, col] = 4
                    elif piece.type == 'knight':
                        state[row, col] = 5
                    elif piece.type == 'pawn':
                        state[row, col] = 6
                elif piece.color == 'black':
                    if piece.type == 'king':
                        state[row, col] = -1
                    elif piece.type == 'queen':
                        state[row, col] = -2
                    elif piece.type == 'rook':
                        state[row, col] = -3
                    elif piece.type == 'bishop':
                        state[row, col] = -4
                    elif piece.type == 'knight':
                        state[row, col] = -5
                    elif piece.type == 'pawn':
                        state[row, col] = -6

    return state.flatten()


# Initialize Q-table
q_table = {}


# Define action selection policy
def epsilon_greedy(q_table, state, epsilon, game_state):
    if random.uniform(0, 1) < epsilon:
        # Select a random move
        return random.choice(game_state.get_legal_moves())
    else:
        # Select the move with the highest Q-value
        q_values = [q_table.get((state, move), 0) for move in game_state.get_legal_moves()]
        max_q = max(q_values)
        if q_values.count(max_q) > 1:
            # Multiple moves have the same max Q-value, choose one at random
            best_moves = [i for i in range(len(game_state.get_legal_moves())) if q_values[i] == max_q]
            return game_state.get_legal_moves()[random.choice(best_moves)]
        else:
            return game_state.get_legal_moves()[q_values.index(max_q)]


# Define Q-learning algorithm
def q_learning(game_state, q_table, num_episodes, gamma, alpha, epsilon):
    for i in range(num_episodes):
        # Reset the game state
        game_state = GameState()
        state = get_state(game_state)
        done = False
        
        while not done:
            # Select an action
            action = epsilon_greedy(q_table, state, epsilon, game_state)

            # Make the move and observe the reward and next state
            game_state.make_move(action)
            next_state = get_state(game_state)
            reward = game_state.get_reward()

            # Update the Q-value for the (state, action) pair
            old_q = q_table.get((state, action), 0)
            next_max_q = max([q_table.get((next_state, move), 0) for move in game_state.get_legal_moves()])
            new_q = (1 - alpha) * old_q + alpha * (reward + gamma * next_max_q)
            q_table[(state, action)] = new_q

            # Update the state and check if the game is over
            state = next_state
            done = game_state.is_game_over()
