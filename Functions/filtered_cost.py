def filtered_months_data(*months):
    # Initialize dictionaries to store filtered data for each category
    filtered_data = {
        "Fixed Costs": [],
        "Variable Costs": []
    }

    # Loop through each month's DataFrame
    for month in months:
        # Filter data for 'Fixed Costs' and 'Variable Costs'
        filtered_data["Fixed Costs"].append(month[month["Category"] == "Fixed Costs"])
        filtered_data["Variable Costs"].append(month[month["Category"] == "Variable Costs"])
    
    # Return the filtered data as a dictionary
    return filtered_data

