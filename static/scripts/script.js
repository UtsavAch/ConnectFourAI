document.addEventListener("DOMContentLoaded", function () {
  //IMPORTANT ELEMENTS
  const main = document.getElementById("main");
  const board = document.getElementById("board");
  const winnerDisplay = document.getElementById("winner");
  const playerScoreDisplay = document.getElementById("playerScore");
  const aiScoreDisplay = document.getElementById("aiScore");
  const matchTitle = document.getElementById("matchTitle");

  // BUTTONS
  const startGameButton = document.getElementById("startGameButton");
  const resetAllButton = document.getElementById("resetAllButton");
  const resetBoardButton = document.getElementById("resetBoardButton");
  const playAgainButton = document.getElementById("playAgainButton");

  //OPTION BUTTONS
  const matchOptions = document.getElementById("matchOptions");
  const playerVsAStar = document.getElementById("playerVsAStar");
  const playerVsMinimax = document.getElementById("playerVsMinimax");
  const playerVsMcts = document.getElementById("playerVsMcts");
  const playerVsPlayer = document.getElementById("playerVsPlayer");
  const aStarVsMcts = document.getElementById("aStarVsMcts");
  const mctsVsMinimax = document.getElementById("mctsVsMinimax");

  // Initialize the board
  function initializeBoard() {
    for (let i = 0; i < 6; i++) {
      const row = board.insertRow();
      for (let j = 0; j < 7; j++) {
        const cell = row.insertCell();
        cell.setAttribute("data-row", i);
        cell.setAttribute("data-col", j);
        cell.addEventListener("click", handleCellClick);
      }
    }
  }

  // Add event handlers to all the cells
  function addEventListenerToCells() {
    const cells = document.querySelectorAll("td"); // Get all the cells
    cells.forEach((cell) => {
      cell.addEventListener("click", handleCellClick);
    });
  }

  function getTopmostCellContent(column) {
    // Get the topmost cell in the specified column
    const topmostCell = document.querySelector(
      `[data-col="${column}"][data-row="0"]`
    );
    // Return the content of the topmost cell
    return topmostCell ? topmostCell.textContent : null;
  }

  //When player clicks the column/cell
  function handleCellClick(event) {
    const cell = event.target;
    const row = cell.getAttribute("data-row");
    const col = cell.getAttribute("data-col");

    // Check if the topmost cell in the column is already filled
    if (
      getTopmostCellContent(col) === "O" ||
      getTopmostCellContent(col) === "X"
    ) {
      // Make all the cells of the column non-clickable
      for (let i = 0; i < 6; i++) {
        const currentCell = document.querySelector(
          `[data-row="${i}"][data-col="${col}"]`
        );
        if (currentCell) {
          currentCell.removeEventListener("click", handleCellClick);
        }
      }
      return;
    }

    // Send the clicked cell information to the backend
    fetch(`/move?row=${row}&col=${col}`)
      .then((response) => response.json())
      .then((data) => {
        updateBoard(data.board);
        if (data.winner_message) {
          displayWinnerMessage(
            data.winner_message,
            data.player_score,
            data.ai_score
          );
        }
        updateScores(data.player_score, data.ai_score);
      });
  }

  function updateBoard(data) {
    const cells = board.getElementsByTagName("td");

    if (data && data.length) {
      for (let cell of cells) {
        const row = cell.getAttribute("data-row");
        const col = cell.getAttribute("data-col");

        if (data[row] && typeof data[row][col] !== "undefined") {
          cell.textContent = data[row][col];
        }
      }
    }
  }

  function displayWinnerMessage(message, playerScore, aiScore) {
    board.style.pointerEvents = "none"; //If a player wins he cannot click on the board unless next round or play again
    if (playerScore == 3 || aiScore == 3) {
      winnerDisplay.textContent = message;
      resetBoardButton.style.display = "none";
      playAgainButton.style.display = "inline";
    } else {
      winnerDisplay.textContent = message;
      resetBoardButton.style.display = "inline"; //Displaying the "Reset board" button while getting winner message
    }
  }

  function updateScores(playerScore, aiScore) {
    playerScoreDisplay.textContent = `Player Score: ${playerScore}`;
    aiScoreDisplay.textContent = `AI Score: ${aiScore}`;
  }

  function resetBoard() {
    // Call /reset when the "Next round/Play again" buttons is clicked to initialize the board
    fetch("/reset_board")
      .then((response) => response.json())
      .then((data) => {
        updateBoard(data.board);
        winnerDisplay.textContent = ""; // Clear the winner display
        resetBoardButton.style.display = "none"; // Hiding the next round button while resetting board
        board.style.pointerEvents = "auto"; //After resetting the board if the board was nonclickable, it becomes clickable
        updateScores(data.player_score, data.ai_score);
        addEventListenerToCells();
      });
  }

  function resetAll() {
    // Call /reset when the reset button is clicked to initialize the board
    fetch("/reset_all")
      .then((response) => response.json())
      .then((data) => {
        updateBoard(data.board);
        winnerDisplay.textContent = ""; // Clear the winner display
        resetBoardButton.style.display = "none"; // Hiding the next round button while resetting all
        main.style.display = "none"; //Hiding all the contents from main
        resetAllButton.style.display = "none";
        startGameButton.style.display = "inline";
        board.style.pointerEvents = "auto"; //After resetting the board if the board was nonclickable, it becomes clickable
        updateScores(data.player_score, data.ai_score);
        addEventListenerToCells();
      });
  }

  function playAgain() {
    // Call /reset when the "Play again" button is clicked
    fetch("/reset_all")
      .then((response) => response.json())
      .then((data) => {
        updateBoard(data.board);
        winnerDisplay.textContent = ""; // Clear the winner display
        resetBoardButton.style.display = "none"; // Hiding the next round button while resetting all
        board.style.pointerEvents = "auto"; //After resetting the board if the board was nonclickable, it becomes clickable
        playAgainButton.style.display = "none";
        updateScores(data.player_score, data.ai_score);
        addEventListenerToCells();
      });
  }

  // Call /reset when the page is loaded to initialize the board
  fetch("/reset_all")
    .then((response) => response.json())
    .then((data) => {
      updateBoard(data);
      updateScores(data.player_score, data.ai_score);
    });

  initializeBoard();

  function startGame() {
    matchOptions.style.display = "flex";
    startGameButton.style.display = "none";
    playAgainButton.style.display = "none";
  }

  /////////////////////////////////////
  function optionButtonChangeDisplay() {
    main.style.display = "block"; //Showing all the contents from main
    matchOptions.style.display = "none"; //Hide all the option buttons
    resetAllButton.style.display = "inline"; //Show the reset button (exit button)
  }

  /////////////////////////////////////
  function playerVsAStarFn() {
    optionButtonChangeDisplay();
    matchTitle.textContent = "Player vs A*";
  }

  function playerVsMinimaxFn() {
    optionButtonChangeDisplay();
    matchTitle.textContent = "Player vs Minimax";
  }

  function playerVsMctsFn() {
    optionButtonChangeDisplay();
    matchTitle.textContent = "Player vs MCTS";
  }

  function playerVsPlayerFn() {
    optionButtonChangeDisplay();
    matchTitle.textContent = "Player1 vs Player2";
  }

  function aStarVsMctsFn() {
    optionButtonChangeDisplay();
    matchTitle.textContent = "A* vs MCTS";
  }

  function mctsVsMinimaxFn() {
    optionButtonChangeDisplay();
    matchTitle.textContent = "MCTS vs Minimax";
  }
  /////////////////////////////////////

  // Attach a click event listener to the reset buttons
  resetAllButton.addEventListener("click", resetAll);
  resetBoardButton.addEventListener("click", resetBoard);
  startGameButton.addEventListener("click", startGame);
  playAgainButton.addEventListener("click", playAgain);

  // Attach a click event listener to the game option buttons
  playerVsAStar.addEventListener("click", playerVsAStarFn);
  playerVsMinimax.addEventListener("click", playerVsMinimaxFn);
  playerVsMcts.addEventListener("click", playerVsMctsFn);
  playerVsPlayer.addEventListener("click", playerVsPlayerFn);
  aStarVsMcts.addEventListener("click", aStarVsMctsFn);
  mctsVsMinimax.addEventListener("click", mctsVsMinimaxFn);
});
