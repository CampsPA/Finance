

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, Column, String, Integer, DECIMAL,Numeric
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2 import sql
from decimal import Decimal



Base = declarative_base()



class Assumptions(Base):
    __tablename__ = 'assumptions'
    #metric_id = Column(Integer, primary_key=True)
    metrics = Column(String, primary_key=True)
    year_2 = Column(DECIMAL(10,2))
    year_1 = Column(DECIMAL(10,2))
    year0 = Column(DECIMAL(10,2))
    year1 = Column(DECIMAL(10,2))
    year2 = Column(DECIMAL(10,2))
    year3 = Column(DECIMAL(10,2))
    year4 = Column(DECIMAL(10,2))
    year5 = Column(DECIMAL(10,2))
    
db_params = {
    'dbname': 'postgres',
    'user': 'Campospa',
    'password': '2883',
    'host': 'localhost',
    'port': '5432'
}


#Connect to the default database to create a new database
conn = psycopg2.connect(**db_params)
conn.autocommit = True
cur = conn.cursor()

'''Comment tgis out once database and table shave been created '''
# Create a new database
new_db_name = 'Statements'
cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(new_db_name)))

# Close the connection to the default database
cur.close()
conn.close()

# Connect to the new database
db_params['dbname'] = new_db_name
conn = psycopg2.connect(**db_params)
cur = conn.cursor()



# Create table assumptions
cur.execute('''
            CREATE TABLE assumptions (
    metrics TEXT PRIMARY KEY,
    year_2 NUMERIC(10,2),
    year_1 NUMERIC(10,2),
    year0 NUMERIC(10,2),
    year1 NUMERIC(10,2),
    year2 NUMERIC(10,2),
    year3 NUMERIC(10,2),
    year4 NUMERIC(10,2),
    year5 NUMERIC(10,2)
);
            ''')



# Commit changes 
conn.commit()

# insert data
insert_query = '''
    INSERT INTO assumptions (metrics, year_2, year_1, year0, year1, year2, year3, year4, year5)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
'''

values = [
('Days in Period', 365, 365, 365, 365, 365, 365, 365, 365),
('Sales Growth', None, None, None, None, None, None, None, None),
('Gross Margin', None, None, None, None, None, None, None, None),
('Distribution Expense (Percent of Sales)', None, None, None, None, None, None, None, None),
('Marketing & Admin Expense (Fixed Cost)', None, None, None, None, None, None, None, None),
('Research Expense (Percent of Sales)', None, None, None, None, None, None, None, None),
('Depreciation (Percent of Sales)', None, None, None, None, None, None, None, None),
('Long-Term Debt Interest Rate (Average Debt)', None, None, None, None, None, None, None, None),
('Tax Rate (Percent of EBT)', None, None, None, None, None, None, None, None),
('Capital Asset Turnover Ratio                           (x)', None, None, None, None, None, None, None, None),
('Receivable Days (Sales Basis)                     (Days)', None, None, None, None, None, None, None, None),
('Inventory Days (COGS Basis)                       (Days)', None, None, None, None, None, None, None, None),
('Payable Days (COGS Basis)                          (Days)', None, None, None, None, None, None, None, None),
('Income Tax Payable (Percent of Taxes) (Days)', None, None, None, None, None, None, None, None),
('Long Term Debt', None, None, None, None, None, None, None, None),
('Common Share Capital', None, None, None, None, None, None, None, None),
('Dividend Payout Ratio ', None, None, None, None, None, None, None, None)
]


cur.executemany(insert_query, values)

#Commit changes and close the connection
conn.commit()
cur.close()
conn.close()
    


# Create a class to fetch data and perform analysis

class Analysis:
    def __init__(self, data_path):
        self.data_path = data_path
        self.income_statement = pd.DataFrame()
        self.balance_sheet = pd.DataFrame()
        self.cash_flow = pd.DataFrame()
        self.assumptions = pd.DataFrame()
        self.years =  ['Year1', 'Year2', 'Year3', 'Year4', 'Year5']
        # add additional sheets
        self.working_capital = pd.DataFrame()
        self.capital_structure = pd.DataFrame()
        #self.engine = create_engine('sqlite:///test.db')
        self.engine = create_engine('postgresql://Campospa:2883@localhost/Statements')
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        

    def get_statements_data(self):
        self.data =  "C:/Users/campo/OneDrive/Desktop/Statements2.xlsx"

        
    def statements(self):
        self.assumptions = pd.read_excel(self.data, sheet_name = 'Assumptions', index_col= 'Metrics',dtype={'Year_2': float, 'Year_1': float,'Year0': float, 'Year1': float, 'Year2': float, 'Year3': float, 'Year4': float, 'Year5': float})
        self.income_statement = pd.read_excel(self.data, sheet_name='Income Statement', index_col='Income Statement',dtype={'Year_2': float, 'Year_1': float,'Year0': float, 'Year1': float, 'Year2': float, 'Year3': float, 'Year4': float, 'Year5': float})
        self.balance_sheet = pd.read_excel(self.data, sheet_name='Balance Sheet', index_col='Balance Sheet',dtype={'Year_2': float, 'Year_1': float,'Year0': float, 'Year1': float, 'Year2': float, 'Year3': float, 'Year4': float, 'Year5': float})
        self.cash_flow =  pd.read_excel(self.data, sheet_name='Cash Flows', index_col='Cash Flows',dtype={'Year_2': float, 'Year_1': float,'Year0': float, 'Year1': float, 'Year2': float, 'Year3': float, 'Year4': float, 'Year5': float})
        #self.assumptions = self.assumptions.astype(str)
        self.working_capital = pd.read_excel(self.data, sheet_name = 'Working Capital', index_col= 'Working Capital')
        self.capital_structure = pd.read_excel(self.data, sheet_name = 'Capital Structure', index_col= 'Capital Structure')

    



    def populate_assumptions_historical(self):
        #Helper method to format values
        def format_decimals(value):
            return round(Decimal(value) * 100, 2)
        
        def format_fixed_cost(value):
            try:
                return "{:.2f}".format(Decimal(value))  # Format as a fixed cost with three decimal places
            except ValueError:
                return "N/A"  # Handle cases where the value cannot be converted to Decimal
            
        
        # Sales Growth
        
        self.sg_year_1 = format_decimals(self.income_statement.at['Revenues', 'Year_1'] / self.income_statement.at['Revenues', 'Year_2'] - 1)
        self.sg_year_0 = format_decimals(self.income_statement.at['Revenues', 'Year0'] / self.income_statement.at['Revenues', 'Year_1'] - 1)

        # Gross Margin
        self.gm_year_2 = format_decimals(self.income_statement.at['Gross Profit', 'Year_2'] / self.income_statement.at['Revenues', 'Year_2'])
        self.gm_year_1 = format_decimals(self.income_statement.at['Gross Profit', 'Year_1'] / self.income_statement.at['Revenues', 'Year_1'])
        self.gm_year_0 = format_decimals(self.income_statement.at['Gross Profit', 'Year0'] / self.income_statement.at['Revenues', 'Year0'])

        # Distribution Expense (Percent of Sales)
        self.dist_exp_2 = format_decimals(self.income_statement.at['Distribution Expenses', 'Year_2'] / self.income_statement.at['Revenues', 'Year_2'] * -1)
        self.dist_exp_1 = format_decimals(self.income_statement.at['Distribution Expenses', 'Year_1'] / self.income_statement.at['Revenues', 'Year_1'] * -1)
        self.dist_exp_0 = format_decimals(self.income_statement.at['Distribution Expenses', 'Year0'] / self.income_statement.at['Revenues', 'Year0'] * -1)

        # Marketing & Admin Expense (Fixed Cost)
        self.mkt_admin_2 = format_fixed_cost(self.income_statement.at['Marketing and Administration', 'Year_2'] * -1)
        self.mkt_admin_1 = format_fixed_cost(self.income_statement.at['Marketing and Administration', 'Year_1'] * -1)
        self.mkt_admin_0 = format_fixed_cost(self.income_statement.at['Marketing and Administration', 'Year0'] * -1)

        # Research Expense (Percent of Sales)
        self.res_exp_2 = format_decimals(self.income_statement.at['Research and Development', 'Year_2'] / self.income_statement.at['Revenues', 'Year_2'] * -1)
        self.res_exp_1 = format_decimals(self.income_statement.at['Research and Development', 'Year_1'] / self.income_statement.at['Revenues', 'Year_1'] * -1)
        self.res_exp_0 = format_decimals(self.income_statement.at['Research and Development', 'Year0'] / self.income_statement.at['Revenues', 'Year0'] * -1)

        # Depreciation
        self.depreciation_2 = format_decimals(self.income_statement.at['Depreciation', 'Year_2'] / self.income_statement.at['Revenues', 'Year_2'] * -1)
        self.depreciation_1 = format_decimals(self.income_statement.at['Depreciation', 'Year_1'] / self.income_statement.at['Revenues', 'Year_1'] * -1)
        self.depreciation_0 = format_decimals(self.income_statement.at['Depreciation', 'Year0'] / self.income_statement.at['Revenues', 'Year0'] * -1)

        # Long-Term Debt Interest Rate
        self.long_term_int_2 = format_decimals(self.income_statement.at['Interest', 'Year_2'] / ((self.balance_sheet.at['Long-Term Debt', 'Year_2'] + self.balance_sheet.at['Long-Term Debt', 'Year2']) / 2) * -1)
        self.long_term_int_1 = format_decimals(self.income_statement.at['Interest', 'Year_1'] / ((self.balance_sheet.at['Long-Term Debt', 'Year_1'] + self.balance_sheet.at['Long-Term Debt', 'Year1']) / 2) * -1)
        self.long_term_int_0 = format_decimals(self.income_statement.at['Interest', 'Year0'] / ((self.balance_sheet.at['Long-Term Debt', 'Year0'] + self.balance_sheet.at['Long-Term Debt', 'Year0']) / 2) * -1)

        # Tax Rate (Percent of EBT)
        self.tax_perc_EBT_2 = format_decimals(self.income_statement.at['Taxes', 'Year_2'] / self.income_statement.at['Earnings Before Taxes', 'Year_2']) * -1
        self.tax_perc_EBT_1 = format_decimals(self.income_statement.at['Taxes', 'Year_1'] / self.income_statement.at['Earnings Before Taxes', 'Year_1']) * -1
        self.tax_perc_EBT_0 = format_decimals(self.income_statement.at['Taxes', 'Year0'] / self.income_statement.at['Earnings Before Taxes', 'Year0']) * -1

        # Capital Asset Turnover Ratio
        self.asset_tur_2 = format_fixed_cost(self.income_statement.at['Revenues', 'Year_2'] / self.balance_sheet.at['Property Plant and Equipment', 'Year_2'])
        self.asset_tur_1 = format_fixed_cost(self.income_statement.at['Revenues', 'Year_1'] / self.balance_sheet.at['Property Plant and Equipment', 'Year_1'])
        self.asset_tur_0 = format_fixed_cost(self.income_statement.at['Revenues', 'Year0'] / self.balance_sheet.at['Property Plant and Equipment', 'Year0'])

        # Receivables Days
        self.receivables_days_2 = format_fixed_cost(self.balance_sheet.at['Trade and Other Receivables', 'Year_2'] / self.income_statement.at['Revenues', 'Year_2'] * 365)
        self.receivables_days_1 = format_fixed_cost(self.balance_sheet.at['Trade and Other Receivables', 'Year_1'] / self.income_statement.at['Revenues', 'Year_1'] * 365)
        self.receivables_days_0 = format_fixed_cost(self.balance_sheet.at['Trade and Other Receivables', 'Year0'] / self.income_statement.at['Revenues', 'Year0'] * 365)

        # Inventory Days (COGS Basis) (Days)
        self.inv_days_2 = format_fixed_cost(self.balance_sheet.at['Inventories', 'Year_2'] / self.income_statement.at['Cost of Goods Sold', 'Year_2'] * 365 * -1)
        self.inv_days_1 = format_fixed_cost(self.balance_sheet.at['Inventories', 'Year_1'] / self.income_statement.at['Cost of Goods Sold', 'Year_1'] * 365 * -1)
        self.inv_days_0 = format_fixed_cost(self.balance_sheet.at['Inventories', 'Year0'] / self.income_statement.at['Cost of Goods Sold', 'Year0'] * 365 * -1)

        # Payable Days
        self.payable_days_2 = format_fixed_cost(self.balance_sheet.at['Trade and Other Payables', 'Year_2'] / self.income_statement.at['Cost of Goods Sold', 'Year_2'] * 365 * -1)
        self.payable_days_1 = format_fixed_cost(self.balance_sheet.at['Trade and Other Payables', 'Year_1'] / self.income_statement.at['Cost of Goods Sold', 'Year_1'] * 365 * -1) 
        self.payable_days_0 = format_fixed_cost(self.balance_sheet.at['Trade and Other Payables', 'Year0'] / self.income_statement.at['Cost of Goods Sold', 'Year0'] * 365 * -1)

        # Income Tax Payable (Percent of Taxes) (Days)
        self.inc_tax_pay_2 = format_decimals(self.balance_sheet.at['Income Taxes Payable', 'Year_2'] / self.income_statement.at['Taxes', 'Year_2']) * -1
        self.inc_tax_pay_1 = format_decimals(self.balance_sheet.at['Income Taxes Payable', 'Year_1'] / self.income_statement.at['Taxes', 'Year_1']) * -1
        self.inc_tax_pay_0 = format_decimals(self.balance_sheet.at['Income Taxes Payable', 'Year0'] / self.income_statement.at['Taxes', 'Year0']) * -1


        # Long Term Debt
        self.assumptions.at['Long Term Debt', 'Year_2'] = self.balance_sheet.at['Long-Term Debt', 'Year_2']
        self.long_term_debt_2 = format_fixed_cost(self.assumptions.at['Long Term Debt', 'Year_2'])
        self.assumptions.at['Long Term Debt', 'Year_1'] = self.balance_sheet.at['Long-Term Debt', 'Year_1']
        self.long_term_debt_1 = format_fixed_cost(self.assumptions.at['Long Term Debt', 'Year_1'])
        self.assumptions.at['Long Term Debt', 'Year0'] = self.balance_sheet.at['Long-Term Debt', 'Year0']
        self.long_term_debt_0 = format_fixed_cost(self.assumptions.at['Long Term Debt', 'Year0'])


        # Common Share Capital
        self.assumptions.at['Common Share Capital', 'Year_2'] = self.balance_sheet.at['Common Stock and Additional Paid-In Capital', 'Year_2']
        self.common_share_cap_2 = format_fixed_cost(self.assumptions.at['Common Share Capital', 'Year_2'])

        self.assumptions.at['Common Share Capital', 'Year_1'] = self.balance_sheet.at['Common Stock and Additional Paid-In Capital', 'Year_1']
        self.common_share_cap_1 = format_fixed_cost(self.assumptions.at['Common Share Capital', 'Year_1'])

        self.assumptions.at['Common Share Capital', 'Year0'] = self.balance_sheet.at['Common Stock and Additional Paid-In Capital', 'Year0']
        self.common_share_cap_0 = format_fixed_cost(self.assumptions.at['Common Share Capital', 'Year0'])

        # Dividend Payout (Percent of Net Income)
        self.div_payout_ratio_2 = format_decimals(self.income_statement.at['Common Dividends', 'Year_2'] / self.income_statement.at['Net Income', 'Year_2'])
        self.div_payout_ratio_1 = format_decimals(self.income_statement.at['Common Dividends', 'Year_1'] / self.income_statement.at['Net Income', 'Year_1'])
        self.div_payout_ratio_0 = format_decimals(self.income_statement.at['Common Dividends', 'Year0'] / self.income_statement.at['Net Income', 'Year0'])


    

    # Define the function to assign a value
    def assign_values(self, df, values_dict):
        for (row_label, column_label), value in values_dict.items():
            df.at[row_label, column_label] = float(value) 

    
    def upload_to_database(self):
        for index, row in self.assumptions.iterrows():
            metrics = index
            values = row.to_dict()

            # Update or create a record in the database
            existing_record = self.session.query(Assumptions).filter_by(metrics=metrics).first()

            if existing_record:
                for column_label, value in values.items():
                    column_name = column_label.replace(" ", "_").lower()
                    setattr(existing_record, column_name, Decimal(value) if value else None)
            else:
                new_record = Assumptions(metrics=metrics, **{column_label.replace(" ", "_").lower(): Decimal(value) if value else None for column_label, value in values.items()})
                self.session.add(new_record)

        # Commit changes to the database
        self.session.commit()


    def populate_assumptions_future(self):
        # Define metrics that should be formatted as percentages and raw numbers
        self.percentage_metrics = [
            'Sales Growth', 
            'Gross Margin',
            'Distribution Expense (Percent of Sales)',
            'Research Expense (Percent of Sales)',
           'Depreciation (Percent of Sales)',
           'Long-Term Debt Interest Rate (Average Debt)',
           'Tax Rate (Percent of EBT)', 
           'Income Tax Payable (Percent of Taxes) (Days)',
           'Dividend Payout Ratio '
         ]
    
        self.raw_number_metrics = [
            'Marketing & Admin Expense (Fixed Cost)',
            'Capital Asset Turnover Ratio                           (x)',
           'Receivable Days (Sales Basis)                     (Days)',
           'Inventory Days (COGS Basis)                       (Days)',
           'Payable Days (COGS Basis)                          (Days)',
           'Long Term Debt',
           'Common Share Capital'
        ]

        # Function to get user input
        def get_user_input(prompt):
            while True:
                try:
                    value = float(input(prompt))
                    return value
                except ValueError:
                    print("Invalid input. Please enter a numerical value.")

            
            # Function to format values
        def format_value(value, is_decimal=True):
            if is_decimal:
                return round(Decimal(value) * 100, 2)
            else:
                return float(round(Decimal(value), 2))

        for metrics in self.percentage_metrics:
            same_value = input(f"Do you want to enter the same value for all years for {metrics}? (yes/no): ").strip().lower()
            
            if same_value == 'yes':
                value = get_user_input(f"Enter {metrics} (as a decimal, e.g., 0.06 for 6%): ")
                formatted_value = format_value(value, is_decimal=True)
                self.assumptions.loc[metrics, self.years] = float(formatted_value)
            else:
                for year in self.years:
                    prompt = f"Enter {metrics} for {year} (as a decimal, e.g., 0.06 for 6%): "
                    value = get_user_input(prompt)
                    self.assumptions.at[metrics, year] = format_value(value, is_decimal=True)

        for metric in self.raw_number_metrics:
            same_value = input(f"Do you want to enter the same value for all years for {metric}? (yes/no): ").strip().lower()
            
            if same_value == 'yes':
                value = get_user_input(f"Enter {metric}: ")
                formatted_value = format_value(value, is_decimal=False)
                self.assumptions.loc[metric, self.years] = formatted_value
            else:
                for year in self.years:
                    prompt = f"Enter {metric} for {year}: "
                    value = get_user_input(prompt)
                    self.assumptions.at[metric, year] = format_value(value, is_decimal=False)

    ##################################################################################################################

    # Modify this to insert values into the database
    def upload_to_database_future(self):
        for metrics, row in self.assumptions.iterrows():                                                                            
            year_values = {f"year(i+1)": Decimal(row[year]) if row[year] else None for i, year in enumerate(self.years)}

            percentage_values = {k.replace(" ", "_").lower(): Decimal(v) if v else None 
                             for k, v in row.items() if metrics in self.percentage_metrics}
            raw_number_values = {k.replace(" ", "_").lower(): Decimal(v) if v else None 
                             for k, v in row.items() if metrics in self.raw_number_metrics}
        

            # Ensure Days in Period is inserted correctly (handle it like the first method)
            if 'Days in Period' in row and row['Days in Period']:
                raw_number_values['Days in Period'] = Decimal(row['Days in Period'])
            else:
                raw_number_values['Days in Period'] = None

            # Update or create a record in the database
            existing_record = self.session.query(Assumptions).filter_by(metrics=metrics).first()


            if existing_record:
                for column_label, value in {**year_values, **percentage_values, **raw_number_values}.items():
                    setattr(existing_record, column_label, value)
            else:
                # Create new record
                new_record = Assumptions(
                    metrics=metrics,
                    **year_values,
                    **percentage_values,
                    **raw_number_values
                )
                self.session.add(new_record)
                

        # Commit changes to the database
        self.session.commit()

    #######################################################################################################

    def clear_database(self):
        with self.Session() as session:
            # Iterate over all tables and delete their contents
            for table in Base.metadata.sorted_tables:
                session.execute(table.delete())
            # Commit the transaction
            session.commit()
        print("Database cleared successfully.")

       
    
        


def main():
    # Create an instance of the Analysis class
    data_path = "C:/Users/campo/OneDrive/Desktop/Statements2.xlsx"
    analysis = Analysis(data_path)
    
    # Load the data
    analysis.get_statements_data()
    analysis.statements()
    
    # Perform historical and future assumptions population
    analysis.populate_assumptions_historical()
    # analysis.clear_database()
     
   

    values_dict = {
            ('Sales Growth', 'Year_1'): analysis.sg_year_1,
            ('Sales Growth', 'Year0'): analysis.sg_year_0,
            ('Gross Margin', 'Year_2'): analysis.gm_year_2,
            ('Gross Margin', 'Year_1'): analysis.gm_year_1,
            ('Gross Margin', 'Year0'): analysis.gm_year_0,
            ('Distribution Expense (Percent of Sales)', 'Year_2'): analysis.dist_exp_2,
            ('Distribution Expense (Percent of Sales)', 'Year_1'): analysis.dist_exp_1,
            ('Distribution Expense (Percent of Sales)', 'Year0'): analysis.dist_exp_0,
            ('Marketing & Admin Expense (Fixed Cost)', 'Year_2'): analysis.mkt_admin_2,
            ('Marketing & Admin Expense (Fixed Cost)', 'Year_1'): analysis.mkt_admin_1,
            ('Marketing & Admin Expense (Fixed Cost)', 'Year0'): analysis.mkt_admin_0,
            ('Research Expense (Percent of Sales)', 'Year_2'): analysis.res_exp_2,
            ('Research Expense (Percent of Sales)', 'Year_1'): analysis.res_exp_1,
            ('Research Expense (Percent of Sales)', 'Year0'): analysis.res_exp_0,
            ('Depreciation (Percent of Sales)', 'Year_2'): analysis.depreciation_2,
            ('Depreciation (Percent of Sales)', 'Year_1'): analysis.depreciation_1,
            ('Depreciation (Percent of Sales)', 'Year0'): analysis.depreciation_0,
            ('Long-Term Debt Interest Rate (Average Debt)', 'Year_2'): analysis.long_term_int_2,
            ('Long-Term Debt Interest Rate (Average Debt)', 'Year_1'): analysis.long_term_int_1,
            ('Long-Term Debt Interest Rate (Average Debt)', 'Year0'): analysis.long_term_int_0,
            ('Tax Rate (Percent of EBT)', 'Year_2'): analysis.tax_perc_EBT_2,
            ('Tax Rate (Percent of EBT)', 'Year_1'): analysis.tax_perc_EBT_1,
            ('Tax Rate (Percent of EBT)', 'Year0'): analysis.tax_perc_EBT_0,
            ('Capital Asset Turnover Ratio                           (x)', 'Year_2'): analysis.asset_tur_2,
            ('Capital Asset Turnover Ratio                           (x)', 'Year_1'): analysis.asset_tur_1,
            ('Capital Asset Turnover Ratio                           (x)', 'Year0'): analysis.asset_tur_0,
            ('Receivable Days (Sales Basis)                     (Days)', 'Year_2'): analysis.receivables_days_2,
            ('Receivable Days (Sales Basis)                     (Days)', 'Year_1'): analysis.receivables_days_1,
            ('Receivable Days (Sales Basis)                     (Days)', 'Year0'): analysis.receivables_days_0,
            ('Inventory Days (COGS Basis)                       (Days)', 'Year_2'): analysis.inv_days_2,
            ('Inventory Days (COGS Basis)                       (Days)', 'Year_1'): analysis.inv_days_1,
            ('Inventory Days (COGS Basis)                       (Days)', 'Year0'): analysis.inv_days_0,
            ('Payable Days (COGS Basis)                          (Days)', 'Year_2'): analysis.payable_days_2,
            ('Payable Days (COGS Basis)                          (Days)', 'Year_1'): analysis.payable_days_1,
            ('Payable Days (COGS Basis)                          (Days)', 'Year0'): analysis.payable_days_0,
            ('Income Tax Payable (Percent of Taxes) (Days)', 'Year_2'): analysis.inc_tax_pay_2,
            ('Income Tax Payable (Percent of Taxes) (Days)', 'Year_1'): analysis.inc_tax_pay_1,
            ('Income Tax Payable (Percent of Taxes) (Days)', 'Year0'): analysis.inc_tax_pay_0,
            ('Long Term Debt', 'Year_2'): analysis.long_term_debt_2,
            ('Long Term Debt', 'Year_1'): analysis.long_term_debt_1,
            ('Long Term Debt', 'Year0'): analysis.long_term_debt_0,
            ('Common Share Capital', 'Year_2'): analysis.common_share_cap_2,
            ('Common Share Capital', 'Year_1'): analysis.common_share_cap_1,
            ('Common Share Capital', 'Year0'): analysis.common_share_cap_0,
            ('Dividend Payout Ratio ', 'Year_2'): analysis.div_payout_ratio_2,
            ('Dividend Payout Ratio ', 'Year_1'): analysis.div_payout_ratio_1,
            ('Dividend Payout Ratio ', 'Year0'): analysis.div_payout_ratio_0,   
        }
   

    analysis.assign_values(analysis.assumptions, values_dict)
    # analysis.upload_to_database()
    analysis.populate_assumptions_future()
    analysis.upload_to_database_future()
    


    # analysis.assign_values(values_dict)

    print(analysis.assumptions)
    #print(analysis.income_statement.columns)
    # df = pd.DataFrame([values_dict], index= ['Metrics'])
    # print(df)

if __name__ == '__main__':
    main()



