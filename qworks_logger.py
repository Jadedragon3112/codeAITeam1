import warnings
import logging

# Filter ignore warning log from openpyxl module
# E.g: UserWarning: Data Validation extension is not supported and will be removed
warnings.simplefilter('ignore', category=UserWarning)

### QWorks configure logging
logging.basicConfig(filename="qwork_app.log", filemode="a", level=logging.INFO)

# Create a logger for your application
logger = logging.getLogger(__name__)

# Create a file handler for the logger
file_handler = logging.FileHandler("qwork_app.log", mode="a")

# Set a formatter for the log messages
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(file_handler)

# Set the logging level for the logger
logger.setLevel(logging.DEBUG)
### End QWorks configure logging
