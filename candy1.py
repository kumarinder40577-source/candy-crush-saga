import streamlit as st
import streamlit.components.v1 as components

# Set Streamlit page config
st.set_page_config(page_title="Candy Crush Saga", layout="centered")

st.title("🍭 Candy Crush Python")
st.write("Click two adjacent candies to swap them!")

# The Game Logic (HTML/JavaScript)
html_code = """
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
                    ctx.roundRect(x + 5, y + 5, TILE_SIZE - 10, TILE_SIZE - 10, 10);
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
            if (matches.length
