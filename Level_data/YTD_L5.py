
def YTD_L5(monthly_data):
    """
    Combine fixed and variable costs for an arbitrary number of months.
    
    Args:
        monthly_data: A dictionary where keys are month names
                      and values are tuples of (fixed_data, variable_data).
    
    Returns:
        combined_L5_Fixed: Aggregated fixed data across all months.
        combined_L5_Variable: Aggregated variable data across all months.
    """
    # Initialize empty dataframes for fixed and variable costs
    combined_L5_Fixed = None
    combined_L5_Variable = None

    for month, (fix_data, var_data) in monthly_data.items():
        # Grouping and summing fixed and variable data for the month
        fix_data = fix_data.groupby(['Order','L3','L4','AccountAndDescpription'])[["Main", "1st Comparison", "Var Comp&Main"]].sum()
        var_data = var_data.groupby(['Order','L3','L4','AccountAndDescpription'])[["Main", "1st Comparison", "Var Comp&Main"]].sum()
        
        # Add the current month's data to the combined dataframes
        if combined_L5_Fixed is None:
            combined_L5_Fixed = fix_data
        else:
            combined_L5_Fixed = combined_L5_Fixed.add(fix_data, fill_value=0)
        
        if combined_L5_Variable is None:
            combined_L5_Variable = var_data
        else:
            combined_L5_Variable = combined_L5_Variable.add(var_data, fill_value=0)
    
    # Resetting indices and rounding
    combined_L5_Fixed = combined_L5_Fixed.reset_index().round(2)
    combined_L5_Variable = combined_L5_Variable.reset_index()

    combined_L5_Fixed.columns = [
        "Order",
        "L3",
        "L4",
        "AccountAndDescpription",
        "Total Main",
        "Total Budget",
        "Total Difference",
    ]
    combined_L5_Variable.columns = [
        "Order",
        "L3",
        "L4",
        "AccountAndDescpription",
        "Total Main",
        "Total Budget",
        "Total Difference",
    ]

    return combined_L5_Fixed, combined_L5_Variable