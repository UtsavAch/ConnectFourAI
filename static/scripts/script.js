document.addEventListener("DOMContentLoaded", function () {
  //IMPORTANT ELEMENTS
  const main = document.getElementById("main");
  const board = document.getElementById("board");
  const winnerDisplay = document.getElementById("winner");
  const playerOneScoreDisplay = document.getElementById("playerOneScore");
  const playerTwoScoreDisplay = document.getElementById("playerTwoScore");
  const matchTitle = document.getElementById("matchTitle");
  const playerOneName = document.getElementById("playerOneName");
  const playerTwoName = document.getElementById("playerTwoName");
  const noteMcts = document.getElementById("noteMcts");

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
  const minimaxVsAStar = document.getElementById("minimaxVsAStar");
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
            data.player_one_score,
            data.player_two_score
          );
        }
        updateScores(data.player_one_score, data.player_two_score);
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

  function displayWinnerMessage(message, playerOneScore, playerTwoScore) {
    board.style.pointerEvents = "none"; //If a player wins he cannot click on the board unless next round or play again
    if (playerOneScore == 3 || playerTwoScore == 3) {
      winnerDisplay.textContent = message;
      resetBoardButton.style.display = "none";
      playAgainButton.style.display = "inline";
    } else {
      winnerDisplay.textContent = message;
      resetBoardButton.style.display = "inline"; //Displaying the "Reset board" button while getting winner message
    }
  }

  function updateScores(playerOneScore, playerTwoScore) {
    playerOneScoreDisplay.textContent = `${playerOneScore}`;
    playerTwoScoreDisplay.textContent = `${playerTwoScore}`;
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
        updateScores(data.player_one_score, data.player_two_score);
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
        noteMcts.style.display = "none";
        board.style.pointerEvents = "auto"; //After resetting the board if the board was nonclickable, it becomes clickable
        updateScores(data.player_one_score, data.player_two_score);
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
        updateScores(data.player_one_score, data.player_two_score);
        addEventListenerToCells();
      });
  }

  // Call /reset when the page is loaded to initialize the board
  fetch("/reset_all")
    .then((response) => response.json())
    .then((data) => {
      updateBoard(data);
      updateScores(data.player_one_score, data.player_two_score);
    });

  initializeBoard();

  function startGame() {
    matchOptions.style.display = "flex";
    startGameButton.style.display = "none";
    playAgainButton.style.display = "none";
  }

  /////////////////////////////////////
  //OPTION BUTTONS
  /////////////////////////////////////
  function optionButtonChangeDisplay(playerOne, playerTwo) {
    main.style.display = "block"; //Showing all the contents from main
    matchOptions.style.display = "none"; //Hide all the option buttons
    resetAllButton.style.display = "inline"; //Show the reset button (exit button)
    matchTitle.textContent = playerOne + " vs " + playerTwo;
    playerOneName.textContent = playerOne + ": ";
    playerTwoName.textContent = playerTwo + ": ";
  }

  function sendButtonClickToBackend(buttonName) {
    // Send the clicked button information to the backend
    fetch("/button_clicked", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ buttonName: buttonName }),
    }).then((response) => response.json());
  }

  /////////////////////////////////////
  function playerVsAStarFn() {
    sendButtonClickToBackend("player_vs_astar");
    optionButtonChangeDisplay("Player", "A*");
  }

  function playerVsMinimaxFn() {
    sendButtonClickToBackend("player_vs_minimax");
    optionButtonChangeDisplay("Player", "Minimax");
  }

  function playerVsMctsFn() {
    sendButtonClickToBackend("player_vs_mcts");
    optionButtonChangeDisplay("Player", "MCTS");
    noteMcts.style.display = "block";
  }

  function minimaxVsAStarFn() {
    sendButtonClickToBackend("minimax_vs_astar");
    optionButtonChangeDisplay("Minimax", "A*");
  }

  function aStarVsMctsFn() {
    sendButtonClickToBackend("astar_vs_mcts");
    optionButtonChangeDisplay("A*", "MCTS");
    noteMcts.style.display = "block";
  }

  function mctsVsMinimaxFn() {
    sendButtonClickToBackend("mcts_vs_minimax");
    optionButtonChangeDisplay("MCTS", "Minimax");
    noteMcts.style.display = "block";
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
  minimaxVsAStar.addEventListener("click", minimaxVsAStarFn);
  aStarVsMcts.addEventListener("click", aStarVsMctsFn);
  mctsVsMinimax.addEventListener("click", mctsVsMinimaxFn);
});
