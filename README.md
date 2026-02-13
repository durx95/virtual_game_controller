# 🎮 Pose Controlled Virtual Game Controller
An end-to-end Computer Vision application that allows users to control directional keys (⬅ ➡ ⬆ ⬇) using body movement captured through a webcam.
The system is built using Python, MediaPipe, OpenCV, and pynput, enabling real-time gesture-based game control.
----

# 🚀 Demo
🎥 Real-time webcam-based pose tracking
🎮 Controls arrow keys using shoulder movement
----

# 🧠 Problem Statement
Traditional gaming relies on physical controllers like keyboards or joysticks.
This project aims to build a touchless virtual controller using AI-powered pose detection, enabling Human-Computer Interaction through body movement.
The goal is to explore:
Computer Vision
Real-time motion detection
AI-based interaction systems
----

# 📊 Features
Real-time pose detection using MediaPipe
Shoulder midpoint tracking
Threshold-based direction detection
Arrow key simulation using pynput
Visual guidance lines for movement reference
Prevents repeated key triggering using direction state logic
-----

# 🛠️ Tech Stack
Programming Language: Python
Computer Vision Library: OpenCV
Pose Detection Framework: MediaPipe
Keyboard Automation: pynput
Hardware Requirement: Webcam
----

# 🧪 Input
Live webcam video feed
User shoulder movement (Left / Right / Up / Down)
----

# 📈 Output
Simulated keyboard arrow key presses
On-screen direction display
Real-time pose landmark visualization
----

# ⚙️ How It Works
Captures live webcam feed.
Detects body pose landmarks using MediaPipe.
Extracts left and right shoulder coordinates.
Calculates midpoint between shoulders.
Compares midpoint with screen center.
If midpoint crosses defined threshold → Triggers corresponding arrow key.
Updates direction only when it changes to avoid repeated key spam.
----