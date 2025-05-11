from flask import Flask, render_template, request
import os
from utilities import generate_bode_plot

app = Flask(__name__)

# Define the path to save uploaded files
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/', methods=['GET', 'POST'])
def index():
    # Get the list of files in the upload folder
    uploaded_files = os.listdir(app.config['UPLOAD_FOLDER'])

    # Handle file upload
    if request.method == 'POST':
        # Handle file upload
        if 'bode_analysis' in request.files:
            file = request.files['bode_analysis']
            if file.filename != '':
                # Save the uploaded file
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(filepath)

                # Get the updated list of files after upload
                uploaded_files = os.listdir(app.config['UPLOAD_FOLDER'])

                return render_template('index.html', uploaded_files=uploaded_files, selected_file=None)

        # Handle file selection for plotting
        elif 'uploaded_files' in request.form:
            selected_file = request.form['uploaded_files']
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], selected_file)

            # Generate the plot for the selected file
            try:
                bode_html = generate_bode_plot(filepath)
            except Exception as e:
                return f"Error processing file: {str(e)}"

            # Return the plot with updated list of files
            return render_template('index.html', plot_html=bode_html, uploaded_files=uploaded_files, selected_file=selected_file)

        # Handle file deletion
        elif 'delete_file' in request.form:
            file_to_delete = request.form['delete_file']
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_to_delete)
            
            try:
                os.remove(file_path)  # Remove the file from the folder
                uploaded_files = os.listdir(app.config['UPLOAD_FOLDER'])  # Update file list
            except Exception as e:
                return f"Error deleting file: {str(e)}"

            # Return the updated list of files after deletion
            return render_template('index.html', uploaded_files=uploaded_files, selected_file=None)

    return render_template('index.html', uploaded_files=uploaded_files, selected_file=None)

if __name__ == '__main__':
    app.run(debug=True)
