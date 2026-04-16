# PiPet-CyberDeck
A two-device AI cyberdeck ecosystem — A Portable AI Tamagotchi-inspired pet + pet house home base. 

Device 1 — The Tamagotchi A Raspberry Pi Zero 2W + Whisplay HAT within an egg shell like a Tamagotchi. Runs a virtual pet game and streaming client to encode and decode audio and send/receive over wifi. Has a A/B/C multi-mode buttons, volume controls, speaker, LED status bar, and a PiSugar battery. 

Device 2 — The Pet House A pet house-shaped cyberdeck running Raspberry Pi 5 8GB with a Freenove 4.3" DSI touchscreen and Rii mini keyboard. The Tamagotchi snaps into a dock cradle built into the front of the house via magnetic pogo pins. When docked it charges and gets updates on new ppet states or games I create later on. 

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
