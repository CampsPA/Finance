
'''I need to be able to save the results of my calculations in the database'''


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
    year2 = Column(DECIMAL)
    year1 = Column(DECIMAL)
    year0 = Column(DECIMAL)
    year_1 = Column(DECIMAL)
    year_2 = Column(DECIMAL)
    year_3 = Column(DECIMAL)
    year_4 = Column(DECIMAL)
    year_5 = Column(DECIMAL)


    


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

# Connect to the new database
db_params['dbname'] = new_db_name
conn = psycopg2.connect(**db_params)
cur = conn.cursor()



# Create table assumptions
cur.execute('''
            CREATE TABLE assumptions (
    metric_id SERIAL PRIMARY KEY,
    Metrics TEXT,
    year2 NUMERIC,
    year1 NUMERIC,
    year0 NUMERIC,
    year_1 NUMERIC,
    year_2 NUMERIC,
    year_3 NUMERIC,
    year_4 NUMERIC,
    year_5 NUMERIC
);
            ''')

# Commit changes 
conn.commit()

# insert data
insert_query = '''
    INSERT INTO assumptions (Metrics, year2, year1, year0, year_1, year_2, year_3, year_4, year_5)
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
    def populated_assumptions_historical(self):
        # Helper method to format values
        def format_percentage(value):
            return round(float(value) * 100, 3)  # Convert to percentage and format to two decimal places
             try:
                 return "{:.3f}".format(float(value))
             except ValueError:
                 return "N/A"
            
            
        

        def format_fixed_cost(value):
            return round(float(value), 3)  # Format as a fixed cost with two decimal places
             try:
                 return "{:.3f}".format(float(value))
             except ValueError:
                 return "N/A"

        self.sg_year_1 = format_percentage(self.income_statement.at['Revenues', 'Year1'] / self.income_statement.at['Revenues', 'Year2'] - 1)
        self.sg_year_0 = format_percentage(self.income_statement.at['Revenues', 'Year0'] / self.income_statement.at['Revenues', 'Year1'] - 1)
        # Gross Margin
        self.gm_year_2 = format_percentage(self.income_statement.at['Gross Profit', 'Year2'] / self.income_statement.at['Revenues', 'Year2'])
        self.gm_year_1 = format_percentage(self.income_statement.at['Gross Profit', 'Year1'] / self.income_statement.at['Revenues', 'Year1'])
        self.gm_year_0 = format_percentage(self.income_statement.at['Gross Profit', 'Year0'] / self.income_statement.at['Revenues', 'Year0'])

        # Distribution Expense (Percent of Sales)
        self.dist_exp_2 = format_percentage(self.income_statement.at['Distribution Expenses', 'Year2'] / self.income_statement.at['Revenues', 'Year2'] * -1 )
        self.dist_exp_1 =  format_percentage(self.income_statement.at['Distribution Expenses', 'Year1'] / self.income_statement.at['Revenues', 'Year1'] * -1 )
        self.dist_exp_0 =  format_percentage(self.income_statement.at['Distribution Expenses', 'Year0'] / self.income_statement.at['Revenues', 'Year0'] * -1 )
        # Marketing & Admin Expense (Fixed Cost)
        self.mkt_admin_2 = format_fixed_cost(self.income_statement.at['Marketing and Administration', 'Year2'] * -1)
        self.mkt_admin_1 = format_fixed_cost(self.income_statement.at['Marketing and Administration', 'Year1'] * -1)
        self.mkt_admin_0 = format_fixed_cost(self.income_statement.at['Marketing and Administration', 'Year0'] * -1)

        # Research Expense (Percent of Sales)
        self.res_exp_2 =  format_percentage(self.income_statement.at['Research and Development', 'Year2'] / self.income_statement.at['Revenues', 'Year2'] * -1 )
        self.res_exp_1 =  format_percentage(self.income_statement.at['Research and Development', 'Year1'] / self.income_statement.at['Revenues', 'Year1'] * -1 )
        self.res_exp_0 =  format_percentage(self.income_statement.at['Research and Development', 'Year0'] / self.income_statement.at['Revenues', 'Year0'] * -1 )

        # Depreciation
        self.depreciation_2 = format_percentage(self.income_statement.at['Depreciation', 'Year2'] / self.income_statement.at['Revenues', 'Year2'] * -1)
        self.depreciation_1 = format_percentage(self.income_statement.at['Depreciation', 'Year1'] / self.income_statement.at['Revenues', 'Year1'] * -1)
        self.depreciation_0 = format_percentage(self.income_statement.at['Depreciation', 'Year0'] / self.income_statement.at['Revenues', 'Year0'] * -1)

        # Long-Term Debt Interest Rate
        self.long_term_int_2 =  format_percentage(self.income_statement.at['Interest', 'Year2'] / ((self.balance_sheet.at['Long-Term Debt', 'Year2'] +  self.balance_sheet.at['Long-Term Debt', 'Year2']) /  2) * -1)
        self.long_term_int_1 =  format_percentage(self.income_statement.at['Interest', 'Year1'] / ((self.balance_sheet.at['Long-Term Debt', 'Year1'] +  self.balance_sheet.at['Long-Term Debt', 'Year1']) /  2) * -1)
        self.long_term_int_0 =  format_percentage(self.income_statement.at['Interest', 'Year0'] / ((self.balance_sheet.at['Long-Term Debt', 'Year0'] +  self.balance_sheet.at['Long-Term Debt', 'Year0']) /  2) * -1)

        # Tax Rate (Percent of EBT)
        self.tax_perc_EBT_2 = format_percentage(self.income_statement.at['Taxes', 'Year2'] / self.income_statement.at['Earnings Before Taxes', 'Year2'] * -1)
        self.tax_perc_EBT_1 = format_percentage(self.income_statement.at['Taxes', 'Year1'] / self.income_statement.at['Earnings Before Taxes', 'Year1'] * -1)
        self.tax_perc_EBT_0 = format_percentage(self.income_statement.at['Taxes', 'Year0'] / self.income_statement.at['Earnings Before Taxes', 'Year0'] * -1)

        # Capital Asset Turnover Ratio
        self.asset_tur_2 = format_fixed_cost(self.income_statement.at['Revenues', 'Year2'] / self.balance_sheet.at['Property Plant and Equipment', 'Year2'])
        self.asset_tur_1 = format_fixed_cost(self.income_statement.at['Revenues', 'Year1'] / self.balance_sheet.at['Property Plant and Equipment', 'Year1'])
        self.asset_tur_0 = format_fixed_cost(self.income_statement.at['Revenues', 'Year0'] / self.balance_sheet.at['Property Plant and Equipment', 'Year0'])

        # Receivables Days
        self.receivables_days_2 = format_fixed_cost(self.balance_sheet.at['Trade and Other Receivables', 'Year2'] / self.income_statement.at['Revenues', 'Year2'] * 365)
        self.receivables_days_1 = format_fixed_cost(self.balance_sheet.at['Trade and Other Receivables', 'Year1'] / self.income_statement.at['Revenues', 'Year1'] * 365)
        self.receivables_days_0 = format_fixed_cost(self.balance_sheet.at['Trade and Other Receivables', 'Year0'] / self.income_statement.at['Revenues', 'Year0'] * 365)

        # Inventory Days (COGS Basis) (Days)
        self.inv_days_2 = format_fixed_cost(self.balance_sheet.at['Inventories', 'Year2'] / self.income_statement.at['Cost of Goods Sold', 'Year2'] * 365 * -1)
        self.inv_days_1 = format_fixed_cost(self.balance_sheet.at['Inventories', 'Year1'] / self.income_statement.at['Cost of Goods Sold', 'Year1'] * 365 * -1)
        self.inv_days_0 = format_fixed_cost(self.balance_sheet.at['Inventories', 'Year0'] / self.income_statement.at['Cost of Goods Sold', 'Year0'] * 365 * -1)

        # Payable Days
        self.payable_days_2 =  format_fixed_cost(self.balance_sheet.at['Trade and Other Payables', 'Year2'] / self.income_statement.at['Cost of Goods Sold', 'Year2'] * 365 * -1)
        self.payable_days_1 =  format_fixed_cost(self.balance_sheet.at['Trade and Other Payables', 'Year1'] / self.income_statement.at['Cost of Goods Sold', 'Year1'] * 365 * -1)
        self.payable_days_0 =  format_fixed_cost(self.balance_sheet.at['Trade and Other Payables', 'Year0'] / self.income_statement.at['Cost of Goods Sold', 'Year0'] * 365 * -1)

        # Income Tax Payable (Percent of Taxes) (Days)
        self.inc_tax_pay_2 = format_percentage(self.balance_sheet.at['Income Taxes Payable', 'Year2'] / self.income_statement.at['Taxes', 'Year2'] * -1)
        self.inc_tax_pay_1 = format_percentage(self.balance_sheet.at['Income Taxes Payable', 'Year1'] / self.income_statement.at['Taxes', 'Year1'] * -1)
        self.inc_tax_pay_0 = format_percentage(self.balance_sheet.at['Income Taxes Payable', 'Year0'] / self.income_statement.at['Taxes', 'Year0'] * -1)

        # Long Term Debt
        self.assumptions.at['Long Term Debt', 'Year2'] = self.balance_sheet.at['Long-Term Debt', 'Year2']
        self.long_term_debt_2 = format_fixed_cost(self.assumptions.at['Long Term Debt', 'Year2'])

        self.assumptions.at['Long Term Debt', 'Year1'] = self.balance_sheet.at['Long-Term Debt', 'Year1']
        self.long_term_debt_1 = format_fixed_cost(self.assumptions.at['Long Term Debt', 'Year1'])

        self.assumptions.at['Long Term Debt', 'Year0'] = self.balance_sheet.at['Long-Term Debt', 'Year0']
        self.long_term_debt_0 = format_fixed_cost(self.assumptions.at['Long Term Debt', 'Year0'])

        #Common Share Capital
        self.assumptions.at['Common Share Capital', 'Year2'] = self.balance_sheet.at['Common Stock and Additional Paid-In Capital', 'Year2']
        self.common_share_cap_2 = format_fixed_cost(self.assumptions.at['Common Share Capital', 'Year2'])

        self.assumptions.at['Common Share Capital', 'Year1'] = self.balance_sheet.at['Common Stock and Additional Paid-In Capital', 'Year1']
        self.common_share_cap_1 = format_fixed_cost(self.assumptions.at['Common Share Capital', 'Year1'])

        self.assumptions.at['Common Share Capital', 'Year0'] = self.balance_sheet.at['Common Stock and Additional Paid-In Capital', 'Year0']
        self.common_share_cap_0 = format_fixed_cost(self.assumptions.at['Common Share Capital', 'Year0'])

         #Dividend Payout Ratio
        self.div_payout_ratio_2 =  format_percentage(self.income_statement.at['Common Dividends', 'Year2'] / self.income_statement.at['Net Income', 'Year2'])
        self.div_payout_ratio_1 =  format_percentage(self.income_statement.at['Common Dividends', 'Year1'] / self.income_statement.at['Net Income', 'Year1'])
        self.div_payout_ratio_0 =  format_percentage(self.income_statement.at['Common Dividends', 'Year0'] / self.income_statement.at['Net Income', 'Year0'])
           
        

         

    # Define the function to assign a value
    def assign_values(self, df, values_dict):
        for (row_label, column_label), value in values_dict.items():
            df.at[row_label, column_label] = value

        
        # print(df.iloc[2])
        # print(df.iloc[3])
        # print(df.iloc[5])
        #print(df.dtypes)

    

    
    
    def upload_to_database(self, df, table_name):
        # Create a SQLAlchemy engine
        #df = df.applymap(lambda x: x.astype(int) if isinstance(x, np.int64) else x)
        engine = create_engine('postgresql://Campospa:2883@localhost/statements')
        

        #Create a session
        Session = sessionmaker(bind=engine)
        session = Session()

        # Insert the data into the specified table
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        

        

    def clear_database(self):
        with self.Session() as session:
            # Iterate over all tables and delete their contents
            for table in Base.metadata.sorted_tables:
                session.execute(table.delete())
            # Commit the transaction
            session.commit()
        print("Database cleared successfully.")


    

   ########################################################################################### 

    
def populate_assumptions_future(self):
        # Define metrics that should be formatted as percentages and raw numbers
        percentage_metrics = [
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
    
        raw_number_metrics = [
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
        def format_value(value, is_percentage=False):
            if is_percentage:
                return "{:.1%}".format(value)
            else:
                return "{:.2f}".format(value)

        for metric in percentage_metrics:
            same_value = input(f"Do you want to enter the same value for all years for {metric}? (yes/no): ").strip().lower()
            
            if same_value == 'yes':
                value = get_user_input(f"Enter {metric} (as a decimal, e.g., 0.06 for 6%): ")
                formatted_value = format_value(value, is_percentage=True)
                self.assumptions.loc[metric, :] = formatted_value
            else:
                for year in self.years:
                    prompt = f"Enter {metric} for {year} (as a decimal, e.g., 0.06 for 6%): "
                    value = get_user_input(prompt)
                    self.assumptions.at[metric, year] = format_value(value, is_percentage=True)

        for metric in raw_number_metrics:
            same_value = input(f"Do you want to enter the same value for all years for {metric}? (yes/no): ").strip().lower()
            
            if same_value == 'yes':
                value = get_user_input(f"Enter {metric}: ")
                formatted_value = format_value(value, is_percentage=False)
                self.assumptions.loc[metric, :] = formatted_value
            else:
                for year in self.years:
                    prompt = f"Enter {metric} for {year}: "
                    value = get_user_input(prompt)
                    self.assumptions.at[metric, year] = format_value(value, is_percentage=False)



    # Forecast future periods for income statement, balance sheet and cash flows 
def forecast_statements(self):
        # Helper method to format values
        def format_fixed_cost(value):
            try:
                return "{:.2f}".format(float(value))
            except ValueError:
                return "N/A"
        #Revenues
            # Initialize a dictionary to hold forecasted revenues
        forecasted_revenues = {}
        
        #try:
            # Get current revenue from Year1
        revenue_current = float(self.income_statement.at['Revenues', 'Year-1'])
            
            # Forecast revenues for Years 1 to 5
        for year in range(1, 6):
            forecasted_revenue = revenue_current * (1 + self.assumptions['Sales Growth', 'Year-1'])
            forecasted_revenues[f'Year{year}'] = format_fixed_cost(forecasted_revenue)
                    
                # Update current revenue for next year
        revenue_current = forecasted_revenue
            
            # Assign forecasted revenues to the assumptions DataFrame
        for year in range(1, 6):
                self.income_statement.at['Forecasted Revenues', f'Year{year}'] = forecasted_revenues[f'Year{year}']
        
        #except (ValueError, KeyError):
            # Handle errors by setting all forecasts to "N/A"
            #for year in range(1, 6):
                #self.income_statement.at['Forecasted Revenues', f'Year{year}'] = "N/A"
       




###############################################################################################
'''


    # Define functions to work with working capital
    def populate_working_capital_historical(self):
            # Define metrics that should be formatted as percentages and raw numbers
            percentage_metrics = ['Income Tax Payable (Percent of Taxes)', 'Depreciation (Percent of Sales)']
        
            raw_number_metrics = ['Revenue', 'Cost of Goods Sold','Taxes','Trade and Other Receivables',
                                'Inventory', 'Trade and Other Payables',
                                'Income Tax Payable', 'Cash from Working Capital Items',
                                'Revenue', 'Capital Asset Turnover Ratio', 'Beginning of Period',
                                'Capital Expenditures/Additions (Disposals)', 'Depreciation Expense',
                                'Net PP&E, End of Period']

            # A function to calculate the percentage metrics
            def calculate_percent_metrics(metric):
                pass



            # A function to calculate raw number metrics
            def calculate_raw_number_metrics(metric):
                pass



            # Populate DataFrame with calculated values
            for metric in percentage_metrics:
                value = calculate_percent_metrics(metric)
                formatted_value = "{:.2%}".format(value)

            # Assign value to the working capital DataFrame
            self.working_capital.loc[metric, :] = formatted_value

            # Populate Dataframe with raw number metrics
            for metric in raw_number_metrics:
                value = calculate_raw_number_metrics(metric)
                formatted_value = "{:.2f}".format(value)

            # assign values to the workinf capital DataFrame
            self.working_capital.loc[metric, :] = formatted_value
'''                   



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
    #analysis.populated_assumptions_historical()
    #analysis.insert_assumptions_data(values_dict)
    # analysis.populate_assumptions_future()
    # analysis.populate_working_capital_historical()
    # analysis.forecast_statements()
    #analysis.upload_to_database(analysis.assumptions, 'assumptions') # works but inserts zero except for long ther debt , common share capital
    analysis.clear_database()
    
    
    
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
    # print(analysis.assumptions)
    #print(analysis.income_statement)
    #print(analysis.working_capital)  # Don't call this until ready
    #print(analysis.capital_structure)
    

if __name__ == '__main__':
    main()
