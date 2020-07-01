import numpy as np
from src.games.Connect4 import Connect4 as Game
from src.ui.pygame_ui import PygameUI
from src.heuristics.Network import Network


def play_games(GameClass, network1, network2, count=1000):
    net1_wins, net2_wins, draws = 0, 0, 0
    for i in range(count):
        position = GameClass.STARTING_STATE
        net1_evals = []
        net2_evals = []
        while not GameClass.is_over(position):
            position = network1.choose_move(position)
            net1_evals.append(network1.evaluation(position))
            if Game.is_over(position):
                break

            position = network2.choose_move(position)
            net2_evals.append(network2.evaluation(position))

        result = Game.get_winner(position)
        net1_rms = np.mean((np.array(net1_evals) - result) ** 2) ** 0.5
        net2_rms = np.mean((np.array(net2_evals) - result) ** 2) ** 0.5
        print(f'Winner {i}: {result}, net 1 rms: {net1_rms}, net 2 rms: {net2_rms}')
        if result == 1:
            net1_wins += 1
        elif result == 0:
            draws += 1
        elif result == -1:
            net2_wins += 1
        else:
            raise Exception()
    print(f'Net 1 wins {net1_wins}, net 2 wins {net2_wins}, draws {draws}')


def play_game_with_ui(GameClass, pygame_ui, network1, network2):
    position = pygame_ui.get_position()
    board_states = [position]

    while not GameClass.is_over(position):
        position = network1.choose_move(position)
        board_states.append(position)
        if Game.is_over(position):
            break

        position = network2.choose_move(position)
        board_states.append(position)

    i = len(board_states) - 1
    while True:
        click = pygame_ui.click_left_or_right()
        if click is None:
            return
        if click:
            i = min(i + 1, len(board_states) - 1)
        else:
            i = max(i - 1, 0)

        position = board_states[i]
        pygame_ui.draw(position)


def main(GameClass):
    network1 = Network(Game, '../heuristics/models/policy1.h5', '../heuristics/models/evaluation1.h5')
    network2 = Network(Game, '../heuristics/models/policy0.h5', '../heuristics/models/evaluation0.h5')
    network1.initialize()
    network2.initialize()
    # play_games(Game, network1, network2)
    pygame_ui = PygameUI(GameClass)
    play_game_with_ui(GameClass, pygame_ui, network1, network2)


if __name__ == '__main__':
    main(Game)