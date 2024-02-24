document.addEventListener("DOMContentLoaded", function () {
  const board = document.getElementById("board");
  const winnerDisplay = document.getElementById("winner");
  const playerScoreDisplay = document.getElementById("playerScore");
  const aiScoreDisplay = document.getElementById("aiScore");
  const resetAllButton = document.getElementById("resetAllButton");
  const resetBoardButton = document.getElementById("resetBoardButton");

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

  function handleCellClick(event) {
    const cell = event.target;
    const row = cell.getAttribute("data-row");
    const col = cell.getAttribute("data-col");

    // Send the clicked cell information to the backend
    fetch(`/move?row=${row}&col=${col}`)
      .then((response) => response.json())
      .then((data) => {
        updateBoard(data.board);
        if (data.winner_message) {
          displayWinnerMessage(data.winner_message);
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

  function displayWinnerMessage(message) {
    board.style.pointerEvents = "none"; //If a player wins he cannot click on the board unless next round or reset
    winnerDisplay.textContent = message;
    resetBoardButton.style.display = "inline"; //Displaying the button while getting winner message
  }

  function updateScores(playerScore, aiScore) {
    playerScoreDisplay.textContent = `Player Score: ${playerScore}`;
    aiScoreDisplay.textContent = `AI Score: ${aiScore}`;
  }

  function resetBoard() {
    // Call /reset when the reset button is clicked to initialize the board
    fetch("/reset_board")
      .then((response) => response.json())
      .then((data) => {
        updateBoard(data.board);
        winnerDisplay.textContent = ""; // Clear the winner display
        resetBoardButton.style.display = "none"; // Hiding the next round button while resetting board
        board.style.pointerEvents = "auto"; //After resetting the board if the board was nonclickable, it becomes clickable
        updateScores(data.player_score, data.ai_score);
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
        board.style.pointerEvents = "auto"; //After resetting the board if the board was nonclickable, it becomes clickable
        updateScores(data.player_score, data.ai_score);
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

  // Attach a click event listener to the reset buttons
  resetAllButton.addEventListener("click", resetAll);
  resetBoardButton.addEventListener("click", resetBoard);
});
