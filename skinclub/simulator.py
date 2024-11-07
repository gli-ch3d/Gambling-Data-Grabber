import pandas as pd
import random

def simulate(case_name, no_of_cases=1, csv_file_path='skinclub_database_processed.csv'):
    """
    Simulate random results for the given case.

    Args:
    - case_name (str): The name of the case to simulate.
    - no_of_cases (int): The number of cases to roll to generate. Default is 1.
    - csv_file_path (str): The file path of the CSV file. Default is 'skinclub_database_processed.csv'.

    Returns:
    - DataFrame: The DataFrame containing the results.
    """
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)

    results = pd.DataFrame()
   
    # Filter rows based on case_name
    filtered_df = df[df['case'] == case_name]

    # Generate and print random numbers for each case
    for _ in range(no_of_cases):
        random_number = random.randint(1, 100000)
        print(f"Random Number for '{case_name}': {random_number}")

        # Find the row where min_val <= random_number <= max_val
        result_row = filtered_df[(filtered_df['min_val'] <= random_number) & (random_number <= filtered_df['max_val'])]
        result_row = result_row[['case', 'cost', 'type', 'skin', 'rarity', 'wear', 'ST', 'price', 'odds', 'return', 'return_p']]
        if not results.empty:
            results = pd.concat([results, result_row], ignore_index=True)
        else:
            results = result_row.reset_index(drop=True)
        print("Result:")
        print(result_row)
        print("\n")
    print(results)
    return results

# Example usage:
simulate('Farm Knife Case',5)
