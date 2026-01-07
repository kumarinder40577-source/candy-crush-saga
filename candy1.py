import streamlit as st
import streamlit.components.v1 as components

# 1. Set Page Configuration
st.set_page_config(page_title="Candy Crush Saga", layout="centered")

st.title("🍭 Candy Crush Python")
st.write("Click two adjacent candies to swap them!")

# 2. The Game Logic (Cleaned HTML/JavaScript)
# Using a raw string (r""") to avoid escape character issues
html_code = r"""
<!DOCTYPE html>
<html>
<head>
    <style>
        canvas { border: 5px solid #444; border-radius: 10px; cursor: pointer; background-color: #333; }
        body { display: flex; flex-direction: column; align-items: center; background: transparent; color: white; font-family: sans-serif; }
        .stats { margin: 10px; font-size: 24px; font-weight: bold; color: #FFD700; }
    </style>
</head>
<body>
    <div class="stats">Score: <span id="score">0</span></div>
    <canvas id="gameCanvas" width="400" height="400"></canvas>

    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        const scoreElement = document.getElementById('score');
        
        const GRID_SIZE = 8;
        const TILE_SIZE = 50;
        const COLORS = ['#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#FF00FF', '#00FFFF'];
        const ICONS = ['🍎', '🍏', '💎', '⭐', '🍭', '🍊'];
        
        let board = [];
        let score = 0;
        let selected = null;

        const playSound = (freq, type) => {
            try {
                const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                const osc = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
                osc.type = type;
                osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
                gain.gain.setValueAtTime(0.1, audioCtx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.2);
                osc.connect(gain);
                gain.connect(audioCtx.destination);
                osc.start();
                osc.stop(audioCtx.currentTime + 0.2);
            } catch(e) { console.log("Audio not supported"); }
        };

        function initBoard() {
            for (let r = 0; r < GRID_SIZE; r++) {
                board[r] = [];
                for (let c = 0; c < GRID_SIZE; c++) {
                    board[r][c] = { color: Math.floor(Math.random() * COLORS.length) };
                }
            }
        }

        function drawBoard() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            for (let r = 0; r < GRID_SIZE; r++) {
                for (let c = 0; c < GRID_SIZE; c++) {
                    const candy = board[r][c];
                    const x = c * TILE_SIZE;
                    const y = r * TILE_SIZE;
                    
                    ctx.fillStyle = COLORS[candy.color];
                    ctx.beginPath();
                    if (ctx.roundRect) {
                        ctx.roundRect(x + 5, y + 5, TILE_SIZE - 10, TILE_SIZE - 10, 10);
                    } else {
                        ctx.rect(x + 5, y + 5, TILE_SIZE - 10, TILE_SIZE - 10);
                    }
                    ctx.fill();
                    
                    ctx.fillStyle = "white";
                    ctx.font = "24px Arial";
                    ctx.textAlign = "center";
                    ctx.fillText(ICONS[candy.color], x + TILE_SIZE/2, y + TILE_SIZE/2 + 8);

                    if (selected && selected.r === r && selected.c === c) {
                        ctx.strokeStyle = "white";
                        ctx.lineWidth = 3;
                        ctx.strokeRect(x+2, y+2, TILE_SIZE-4, TILE_SIZE-4);
                    }
                }
            }
        }

        function checkMatches() {
            let toMatch = [];
            for (let r = 0; r < GRID_SIZE; r++) {
                for (let c = 0; c < GRID_SIZE - 2; c++) {
                    if (board[r][c].color === board[r][c+1].color && board[r][c].color === board[r][c+2].color) {
                        toMatch.push({r, c}, {r, c:c+1}, {r, c:c+2});
                    }
                }
            }
            for (let r = 0; r < GRID_SIZE - 2; r++) {
                for (let c = 0; c < GRID_SIZE; c++) {
                    if (board[r][c].color === board[r+1][c].color && board[r][c].color === board[r+2][c].color) {
                        toMatch.push({r, c}, {r:r+1, c}, {r:r+2, c});
                    }
                }
            }
            return toMatch;
        }

        async function processMatches() {
            let matches = checkMatches();
            if (matches.length > 0) {
                playSound(440, 'sine');
                score += matches.length * 10;
                scoreElement.innerText = score;
                matches.forEach(m => board[m.r][m.c].color = -1);
                drawBoard();
                await new Promise(r => setTimeout(r, 200));
                
                for (let c = 0; c < GRID_SIZE; c++) {
                    let emptySpace = 0;
                    for (let r = GRID_SIZE - 1; r >= 0; r--) {
                        if (board[r][c].color === -1) {
                            emptySpace++;
                        } else if (emptySpace > 0) {
                            board[r + emptySpace][c].color = board[r][c].color;
                            board[r][c].color = -1;
                        }
                    }
                    for (let r = 0; r < emptySpace; r++) {
                        board[r][c].color = Math.floor(Math.random() * COLORS.length);
                    }
                }
                drawBoard();
                setTimeout(processMatches, 300);
            }
        }

        canvas.onclick = (e) => {
            const rect = canvas.getBoundingClientRect();
            const c = Math.floor((e.clientX - rect.left) / TILE_SIZE);
            const r = Math.floor((e.clientY - rect.top) / TILE_SIZE);

            if (!selected) {
                selected = {r, c};
                playSound(600, 'square');
            } else {
                const dist = Math.abs(r - selected.r) + Math.abs(c - selected.c);
                if (dist === 1) {
                    let temp = board[r][c].color;
                    board[r][c].color = board[selected.r][selected.c].color;
                    board[selected.r][selected.c].color = temp;
                    processMatches();
                }
                selected = null;
            }
            drawBoard();
        };

        initBoard();
        while(checkMatches().length > 0) { initBoard(); }
        drawBoard();
    </script>
</body>
</html>
"""

# 3. Render the game in Streamlit
components.html(html_code, height=550)
