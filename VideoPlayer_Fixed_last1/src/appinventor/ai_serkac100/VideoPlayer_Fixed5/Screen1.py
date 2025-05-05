"""
MIT App Inventor Video Player Emulator - Screen1
This is a Python emulator/wrapper for the MIT App Inventor project
"""

import sys
import os
import flask
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Global storage for video links (mimicking TinyDB in App Inventor)
tinydb_storage = {
    "VideoLink1": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",  # Default video link for testing
    "VideoLink2": "",
    "VideoLink3": "",
}

@app.route('/')
def home():
    """Render the main screen (Screen1) of the app"""
    # Emulate the Screen1 interface with video player and buttons
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Video Player - Screen1</title>
        <style>
            body {
                background-color: blue;
                font-family: Arial, sans-serif;
                color: white;
                text-align: center;
                margin: 0;
                padding: 20px;
            }
            .debug-label {
                background-color: rgba(255,255,255,0.7);
                color: red;
                padding: 10px;
                margin-bottom: 20px;
                border-radius: 5px;
                text-align: left;
                font-weight: bold;
            }
            .button-row {
                display: flex;
                justify-content: space-around;
                margin-bottom: 10px;
            }
            button {
                background-color: white;
                border: none;
                color: black;
                padding: 10px 20px;
                font-size: 16px;
                font-weight: bold;
                border-radius: 5px;
                cursor: pointer;
            }
            .settings-button {
                background-color: #cccccc;
                margin-top: 20px;
            }
            .debug-button {
                background-color: #ffcc00;
                margin-top: 10px;
                margin-bottom: 10px;
            }
            .video-container {
                margin-top: 20px;
                height: 300px;
                background-color: black;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
            }
            #videoPlayer {
                width: 100%;
                height: 100%;
            }
        </style>
    </head>
    <body>
        <div class="debug-label" id="debugLabel">Debug Info will appear here</div>
        
        <div class="button-row">
            <button onclick="playVideo(1)">Video 1</button>
            <button onclick="playVideo(2)">Video 2</button>
            <button onclick="playVideo(3)">Video 3</button>
        </div>
        
        <div class="button-row">
            <button onclick="playVideo(4)">Video 4</button>
            <button onclick="playVideo(5)">Video 5</button>
            <button onclick="playVideo(6)">Video 6</button>
        </div>
        
        <div class="button-row">
            <button onclick="playVideo(7)">Video 7</button>
            <button onclick="playVideo(8)">Video 8</button>
            <button onclick="playVideo(9)">Video 9</button>
        </div>
        
        <div class="button-row">
            <button onclick="playVideo(10)">Video 10</button>
            <button onclick="playVideo(11)">Video 11</button>
            <button onclick="playVideo(12)">Video 12</button>
        </div>
        
        <button class="debug-button" onclick="showDebugInfo()">Show TinyDB Values</button>
        
        <div class="video-container" id="videoContainer">
            <div id="videoPlaceholder">Video will appear here when played</div>
            <iframe id="videoPlayer" style="display:none;" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
        </div>
        
        <button class="settings-button" onclick="goToSettings()">Settings</button>
        
        <script>
            // Initialize the app
            document.addEventListener('DOMContentLoaded', function() {
                document.getElementById('debugLabel').innerText = 'Initialized Video Player...';
                loadLinksFromTinyDB();
            });
            
            // Load links from TinyDB (via AJAX)
            function loadLinksFromTinyDB() {
                fetch('/get_links')
                    .then(response => response.json())
                    .then(data => {
                        let linkCount = 0;
                        if (data.VideoLink1 && data.VideoLink1 !== '') linkCount++;
                        if (data.VideoLink2 && data.VideoLink2 !== '') linkCount++;
                        if (data.VideoLink3 && data.VideoLink3 !== '') linkCount++;
                        
                        document.getElementById('debugLabel').innerText = 'Loaded links from TinyDB: ' + linkCount + ' links found';
                    })
                    .catch(error => {
                        document.getElementById('debugLabel').innerText = 'Error loading links: ' + error;
                    });
            }
            
            // Play video based on button number
            function playVideo(num) {
                document.getElementById('debugLabel').innerText = 'Button' + num + ' clicked';
                
                fetch('/get_link?id=' + num)
                    .then(response => response.json())
                    .then(data => {
                        if (data.link && data.link !== '') {
                            document.getElementById('debugLabel').innerText = 'Playing Video ' + num + ': ' + data.link;
                            
                            // Extract YouTube video ID
                            let videoId = '';
                            if (data.link.includes('youtube.com/watch?v=')) {
                                videoId = data.link.split('v=')[1];
                                const ampersandPosition = videoId.indexOf('&');
                                if (ampersandPosition !== -1) {
                                    videoId = videoId.substring(0, ampersandPosition);
                                }
                            } else if (data.link.includes('youtu.be/')) {
                                videoId = data.link.split('youtu.be/')[1];
                            }
                            
                            if (videoId) {
                                document.getElementById('videoPlaceholder').style.display = 'none';
                                document.getElementById('videoPlayer').style.display = 'block';
                                document.getElementById('videoPlayer').src = 'https://www.youtube.com/embed/' + videoId + '?autoplay=1';
                            } else {
                                alert('Invalid YouTube URL format');
                            }
                        } else {
                            alert('No video link set for Video ' + num + '. Please configure in Settings.');
                        }
                    })
                    .catch(error => {
                        alert('Error: ' + error);
                    });
            }
            
            // Show debug information
            function showDebugInfo() {
                fetch('/get_links')
                    .then(response => response.json())
                    .then(data => {
                        let debugInfo = 'Current TinyDB Values:\\n';
                        debugInfo += 'VideoLink1: ' + (data.VideoLink1 || '[Not Found]') + '\\n';
                        debugInfo += 'VideoLink2: ' + (data.VideoLink2 || '[Not Found]') + '\\n';
                        debugInfo += 'VideoLink3: ' + (data.VideoLink3 || '[Not Found]') + '\\n';
                        
                        alert(debugInfo);
                    })
                    .catch(error => {
                        alert('Error loading debug info: ' + error);
                    });
            }
            
            // Navigate to settings screen
            function goToSettings() {
                window.location.href = '/settings';
            }
        </script>
    </body>
    </html>
    """)

@app.route('/settings')
def settings():
    """Render the settings screen (Screen2) of the app"""
    # Emulate the Settings screen (Screen2) interface
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Video Settings - Screen2</title>
        <style>
            body {
                background-color: #99ccff;
                font-family: Arial, sans-serif;
                color: black;
                text-align: center;
                margin: 0;
                padding: 20px;
            }
            h1 {
                font-weight: bold;
                font-size: 24px;
                margin-bottom: 20px;
            }
            .form-group {
                display: flex;
                margin-bottom: 15px;
                align-items: center;
            }
            label {
                flex: 1;
                text-align: right;
                padding-right: 10px;
            }
            input {
                flex: 2;
                padding: 8px;
                border-radius: 4px;
                border: 1px solid #ccc;
            }
            .status-label {
                color: blue;
                font-weight: bold;
                margin: 15px 0;
            }
            .button-container {
                margin-top: 20px;
                display: flex;
                justify-content: center;
                gap: 10px;
            }
            .save-button {
                background-color: #00cc00;
                border: none;
                color: white;
                padding: 10px 20px;
                font-size: 16px;
                border-radius: 5px;
                cursor: pointer;
            }
            .debug-button {
                background-color: #ff9900;
                border: none;
                color: white;
                padding: 10px 20px;
                font-size: 16px;
                border-radius: 5px;
                cursor: pointer;
            }
            .back-button {
                background-color: #cccccc;
                border: none;
                color: black;
                padding: 10px 20px;
                font-size: 16px;
                border-radius: 5px;
                cursor: pointer;
            }
        </style>
    </head>
    <body>
        <h1>Video Settings</h1>
        
        <div class="form-group">
            <label for="video1">Video 1 URL:</label>
            <input type="text" id="video1" placeholder="Enter URL for Video 1">
        </div>
        
        <div class="form-group">
            <label for="video2">Video 2 URL:</label>
            <input type="text" id="video2" placeholder="Enter URL for Video 2">
        </div>
        
        <div class="form-group">
            <label for="video3">Video 3 URL:</label>
            <input type="text" id="video3" placeholder="Enter URL for Video 3">
        </div>
        
        <div class="status-label" id="statusLabel">Enter video URLs above and tap Save</div>
        
        <div class="button-container">
            <button class="save-button" onclick="saveSettings()">Save Settings</button>
            <button class="debug-button" onclick="showDebugInfo()">Debug</button>
            <button class="back-button" onclick="goBack()">Back to Videos</button>
        </div>
        
        <script>
            // Initialize the settings screen
            document.addEventListener('DOMContentLoaded', function() {
                loadSettings();
                document.getElementById('statusLabel').innerText = 'Settings screen initialized. Edit video URLs and tap Save.';
            });
            
            // Load current settings
            function loadSettings() {
                fetch('/get_links')
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('video1').value = data.VideoLink1 || '';
                        document.getElementById('video2').value = data.VideoLink2 || '';
                        document.getElementById('video3').value = data.VideoLink3 || '';
                    })
                    .catch(error => {
                        alert('Error loading settings: ' + error);
                    });
            }
            
            // Save settings
            function saveSettings() {
                const data = {
                    VideoLink1: document.getElementById('video1').value,
                    VideoLink2: document.getElementById('video2').value,
                    VideoLink3: document.getElementById('video3').value
                };
                
                fetch('/save_links', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data),
                })
                .then(response => response.json())
                .then(data => {
                    document.getElementById('statusLabel').innerText = 'Video links saved successfully!';
                    alert('All video links have been saved to TinyDB. They will be available when you return to the main screen.');
                })
                .catch((error) => {
                    alert('Error saving settings: ' + error);
                });
            }
            
            // Show debug information
            function showDebugInfo() {
                fetch('/get_links')
                    .then(response => response.json())
                    .then(data => {
                        let debugInfo = 'Current TinyDB Values:\\n';
                        debugInfo += 'VideoLink1: ' + (data.VideoLink1 || '[Not Found]') + '\\n';
                        debugInfo += 'VideoLink2: ' + (data.VideoLink2 || '[Not Found]') + '\\n';
                        
                        alert(debugInfo);
                    })
                    .catch(error => {
                        alert('Error loading debug info: ' + error);
                    });
            }
            
            // Go back to main screen
            function goBack() {
                window.location.href = '/';
            }
        </script>
    </body>
    </html>
    """)

@app.route('/get_links')
def get_links():
    """API endpoint to get all video links"""
    return jsonify(tinydb_storage)

@app.route('/get_link')
def get_link():
    """API endpoint to get a specific video link"""
    link_id = request.args.get('id', 1)
    try:
        link_id = int(link_id)
    except ValueError:
        link_id = 1
    
    # Only implemented for first 3 links for now
    if link_id == 1:
        return jsonify({"link": tinydb_storage.get("VideoLink1", "")})
    elif link_id == 2:
        return jsonify({"link": tinydb_storage.get("VideoLink2", "")})
    elif link_id == 3:
        return jsonify({"link": tinydb_storage.get("VideoLink3", "")})
    else:
        return jsonify({"link": ""})

@app.route('/save_links', methods=['POST'])
def save_links():
    """API endpoint to save video links"""
    data = request.json
    
    # Update the TinyDB storage with new values
    if 'VideoLink1' in data:
        tinydb_storage['VideoLink1'] = data['VideoLink1']
    if 'VideoLink2' in data:
        tinydb_storage['VideoLink2'] = data['VideoLink2']
    if 'VideoLink3' in data:
        tinydb_storage['VideoLink3'] = data['VideoLink3']
    
    return jsonify({"status": "success"})

def render_template_string(template):
    """Simple function to mimic Flask's render_template_string"""
    return template

if __name__ == '__main__':
    # Get port from command line arguments or use default
    port = 5000
    if len(sys.argv) > 2 and sys.argv[1] == '--port':
        try:
            port = int(sys.argv[2])
        except ValueError:
            pass
    
    print(f"Starting MIT App Inventor Emulator on port {port}")
    print("This is a web-based emulator for the MIT App Inventor Video Player project")
    print("Open your browser to http://localhost:5000/ to view the app")
    
    app.run(host='0.0.0.0', port=port, debug=True)