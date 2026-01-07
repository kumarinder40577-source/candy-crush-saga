import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Candy Crush Saga", layout="centered")

st.title("🍭 Candy Crush with Music")
st.write("Turn your volume up! A classical-style melody will play.")

html_code = r"""
<!DOCTYPE html>
<html>
<head>
    <style>
        canvas { border: 5px solid #444; border-radius: 10px; cursor: pointer; background-color: #333; }
        body { display: flex; flex-direction: column; align-items: center; background: transparent; color: white; font-family: sans-serif; }
        .stats { margin: 10px; font-size: 24px; font-weight: bold; color: #FFD700; }
        #musicBtn { margin-bottom: 10px; padding: 10px; cursor: pointer; border-radius: 5px; border: none; background: #FFD700; font-weight: bold; }
    </style>
</head>
<body>
    <button id="musicBtn">🎵 Start Music & Game</button>
    <div class="stats">Score: <span id="score">0</span></div>
    <canvas id="gameCanvas" width="400" height="400"></canvas>

    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        const scoreElement = document.getElementById('score');
        const musicBtn = document.getElementById('musicBtn');
        
        const GRID_SIZE = 8;
        const TILE_SIZE = 50;
        const COLORS = ['#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#FF00FF', '#00FFFF'];
        const ICONS = ['🍎', '🍏', '💎', '⭐', '🍭', '🍊'];
        
        let board = [];
        let score = 0;
        let selected = null;
        let audioStarted = false;

        // --- Classical Tune Logic ---
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        
        // C-Major Arpeggio for a "Classical" feel
        const melody = [261.63, 329.63, 392.00, 523.25, 392.00, 329.63]; 
        let noteIndex = 0;

        function playMelody() {
            if (!audioStarted) return;
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            
            osc.type = 'triangle'; // Softer, classical sound
            osc.frequency.setValueAtTime(melody[noteIndex], audioCtx.currentTime);
            
            gain.gain.setValueAtTime(0, audioCtx.currentTime);
            gain.gain.linearRampToValueAtTime(0.05, audioCtx.currentTime + 0.1);
            gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.5);
            
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            
            osc.start();
            osc.stop(audioCtx.currentTime + 0.5);
            
            noteIndex = (noteIndex + 1) % melody.length;
            setTimeout(playMelody, 500); // Speed of the tune
        }

        // --- Sound Effects ---
        const playEffect = (freq, type) => {
            if (!audioStarted) return;
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

        musicBtn.onclick = () => {
            if (!audioStarted) {
                audioCtx.resume();
                audioStarted = true;
                playMelody();
                musicBtn.innerText = "🔊 Music Playing";
            }
        };

        // --- Game Logic ---
        function initBoard() {
            for (let r = 0; r < GRID_SIZE; r++) {
                board[r] = [];
                for (let c = 0; c
