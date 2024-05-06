import os
import pandas as pd
from pandasai import SmartDataframe
from pandasai import Agent
# Instantiate a LLM
from pandasai.llm import OpenAI
import json
import warnings
import detect_group_context as detect_group_context
from config.default import Default
from qworks_logger import logger
from df_manager import DataFrameManager
from dotenv import load_dotenv

load_dotenv()

# os.environ["OPENAI_API_KEY"] = ""
# os.environ["PANDASAI_API_KEY"] = ""
os.environ.pop("PANDASAI_API_KEY", None)

# Filter ignore warning log from openpyxl module
# E.g: UserWarning: Data Validation extension is not supported and will be removed
warnings.simplefilter('ignore', category=UserWarning)


### QWorks code
llm = OpenAI(
    temperature = 0,
    seed = 26
)
# Replace file path with with the actual path to your Excel file.
file_path = Default.DATASET_FILE_PATH
data_frame_manager = DataFrameManager(file_path)

CONFIG = {
    "llm": llm, 
    "enable_cache": False, 
    "enforce_privacy": True,
    "max_retries": 10
}

def client(text, role="assistant"):
    completion = llm.client.create(
            model="gpt-3.5-turbo", # gpt-3.5-turbo-instruct
            messages=[
                {"role": role, "content": text}
            ]
        )
    return completion.choices[0].message.content

def summarize(question, answer):
    context = f"Giving I have this question: {question} and this answer: '{str(answer)}'. Summarize the answer to make it match with the question in the human language and return the answer only."
    # print("Context: ", context)
    return client(context, role="user")
    # return agent.chat(context)
    
def handle_default(question):
    return "I'm sorry, I don't understand the question."
    
def handle_question_agent(question, dfs):
    result = None
    # Check the user input and call the associated function
    try:
        (sdfs, field_descriptions) = init_sdf_with_description(dfs)
        agent = Agent(sdfs, CONFIG)

        field_descriptions_context = ""
        for field, description in field_descriptions.items():
            field_descriptions_context = field_descriptions_context + f"`{field}`: {description}\n"

        prompt = """`dfs: list[pd.DataFrame]` is already declared. 
Don't redeclare or update the data of `dfs`. 
Based on provided `dfs` and field descriptions, generate code (using pandas {pandas_version}) to get the answer with actual `dfs`.
If result type is `string`, please convert `list`, `dict` to string.
If the question relates to listing all of the entries the `result` type should be `dataframe` and include all columns. 
Please use `datetime_as_string` of numpy to convert `numpy.datetime64` to string with format as US date time.
Please use `concat` instead of `merge` for dataframes.
Please don't convert the text/string to number/int.
Please ignore all hidden rows.

### Field Descriptions:
{field_descriptions_context}

### Question: {question}"""

        answer = agent.chat(prompt.format(question=question, field_descriptions_context=field_descriptions_context, pandas_version=pd.__version__))
        result = summarize(question, answer)
    except Exception as ex:
        logger.warn(f"Can not anwser question with agent: {str(ex)}")
        # Back to detect with group question 
        result = detect_group_context.chat_with_answer(question)
    
    return result

# TODO: get description mapping of dfs and init sdf
def init_sdf_with_description(dfs):
    sdfs = []
    field_descriptions = {}
    for table_name, df in dfs.items():

        logger.debug(f"### Table {table_name}:")
        logger.debug(df.head().to_string())
        logger.debug("###################")

        table_context = data_frame_manager.table_context[table_name]

        logger.debug(f"TABLE CONTEXT: \n {table_context}")

        sdf = SmartDataframe(df, name=table_name, description=table_context['description'], config=CONFIG) 
        sdfs.append(sdf)
        
        field_descriptions.update(table_context['field_descriptions']) 
        
    return sdfs, field_descriptions
    
def create_prompt(question):
    prompt = f"""
Context:
	Table 'Case creation' includes headers: 'Case Type', 'Upload Type', 'Case ID-Name'. This table stores basic information about the creation of a case, including the type/kind of the template, how it was uploaded, what action should be taken on this file, and a unique identifier.
	Table 'Case references' includes headers: 'Accounting Arrangement (AA)', 'Agreement', 'Opportunity', 'Offer'. This table links the case to other relevant entities such as accounting arrangements, agreements, opportunities, and offers.
	Table 'Business partner details' includes headers: 'FinCorp Legal Entity', 'Account Legal Entity', 'End Customer', 'Country'. This table identifies the involved parties, including legal entities and the end customer, along with their respective countries.
	Table 'Other case details' includes headers: 'Agreement Start / End Dates', 'Agreement Type', 'Agreement Status', 'Sales Mode', 'Lead BG/BU', 'Tax Category', 'Split Mode'. This table provides additional information about the agreement, such as dates, type, status, sales mode, lead business group/unit, tax category, and split mode.
	Table 'Phases' includes headers: 'Phase ID', 'Phase Name', 'Phase Start Date', 'Phase End Date', 'Price Year'. This table outlines the different phases of the project, including their IDs, names, start and end dates, and price per year.
	Table 'Location management' includes headers: 'Level', 'Level Name', 'Location Name', 'Parent level'. This table describes the customer's location in a hierarchical structure, specifying levels, names, and parent levels.
	Table 'Offering tags' includes headers: 'Tag Name', 'Tag Value', 'Visible to Customer', 'Tag Assignment Rule'. This table lists tags associated with the offering, including their names, values, visibility to the customer, and assignment rules.
	Table 'Offering categories' includes headers: 'Level', 'Name', 'Parent level'. This table categorizes the offering in a hierarchical structure with levels, names, and parent levels.
	Table 'Incoterms' includes headers: 'Incoterm', 'Incoterm (short)', 'HW', 'SW', 'Services', 'Delivered Place', 'Local/Foreign'. This table defines the international commercial terms used in the agreement, including their codes, descriptions, applicability to hardware, software, and services, delivery location, and local/foreign status.
	Table 'Currencies' includes headers: 'Currency', 'Exchange rate to', 'EUR', 'Local/Foreign'. This table lists the involved currencies, their exchange rates to Euro, and their local/foreign status.
	Table 'BoQ' (Bill of Quantities) includes headers: 'Element Type', 'Parent', 'Reference', 'External Reference', 'Description', 'CPB Additional Attributes', 'Local/Foreign', 'Pricing Type', 'Duration', 'Pricing Model', 'Pricing Metric', 'Pricing Metric Factor', 'Classification L1', 'Classification L2', 'Ordering Conditions', 'Order Preparation Attributes', 'Finalized Conf', 'CPB Tags / Categories Attributes', 'Category L1', 'Category L2', 'Course type', 'Course Level', 'Delivery Type', 'Curriculum Title'. This table provides a detailed list of products/services, including element type, parent-child relationships, references, descriptions, attributes, pricing details, classifications, ordering conditions, and delivery information. 
        The 'Element Type' field has values: CFE T1 (Customer Facing Element Type 1), CFE T2 (Customer Facing Element Type 2), SI AC, NSE (Non Sold Element), etc. CFE T1 is also known as T1 or type 1. CFE T2 is also known as T2 or type 2.
	Table 'Contextual Attributes' includes headers: 'Deployment Type', 'Configuration Type', 'Country', 'OC L1', 'OC L2', 'Quantity Phase 1', 'Quantity Phase 2', 'Quantity Phase 3', 'Quantity Phase 4', 'Quantity Phase 5', 'Quantity Phase 6', 'External Reference (T2)', 'Description (T2)', 'Configuration CLP'. This table specifies additional attributes relevant to the deployment, configuration, and quantities of products/services across different phases.
	Table 'Pricing schemes' includes headers: 'Pricing Scheme Name', 'Pricing Scheme Type', 'Pricing Waterfall Group', 'Application Scope (Type)', 'Application Scope (Value)', 'Phases', 'Business Rationale', 'Method of Calculation', 'Factor', 'Value', 'Expiration Date', 'Other Condition', 'X Value', 'Y Value', 'Only Applicable to this Contract'. This table defines the pricing schemes applied to the case, including their names, types, application scope, rationale, calculation methods, factors, values, and conditions.
	Table 'NSE attached scope' includes headers: 'NSE Reference', 'NSE Description', 'Application Scope (Type)', 'Application Scope (Value)'. This table contains data of the NSE (Non Sold Element) product/service including their references, descriptions, and application scope.
	Table 'Missing SI Information' includes headers: 'SI Code', 'SI Name', 'SI Type', 'Design Type', 'Classification L3', 'Profit Center', 'IRP (base) (EUR)'. This table identifies any missing information related to standard services, such as their codes, names, types, design types, classifications, and prices.
	Table 'Payment terms' includes headers: 'Application Scope (Type)', 'Application Scope (Value)', 'Days', 'Due From', 'SI Code'. This table specifies the payment terms for the case, including application scope, due dates, and associated standard services.
	Table 'Billing plan - event' includes headers: 'Billing Milestone Clause', 'Type', 'Value'. This table outlines event-based billing milestones with their clauses, types, and values.
	Table 'Billing plan - recurrent' includes headers: 'Billing Milestone Clause', 'Invoicing Frequency (in months)', 'Invoicing Option', 'Start Date', 'End Date'. This table defines recurring billing milestones with their clauses, frequencies, options, and start/end dates.
	Table 'Product related terms' includes headers: 'Application Scope (Type)', 'Application Scope (Value)', 'Warranty Period', 'Lead time with forecast', 'Lead time without forecast'. This table specifies product-related terms like warranty periods and lead times with/without forecast, including their application scope.

Tell me which tables containing answer for the question at the end.  

Just provide Answer with this JSON template including attributes "table_name", "confidence_score" (value in range 0 - 1).
Here is an example: 
    {{ "tables": [ {{ "table_name": "Case creation", "confidence_score": "0.9" }}, {{ "table_name": "Case references", "confidence_score": "0.8" }} ] }} 

If the question involves duplicate entries or comparing multiple sheets or the question is unclear, such as  `Are there any duplicates on any of the sheets?`, `Are all the contextual data used with the product boq?`, `What is this?`...please don't answer with any tables and answer should be an empty JSON like {{}}

Question: `{question}`"""

    response = None
    response = client(prompt)
    if response:
        logger.debug(f"Tables detected: {response}") 
        rs_json = json.loads(response)
        # Extract tables with confidence score > 0.5
        filtered_tables = []
        if "tables" not in rs_json:
            return filtered_tables
        
        for table in rs_json["tables"]:
            if float(table["confidence_score"]) > 0.5:
                filtered_tables.append(table["table_name"])
        
    return filtered_tables

def get_data_frame(table_name):
    return data_frame_manager.get_dataframe(table_name)

def get_data_frames(table_names):
    filtered_dfs = {}
    for table in table_names:
        df = get_data_frame(table)
        filtered_dfs[table] = df
    
    return filtered_dfs

def get_file_path():
    return data_frame_manager.file_path
    
def set_file_path(new_path):
    global file_path
    file_path = new_path
    global data_frame_manager
    data_frame_manager = DataFrameManager(new_path)
    
def chat(user_input, tables = []):
    logger.info(f"### QUERY")
    logger.info(f"Question: {user_input}")
    
    # TODO: Handle prompt change
    if not tables:
        tables = create_prompt(user_input)
    
    dfs = get_data_frames(tables)
    
    # Check if all DataFrames in the list are empty
    if not dfs or (all(df.empty for df in dfs.values())):
        # logger.info("### Call detect group context ####")
        # answer = detect_group_context.chat_with_answer(user_input)
        answer = "I'm sorry, I don't understand your question."
    else: 
        answer = handle_question_agent(user_input, dfs)
    
    logger.info(f"Answer: {answer}")
    
    return answer
