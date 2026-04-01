# Sonus - Premium Music Player

Sonus is a sleek, modern, web-based music streaming application. It features a premium "glassmorphism" user interface, live search autocomplete, dynamic cinematic backgrounds, and high-quality audio streaming powered by a custom Python backend integrating with the JioSaavn API.

## ✨ Features

* **Premium UI/UX:** Ultra-glassmorphism aesthetic with Apple-style "frosted glass" panels and a responsive, mobile-first design.
* **Cinematic Intro:** A Netflix-style dramatic logo reveal upon launching the app.
* **Live Search:** Instant autocomplete search for songs, albums, and movies without needing to press Enter.
* **High-Quality Audio:** Fetches and decrypts 320kbps high-fidelity AAC audio streams.
* **Dynamic Backgrounds:** The background seamlessly transitions to a massive, blurred, breathing version of the currently playing album artwork.
* **Direct Downloads:** One-click downloads for any playing track directly to your local device.
* **Custom Audio Engine:** Fully custom HTML5 audio player with progress tracking, volume control, and seeking.

## 🛠️ Tech Stack

* **Backend:** Python, Flask, Requests
* **Frontend:** HTML5, Vanilla JavaScript, Tailwind CSS (via CDN)
* **Icons:** FontAwesome
* **API:** JioSaavn Unofficial API (Search & Streaming)

## 📁 Project Structure

Make sure your files are organized exactly like this before running the application:

```text
MyMusicApp/
│
├── app.py                # The Flask backend server and API logic
└── templates/            # Folder required by Flask for HTML files
    └── index.html        # The frontend UI, Tailwind, and JavaScript
