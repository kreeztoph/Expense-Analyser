import pandas as pd

def filtered_months_data(*months):
    filtered_data = {
        "Fixed Costs": [],
        "Variable Costs": []
    }

    # Define the default DataFrame
    default_df = pd.DataFrame({
        'Order': ['N/A'],
        'L3': ['N/A'],
        'L4': ['N/A'],
        'AccountAndDescpription': ['N/A'],
        'Main': [0],
        '1st Comparison': [0],
        'Var Comp&Main': [0]
    })

    

    for idx, month in enumerate(months):
        # Modify your condition
        if month.empty or "Category" not in month.columns:
            # If empty or missing "Category", append default DataFrames
            filtered_data["Fixed Costs"].append(default_df)
            filtered_data["Variable Costs"].append(default_df)
        else:
            # Otherwise filter normally
            filtered_data["Fixed Costs"].append(month[month["Category"] == "Fixed Costs"])
            filtered_data["Variable Costs"].append(month[month["Category"] == "Variable Costs"])
    
    return filtered_data
