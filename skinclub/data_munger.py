import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import csv

## Process skinclub_database.csv
# Import Data
df = pd.read_csv('skinclub_database.csv') 

# Convert -null- wear into 'nw' (no wear)
df.loc[ df['wear'] == ' ', 'wear'] = 'nw'

## Calculate & Convert Units
df['price'] = df['price'].str.replace('$', '').astype(float)
df['cost'] = df['cost'].str.replace('$', '').astype(float)
df['odds'] = df['odds'].str.replace('%', '').astype(float)

df['return'] = df['price'] - df['cost']
df['return_p'] = ((df['price'] / df['cost'])*100)-100

df.to_csv("skinclub_database_processed.csv",index=False)

## Case by Case Statistics
cases = pd.unique(df['case'])
''' Legend ~~~
    cases               = Case Name
    cost                = Cost per Open
    ROI                 = Avg Rate of Investment
    Outcomes            = Number of Outcomes
    Profit_Chance       = Chance to Breakeven/Profit
    Profit_Stat         = Minimum Roll to Breakeven/Profit
    Min_Return          = Lowest Possible Return ($)
    Min_Return_p        = Lowest Possible Return (%)
    Avg_loss_return     = Avg Loss on a losing roll ($) 
    Avg_loss_return_p   = Avg Loss on a losing roll (%) 
    Max_Return          = Maximum Possible Return ($)
    Max_Return_p        = Maximum Possible Return (%)
    Avg_gain_return     = Avg Gain on a winning roll ($)
    Avg_gain_return_p   = Avg Gain on a winning roll (%)
    Roll_50             = Theretical 50 roll return ($)
    Roll_50_p           = Theretical 50 roll return (%)
    Roll_100            = Theretical 100 roll return ($)
    Roll_100_p          = Theretical 100 roll return (%)
    Roll_1000           = Theretical 1000 roll return ($)
    Roll_1000_p         = Theretical 1000 roll return (%)
    '''
with open('case_stats.csv', 'w', newline='', encoding='utf-8') as file:

    # Set-Up CSV output
    writer = csv.writer(file)
    fields = ['case', 'cost', 'ROI', 'Outcomes', 'Profit_Chance', 'Profit_Stat', 'Min_Return', 'Min_Return_p', 'Avg_loss_return', 'Avg_loss_return_p', 'Max_Return',
        'Max_Return_p', 'Avg_gain_return', 'Avg_gain_return_p', 'Roll_50', 'Roll_50_p', 'Roll_100', 'Roll_100_p', 'Roll_1000', 'Roll_1000_p', 'Roll_100000', 'Roll_100000_p']
    writer.writerow(['case', 'cost', 'ROI', 'Outcomes', 'Profit_Chance', 'Profit_Stat', 'Min_Return', 'Min_Return_p', 'Avg_loss_return', 'Avg_loss_return_p', 'Max_Return',
        'Max_Return_p', 'Avg_gain_return', 'Avg_gain_return_p', 'Roll_50', 'Roll_50_p', 'Roll_100', 'Roll_100_p', 'Roll_1000', 'Roll_1000_p', 'Roll_100000', 'Roll_100000_p'])
    
    # Loop thru each case
    for case in cases:
        
        # Isolate Each Case
        data = df.loc[df['case'] == case]

        # Determine No of Outcomes
        Outcomes, col = data.shape

        # Reset indexing for counter
        data = data.reset_index(drop=True)

        # Determine Cost
        cost = data.at[1,'cost']

        # Calculate ROI
        Net_Profit = 0
        for n in range(Outcomes):
            odd_val = data.at[n,'odds']
            ret_val = data.at[n,'return']
            calc = (odd_val * ret_val)
            Net_Profit += calc
        ROI = (Net_Profit / cost) * 100

        # Gain Calculations
        gain_set = data[data['price'] >= data['cost']]

            # Determine No of Outcomes
        Pos_results, col = gain_set.shape

            # Reset indexing for counter
        gain_set = gain_set.reset_index(drop=True)

            # Calculate Avg Positive Return
        Avg_gain_return = 0
        for n in range(Pos_results):
            odd_val = gain_set.at[n,'odds']
            ret_val = gain_set.at[n,'return']
            calc = (odd_val * ret_val)
            Avg_gain_return += calc
        Avg_gain_return_p = Avg_gain_return/cost

            # Calculate Max Gain
        stats = gain_set['return']
        Max_Return = stats.max()
        stats = gain_set['return_p']
        Max_Return_p = stats.max()
        
        # Breakeven Calculations
        stats = gain_set['min_val']
        Profit_Stat = stats.min()
        Profit_Chance = (100000-Profit_Stat)/1000

        # Loss Calculations
        loss_set = data[data['price'] < data['cost']]

            # Determine No of Outcomes
        Neg_results, col = loss_set.shape

            # Reset indexing for counter
        loss_set = loss_set.reset_index(drop=True)

            # Calculate Avg Negative Return
        Avg_loss_return = 0
        for n in range(Neg_results):
            odd_val = loss_set.at[n,'odds']
            ret_val = loss_set.at[n,'return']
            calc = (odd_val * ret_val)
            Avg_loss_return += calc
        Avg_loss_return_p = Avg_loss_return/cost

            # Calculate Min Gain
        stats = loss_set['return']
        Min_Return = stats.min()
        stats = loss_set['return_p']
        Min_Return_p = stats.min()

        ## Theoretical Rolls
            # Roll Calculations
            # ~50 Rolls
        data['roll50'] = round((data['odds']/100)* 50)
        no_roll = data['roll50'].sum()
        data['prof'] = data['roll50'] * data['price']
        Roll_50 = (data['prof'].sum()) - (no_roll * cost)
        Roll_50_p = Roll_50/(no_roll * cost) * 100
            # ~100 Rolls
        data['roll100'] = round((data['odds']/100)* 100)
        no_roll = data['roll100'].sum()
        data['prof'] = data['roll100'] * data['price']
        Roll_100 = (data['prof'].sum()) - (no_roll * cost)
        Roll_100_p = Roll_100/(no_roll * cost) * 100
            # ~1000 Rolls
        data['roll1000'] = round((data['odds']/100)* 1000)
        no_roll = data['roll1000'].sum()
        data['prof'] = data['roll1000'] * data['price']
        Roll_1000 = (data['prof'].sum()) - (no_roll * cost)
        Roll_1000_p = Roll_1000/(no_roll * cost) * 100
            ## ~100000 Rolls
        data['roll100000'] = round((data['odds']/100)* 100000)
        no_roll = data['roll100000'].sum()
        data['prof'] = data['roll100000'] * data['price']
        Roll_100000 = (data['prof'].sum()) - (no_roll * cost)
        Roll_100000_p = Roll_100000/(no_roll * cost) * 100

        print(case, cost, ROI, Outcomes, Profit_Chance, Profit_Stat, Min_Return, Min_Return_p, Avg_loss_return, Avg_loss_return_p, Max_Return,
                          Max_Return_p, Avg_gain_return, Avg_gain_return_p, Roll_50, Roll_50_p, Roll_100, Roll_100_p, Roll_1000, Roll_1000_p, Roll_100000, Roll_100000_p)
        writer.writerow([case, cost, ROI, Outcomes, Profit_Chance, Profit_Stat, Min_Return, Min_Return_p, Avg_loss_return, Avg_loss_return_p, Max_Return,
                          Max_Return_p, Avg_gain_return, Avg_gain_return_p, Roll_50, Roll_50_p, Roll_100, Roll_100_p, Roll_1000, Roll_1000_p, Roll_100000, Roll_100000_p])

#print(cases)
## Gather individual cases and add more data into listings

