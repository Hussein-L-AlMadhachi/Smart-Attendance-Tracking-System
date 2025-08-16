# app.py
from flask import Flask, render_template, request, redirect, url_for
import os
import service.register
import service.monitor




# Configuration
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'known_faces'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.secret_key = 'super_secret_key'  # Needed for flashing messages

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}



def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/upload', methods=['GET', 'POST'])
def upload_face():
    if request.method == 'POST':
        # Get the name
        name = request.form.get('name', '').strip()
        if not name:
            return render_template('upload.jinja', message="Name is required.", msg_type="error")

        # Check if file is uploaded
        if 'photo' not in request.files:
            return render_template('upload.jinja', message="No file selected.", msg_type="error")

        file = request.files['photo']
        if file.filename == '':
            return render_template('upload.jinja', message="No file selected.", msg_type="error")

        if not allowed_file(file.filename):
            return render_template('upload.jinja', message="Invalid file type. Use JPG, PNG, etc.", msg_type="error")

        # Secure the filename and save as name.extension
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"{name}.{ext}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        try:
            file.save(filepath)
            message = f"✅ Successfully saved {name}'s face as {filename}!"
            msg_type = "success"
        except Exception as e:
            message = f"❌ Error saving file: {str(e)}"
            msg_type = "error"

        service.register.register_faces()

        return render_template('upload.jinja', message=message, msg_type=msg_type)

    return render_template('upload.jinja')



@app.route('/list')
def list_faces():
    faces = os.listdir(app.config['UPLOAD_FOLDER'])
    return f"<h2>Known Faces ({len(faces)}):</h2><pre>{'<br>'.join(faces)}</pre>"



@app.route('/')
def index():
    return render_template('index.jinja')



@app.route('/monitor')
def monitor():
    service.monitor.monitor_faces()
    return redirect( url_for("index") )



if __name__ == '__main__':
    print("🌍 Starting Flask app at http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)


