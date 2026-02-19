from flask import Flask, render_template, request, redirect, url_for, flash
from utils.resume_parser import parse_resume
from utils.job_matcher import get_matching_jobs
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.secret_key = 'supersecretkey' # Required for flash messages
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    jobs = []
    debug_log = []
    if request.method == 'POST':
        print("POST request received")
        if 'resume' not in request.files:
            print("No resume file in request")
            flash('No file part', 'error')
            return redirect(request.url)
        file = request.files['resume']
        if file.filename == '':
            print("No filename selected")
            flash('No selected file', 'error')
            return redirect(request.url)
        
        if file:
            try:
                print(f"Uploading file: {file.filename}")
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(filepath)
                print(f"File saved to: {filepath}")
                
                # Parse resume
                resume_text = parse_resume(filepath)
                print(f"Resume text length: {len(resume_text)}")
                
                if not resume_text:
                    print("Failed to parse resume text")
                    flash('Could not extract text from resume. Ensure it is a valid PDF.', 'error')
                else:
                    flash('Resume uploaded and parsed successfully!', 'success')
                
                # Get matching jobs (mock for now)
                filters = {
                    'location': request.form.get('location'),
                    'experience': request.form.get('experience'),
                    'role': request.form.get('role')
                }
                print(f"Filters: {filters}")
                jobs, debug_log = get_matching_jobs(resume_text, filters)
                print(f"Found {len(jobs)} jobs")
                
                if not jobs and resume_text:
                    flash('No matching jobs found for your profile.', 'error')
                    for log in debug_log:
                        print(f"DEBUG: {log}") # Still print to console
                    
            except Exception as e:
                print(f"Error processing upload: {e}")
                flash(f'An error occurred: {str(e)}', 'error')
                debug_log = [str(e)]
            
    return render_template('index.html', jobs=jobs, debug_log=debug_log)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
