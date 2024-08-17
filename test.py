import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, Column, String, Integer, Float, DECIMAL, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, relationship,session
import psycopg2
from psycopg2 import sql




Base = declarative_base()


class Assumptions(Base):
    __tablename__ = 'assumptions'
    metric_id = Column(Integer, primary_key=True)
    metric_name = Column(String)
    year2 = Column(DECIMAL(10,2))
    year1 = Column(DECIMAL(10,2))
    year0 = Column(DECIMAL(10,2))
    year_1 = Column(DECIMAL(10,2))
    year_2 = Column(DECIMAL(10,2))
    year_3 = Column(DECIMAL(10,2))
    year_4 = Column(DECIMAL(10,2))
    year_5 = Column(DECIMAL(10,2))
    

    


#################################################################

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
new_db_name = 'statements'
cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(new_db_name)))

# Close the connection to the default database
cur.close()
conn.close()

# # Connect to the new database
# db_params['dbname'] = new_db_name
# conn = psycopg2.connect(**db_params)
# cur = conn.cursor()



# Create table assumptions
cur.execute('''
            CREATE TABLE assumptions (
    metric_id SERIAL PRIMARY KEY,
    metric_name TEXT,
    year2 NUMERIC(10,2),
    year1 NUMERIC(10,2),
    year0 NUMERIC(10,2),
    year_1 NUMERIC(10,2),
    year_2 NUMERIC(10,2),
    year_3 NUMERIC(10,2),
    year_4 NUMERIC(10,2),
    year_5 NUMERIC(10,2)
);
            ''')



# Commit changes 
conn.commit()


# insert data
insert_query = '''
    INSERT INTO assumptions (metric_name, year2, year1, year0, year_1, year_2, year_3, year_4, year_5)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
'''

values = [
('', None, None, None, None, None, None,None, None),
('Days in Period', None, None, None, None, None, None, None, None),
('Sales Growth', None, None, None, None, None, None, None, None),
('Gross Margin', None, None, None, None, None, None, None, None),
('Distribution Expense (Percent of Sales)', None, None, None, None, None, None, None, None),
('Marketing & Admin Expense (Fixed Cost)', None, None, None, None, None, None, None, None),
('Research Expense (Percent of Sales)', None, None, None, None, None, None, None, None),
('Depreciation (Percent of Sales)', None, None, None, None, None, None, None, None),
('Long-Term Debt Interest Rate (Average Debt)', None, None, None, None, None, None, None, None),
('Tax Rate (Percent of EBT)', None, None, None, None, None, None, None, None),
('Capital Asset Turnover Ratio (x)', None, None, None, None, None, None, None, None),
('Receivable Days (Sales Basis) (Days)', None, None, None, None, None, None, None, None),
('Inventory Days (COGS Basis) (Days)', None, None, None, None, None, None, None, None),
('Payable Days (COGS Basis) (Days)', None, None, None, None, None, None, None, None),
('Income Tax Payable (Percent of Taxes) (Days)', None, None, None, None, None, None, None, None),
('Long Term Debt', None, None, None, None, None, None, None, None),
('Common Share Capital', None, None, None, None, None, None, None, None),
('Dividend Payout Ratio', None, None, None, None, None, None, None, None)
]

cur.executemany(insert_query, values)

#Commit changes and close the connection
conn.commit()
cur.close()
conn.close()

#################################################################################################


# Create a class to fetch data and perform analysis

class Analysis:
    def __init__(self, data_path):
        self.data_path = data_path
        self.income_statement = pd.DataFrame()
        self.balance_sheet = pd.DataFrame()
        self.cash_flow = pd.DataFrame()
        self.assumptions = pd.DataFrame()
        self.years =  ['Year-1', 'Year-2', 'Year-3', 'Year-4', 'Year-5']
        # add additional sheets
        self.working_capital = pd.DataFrame()
        self.capital_structure = pd.DataFrame()
        self.engine = create_engine('postgresql://Campospa:2883@localhost/statements')
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

        
                

    def get_statements_data(self):
        #self.data =  "C:/Users/campo/OneDrive/Desktop/Statements.xlsx"
        self.data =  "C:/Users/campo/OneDrive/Desktop/Statements2.xlsx"

        
    def statements(self):
        self.assumptions = pd.read_excel(self.data, sheet_name = 'Assumptions', index_col= 'Metrics')
        self.income_statement = pd.read_excel(self.data, sheet_name='Income Statement', index_col='Income Statement')
        self.balance_sheet = pd.read_excel(self.data, sheet_name='Balance Sheet', index_col='Balance Sheet')
        self.cash_flow =  pd.read_excel(self.data, sheet_name='Cash Flows', index_col='Cash Flows')
        self.assumptions = self.assumptions.astype(str)
        self.working_capital = pd.read_excel(self.data, sheet_name = 'Working Capital', index_col= 'Working Capital')
        self.capital_structure = pd.read_excel(self.data, sheet_name = 'Capital Structure', index_col= 'Capital Structure')

    
    # Create a class to calculate and assign historical assumption values
    def populate_assumptions_historical(self):
        # Helper method to format values
        def format_decimals(value):
            return round(float(value) * 100, 2)  # Format to decimals 
        

        def format_fixed_cost(value):
            try:
                return "{:.2f}".format(float(value))  # Format as a fixed cost with three decimal places
            except ValueError:
                return "N/A"  # Handle cases where the value cannot be converted to float
        
        #Sales growth
        # Sales growth
        self.sg_year_1 = format_decimals(float(self.income_statement.at['Revenues', 'Year1']) / float(self.income_statement.at['Revenues', 'Year2']) - 1)
        self.sg_year_0 = format_decimals(float(self.income_statement.at['Revenues', 'Year0']) / float(self.income_statement.at['Revenues', 'Year1']) - 1)

        # Gross Margin
        self.gm_year_2 = format_decimals(float(self.income_statement.at['Gross Profit', 'Year2']) / float(self.income_statement.at['Revenues', 'Year2']))
        self.gm_year_1 = format_decimals(float(self.income_statement.at['Gross Profit', 'Year1']) / float(self.income_statement.at['Revenues', 'Year1']))
        self.gm_year_0 = format_decimals(float(self.income_statement.at['Gross Profit', 'Year0']) / float(self.income_statement.at['Revenues', 'Year0']))

        # Distribution Expense (Percent of Sales)
        self.dist_exp_2 = format_decimals(float(self.income_statement.at['Distribution Expenses', 'Year2']) / float(self.income_statement.at['Revenues', 'Year2']) * -1)
        self.dist_exp_1 = format_decimals(float(self.income_statement.at['Distribution Expenses', 'Year1']) / float(self.income_statement.at['Revenues', 'Year1']) * -1)
        self.dist_exp_0 = format_decimals(float(self.income_statement.at['Distribution Expenses', 'Year0']) / float(self.income_statement.at['Revenues', 'Year0']) * -1)

        # Marketing & Admin Expense (Fixed Cost)
        self.mkt_admin_2 = format_fixed_cost(float(self.income_statement.at['Marketing and Administration', 'Year2']) * -1)
        self.mkt_admin_1 = format_fixed_cost(float(self.income_statement.at['Marketing and Administration', 'Year1']) * -1)
        self.mkt_admin_0 = format_fixed_cost(float(self.income_statement.at['Marketing and Administration', 'Year0']) * -1)

        # Research Expense (Percent of Sales)
        self.res_exp_2 = format_decimals(float(self.income_statement.at['Research and Development', 'Year2']) / float(self.income_statement.at['Revenues', 'Year2']) * -1)
        self.res_exp_1 = format_decimals(float(self.income_statement.at['Research and Development', 'Year1']) / float(self.income_statement.at['Revenues', 'Year1']) * -1)
        self.res_exp_0 = format_decimals(float(self.income_statement.at['Research and Development', 'Year0']) / float(self.income_statement.at['Revenues', 'Year0']) * -1)

        # Depreciation
        self.depreciation_2 = format_decimals(float(self.income_statement.at['Depreciation', 'Year2']) / float(self.income_statement.at['Revenues', 'Year2']) * -1)
        self.depreciation_1 = format_decimals(float(self.income_statement.at['Depreciation', 'Year1']) / float(self.income_statement.at['Revenues', 'Year1']) * -1)
        self.depreciation_0 = format_decimals(float(self.income_statement.at['Depreciation', 'Year0']) / float(self.income_statement.at['Revenues', 'Year0']) * -1)

        # Long-Term Debt Interest Rate
        self.long_term_int_2 = format_decimals(float(self.income_statement.at['Interest', 'Year2']) / ((float(self.balance_sheet.at['Long-Term Debt', 'Year2']) + float(self.balance_sheet.at['Long-Term Debt', 'Year2'])) / 2) * -1)
        self.long_term_int_1 = format_decimals(float(self.income_statement.at['Interest', 'Year1']) / ((float(self.balance_sheet.at['Long-Term Debt', 'Year1']) + float(self.balance_sheet.at['Long-Term Debt', 'Year1'])) / 2) * -1)
        self.long_term_int_0 = format_decimals(float(self.income_statement.at['Interest', 'Year0']) / ((float(self.balance_sheet.at['Long-Term Debt', 'Year0']) + float(self.balance_sheet.at['Long-Term Debt', 'Year0'])) / 2) * -1)

        # Tax Rate (Percent of EBT)
        self.tax_perc_EBT_2 = format_decimals(float(self.income_statement.at['Taxes', 'Year2']) / float(self.income_statement.at['Earnings Before Taxes', 'Year2']) * -1)
        self.tax_perc_EBT_1 = format_decimals(float(self.income_statement.at['Taxes', 'Year1']) / float(self.income_statement.at['Earnings Before Taxes', 'Year1']) * -1)
        self.tax_perc_EBT_0 = format_decimals(float(self.income_statement.at['Taxes', 'Year0']) / float(self.income_statement.at['Earnings Before Taxes', 'Year0']) * -1)

        # Capital Asset Turnover Ratio
        self.asset_tur_2 = format_fixed_cost(float(self.income_statement.at['Revenues', 'Year2']) / float(self.balance_sheet.at['Property Plant and Equipment', 'Year2']))
        self.asset_tur_1 = format_fixed_cost(float(self.income_statement.at['Revenues', 'Year1']) / float(self.balance_sheet.at['Property Plant and Equipment', 'Year1']))
        self.asset_tur_0 = format_fixed_cost(float(self.income_statement.at['Revenues', 'Year0']) / float(self.balance_sheet.at['Property Plant and Equipment', 'Year0']))

        # Receivables Days
        self.receivables_days_2 = format_fixed_cost(float(self.balance_sheet.at['Trade and Other Receivables', 'Year2']) / float(self.income_statement.at['Revenues', 'Year2']) * 365)
        self.receivables_days_1 = format_fixed_cost(float(self.balance_sheet.at['Trade and Other Receivables', 'Year1']) / float(self.income_statement.at['Revenues', 'Year1']) * 365)
        self.receivables_days_0 = format_fixed_cost(float(self.balance_sheet.at['Trade and Other Receivables', 'Year0']) / float(self.income_statement.at['Revenues', 'Year0']) * 365)

        # Inventory Days (COGS Basis) (Days)
        self.inv_days_2 = format_fixed_cost(float(self.balance_sheet.at['Inventories', 'Year2']) / float(self.income_statement.at['Cost of Goods Sold', 'Year2']) * 365 * -1)
        self.inv_days_1 = format_fixed_cost(float(self.balance_sheet.at['Inventories', 'Year1']) / float(self.income_statement.at['Cost of Goods Sold', 'Year1']) * 365 * -1)
        self.inv_days_0 = format_fixed_cost(float(self.balance_sheet.at['Inventories', 'Year0']) / float(self.income_statement.at['Cost of Goods Sold', 'Year0']) * 365 * -1)

        # Payable Days
        self.payable_days_2 = format_fixed_cost(float(self.balance_sheet.at['Trade and Other Payables', 'Year2']) / float(self.income_statement.at['Cost of Goods Sold', 'Year2']) * 365 * -1)
        self.payable_days_1 = format_fixed_cost(float(self.balance_sheet.at['Trade and Other Payables', 'Year1']) / float(self.income_statement.at['Cost of Goods Sold', 'Year1']) * 365 * -1)
        self.payable_days_0 = format_fixed_cost(float(self.balance_sheet.at['Trade and Other Payables', 'Year0']) / float(self.income_statement.at['Cost of Goods Sold', 'Year0']) * 365 * -1)

        # Income Tax Payable (Percent of Taxes) (Days)
        self.inc_tax_pay_2 = format_decimals(float(self.balance_sheet.at['Income Taxes Payable', 'Year2']) / float(self.income_statement.at['Taxes', 'Year2']) * -1)
        self.inc_tax_pay_1 = format_decimals(float(self.balance_sheet.at['Income Taxes Payable', 'Year1']) / float(self.income_statement.at['Taxes', 'Year1']) * -1)
        self.inc_tax_pay_0 = format_decimals(float(self.balance_sheet.at['Income Taxes Payable', 'Year0']) / float(self.income_statement.at['Taxes', 'Year0']) * -1)

        # Long Term Debt
        self.assumptions.at['Long Term Debt', 'Year2'] = float(self.balance_sheet.at['Long-Term Debt', 'Year2'])
        self.long_term_debt_2 = format_fixed_cost(self.assumptions.at['Long Term Debt', 'Year2'])

        self.assumptions.at['Long Term Debt', 'Year1'] = float(self.balance_sheet.at['Long-Term Debt', 'Year1'])
        self.long_term_debt_1 = format_fixed_cost(self.assumptions.at['Long Term Debt', 'Year1'])

        self.assumptions.at['Long Term Debt', 'Year0'] = float(self.balance_sheet.at['Long-Term Debt', 'Year0'])
        self.long_term_debt_0 = format_fixed_cost(self.assumptions.at['Long Term Debt', 'Year0'])

        # Common Share Capital
        self.assumptions.at['Common Share Capital', 'Year2'] = float(self.balance_sheet.at['Common Stock and Additional Paid-In Capital', 'Year2'])
        self.common_share_cap_2 = format_fixed_cost(self.assumptions.at['Common Share Capital', 'Year2'])

        self.assumptions.at['Common Share Capital', 'Year1'] = float(self.balance_sheet.at['Common Stock and Additional Paid-In Capital', 'Year1'])
        self.common_share_cap_1 = format_fixed_cost(self.assumptions.at['Common Share Capital', 'Year1'])

        self.assumptions.at['Common Share Capital', 'Year0'] = float(self.balance_sheet.at['Common Stock and Additional Paid-In Capital', 'Year0'])
        self.common_share_cap_0 = format_fixed_cost(self.assumptions.at['Common Share Capital', 'Year0'])

        # Dividend Payout Ratio
        self.div_payout_ratio_2 = format_decimals(float(self.income_statement.at['Common Dividends', 'Year2']) / float(self.income_statement.at['Net Income', 'Year2']))
        self.div_payout_ratio_1 = format_decimals(float(self.income_statement.at['Common Dividends', 'Year1']) / float(self.income_statement.at['Net Income', 'Year1']))
        self.div_payout_ratio_0 = format_decimals(float(self.income_statement.at['Common Dividends', 'Year0']) / float(self.income_statement.at['Net Income', 'Year0']))

    
        

         

    # Define the function to assign a value
    def assign_values(self, df, values_dict):
        for (row_label, column_label), value in values_dict.items():
            df.at[row_label, column_label] = value

        
        print(df) #This function assigns the values correctly
    
    
    def upload_to_database(self, df, table_name):
         # Insert the data into the specified table
        df.to_sql(table_name, con=self.engine, if_exists='replace', index=False) # append or replace?
        # Print the DataFrame to check its content
        print("Uploading DataFrame to database:")
        print(df)
      
        '''This does not upload the correct values'''
        

        

    def clear_database(self):
        with self.Session() as session:
            # Iterate over all tables and delete their contents
            for table in Base.metadata.sorted_tables:
                session.execute(table.delete())
            # Commit the transaction
            session.commit()
        print("Database cleared successfully.")





# Run the program

def main():
    # Create an instance of the Analysis class
    data_path = "C:/Users/campo/OneDrive/Desktop/Statements2.xlsx"
    analysis = Analysis(data_path)
    
    
    
    # Load the data
    analysis.get_statements_data()
    analysis.statements()

    # # Fetch data from analysis
    # data = analysis.populated_assumptions_historical() # dont know if that works?
    
    # Perform historical and future assumptions population
    analysis.populate_assumptions_historical()
    # analysis.populate_assumptions_future()
    analysis.upload_to_database(analysis.assumptions, 'assumptions') # works but inserts zero except for long ther debt , common share capital
    #analysis.clear_database()
    
    
    
    values_dict = {
            ('Sales Growth', 'Year1'): analysis.sg_year_1,
            ('Sales Growth', 'Year0'): analysis.sg_year_0,
            ('Gross Margin', 'Year2'): analysis.gm_year_2,
            ('Gross Margin', 'Year1'): analysis.gm_year_1,
            ('Gross Margin', 'Year0'): analysis.gm_year_0,
            ('Distribution Expense (Percent of Sales)', 'Year2'): analysis.dist_exp_2,
            ('Distribution Expense (Percent of Sales)', 'Year1'): analysis.dist_exp_1,
            ('Distribution Expense (Percent of Sales)', 'Year0'): analysis.dist_exp_0,
            ('Marketing & Admin Expense (Fixed Cost)', 'Year2'): analysis.mkt_admin_2,
            ('Marketing & Admin Expense (Fixed Cost)', 'Year1'): analysis.mkt_admin_1,
            ('Marketing & Admin Expense (Fixed Cost)', 'Year0'): analysis.mkt_admin_0,
            ('Research Expense (Percent of Sales)', 'Year2'): analysis.res_exp_2,
            ('Research Expense (Percent of Sales)', 'Year1'): analysis.res_exp_1,
            ('Research Expense (Percent of Sales)', 'Year0'): analysis.res_exp_0,
            ('Depreciation (Percent of Sales)', 'Year2'): analysis.depreciation_2,
            ('Depreciation (Percent of Sales)', 'Year1'): analysis.depreciation_1,
            ('Depreciation (Percent of Sales)', 'Year0'): analysis.depreciation_0,
            ('Long-Term Debt Interest Rate (Average Debt)', 'Year2'): analysis.long_term_int_2,
            ('Long-Term Debt Interest Rate (Average Debt)', 'Year1'): analysis.long_term_int_1,
            ('Long-Term Debt Interest Rate (Average Debt)', 'Year0'): analysis.long_term_int_0,
            ('Tax Rate (Percent of EBT)', 'Year2'): analysis.tax_perc_EBT_2,
            ('Tax Rate (Percent of EBT)', 'Year1'): analysis.tax_perc_EBT_1,
            ('Tax Rate (Percent of EBT)', 'Year0'): analysis.tax_perc_EBT_0,
            ('Capital Asset Turnover Ratio                           (x)', 'Year2'): analysis.asset_tur_2,
            ('Capital Asset Turnover Ratio                           (x)', 'Year1'): analysis.asset_tur_1,
            ('Capital Asset Turnover Ratio                           (x)', 'Year0'): analysis.asset_tur_0,
            ('Receivable Days (Sales Basis)                     (Days)', 'Year2'): analysis.receivables_days_2,
            ('Receivable Days (Sales Basis)                     (Days)', 'Year1'): analysis.receivables_days_1,
            ('Receivable Days (Sales Basis)                     (Days)', 'Year0'): analysis.receivables_days_0,
            ('Inventory Days (COGS Basis)                       (Days)', 'Year2'): analysis.inv_days_2,
            ('Inventory Days (COGS Basis)                       (Days)', 'Year1'): analysis.inv_days_1,
            ('Inventory Days (COGS Basis)                       (Days)', 'Year0'): analysis.inv_days_0,
            ('Payable Days (COGS Basis)                          (Days)', 'Year2'): analysis.payable_days_2,
            ('Payable Days (COGS Basis)                          (Days)', 'Year1'): analysis.payable_days_1,
            ('Payable Days (COGS Basis)                          (Days)', 'Year0'): analysis.payable_days_0,
            ('Income Tax Payable (Percent of Taxes) (Days)', 'Year2'): analysis.inc_tax_pay_2,
            ('Income Tax Payable (Percent of Taxes) (Days)', 'Year1'): analysis.inc_tax_pay_1,
            ('Income Tax Payable (Percent of Taxes) (Days)', 'Year0'): analysis.inc_tax_pay_0,
            ('Long Term Debt', 'Year2'): analysis.long_term_debt_2,
            ('Long Term Debt', 'Year1'): analysis.long_term_debt_1,
            ('Long Term Debt', 'Year0'): analysis.long_term_debt_0,
            ('Common Share Capital', 'Year2'): analysis.common_share_cap_2,
            ('Common Share Capital', 'Year1'): analysis.common_share_cap_1,
            ('Common Share Capital', 'Year0'): analysis.common_share_cap_0,
            ('Dividend Payout Ratio ', 'Year2'): analysis.div_payout_ratio_2,
            ('Dividend Payout Ratio ', 'Year1'): analysis.div_payout_ratio_1,
            ('Dividend Payout Ratio ', 'Year0'): analysis.div_payout_ratio_0,   
        }
    

    

    analysis.assign_values(analysis.assumptions, values_dict)

    # Print the assumptions DataFrame
    #print(analysis.assumptions)
    #print(analysis.assumptions.info())
    #print(analysis.assumptions.columns)
    #print(analysis.assumptions.index)
  
    
    

if __name__ == '__main__':
    main()

===================================================================================================

This is the output when I print the df: 

Metrics
Days in Period                                           365       365       365    365    365    365    365    365
Sales Growth                                               0      6.48      7.37      0      0      0      0      0
Gross Margin                                           53.18     56.45     57.42      0      0      0      0      0
Distribution Expense (Percent of Sales)                 7.23      7.41      6.62      0      0      0      0      0
Marketing & Admin Expense (Fixed Cost)              23507.00  26569.00  30830.00      0      0      0      0      0
Research Expense (Percent of Sales)                     2.17      2.23      2.18      0      0      0      0      0
Depreciation (Percent of Sales)                         3.64      3.23      3.12      0      0      0      0      0
Long-Term Debt Interest Rate (Average Debt)              6.2       6.2       6.2      0      0      0      0      0
Tax Rate (Percent of EBT)                              34.75     24.34     15.28      0      0      0      0      0
Capital Asset Turnover Ratio                   ...      4.23      4.26      4.40      0      0      0      0      0
Receivable Days (Sales Basis)                  ...     56.86     59.25     57.72      0      0      0      0      0
Inventory Days (COGS Basis)                    ...     68.63     74.35     74.00      0      0      0      0      0
Payable Days (COGS Basis)                      ...     95.76    101.55    102.00      0      0      0      0      0
Income Tax Payable (Percent of Taxes) (Days)           39.41     36.81     37.01      0      0      0      0      0
Long Term Debt                                      20000.00  20000.00  20000.00      0      0      0      0      0
Common Share Capital                                 7627.00   7627.00   7627.00      0      0      0      0      0
Dividend Payout Ratio                                  83.16     55.76     33.66      0      0      0      0      0

This is what is been inserted to the database:

Metrics
Days in Period                                          365      365      365    365    365    365    365    365
Sales Growth                                              0        0        0      0      0      0      0      0
Gross Margin                                              0        0        0      0      0      0      0      0
Distribution Expense (Percent of Sales)                   0        0        0      0      0      0      0      0
Marketing & Admin Expense (Fixed Cost)                    0        0        0      0      0      0      0      0
Research Expense (Percent of Sales)                       0        0        0      0      0      0      0      0
Depreciation (Percent of Sales)                           0        0        0      0      0      0      0      0
Long-Term Debt Interest Rate (Average Debt)               0        0        0      0      0      0      0      0
Tax Rate (Percent of EBT)                                 0        0        0      0      0      0      0      0
Capital Asset Turnover Ratio                   ...        0        0        0      0      0      0      0      0
Receivable Days (Sales Basis)                  ...        0        0        0      0      0      0      0      0
Inventory Days (COGS Basis)                    ...        0        0        0      0      0      0      0      0
Payable Days (COGS Basis)                      ...        0        0        0      0      0      0      0      0
Income Tax Payable (Percent of Taxes) (Days)              0        0        0      0      0      0      0      0
Long Term Debt                                      20000.0  20000.0  20000.0      0      0      0      0      0
Common Share Capital                                 7627.0   7627.0   7627.0      0      0      0      0      0
Dividend Payout Ratio                                     0        0        0      0      0      0      0      0

Why?

