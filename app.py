from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Board initialization
board = [""] * 9
current_player = "X"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/move", methods=["POST"])
def move():
    global board, current_player
    data = request.json
    pos = data["pos"]

    if board[pos] == "":
        board[pos] = current_player
        winner = check_winner()
        current_player = "O" if current_player == "X" else "X"
        return jsonify({"board": board, "winner": winner})
    return jsonify({"board": board, "winner": None})

@app.route("/reset", methods=["POST"])
def reset():
    global board, current_player
    board = [""] * 9
    current_player = "X"
    return jsonify({"board": board, "winner": None})

def check_winner():
    wins = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),   # rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),   # columns
        (0, 4, 8), (2, 4, 6)               # diagonals
    ]
    for a, b, c in wins:
        if board[a] != "" and board[a] == board[b] == board[c]:
            return board[a]
    if "" not in board:
        return "Draw"
    return None

