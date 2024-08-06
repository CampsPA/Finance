import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



# Create a class to fetch data and perform analysis

class Analysis:
    def __init__(self):
        self.income_statement = pd.DataFrame()
        self.balance_sheet = pd.DataFrame()
        self.cash_flow = pd.DataFrame()
        self.cash_flow = pd.DataFrame()
        self.assumptions = pd.DataFrame()
        

    def get_statements_data(self):
        #self.data =  "C:/Users/campo/OneDrive/Desktop/Statements.xlsx"
        self.data =  "C:/Users/campo/OneDrive/Desktop/Statements2.xlsx"
        
        

    def statements(self):
        self.assumptions = pd.read_excel(self.data, sheet_name = 'Assumptions', index_col= 'Metrics')
        #self.assumptions = self.assumptions[['Year2','Year1','Year0']]
        self.income_statement = pd.read_excel(self.data, sheet_name='Income Statement', index_col='Income Statement')
        self.balance_sheet = pd.read_excel(self.data, sheet_name='Balance Sheet', index_col='Balance Sheet')
        self.cash_flow =  pd.read_excel(self.data, sheet_name='Cash Flows', index_col='Cash Flows')
        self.assumptions = self.assumptions.astype(str)



    def populated_assumptions_historical(self):
        
        # Helper method to format values
        def format_percentage(value):
            return "{:.1%}".format(value)

        def format_fixed_cost(value):
            try:
                return "{:.0f}".format(float(value))
            except ValueError:
                return "N/A"

        #Sales growth
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
        self.long_term_debt_2 = format_fixed_cost(self.assumptions.at['Long Term Debt', 'Year2'] = self.balance_sheet.at['Long-Term Debt', 'Year2'])
        self.long_term_debt_1 = format_fixed_cost(self.assumptions.at['Long Term Debt', 'Year1'] = self.balance_sheet.at['Long-Term Debt', 'Year1'])
        self.long_term_debt_0 = format_fixed_cost(self.assumptions.at['Long Term Debt', 'Year0'] = self.balance_sheet.at['Long-Term Debt', 'Year0']) 

        #Common Share Capital




    # Define the function to assign a value
    def assign_values(self, df, values_dict):
        for (row_label, column_label), value in values_dict.items():
            df.at[row_label, column_label] = value


# Run the program
if __name__ == '__main__':
    analysis = Analysis()
    analysis.get_statements_data()
    analysis.statements()
    analysis.populated_assumptions_historical()
    

        
    

   
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
          ('Inventory Days (COGS Basis)                       (Days)', 'Year-2'): analysis.inv_days_2,
          ('Inventory Days (COGS Basis)                       (Days)', 'Year-1'): analysis.inv_days_1,
          ('Inventory Days (COGS Basis)                       (Days)', 'Year-0'): analysis.inv_days_0,
          ('Payable Days (COGS Basis)                          (Days)', 'Year-2'): analysis.payable_days_2,
          ('Payable Days (COGS Basis)                          (Days)', 'Year-1'): analysis.payable_days_1,
          ('Payable Days (COGS Basis)                          (Days)', 'Year-0'): analysis.payable_days_0,
          ('Income Tax Payable (Percent of Taxes) (Days)', 'Year-2'): analysis.inc_tax_pay_2,
          ('Income Tax Payable (Percent of Taxes) (Days)', 'Year-1'): analysis.inc_tax_pay_1,
          ('Income Tax Payable (Percent of Taxes) (Days)', 'Year-0'): analysis.inc_tax_pay_0,
          ('Long Term Debt', 'Year-2'): analysis.long_term_debt_2,
          ('Long Term Debt', 'Year-1'): analysis.long_term_debt_1,
          ('Long Term Debt', 'Year-0'): analysis.long_term_debt_0,
        #  ('Common Share Capital', 'Year-2'): analysis.common_share_cap_2,
        #  ('Common Share Capital', 'Year-1'): analysis.common_share_cap_1,
        #  ('Common Share Capital', 'Year-0'): analysis.common_share_cap_0,
        #  ('Dividend Payout Ratio ', 'Year-2'): analysis.div_payout_ratio_2,
        #  ('Dividend Payout Ratio ', 'Year-1'): analysis.div_payout_ratio_1,
        #  ('Dividend Payout Ratio ', 'Year-0'): analysis.div_payout_ratio_0,   
     }
  



analysis.assign_values(analysis.assumptions, values_dict)



#print(analysis.assumptions.columns)
print(analysis.assumptions)
#print(analysis.income_statement)
#print(analysis.balance_sheet)
#print(analysis.cash_flow)





