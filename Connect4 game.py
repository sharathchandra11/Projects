 #1. Setting Up the Game Environment
class ConnectFour(QWidget):
    def _init_(self):
        super()._init_()
        self.ai_depth = 16  # Depth of the minimax algorithm
        self.initUI()

    def initUI(self):
        # PyQT initialization
        self.setWindowTitle('Connect Four')
        self.setGeometry(100, 100, 500, 500)
        self.setupButtons()
        self.setupLabel()
        self.setupBoard()

    def setupButtons(self):
        # Initialize buttons for game modes and exit
        self.start_button = QPushButton('Start', self)
        self.start_button.clicked.connect(self.start_game)
        self.player_vs_player_button = QPushButton('Player vs Player', self)
        self.player_vs_player_button.clicked.connect(self.player_vs_player)
        self.player_vs_ai_button = QPushButton('Player vs AI', self)
        self.player_vs_ai_button.clicked.connect(self.player_vs_ai)
        self.exit_button = QPushButton('Exit', self)
        self.exit_button.clicked.connect(self.close)

    def setupLabel(self):
        # Label to display game status
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        font = QFont("Arial", 14, QFont.Bold)
        self.label.setFont(font)

    def setupBoard(self):
        # Grid layout for game board
        vbox = QVBoxLayout()
        vbox.addWidget(self.start_button)
        vbox.addWidget(self.player_vs_player_button)
        vbox.addWidget(self.player_vs_ai_button)
        vbox.addWidget(self.exit_button)
        vbox.addWidget(self.label)
        self.grid_layout = QGridLayout()
        vbox.addLayout(self.grid_layout)
        self.setLayout(vbox)

#2. Defining the Grid
    def draw_board(self):
        # Create game board
        self.columns = 7
        self.rows = 6
        self.board = [[' ' for _ in range(self.columns)] for _ in range(self.rows)]
        for i in reversed(range(self.grid_layout.count())):
            self.grid_layout.itemAt(i).widget().setParent(None)
        self.buttons = []
        for i in range(self.rows):
            row_buttons = []
            for j in range(self.columns):
                btn = QPushButton()
                row_buttons.append(btn)
                btn.clicked.connect(lambda _, col=j, row=i: self.place_piece(col))
                self.grid_layout.addWidget(btn, i, j)
                btn.setFixedSize(60, 60)  # Adjust button size
            self.buttons.append(row_buttons)

 #3. Drawing the Grid
    def update_board_ui(self):
        for i in range(self.rows):
            for j in range(self.columns):
                if self.board[i][j] == 'X':
                    self.buttons[i][j].setStyleSheet("background-color: red; border-radius: 50%;")
                elif self.board[i][j] == 'O':
                    self.buttons[i][j].setStyleSheet("background-color: yellow; border-radius: 50%;")

 #4. Handling User Input
    def place_piece(self, col):
        if self.mode == "PvP":
            self.player_vs_player_move(col)
        elif self.mode == "PvAI":
            self.player_vs_ai_move(col)

 #5. Game Logic
    def player_vs_player_move(self, col):
        for row in reversed(range(self.rows)):
            if self.board[row][col] == ' ':
                self.board[row][col] = 'X' if self.label.text() == "Player 1's turn" else 'O'
                self.update_board_ui()
                if self.check_winner(row, col):
                    self.label.setText("Player 1 wins!" if self.label.text() == "Player 1's turn" else "Player 2 wins!")
                    self.disable_buttons()
                else:
                    self.label.setText("Player 2's turn" if self.label.text() == "Player 1's turn" else "Player 1's turn")
                return
        self.label.setText("Column is full!")

 #6. AI Logic
    def player_vs_ai_move(self, col):
        for row in reversed(range(self.rows)):
            if self.board[row][col] == ' ':
                self.board[row][col] = 'X'
                self.update_board_ui()
                if self.check_winner(row, col):
                    self.label.setText("Player wins!")
                    self.disable_buttons()
                    return
                self.label.setText("AI's turn")
                self.ai_move()
                return
        self.label.setText("Column is full!")

 #7. Game Over Handling
    def ai_move(self):
        if self.label.text().startswith("Player wins!") or self.label.text().startswith("AI wins!"):
            return
        col = self.get_best_move()
        for row in reversed(range(self.rows)):
            if self.board[row][col] == ' ':
                self.board[row][col] = 'O'
                self.update_board_ui()
                if self.check_winner(row, col):
                    self.label.setText("AI wins!")
                    self.disable_buttons()
                    return
                self.label.setText("Player's turn")
                return

 #8. Rendering
    def disable_buttons(self):
        for row in self.buttons:
            for button in row:
                button.setEnabled(False)

#9. Optimization and Refinement
if _name_ == '_main_':
    app = QApplication(sys.argv)
    window = ConnectFour()
    sys.exit(app.exec_())
