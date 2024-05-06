import numpy as np
import pandas as pd
from collections import defaultdict

TABLE_CONTEXT = {
    '1.4.0': {
        'Case creation': {
            'sheet_name': 'Header',
            'is_horizontal_table': True,
            'description': "This table stores basic information about the creation of a case, including the type of case, how it was uploaded, and a unique identifier.",
            'columns': ["Case Type", "Upload Type", "Case ID-Name"],
            'field_descriptions': {
                'Case Type': 'Type/kind of the uploaded template.',
                'Upload Type': 'Action should be taken on the uploaded file/template.'
            }
        },
        'Case references': {
            'sheet_name': 'Header',
            'is_horizontal_table': True,
            'description': "This table links the case to other relevant entities such as accounting arrangements, agreements, opportunities, and offers.",
            'columns': ["Accounting Arrangement (AA)", "Agreement", "Opportunity", "Offer"],
            'field_descriptions': {}
        },
        'Business partner details': {
            'sheet_name': 'Header',
            'is_horizontal_table': True,
            'description': "This table identifies the involved parties, including legal entities and the end customer, along with their respective countries. Use this table to answer the question related to customer name, end customer.",
            'columns': ["FinCorp Legal Entity", "Account Legal Entity", "End Customer", "Country"],
            'field_descriptions': {
                'End Customer': 'Customer name.'
            }
        },
        'Other case details': {
            'sheet_name': 'Header',
            'is_horizontal_table': True,
            'description': "This table provides additional information about the agreement associated with the case, such as dates, type, status, sales mode, lead business group/unit, tax category, and split mode.",
            'columns': ["Agreement Start / End Dates", "Agreement Type", "Agreement Status", "Sales Mode", "Lead BG/BU", "Tax Category", "Split Mode"],
            'field_descriptions': {}
        },
        'Phases': {
            'sheet_name': 'Contextual data',
            'is_horizontal_table': False,
            'description': "This table outlines the different phases of the project, including their IDs, names, start and end dates, and price per year.",
            'columns': ["Phase ID", "Phase Name", "Phase Start Date", "Phase End Date", "Price Year"],
            'field_descriptions': {
                'Phase ID': 'ID of phase. It is unique. Ex: Phase 1, Phase 2...'
            }
        },
        'Location management': {
            'sheet_name': 'Contextual data',
            'is_horizontal_table': False,
            'description': "This table describes the customer's location in a hierarchical structure, specifying levels, names, and parent levels. Use this table to answer the question related to customer location, customer country.",
            'columns': ["Level", "Level Name", "Location Name", "Parent level"],
            'field_descriptions': {
                'Location Name': 'Location of customer.'
            }
        },
        'Offering tags': {
            'sheet_name': 'Contextual data',
            'is_horizontal_table': False,
            'description': "This table lists tags associated with the offering, including their names, values, visibility to the customer, and assignment rules.",
            'columns': ["Tag Name", "Tag Value", "Visible to Customer", "Tag Assignment Rule"],
            'field_descriptions': {}
        },
        'Offering categories': {
            'sheet_name': 'Contextual data',
            'is_horizontal_table': False,
            'description': "This table categorizes the offering in a hierarchical structure with levels, names, and parent levels.",
            'columns': ["Level", "Name", "Parent level"],
            'field_descriptions': {}
        },
        'Incoterms': {
            'sheet_name': 'Contextual data',
            'is_horizontal_table': False,
            'description': "This table defines the international commercial terms used in the agreement, including their codes, descriptions, applicability to hardware, software, and services, delivery location, and local/foreign status.",
            'columns': ["Incoterm", "Incoterm (short)", "HW", "SW", "Services", "Delivered Place", "Local/Foreign"],
            'field_descriptions': {}
        },
        'Currencies': {
            'sheet_name': 'Contextual data',
            'is_horizontal_table': False,
            'description': "This table lists the involved currencies, their exchange rates to Euro, and their local/foreign status.",
            'columns': ["Currency", "Exchange rate to", "EUR"],
            'field_descriptions': {
                "Currency": "Name of the currency. Ex: EUR, USD,...",
                "Exchange rate to": "Unit of current  will be exchanged. Ex: 1 USD =, 1 EUR =...",
                "EUR": "Actual exchange rate. Ex: 1, 0.85..."
            }
        },
        'BoQ': {
            'sheet_name': 'BoQ',
            'is_horizontal_table': False,
            'description': "This table provides a detailed list of products/services, including element type, parent-child relationships, references, descriptions, attributes, pricing details, classifications, ordering conditions, and delivery information.",
            'columns': [
                'Element Type',
                'Parent',
                'External Reference',
                'Description',
                'CPB Additional Attributes',
                'Local/Foreign',
                'Pricing Type',
                'Duration',
                'Pricing Model',
                'Pricing Metric',
                'Pricing Metric Factor',
                'Classification L1',
                'Classification L2',
                'Ordering Conditions',
                'Order Preparation Attributes',
                'Finalized Conf',
                'CPB Tags / Categories Attributes',
                'Category L1',
                'Category L2',
                'Course type',
                'Course Level',
                'Delivery Type',
                'Curriculum Title',
                'Column7',
                'Column8',
                'Column9',
                'Column10',
                'SI Attributes',
                'Product - Service (ID)',
                'Product - Service (Description)',
                'Model (ID)',
                'Model (Description)',
                'Release (ID)',
                'Release (Description)',
                'WHAT (ID)',
                'WHAT (Description)',
                'PCI (ID)',
                'PCI (Description)',
                'Configured Profit Center (ID)',
                'Configured Profit Center (Description)',
                'Config ID',
                'Cost Phase 1',
                'Cost Phase 2',
                'Cost Phase 3',
                'Cost Phase 4',
                'Cost Phase 5',
                'Cost Phase 6',
                'Cost Phase 7',
                'Cost Phase 8',
                'Cost Phase 9',
                'Cost Phase 10',
                'Cost Phase 11',
                'Cost Phase 12',
                'Cost Phase 13',
                'Cost Phase 14',
                'Cost Phase 15',
                'CLP Phase 1',
                'CLP Phase 2',
                'CLP Phase 3',
                'CLP Phase 4',
                'CLP Phase 5',
                'CLP Phase 6',
                'CLP Phase 7',
                'CLP Phase 8',
                'CLP Phase 9',
                'CLP Phase 10',
                'CLP Phase 11',
                'CLP Phase 12',
                'CLP Phase 13',
                'CLP Phase 14',
                'CLP Phase 15',
                'CNP Phase 1',
                'CNP Phase 2',
                'CNP Phase 3',
                'CNP Phase 4',
                'CNP Phase 5',
                'CNP Phase 6',
                'CNP Phase 7',
                'CNP Phase 8',
                'CNP Phase 9',
                'CNP Phase 10',
                'CNP Phase 11',
                'CNP Phase 12',
                'CNP Phase 13',
                'CNP Phase 14',
                'CNP Phase 15',
                'Reference Quantities',
                'Quantities_1',
                'Quantities_2',
                'Quantities_3',
                'Quantities_4',
                'Quantities_5',
                'Quantities_6',
            ],
            'field_descriptions': {}
        },
        'Contextual Attributes': {
            'sheet_name': 'BoQ',
            'is_horizontal_table': True,
            'description': "This table specifies additional attributes relevant to the deployment, configuration, and quantities of products/services across different phases.",
            'columns': ["Deployment Type", "Configuration Type", "Country", "OC L1", "OC L2", "Quantity Phase 1", "Quantity Phase 2", "Quantity Phase 3", "Quantity Phase 4", 
                        "Quantity Phase 5", "Quantity Phase 6", "External Reference (T2)", "Description (T2)", "Configuration CLP"],
            'field_descriptions': {}
        },
        'Pricing schemes': {
            'sheet_name': 'Pricing Schemes',
            'is_horizontal_table': False,
            'description': "This table defines the pricing schemes applied to the case, including their names, types, application scope, rationale, calculation methods, factors, values, and conditions.",
            'columns': [
                'Pricing Scheme Name', 
                'Pricing Scheme Type', 
                'Pricing Waterfall Group',
                'Application Scope (Type)',
                'Application Scope (Value)',
                'Phases', 
                'Business Rationale',
                'Method of Calculation', 
                'Factor',
                'Value',
                'Expiration Date',
                'Other Condition',
                'X Value',
                'Y Value',
                'Only Applicable to this Contract'
            ],
            'field_descriptions': {}
        },
        'NSE attached scope': {
            'sheet_name': 'NSE scope',
            'is_horizontal_table': False,
            'description': "This table describes the scope of any attached non-standard services, including their references, descriptions, and application scope.",
            'columns': ['NSE Reference', 'NSE Description', 'Application Scope (Type)', 'Application Scope (Value)'],
            'field_descriptions': {}
        },
        'Missing SI Information': {
            'sheet_name': 'Missing SI info',
            'is_horizontal_table': False,
            'description': "This table identifies any missing information related to standard services, such as their codes, names, types, design types, classifications, and prices.",
            'columns': ['SI Code', 'SI Name', 'SI Type', 'Design Type', 'Classification L3', 'Profit Center', 'IRP (base) (EUR)'], 
            'field_descriptions': {}
        },
        'Payment terms': {
            'sheet_name': 'Payment Terms',
            'is_horizontal_table': False,
            'description': "This table specifies the payment terms for the case, including application scope, due dates, and associated standard services.",
            'columns': ['Application Scope (Type)', 'Application Scope (Value)', 'Days', 'Due From'],
            'field_descriptions': {}
        },
        'Billing plan - event': {
            'sheet_name': 'Billing Plan',
            'is_horizontal_table': False,
            'description': "This table outlines event-based billing milestones with their clauses, types, and values.",
            'columns': ["Billing Plan ID", "Application Scope (Type)", "Application Scope (Value)", "Billing Milestone Clause", "Type", "Value"],
            'field_descriptions': {}
        },
        'Billing plan - recurrent': {
            'sheet_name': 'Billing Plan',
            'is_horizontal_table': False,
            'description': "This table defines recurring billing milestones with their clauses, frequencies, options, and start/end dates.",
            'columns': ["Billing Plan ID", "Application Scope (Type)", "Application Scope (Value)", "Billing Milestone Clause", "Invoicing Frequency (in months)", "Invoicing Option", "Start Date", "End Date"],
            'field_descriptions': {}
        },
        'Product related terms': {
            'sheet_name': 'Operational T&Cs',
            'is_horizontal_table': False,
            'description': "This table specifies product-related terms like warranty periods and lead times with/without forecast, including their application scope.",
            'columns': ['Application Scope (Type)', 'Application Scope (Value)', 'Warranty Period', 'Lead time with forecast', 'Lead time without forecast'],
            'field_descriptions': {}
        }
    },
    '1.4.3': {
        'Case creation': {
            'sheet_name': 'Header',
            'is_horizontal_table': True,
            'description': "This table stores basic information about the creation of a case, including the type of case, how it was uploaded, and a unique identifier.",
            'columns': ["Case Type", "Upload Type", "Case ID-Name"],
            'field_descriptions': {
                'Case Type': 'Type/kind of the uploaded template.',
                'Upload Type': 'Action should be taken on the uploaded file/template.'
            }
        },
        'Case references': {
            'sheet_name': 'Header',
            'is_horizontal_table': True,
            'description': "This table links the case to other relevant entities such as accounting arrangements, agreements, opportunities, and offers.",
            'columns': ["Accounting Arrangement (AA)", "Agreement", "Opportunity", "Offer"],
            'field_descriptions': {}
        },
        'Business partner details': {
            'sheet_name': 'Header',
            'is_horizontal_table': True,
            'description': "This table identifies the involved parties, including legal entities and the end customer, along with their respective countries. Use this table to answer the question related to customer name, end customer.",
            'columns': ["Nokia Legal Entity", "Account Legal Entity", "End Customer", "Country"],
            'field_descriptions': {
                'End Customer': 'Customer name.'
            }
        },
        'Other case details': {
            'sheet_name': 'Header',
            'is_horizontal_table': True,
            'description': "This table provides additional information about the agreement associated with the case, such as dates, type, status, sales mode, lead business group/unit, tax category, and split mode.",
            'columns': ["Agreement Start / End Dates", "Agreement Type", "Agreement Status", "Sales Mode", "Lead BG/BU", "Tax Category", "Split Mode"],
            'field_descriptions': {}
        },
        'Phases': {
            'sheet_name': 'Contextual data',
            'is_horizontal_table': False,
            'description': "This table outlines the different phases of the project, including their IDs, names, start and end dates, and price per year.",
            'columns': ["Phase ID", "Phase Name", "Phase Start Date", "Phase End Date", "Price Year"],
            'field_descriptions': {
                'Phase ID': 'ID of phase. It is unique. Ex: Phase 1, Phase 2...'
            }
        },
        'Location management': {
            'sheet_name': 'Contextual data',
            'is_horizontal_table': False,
            'description': "This table describes the customer's location in a hierarchical structure, specifying levels, names, and parent levels. Use this table to answer the question related to customer location, customer country.",
            'columns': ["Level", "Level Name", "Location Name", "Parent Location Name"],
            'field_descriptions': {
                'Location Name': 'Location of customer.'
            }
        },
        'Offering tags': {
            'sheet_name': 'Contextual data',
            'is_horizontal_table': False,
            'description': "This table lists tags associated with the offering, including their names, values, visibility to the customer, and assignment rules.",
            'columns': ["Tag Name", "Tag Value", "Visible to Customer", "Tag Assignment Rule"],
            'field_descriptions': {}
        },
        'Offering categories': {
            'sheet_name': 'Contextual data',
            'is_horizontal_table': False,
            'description': "This table categorizes the offering in a hierarchical structure with levels, names, and parent levels.",
            'columns': ["Level", "Name", "Parent Name"],
            'field_descriptions': {}
        },
        'Incoterms': {
            'sheet_name': 'Contextual data',
            'is_horizontal_table': False,
            'description': "This table defines the international commercial terms used in the agreement, including their codes, descriptions, applicability to hardware, software, and services, delivery location, and local/foreign status.",
            'columns': ["Incoterm", "Incoterm (short)", "HW", "SW", "Services", "Delivered Place", "Local/Foreign"],
            'field_descriptions': {}
        },
        'Currencies': {
            'sheet_name': 'Contextual data',
            'is_horizontal_table': False,
            'description': "This table lists the involved currencies, their exchange rates to Euro, and their local/foreign status.",
            'columns': ["Currency", "Exchange rate to", "EUR", "Local/Foreign"],
            'field_descriptions': {
                "Currency": "Name of the currency. Ex: EUR, USD,...",
                "Exchange rate to": "Unit of current  will be exchanged. Ex: 1 USD =, 1 EUR =...",
                "EUR": "Actual exchange rate. Ex: 1, 0.85..."
            }
        },
        'BoQ': {
            'sheet_name': 'BoQ',
            'is_horizontal_table': False,
            'description': "This table provides a detailed list of products/services, including element type, parent-child relationships, references, descriptions, attributes, pricing details, classifications, ordering conditions, and delivery information.",
            'columns': [
                'Element Type',
                'Parent',
                'External Reference',
                'Description',
                'CFE Additional Attributes',
                'Local/Foreign',
                'Pricing Type',
                'Duration',
                'Pricing Model',
                'Pricing Metric',
                'Pricing Metric Factor',
                'Classification L1',
                'Classification L2',
                'Ordering Conditions',
                'Order Preparation Attributes',
                'Finalized Conf',
                'CFE Tags / Categories Attributes',
                'Billing',
                'Billing-2',
                'Country',
                'Column4',
                'Country2',
                'Column6',
                'Column7',
                'Column8',
                'Column9',
                'Column10',
                'SI Attributes',
                'Product - Service (ID)',
                'Product - Service (Description)',
                'Model (ID)',
                'Model (Description)',
                'Release (ID)',
                'Release (Description)',
                'WHAT (ID)', 'WHAT (Description)',
                'PCI (ID)',
                'PCI (Description)',
                'Configured Profit Center (ID)',
                'Configured Profit Center (Description)',
                'Config ID',
                'Cost Phase 1',
                'Cost Phase 2',
                'Cost Phase 3',
                'Cost Phase 4',
                'Cost Phase 5',
                'Cost Phase 6',
                'Cost Phase 7',
                'Cost Phase 8',
                'Cost Phase 9',
                'Cost Phase 10',
                'Cost Phase 11',
                'Cost Phase 12',
                'Cost Phase 13',
                'Cost Phase 14',
                'Cost Phase 15',
                'CLP Phase 1',
                'CLP Phase 2',
                'CLP Phase 3',
                'CLP Phase 4',
                'CLP Phase 5',
                'CLP Phase 6',
                'CLP Phase 7',
                'CLP Phase 8',
                'CLP Phase 9',
                'CLP Phase 10',
                'CLP Phase 11',
                'CLP Phase 12',
                'CLP Phase 13',
                'CLP Phase 14',
                'CLP Phase 15',
                'CNP Phase 1',
                'CNP Phase 2',
                'CNP Phase 3',
                'CNP Phase 4',
                'CNP Phase 5',
                'CNP Phase 6',
                'CNP Phase 7',
                'CNP Phase 8',
                'CNP Phase 9',
                'CNP Phase 10',
                'CNP Phase 11',
                'CNP Phase 12',
                'CNP Phase 13',
                'CNP Phase 14',
                'CNP Phase 15',
                'Reference Quantities',
                'Quantities_1',
                'Quantities_2',
                'Quantities_3',
                'Quantities_4',
                'Quantities_5',
                'Quantities_6',
                'Quantities_7',
                'Quantities_8',
                'Quantities_9',
                'Quantities_10'
            ],
            'field_descriptions': {
                'External Reference': 'This field contains the product code',
                'Element Type': 'This field has values: CFE T1 (Customer Facing Element Type 1), CFE T2 (Customer Facing Element Type 2), SI AC, NSE (Non Sold Element), etc. CFE T1 is also known as T1 or type 1. CFE T2 is also known as T2 or type 2.'
            }
        },
        'Contextual Attributes': {
            'sheet_name': 'BoQ',
            'is_horizontal_table': True,
            'description': "This table specifies additional attributes relevant to the deployment, configuration, and quantities of products/services across different phases.",
            'columns': [
                "Deployment Type", "Country", "External Reference (T2)", "Description (T2)", "Configuration CLP",
                "Quantity Phase 1", "Quantity Phase 2", "Quantity Phase 3", "Quantity Phase 4", "Quantity Phase 5",
                "Quantity Phase 6", "Quantity Phase 7", "Quantity Phase 8", "Quantity Phase 9", "Quantity Phase 10",
                "Quantity Phase 11", "Quantity Phase 12", "Quantity Phase 13", "Quantity Phase 14", "Quantity Phase 15"
            ],
            'field_descriptions': {}
        },
        'Pricing schemes': {
            'sheet_name': 'Pricing Schemes',
            'is_horizontal_table': False,
            'description': "This table defines the pricing schemes applied to the case, including their names, types, application scope, rationale, calculation methods, factors, values, and conditions.",
            'columns': [
                'Pricing Scheme Name',
                'Pricing Scheme Type',
                'Pricing Waterfall Group',
                'Application Scope (Type)',
                'Application Scope (Value)',
                'Phases',
                'Business Rationale',
                'Method of Calculation',
                'Factor',
                'Value',
                'Expiration Date',
                'Other Condition',
                'X Value',
                'Y Value',
                'Only Applicable to this Contract'
            ],
            'field_descriptions': {}
        },
        'NSE attached scope': {
            'sheet_name': 'NSE scope',
            'is_horizontal_table': False,
            'description': "This table contains data of the NSE (Non Sold Element) product/service including their references, descriptions, and application scope.",
            'columns': ['NSE Reference', 'NSE Description', 'Application Scope (Type)', 'Application Scope (Value)'],
            'field_descriptions': {
                'NSE Reference': 'This field contains the product code (also know as `External Refercene` in `BoQ`) of NSE product from `BoQ` sheet.',
                'NSE Description': 'This field contains the product description (also know as `Description` in `BoQ`) of NSE product from `BoQ` sheet.',
                'Application Scope (Type)': 'This field contains the application scope type of NSE product from `BoQ` sheet.',
                'Application Scope (Type)': 'This field contains the application scope value of NSE product from `BoQ` sheet.'
            }
        },
        'Missing SI Information': {
            'sheet_name': 'Missing SI info',
            'is_horizontal_table': False,
            'description': "This table identifies any missing information related to standard services, such as their codes, names, types, design types, classifications, and prices.",
            'columns': ['SI Code', 'SI Name', 'SI Type', 'Design Type', 'Classification L3', 'Profit Center', 'IRP (base) (EUR)'],
            'field_descriptions': {}
        },
        'Payment terms': {
            'sheet_name': 'Payment Terms',
            'is_horizontal_table': False,
            'description': "This table specifies the payment terms for the case, including application scope, due dates, and associated standard services.",
            'columns': ['Application Scope (Type)', 'Application Scope (Value)', 'Days', 'Due From'],
            'field_descriptions': {}
        },
        'Billing plan - event': {
            'sheet_name': 'Billing Plan',
            'is_horizontal_table': False,
            'description': "This table outlines event-based billing milestones with their clauses, types, and values.",
            'columns': ["Billing Plan ID", "Application Scope (Type)", "Application Scope (Value)", "Billing Milestone Clause", "Type", "Value"],
            'field_descriptions': {}
        },
        'Billing plan - recurrent': {
            'sheet_name': 'Billing Plan',
            'is_horizontal_table': False,
            'description': "This table defines recurring billing milestones with their clauses, frequencies, options, and start/end dates.",
            'columns': ["Billing Plan ID", "Application Scope (Type)", "Application Scope (Value)", "Billing Milestone Clause", "Invoicing Frequency", "Invoicing Option", "Start Date", "End Date"],
            'field_descriptions': {}
        },
        'Product related terms': {
            'sheet_name': 'Operational T&Cs',
            'is_horizontal_table': False,
            'description': "This table specifies product-related terms like warranty periods and lead times with/without forecast, including their application scope.",
            'columns': ['Application Scope (Type)', 'Application Scope (Value)', 'Warranty Period', 'Lead time with forecast', 'Lead time without forecast'],
            'field_descriptions': {}
        }
    }
}


class DataFrameManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.dataframes = {}
        self.init()

    def init(self):
        self.header_sheet_name = "Header"
        self.contextual_data_sheet_name = "Contextual data"
        self.boq_sheet_name = "BoQ"
        self.billing_plan_sheet_name = "Billing Plan"
        self.operational_tcs_sheet_name = "Operational T&Cs"
        self.pricing_schemes_sheet_name = 'Pricing Schemes'
        self.payment_terms_sheet_name = 'Payment Terms'
        self.missing_si_information_sheet_name = 'Missing SI info'
        self.nse_scope_sheet_name = 'NSE scope'
        self.version = self.get_current_version()
        self.table_context = TABLE_CONTEXT[self.version]
        
    def get_dataframe(self, table_name):
        if table_name not in self.dataframes:
            # Read excel only when dataframe is requested for the first time
            # df = pd.read_excel(self.file_path, sheet_name=table_name)
            df = self.extract_df(table_name)
            self.dataframes[table_name] = df
        return self.dataframes[table_name]
    
    def reload_dataframe(self):
        self.dataframes = {}

    def get_current_version(self):
        df = pd.read_excel(self.file_path, sheet_name='Header', header=None)
        filtered_df = df[df[0] == 'File Version']
        return filtered_df.iloc[0, 1]

    def get_sub_df(self, table_name):
        print(f"Version: {self.version}")
        headers = self.table_context[table_name]['columns']
        is_horizontal_table = self.table_context[table_name]['is_horizontal_table']
        sheet_name = self.table_context[table_name]['sheet_name']
        columns = []
        index = None
        indexes = []
        
        sub_df = pd.read_excel(self.file_path, sheet_name=sheet_name)
        sub_df = sub_df.reset_index(drop=True)

        # Strip White Space
        sub_df = sub_df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

        # Swap rows and columns
        if is_horizontal_table:
            for header in headers:
                row, col = np.where(sub_df == header)
                indexes.append(row[0])

            sub_df = sub_df.loc[indexes]
            sub_df = sub_df.transpose().reset_index(drop=True)
        
        sub_df.columns = [i for i in range(len(sub_df.columns))]

        # Find index and columns    
        row_cols = defaultdict(list)
        for header in headers:
            rows, cols = np.where(sub_df == header)
        
            for row, col in zip(rows, cols):
                row_cols[row].append(col)
        
        for row, cols in row_cols.items():
            if len(cols) >= len(headers):
                index = row
                columns = cols
                break       
                
        columns.sort()
        header_cols = []
        for j in range(len(columns)):
            if j == 0:
                if columns[j + 1] - columns[j] == 1:
                    header_cols.append(columns[j])
            elif j == len(columns) - 1:
                if columns[j] - columns[j - 1] == 1:
                    header_cols.append(columns[j])
            elif columns[j + 1] - columns[j] == 1 or columns[j] - columns[j - 1] == 1:
                header_cols.append(columns[j])            
        
        # Split sub df
        filtered_df = sub_df.query('index > @index')[header_cols]
        filtered_df.columns = headers

        # Drop NaN
        data_frame = filtered_df.dropna(axis=0, how='all')

        # Reset index.
        data_frame = data_frame.reset_index(drop=True)

        # Replace NaN in numeric columns with 0
        numeric_cols = data_frame.select_dtypes(include=np.number).columns
        data_frame[numeric_cols] = data_frame[numeric_cols].fillna(0)

        # Replace NaN in string columns with '-'
        string_cols = data_frame.select_dtypes(include='object').columns
        data_frame[string_cols] = data_frame[string_cols].fillna('-')

        return data_frame
    
    def case_creation_df(self):
        return self.get_sub_df('Case creation')
    def case_references_df(self):
        return self.get_sub_df('Case references')
    def business_partner_details_df(self):
        return self.get_sub_df('Business partner details')
    def other_case_details_df(self):
        return self.get_sub_df('Other case details')

    def phases_df(self):
        return self.get_sub_df('Phases')
    def location_management_df(self):
        return self.get_sub_df('Location management')
    def offering_tags_df(self):
        return self.get_sub_df('Offering tags')
    def offering_categories_df(self):
        return self.get_sub_df('Offering categories')
    def incoterms_df(self):
        return self.get_sub_df('Incoterms')
    def currencies_df(self):
        return self.get_sub_df('Currencies')

    def contextual_attributes_df(self):
        return self.get_sub_df('Contextual Attributes')
        
    def pricing_schemes_df(self):
        return self.get_sub_df('Pricing schemes')
    
    def nse_attached_scope_df(self):
        return self.get_sub_df('NSE attached scope')
    
    def missing_si_information_df(self):
        return self.get_sub_df('Missing SI Information')
    
    def payment_terms_df(self):
        return self.get_sub_df('Payment terms')
    
    def billing_plan_event_df(self):
        return self.get_sub_df('Billing plan - event')
        
    def billing_plan_recurrent_df(self):
        return self.get_sub_df('Billing plan - recurrent')
    
    def product_related_terms_df(self):
        return self.get_sub_df('Product related terms')
    
    def boq_df(self):
        return self.get_sub_df('BoQ')
    
    def function_mapping(self):
        df_map = {
            "Case creation": self.case_creation_df,
            "Case references": self.case_references_df,
            "Business partner details": self.business_partner_details_df,
            "Other case details": self.other_case_details_df,
            "Phases": self.phases_df,
            "Location management": self.location_management_df,
            "Offering tags": self.offering_tags_df,
            "Offering categories": self.offering_categories_df,
            "Incoterms": self.incoterms_df,
            "Currencies": self.currencies_df,
            "BoQ": self.boq_df,
            "Contextual Attributes": self.contextual_attributes_df,
            "Pricing schemes": self.pricing_schemes_df,
            "NSE attached scope": self.nse_attached_scope_df,
            "Missing SI Information": self.missing_si_information_df,
            "Payment terms": self.payment_terms_df,
            "Billing plan - event": self.billing_plan_event_df,
            "Billing plan - recurrent": self.billing_plan_recurrent_df,
            "Product related terms": self.product_related_terms_df,
        }
        return df_map
        
    def extract_df(self, table_name):
        result = None
        # Check the user input and call the associated function
        function_mapping = self.function_mapping()
        if table_name in function_mapping:
            function = function_mapping[table_name]
            result = function()
        else:
            # Default extraction for regular tables
            result = pd.read_excel(self.file_path, sheet_name=table_name)
            # raise ValueError(f"Table '{table_name}' not found in Excel file '{self.file_path}'.")
        
        return result

        
        