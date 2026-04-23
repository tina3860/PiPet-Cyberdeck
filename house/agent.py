import json
import requests
import subprocess
import tempfile
import os
import threading
import time
import re
import wave
import pygame
from PIL import Image
from datetime import datetime
from ddgs import DDGS

# -------------------------
# DISPLAY ENVIRONMENT
# -------------------------
os.environ["DISPLAY"] = ":0"
os.environ["SDL_AUDIODRIVER"] = "dummy"

# -------------------------
# SHARED STATE
# -------------------------
state = {
    "animation":        "idle",
    "running":          True,
    "chat_text":        "",
    "display_chars":    0,
    "typewriter_speed": 3,
    "stats": {
        "hunger":      80,
        "happiness":   70,
        "health":      90,
        "energy":      60,
        "cleanliness": 85,
    }
}

# -------------------------
# LOAD CONFIG
# -------------------------
with open("config/config.json", "r") as f:
    config = json.load(f)

# -------------------------
# LOAD MEMORY
# -------------------------
MEMORY_PATH = "memory.json"

def load_memory():
    if os.path.exists(MEMORY_PATH):
        with open(MEMORY_PATH, "r") as f:
            return json.load(f)
    return {}

def save_memory(memory):
    with open(MEMORY_PATH, "w") as f:
        json.dump(memory, f, indent=2)

memory = load_memory()

# -------------------------
# DUCKDUCKGO SEARCH
# -------------------------
def should_search(query):
    """Decide if query needs a web search"""
    search_triggers = [
        "weather", "temperature", "forecast",
        "time", "date", "today", "tonight",
        "news", "latest", "current", "right now",
        "stock", "price",
        "recipe", "how to make", "ingredients",
        "who is", "what is", "when did", "where is",
        "roth ira", "401k", "finance", "invest",
        "define", "meaning of",
    ]
    query_lower = query.lower()
    return any(trigger in query_lower for trigger in search_triggers)

def web_search(query):
    """Search DuckDuckGo and return summarized results"""
    try:
        print(f"🔍 Searching: {query}")
        results = DDGS().text(
            query + f" {memory.get('location', 'Walnut Creek CA')}",
            max_results=3
        )
        if not results:
            return None

        # Build context from results
        context = "Web search results:\n"
        sources = []
        for r in results:
            context += f"- {r['body']}\n"
            sources.append(r['href'])

        return context, sources
    except Exception as e:
        print(f"Search error: {e}")
        return None, []

# -------------------------
# OLLAMA
# -------------------------
OLLAMA_URL = "http://localhost:11434/api/chat"
messages   = []

# -------------------------
# DISPLAY SETTINGS
# -------------------------
WIDTH    = 800
HEIGHT   = 480
FPS      = 8
ANIM_DIR = "/home/tina386/PiPet-Cyberdeck-Ecosystem/house/animations"

# -------------------------
# GIF LOADER
# -------------------------
def load_gif(filename):
    frames = []
    gif = Image.open(os.path.join(ANIM_DIR, filename))
    for frame in range(gif.n_frames):
        gif.seek(frame)
        frame_img = gif.convert("RGB")
        frame_img = frame_img.resize((WIDTH, HEIGHT), Image.NEAREST)
        frames.append(frame_img)
    return frames

def pil_to_pygame(pil_image):
    return pygame.image.fromstring(
        pil_image.tobytes(), pil_image.size, "RGB"
    )

# -------------------------
# STAT HELPERS
# -------------------------
def get_bar_color(value):
    if value >= 70:
        return (100, 200, 120)
    elif value >= 40:
        return (255, 200, 50)
    else:
        return (220, 80, 80)

def get_lowest_stats(stats):
    sorted_stats = sorted(stats.items(), key=lambda x: x[1])
    return [sorted_stats[0][0], sorted_stats[1][0]]

# -------------------------
# TEXT HELPERS
# -------------------------
def clean_text(text):
    text = text.encode('ascii', 'ignore').decode('ascii')
    text = re.sub(r'\*+', '', text)
    text = re.sub(r'#+', '', text)
    text = re.sub(r'http\S+', '', text)   # remove URLs from speech
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# -------------------------
# DISPLAY THREAD
# -------------------------
def display_thread():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    clock  = pygame.time.Clock()

    print("Loading animations...")
    animations = {
        "idle":      load_gif("Cat_idle_house.gif"),
        "listening": load_gif("Cat_listen_house.gif"),
        "thinking":  load_gif("Cat_think_house.gif"),
        "speaking":  load_gif("Cat_speak_house.gif"),
        "error":     load_gif("Cat_error_house.gif"),
    }
    print("Animations loaded!")

    widget_collapsed = pygame.image.load(
        os.path.join(ANIM_DIR, "Status-bar-collapsed.png")
    ).convert_alpha()
    widget_expanded = pygame.image.load(
        os.path.join(ANIM_DIR, "Status-bar-expanded.png")
    ).convert_alpha()
    widget_collapsed = pygame.transform.scale(widget_collapsed, (240, 160))
    widget_expanded  = pygame.transform.scale(widget_expanded,  (240, 160))

    chat_box = pygame.image.load(
        os.path.join(ANIM_DIR, "Chat-box.png")
    ).convert_alpha()
    chat_box = pygame.transform.scale(chat_box, (800, 100))

    font_large = pygame.font.SysFont("monospace", 20, bold=True)
    font_small = pygame.font.SysFont("monospace", 13, bold=True)
    chat_font  = pygame.font.SysFont("monospace", 20)

    BAR_X      = 82
    BAR_WIDTH  = 136
    BAR_HEIGHT = 14

    BARS_COLLAPSED = [{"y": 24, "stat": None}, {"y": 40, "stat": None}]
    BARS_EXPANDED  = [
        {"y": 24, "stat": "hunger"},
        {"y": 40, "stat": "happiness"},
        {"y": 56, "stat": "health"},
        {"y": 72, "stat": "energy"},
        {"y": 88, "stat": "cleanliness"},
    ]

    ARROW_COLLAPSED = pygame.Rect(182, 56,  56, 26)
    ARROW_EXPANDED  = pygame.Rect(194, 108, 26, 18)

    CHAT_BOX_Y     = 380
    CHAT_TEXT_X    = 20
    CHAT_TEXT_Y    = CHAT_BOX_Y + 25
    CHAT_MAX_WIDTH = 760

    def handle_tap(pos, widget_open):
        arrow = ARROW_EXPANDED if widget_open else ARROW_COLLAPSED
        if arrow.collidepoint(pos):
            return not widget_open
        return widget_open

    def draw_stat_widget(screen, stats, widget_open):
        img = widget_expanded if widget_open else widget_collapsed
        screen.blit(img, (0, 0))
        if widget_open:
            bars = BARS_EXPANDED
            name_surf = font_small.render("Pip", True, (80, 50, 50))
            name_x = (78 - name_surf.get_width()) // 2 + 8
            screen.blit(name_surf, (name_x, 87))
        else:
            lowest = get_lowest_stats(stats)
            bars = [
                {"y": BARS_COLLAPSED[0]["y"], "stat": lowest[0]},
                {"y": BARS_COLLAPSED[1]["y"], "stat": lowest[1]},
            ]
            name_surf = font_large.render("Pip", True, (80, 50, 50))
            name_x = (160 - name_surf.get_width()) // 2 + 28
            screen.blit(name_surf, (name_x, 59))
        for bar in bars:
            stat_name = bar["stat"]
            if not stat_name:
                continue
            value      = stats[stat_name]
            fill_width = int((value / 100) * BAR_WIDTH)
            color      = get_bar_color(value)
            pygame.draw.rect(screen, color,
                           (BAR_X, bar["y"], fill_width, BAR_HEIGHT))

    def wrap_text(text, font, max_width):
        words = text.split(' ')
        lines = []
        current_line = ""
        for word in words:
            while font.size(word)[0] > max_width:
                for i in range(len(word), 0, -1):
                    if font.size(word[:i])[0] <= max_width:
                        if current_line:
                            lines.append(current_line.strip())
                            current_line = ""
                        lines.append(word[:i])
                        word = word[i:]
                        break
            test_line = current_line + word + " "
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line.strip())
                current_line = word + " "
        if current_line:
            lines.append(current_line.strip())
        return lines

    def draw_chat_box(screen, chat_text, display_chars):
        nonlocal scroll_offset, last_text
        screen.blit(chat_box, (0, CHAT_BOX_Y))
        if not chat_text:
            scroll_offset = 0
            last_text = ""
            return
        if chat_text != last_text:
            scroll_offset = 0
            last_text = chat_text
        visible_text = chat_text[:display_chars]
        lines        = wrap_text(visible_text, chat_font, CHAT_MAX_WIDTH)
        line_height  = 26
        max_visible  = 3
        total_lines  = len(lines)
        if total_lines > max_visible:
            scroll_offset = total_lines - max_visible
        visible_lines = lines[scroll_offset:scroll_offset + max_visible]
        for i, line in enumerate(visible_lines):
            text_surf = chat_font.render(line, True, (80, 50, 50))
            screen.blit(text_surf, (CHAT_TEXT_X, CHAT_TEXT_Y + i * line_height))

    frame_index        = 0
    widget_open        = False
    prev_anim          = "idle"
    typewriter_counter = 0
    scroll_offset      = 0
    last_text          = ""

    print("Display running!")
    state["display_ready"] = True

    while state["running"]:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state["running"] = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state["running"] = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                widget_open = handle_tap(event.pos, widget_open)
            if event.type == pygame.FINGERDOWN:
                tap_x = int(event.x * WIDTH)
                tap_y = int(event.y * HEIGHT)
                widget_open = handle_tap((tap_x, tap_y), widget_open)

        current_anim = state["animation"]
        if current_anim != prev_anim:
            frame_index = 0
            prev_anim   = current_anim

        frames  = animations[current_anim]
        surface = pil_to_pygame(frames[frame_index])
        screen.blit(surface, (0, 0))
        draw_stat_widget(screen, state["stats"], widget_open)
        draw_chat_box(screen, state["chat_text"], state["display_chars"])

        typewriter_counter += 1
        if typewriter_counter >= 1:
            typewriter_counter = 0
            if state["display_chars"] < len(state["chat_text"]):
                state["display_chars"] += state["typewriter_speed"]

        pygame.display.flip()
        frame_index = (frame_index + 1) % len(frames)
        clock.tick(FPS)

    pygame.quit()

# -------------------------
# AGENT FUNCTIONS
# -------------------------
def record_audio():
    state["animation"]     = "listening"
    state["chat_text"]     = "Listening..."
    state["display_chars"] = 13
    print("🎤 Listening for 5 seconds...")
    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    try:
        subprocess.run([
            "arecord",
            "-D", "plughw:3,0",
            "-f", "S16_LE",
            "-r", "16000",
            "-c", "1",
            "-d", "5",
            tmp.name
        ], timeout=7)
    except subprocess.TimeoutExpired:
        print("Recording timed out!")
    except Exception as e:
        print(f"Recording error: {e}")
    state["chat_text"]     = "Thinking..."
    state["display_chars"] = 12
    state["animation"]     = "thinking"
    return tmp.name

def transcribe(audio_file):
    state["animation"]     = "thinking"
    state["chat_text"]     = "Transcribing..."
    state["display_chars"] = 15
    print("💭 Transcribing...")
    subprocess.run(
        ["whisper", audio_file,
         "--model", "tiny",
         "--language", "English",
         "--output_format", "txt",
         "--output_dir", "/tmp"],
        capture_output=True, text=True
    )
    base     = os.path.splitext(os.path.basename(audio_file))[0]
    txt_file = f"/tmp/{base}.txt"
    if os.path.exists(txt_file):
        with open(txt_file) as f:
            return f.read().strip()
    return ""

def chat(user_input):
    state["animation"]     = "thinking"
    state["chat_text"]     = "Thinking..."
    state["display_chars"] = 12

    # Real time and date
    current_time = datetime.now().strftime("%I:%M %p")
    current_date = datetime.now().strftime("%A, %B %d, %Y")

    # Build system prompt with memory
    system = (
        f"{config['system_prompt']} "
        f"The user's name is {memory.get('name', 'Meow-mi')}. "
        f"Location: {memory.get('location', 'Walnut Creek, CA')}. "
        f"Current time: {current_time}. Today is {current_date}. "
        f"Preferences: {json.dumps(memory.get('preferences', {}))}. "
        f"Keep responses short and simple. Never read URLs aloud. "
        f"When citing sources, just mention the site name not the full URL."
    )

    # Check if we need to search
    search_context = ""
    sources        = []
    if should_search(user_input):
        state["chat_text"]     = "Searching..."
        state["display_chars"] = 11
        result = web_search(user_input)
        if result and result[0]:
            search_context, sources = result
            print(f"🔍 Found {len(sources)} sources")

    # Build messages with optional search context
    user_message = user_input
    if search_context:
        user_message = f"{user_input}\n\nContext from web search:\n{search_context}"

    messages.append({"role": "user", "content": user_message})

    try:
        response = requests.post(OLLAMA_URL, json={
            "model": config["text_model"],
            "messages": [
                {"role": "system", "content": system}
            ] + messages,
            "stream": False
        })
        reply = response.json()["message"]["content"]

        # Add source links to display (not spoken)
        if sources:
            display_reply = reply + "\n\nSources: " + " | ".join(
                [s.split('/')[2] for s in sources[:2]]  # just domain names
            )
        else:
            display_reply = reply

        messages.append({"role": "assistant", "content": reply})
        return reply, display_reply

    except Exception as e:
        state["animation"] = "error"
        print(f"Chat error: {e}")
        return "Sorry, I had a problem thinking!", "Sorry, I had a problem thinking!"

def speak(text, display_text=None):
    if display_text is None:
        display_text = text
    state["animation"]     = "speaking"
    cleaned = clean_text(text)
    state["chat_text"]     = display_text
    state["display_chars"] = 0
    print("🔊 Speaking...")

    subprocess.run([
        config["piper_path"],
        "--model", config["voice_model"],
        "--output_file", "/tmp/response.wav"
    ], input=cleaned.encode(), capture_output=True)

    try:
        with wave.open("/tmp/response.wav", "r") as wav_file:
            frames   = wav_file.getnframes()
            rate     = wav_file.getframerate()
            duration = frames / float(rate)
    except:
        duration = len(cleaned) * 0.06

    total_frames = duration * FPS
    text_len     = len(display_text)
    if total_frames > 0:
        chars_per_frame = max(1, int(text_len / total_frames))
    else:
        chars_per_frame = 3

    state["typewriter_speed"] = chars_per_frame
    time.sleep(0.5)
    subprocess.run(["paplay", "/tmp/response.wav"])
    state["animation"]        = "idle"
    time.sleep(2)
    state["chat_text"]        = ""
    state["display_chars"]    = 0
    state["typewriter_speed"] = 3

# -------------------------
# MAIN
# -------------------------
if __name__ == "__main__":

    state["display_ready"] = False

    display = threading.Thread(target=display_thread, daemon=True)
    display.start()

    print("Waiting for display...")
    while not state.get("display_ready", False):
        time.sleep(0.1)

    print("Pet House AI is ready!")
    print("  - Press Enter to speak")
    print("  - Type a message and press Enter to chat by text")
    print("  - Type 'quit' to exit")

    try:
        while state["running"]:
            state["animation"] = "idle"
            user_input = input("\nYou: ")

            if user_input.lower() == "quit":
                state["running"] = False
                break
            elif user_input == "":
                audio_file = record_audio()
                text = transcribe(audio_file)
                print(f"Transcribed: '{text}'")
                if text:
                    print(f"You said: {text}")
                    reply, display_reply = chat(text)
                    print(f"Pip: {reply}")
                    speak(reply, display_reply)
                else:
                    state["animation"]     = "error"
                    state["chat_text"]     = "I couldn't hear anything, try again!"
                    state["display_chars"] = 38
                    time.sleep(2)
                    state["animation"]     = "idle"
                    state["chat_text"]     = ""
                    state["display_chars"] = 0
                    print("Couldn't hear anything, try again!")
            else:
                reply, display_reply = chat(user_input)
                print(f"Pip: {reply}")
                speak(reply, display_reply)

    except KeyboardInterrupt:
        state["running"] = False
        print("\nShutting down...")