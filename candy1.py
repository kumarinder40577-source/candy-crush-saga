import streamlit as st
import streamlit.components.v1 as components

# 1. Setup Page Config
st.set_page_config(page_title="Candy Crush Saga Clone", layout="centered")

# 2. Define your HTML/CSS/JS string (Line 4 fix)
# Ensure this ends with exactly three quotes """
crash_candy_html = """
<div id="game-container">
    <h2 style="color: white; text-align: center;">Candy Crush Web Edition</h2>
    <canvas id="gameCanvas" width="400" height="400" style="border:2px solid #fff;"></canvas>
</div>

<script>
    // Your JavaScript Game Logic goes here
    console.log("Game Loaded");
</script>

<style>
    body { background-color: #222; }
    #game-container { display: flex; flex-direction: column; align-items: center; }
</style>
""" 

# 3. Streamlit UI Elements
st.title("🍬 Candy Crush Saga")
st.write("Welcome to the Streamlit version of the game!")

# 4. Inject the HTML/JS into the Streamlit app
# Increase height/width based on your game size
components.html(crash_candy_html, height=600, scrolling=True)

st.info("Note: If the game doesn't appear, check your JavaScript console for errors.")
