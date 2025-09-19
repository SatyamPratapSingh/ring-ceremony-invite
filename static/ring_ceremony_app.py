
from flask import Flask, render_template_string, request
import sqlite3
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


def init_db():
    if os.path.exists('photos.db'):
        os.remove('photos.db')  # Delete corrupted DB
    conn = sqlite3.connect('photos.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS photos (id INTEGER PRIMARY KEY, filename TEXT)''')
    conn.commit()
    conn.close()


init_db()

html_template = """
<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>Ring Ceremony Invitation</title>
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background-image: url('shared image (1).jfif'); /* Replace with actual image path */
            background-size: cover;
            background-position: center;
            color: white;
            margin: 0;
            padding: 0;
        }
        .container {
            background-color: rgba(0, 0, 0, 0.7);
            padding: 20px;
            border-radius: 10px;
            max-width: 90%;
            margin: 30px auto;
            box-shadow: 0 0 10px rgba(255,255,255,0.3);
        }
        input[type="file"], button {
            margin: 10px 0;
            padding: 10px;
            border-radius: 5px;
            border: none;
        }
        button {
            background-color: #ffcc00;
            color: #000;
            cursor: pointer;
        }
        .contacts p {
            margin: 5px 0;
        }
        @media (max-width: 600px) {
            h1, h2, h3, p {
                font-size: 90%;
            }
        }
    </style>
</head>
<body>
    <div class='container'>
        <h1>You're Invited!</h1>
        <h2>Ring Ceremony of [Name1] & [Name2]</h2>
        <p>Join us for a joyful celebration of love and togetherness.</p>

        <h3>Upload Your Photo</h3>
        <form method='POST' enctype='multipart/form-data'>
            <input type='file' name='photo' accept='image/*'>
            <button type='submit'>Upload</button>
        </form>

        <div class='contacts'>
            <h3>Contact Us</h3>
            <p><strong>Travel:</strong> Surya</p>
    <p><strong>Phone:</strong> +91-9876543210</p>
    <p><strong>Logistic:</strong> Satyam</p>
    <p><strong>Phone:</strong> +91-9876543210</p>
    <p><strong>Hotels:</strong> Shubham</p>
    <p><strong>Phone:</strong> +91-9876543210</p>
    <h2> Medical and dental services-NOT Available</h2>
        </div>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def invite():
    if request.method == 'POST':
        photo = request.files['photo']
        if photo:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], photo.filename)
            photo.save(filepath)
            conn = sqlite3.connect('photos.db')
            c = conn.cursor()
            c.execute("INSERT INTO photos (filename) VALUES (?)", (photo.filename,))
            conn.commit()
            conn.close()
    return render_template_string(html_template)

if __name__ == '__main__':
    app.run(debug=True)
