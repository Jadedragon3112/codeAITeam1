import os
from dotenv import load_dotenv
from flask import Flask

load_dotenv()
app = Flask(__name__)


class Default(object):
    DATASET_FILE_PATH = os.getenv('DATASET_PATH', '/home/azureuser/project_ai/dataset/data1_v2.xlsx')
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', './uploads/datasets')
    ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}