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

# Resources
## What I bought - Amazon Storefront
- House
Raspberry Pi 5 Starter Kit
https://www.pishop.us/product/raspberry-pi-5-budget-kit-8gb/

FREENOVE Raspberry Pi 5 Case with Screen (4.3'' Touchscreen), 128GB M.2 NVMe SSD 800 MB/s, 5 MP Camera, OLED Screen, Stereo Speakers, 3.5 mm and Optical Audio 
https://www.amazon.com/dp/B0F59W14PB?ref=ppx_yo2ov_dt_b_fed_asin_title&th=1

SunFounder USB 2.0 Mini Microphone for Raspberry Pi 5/4B/3B+/3B
https://www.amazon.com/dp/B01KLRBHGM?ref=ppx_yo2ov_dt_b_fed_asin_title

Mini Keyboard with Touchpad, Mini Bluetooth Keyboard
https://www.amazon.com/dp/B0G3NZT2XN?ref=ppx_yo2ov_dt_b_fed_asin_title

- Pet
Raspberry Pi Zero 2W with Pre-soldered Headers
https://www.amazon.com/dp/B0D7VKHJQL?ref=ppx_yo2ov_dt_b_fed_asin_title

PiSugar 3 Portable Pwnagotchi Power Management Board for Raspberry Pi Zero W/WH Model
https://www.amazon.com/dp/B0FB3N1YSK?ref=ppx_yo2ov_dt_b_fed_asin_title

Whisplay Hat for Raspberry Pi Zero 
https://www.amazon.com/dp/B0FPG8S6K6?ref=ppx_yo2ov_dt_b_fed_asin_title


## 3d Model file sources
3D Printable Cat House Display with Cat STL Model (Digital Download): https://www.etsy.com/listing/4347595034/3d-printable-cat-house-display-with-cat?ref=cart

Tamagotchi cat seat/Display stand
https://cults3d.com/en/3d-model/game/tamagotchi-seats



## Youtube Videos
- Inspo for the pet: https://www.youtube.com/watch?v=Nwu2DruSuyI
- Inspo for the house: https://youtu.be/l5ggH-YhuAw?si=hnKl_vyuef4Zn_PD
- Set up raspberry pi: https://youtu.be/3zEzh5-f4KA?si=dgzxZ08z_SBW3skF
- How to Add a Power Button to Your Raspberry Pi (+ FLIRC Case Install!): https://www.youtube.com/watch?v=wVnMZ4DXDNo

## Documentation
- Pi Sugar 3: I was really confused on how to turn on and off my pet. This was very helpful: https://docs.pisugar.com/docs/product-wiki/battery/pisugar3/pisugar-3-series#software-installation


## Github Repos References
PiSugar / Whisplay
https://github.com/PiSugar/Whisplay

ollama / ollama
https://github.com/ollama/ollama

PiSugar / pisugar-power-manager-rs
https://github.com/PiSugar/pisugar-power-manager-rs

openai / whisper
https://github.com/openai/whisper

rhasspy / piper
https://github.com/rhasspy/piper

Picotamachibi
https://github.com/kevinmcaleer/picotamachibi/tree/main

openWakeWord
https://github.com/dscripka/openWakeWord/tree/main


## Additional Resources
- https://www.reddit.com/r/cyberDeck/
- 

# Final Thoughts
