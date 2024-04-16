from .models import PlayerMove

def check_winner(game):
    """
    if winner exists, return Player instance with symbol
    """

    # Fetch players based on their symbols
    o_player = game.player_set.filter(symbol='o').first()
    x_player = game.player_set.filter(symbol='x').first()

    print(o_player, x_player)

    # Get all moves for the particular game and sort them by id
    game_moves = PlayerMove.objects.filter(player__game=game).order_by('id')

    # Extract the symbols of the moves and create a list
    sorted_moves = [move.player.symbol if move else '' for move in game_moves]

    if len(sorted_moves) >= 5:  # Need at least 5 moves to have a potential winner
        winner = None

        # Define winning combinations
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Horizontal
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Vertical
            [0, 4, 8], [2, 4, 6]              # Diagonal
        ]

        # Check each winning combination
        for combination in winning_combinations:
            symbols = [sorted_moves[pos] for pos in combination if pos < len(sorted_moves)]
            if len(symbols) == 3 and all(symbols) and len(set(symbols)) == 1:
                if symbols[0] == 'x':
                    winner = x_player
                elif symbols[0] == 'o':
                    winner = o_player
                break  # If a winner is found, no need to check further

        return winner

    return None
