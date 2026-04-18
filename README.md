# PiPet-CyberDeck
A two-device AI cyberdeck ecosystem — A Portable AI Tamagotchi-inspired pet + pet house home base. 

Device 1 — A Raspberry Pi Zero 2W + Whisplay HAT (built-in display, mic, and speaker) within an egg shell like a Tamagotchi. Runs a virtual pet game on the Whisplay display and acts as a streaming client to encode and decode audio over WiFi to the Pet House AI. Has A/B/C multi-mode buttons, volume controls, LED status bar, and a PiSugar 3 battery. The Tamagotchi snaps into a dock cradle built into the front of the house via magnetic pogo pins. When docked it charges and gets updates on new pet states or games I create later on. 

Device 2 — The Pet House A pet house-shaped cyberdeck running Raspberry Pi 5 8GB with a Freenove 4.3" DSI touchscreen and Rii mini keyboard.

## Pet House

### ✨ Features
- 100% Local Intelligence: Powered by Ollama (LLM) and Whisper.cpp (Speech-to-Text). No API fees, no cloud data usage.
- Open Source Wake Word: Wakes up to your custom model using OpenWakeWord (Offline & Free). No access keys required.
- Hardware-Aware Audio: Automatically detects your microphone's sample rate and resamples audio on the fly to prevent ALSA errors.
- Smart Web Search: Uses DuckDuckGo to find real-time news and information when the LLM doesn't know the answer.
- Reactive Talking Tamgotchi Pet: The GUI updates the character's face based on its state (Listening, Thinking, Speaking, Idle).
- Fast Text-to-Speech: Uses Piper TTS for low-latency, high-quality voice generation on the Pi.
- Vision Capable: Can "see" and describe the world using a connected camera and the Moondream vision model

## Pi-Pet

### ✨ Features



# Pet States

## Tamgotchi (more, cuter, game-focused):

Idle / blinking
Happy / dancing
Hungry / sad empty bowl
Sleeping / ZZZs floating
Playing / mini game sprites
Eating / chomping
Sick / dizzy stars
Excited / docking animation when snapping into house
Pooping 💩 (classic Tamagotchi!)

## House animations (fewer, simpler, AI state-focused):

Idle / gentle loop
Listening / perked ears or sound waves
Thinking / thinking bubble or spinning
Speaking / mouth moving
Error / confused face




To answer your questions:

🎮 Buttons The Whisplay HAT has 3 buttons (A, B, C). How do you want them to work?

Option 1: A = navigate left, B = select/confirm, C = navigate right

Option 2: A = navigate menu, B = confirm, C = cancel/back

Or something else?

📋 Menu/Toolbar Picotamachibi had icons across the top. Do you want:

Same style toolbar with icons?

Or a different navigation style since your screen is bigger?

What actions do you want available?

Feed

Play

Sleep

Medicine

Clean/Toilet

Stats view

Pause

Anything else?

🎮 Mini Games Do you want any mini games for the play action? Simple ones like:

Guess the number

Button timing game

Rock paper scissors

🏠 Docking When egg docks to Pet House, what should happen beyond charging and syncing? Any special interactions?

📊 Stats Display How do you want to show Pip's stats?

Little bar graphs?

Numbers?

Just the animation reflects her mood?


# Amazon StoreFront

# 3d Model file sources
