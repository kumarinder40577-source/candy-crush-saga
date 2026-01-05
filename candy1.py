import streamlit.components.v1 as components

# We define the HTML/JS as a string
crash_candy_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        #game-container {
            background: radial-gradient(circle, #6a11cb 0%, #2575fc 100%);
            min-height: 650px; display: flex; flex-direction: column; align-items: center; justify-content: center;
            font-family: 'Segoe UI', sans-serif; border-radius: 20px; position: relative;
        }
        .ui-panel {
            background: rgba(255, 255, 255, 0.2); backdrop-filter: blur(15px);
            border-radius: 25px; padding: 20px; margin-bottom: 20px;
            border: 2px solid rgba(255, 255, 255, 0.3); text-align: center; color: white;
        }
        .score-text { font-size: 32px; font-weight: 900; }
        .grid {
            width: 340px; height: 340px; display: grid; grid-template-columns: repeat(8, 1fr);
            background: rgba(0, 0, 0, 0.3); border: 8px solid rgba(255, 255, 255, 0.1);
            border-radius: 15px; padding: 10px; gap: 5px;
        }
        .grid div {
            width: 38px; height: 38px; display: flex; align-items: center; justify-content: center;
            font-size: 28px; cursor: pointer; user-select: none;
            transition: transform 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }
        @keyframes candy-crush {
            0% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.5); filter: brightness(2); }
            100% { transform: scale(0); opacity: 0; }
        }
        .crushing { animation: candy-crush 0.4s forwards; pointer-events: none; }
        .selected { transform: scale(1.3) !important; filter: drop-shadow(0 0 10px gold); z-index: 10; }
        .red::before { content: '🍬'; }
        .blue::before { content: '🍭'; }
        .green::before { content: '🍏'; }
        .yellow::before { content: '🍋'; }
        .purple::before { content: '🍇'; }
        .orange::before { content: '🍊'; }
        .blank { visibility: hidden; }
        .btn-reset {
            margin-top: 20px; background: #FFD700; border: none; padding: 12px 30px;
            font-weight: bold; border-radius: 50px; cursor: pointer;
        }
    </style>
</head>
<body>
    <div id="game-container">
        <div class="ui-panel">
            <div style="font-weight:bold;">CRASH COLAB</div>
            <div class="score-text">Score: <span id="score">0</span></div>
        </div>
        <div class="grid" id="grid"></div>
        <button class="btn-reset" onclick="resetGame()">NEW GAME</button>
    </div>

    <script>
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    function playCrunchSound() {
        if (audioCtx.state === 'suspended') audioCtx.resume();
        const bufferSize = audioCtx.sampleRate * 0.2;
        const buffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
        const data = buffer.getChannelData(0);
        for (let i = 0; i < bufferSize; i++) { data[i] = Math.random() * 2 - 1; }
        const noise = audioCtx.createBufferSource();
        noise.buffer = buffer;
        const filter = audioCtx.createBiquadFilter();
        filter.type = 'lowpass';
        filter.frequency.setValueAtTime(1000, audioCtx.currentTime);
        filter.frequency.exponentialRampToValueAtTime(100, audioCtx.currentTime + 0.1);
        const gain = audioCtx.createGain();
        gain.gain.setValueAtTime(0.3, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.15);
        noise.connect(filter); filter.connect(gain); gain.connect(audioCtx.destination);
        noise.start();
    }

    const grid = document.getElementById('grid');
    const scoreDisplay = document.getElementById('score');
    const width = 8;
    const candyTypes = ['red', 'blue', 'green', 'yellow', 'purple', 'orange'];
    let squares = [];
    let score = 0;
    let firstSelection = null;

    function createBoard() {
        grid.innerHTML = '';
        squares = [];
        for (let i = 0; i < width * width; i++) {
            const square = document.createElement('div');
            square.setAttribute('id', i);
            let randomType = candyTypes[Math.floor(Math.random() * candyTypes.length)];
            square.classList.add(randomType);
            square.addEventListener('click', handleClick);
            grid.appendChild(square);
            squares.push(square);
        }
    }

    function handleClick() {
        if (!firstSelection) {
            firstSelection = this;
            this.classList.add('selected');
        } else {
            const firstId = parseInt(firstSelection.id);
            const secondId = parseInt(this.id);
            const validMoves = [firstId - 1, firstId + 1, firstId - width, firstId + width];
            if (validMoves.includes(secondId)) {
                let firstClass = firstSelection.className.replace('selected', '').trim();
                let secondClass = this.className;
                firstSelection.className = secondClass;
                this.className = firstClass;
                setTimeout(() => {
                    if (!checkMatches()) {
                        this.className = firstClass;
                        firstSelection.className = secondClass;
                    }
                }, 250);
            }
            firstSelection.classList.remove('selected');
            firstSelection = null;
        }
    }

    function checkMatches() {
        let found = false;
        let matchSet = new Set();
        for (let i = 0; i < 64; i++) {
            if (i % 8 > 5) continue;
            let row = [i, i+1, i+2];
            let type = squares[i].className;
            if (type !== 'blank' && !squares[i].classList.contains('crushing') &&
                row.every(idx => squares[idx].className === type)) {
                row.forEach(idx => matchSet.add(idx));
            }
        }
        for (let i = 0; i < 48; i++) {
            let col = [i, i+width, i+width*2];
            let type = squares[i].className;
            if (type !== 'blank' && !squares[i].classList.contains('crushing') &&
                col.every(idx => squares[idx].className === type)) {
                col.forEach(idx => matchSet.add(idx));
            }
        }
        if (matchSet.size > 0) {
            playCrunchSound();
            matchSet.forEach(idx => {
                squares[idx].classList.add('crushing');
                setTimeout(() => { squares[idx].className = 'blank'; }, 400);
            });
            score += matchSet.size * 5;
            scoreDisplay.innerHTML = score;
            found = true;
        }
        return found;
    }

    function moveDown() {
        for (let i = 0; i < 56; i++) {
            if (squares[i + width].className === 'blank') {
                squares[i + width].className = squares[i].className;
                squares[i].className = 'blank';
            }
        }
        for (let i = 0; i < 8; i++) {
            if (squares[i].className === 'blank') {
                squares[i].className = candyTypes[Math.floor(Math.random() * candyTypes.length)];
            }
        }
