from flask import Flask, request, jsonify
# from flask_swagger_ui import get_swaggerui_blueprint
import detect_group_context as detect_group_context
import generic_context as generic_context
from dotenv import load_dotenv
import os
from werkzeug.utils import secure_filename
from config.default import Default

load_dotenv()
app = Flask(__name__)

# Directory where datasets are stored
UPLOAD_FOLDER = Default.UPLOAD_FOLDER
ALLOWED_EXTENSIONS = Default.ALLOWED_EXTENSIONS

@app.route('/api/chat', methods=['POST'])  # Adjust route and method
def chat_api():
    # Extract data from request (e.g., JSON, query parameters, form data)
    data = request.get_json()  # Assuming JSON data
    user_input = data['user_input']
    # Process data or interact with external services
    # ...
    # response = {'message': 'API processed data successfully!'}  # Example response
    response = detect_group_context.chat(user_input)
    # response['Question'] = user_input
    return jsonify(response)


@app.route('/api/chat/v4', methods=['POST'])  # Adjust route and method
def chat_api_v4():
    # Extract data from request (e.g., JSON, query parameters, form data)
    data = request.get_json()  # Assuming JSON data
    user_input = data['user_input']
    
    group_number = detect_group_context.detectQueryGroup(user_input)
    try:
        answer = detect_group_context.chat_with_answer(group_number, user_input)
    except:
        answer = generic_context.chat(user_input)
    
    response = {}
    if not isinstance(answer, str):
        response["Assistant"] = str(answer)  # Convert non-strings using str()
    else:
        response["Assistant"] = answer
    # response['Question'] = user_input
    
    # suggestedReplies
    suggestedReplies = detect_group_context.suggested_replies(group_number, user_input)
    response["suggestedReplies"] = suggestedReplies
    
    return jsonify(response)

@app.route('/api/upload-datasets', methods=['POST'])
def upload_datasets():
    """
    Uploads datasets provided in the request.

    Returns:
        JSON response containing either a success message if the upload was successful,
        or a list of errors if there were any issues with the uploaded files.
    """
    files = request.files.getlist('datasets')
    if not files:
        return jsonify({"errors": ["No file provided"]}), 400
    
    errors = []
    valid_files = {}
    for file in files:
        filename = secure_filename(file.filename)
        if '.' not in filename or filename.rsplit('.', 1)[1].lower() not in ALLOWED_EXTENSIONS:
            errors.append(f"{filename} is invalid or not supported.")
        else:
            valid_files[filename] = file    

    if errors:
        return jsonify({"errors": errors}), 400      

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    for valid_filename, valid_file in valid_files.items():
        valid_file.save(os.path.join(UPLOAD_FOLDER, valid_filename))
    
    return jsonify({"message": "Uploaded successfully!"}), 201

@app.route('/api/update-context', methods=['POST'])
def update_context():
    """
    Updates the context with the dataset's file name provided in the request.

    Returns:
        JSON response containing either a success message if the update was successful,
        or an error message if there were any issues.
    """
    body = request.get_json()
    if "filename" not in body or not body['filename']:
        return jsonify({"error": "Filename is required"}), 400

    filename = body['filename']
    new_dataset_path = os.path.join(UPLOAD_FOLDER, filename)

    if not os.path.exists(new_dataset_path):
        return jsonify({"error": "Dataset not found"}), 404
    
    os.environ['DATASET_PATH'] = new_dataset_path

    # Reload new dataset
    detect_group_context.set_file_path(new_dataset_path)
    generic_context.set_file_path(new_dataset_path)

    # Suggested replies: Default load 12 questions
    suggestedReplies = detect_group_context.suggested_replies_default()
    
    response = {}
    response["message"] = f"{filename} is set as current context"
    response["suggestedReplies"] = suggestedReplies
    
    return jsonify(response), 200

@app.route('/api/datasets', methods=['GET'])
def list_datasets():
    """
    Retrieves a list of filenames from the upload folder.
    If the folder is not found, returns an error message.
    """
    try:
        # Get all filenames in the upload folder
        filenames = [f for f in os.listdir(UPLOAD_FOLDER) if os.path.isfile(os.path.join(UPLOAD_FOLDER, f))]
        return jsonify({'datasets': filenames}), 200
    except FileNotFoundError:
    # Handle folder not found error
        return jsonify({'error': 'Dataset folder not found'}), 404
    
@app.route('/api/current-context', methods=['GET'])
def get_current_context():
    current_context_path = generic_context.get_file_path()
    
    return jsonify({"message": f"The current context is loaded from {current_context_path}"}), 200
 
@app.route('/api/retrieve-dataframe', methods=['POST'])
def retrive_dataframe():
    body = request.get_json()
    if 'table_name' not in body or not body['table_name']:
        return jsonify({"error": "table_name is required"}), 400
    
    table = body['table_name']
    df = generic_context.get_data_frame(table)
    
    return jsonify({"Dataset Content": f"{df.to_string()}"}), 200
  
  
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)  # Set debug=False for production
