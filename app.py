import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max-limit
app.config['SECRET_KEY'] = 'your_secret_key'

# Create upload directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'videos'), exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'images'), exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        # Get form data
        roll = request.form.get('roll')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        institute = request.form.get('institute')
        stream = request.form.get('stream')
        year = request.form.get('year')
        email = request.form.get('email')
        phone = request.form.get('phone')
        
        # Handle selfie upload
        if 'selfie' in request.files:
            selfie = request.files['selfie']
            if selfie.filename != '':
                filename = secure_filename(f"{roll}_selfie.jpg")
                selfie.save(os.path.join(app.config['UPLOAD_FOLDER'], 'images', filename))
        
        # Handle video upload
        if 'video' in request.files:
            video = request.files['video']
            if video.filename != '':
                video_filename = secure_filename(f"{roll}_video.webm")
                video.save(os.path.join(app.config['UPLOAD_FOLDER'], 'videos', video_filename))
        
        # Here you would typically save data to a database
        # For now, just return success
        return jsonify({'success': True, 'message': 'Form submitted successfully!'})
    
    return jsonify({'success': False, 'message': 'Something went wrong!'})

@app.route('/save-video', methods=['POST'])
def save_video():
    if 'video' in request.files:
        video = request.files['video']
        roll = request.form.get('roll', 'unknown')
        if video.filename != '':
            video_filename = secure_filename(f"{roll}_video.webm")
            video_path = os.path.join(app.config['UPLOAD_FOLDER'], 'videos', video_filename)
            video.save(video_path)
            return jsonify({'success': True, 'filename': video_filename})
    return jsonify({'success': False})

if __name__ == '__main__':
    app.run(debug=True)
