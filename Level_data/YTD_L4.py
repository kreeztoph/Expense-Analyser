
def YTD_L4(monthly_data):
    """
    Combine fixed and variable costs for an arbitrary number of months.

    Args:
        monthly_data: A dictionary where keys are month names
                      and values are tuples of (fixed_data, variable_data).

    Returns:
        combined_L4_Fixed: Aggregated fixed data across all months.
        combined_L4_Variable: Aggregated variable data across all months.
    """
    # Initialize empty dataframes for fixed and variable costs
    combined_L4_Fixed = None
    combined_L4_Variable = None

    for month, (fix_data, var_data) in monthly_data.items():
        # Grouping and summing fixed and variable data for the month
        fix_data = fix_data.groupby(['Order','L3','L4'])[
            ["Main", "1st Comparison", "Var Comp&Main"]
        ].sum()
        var_data = var_data.groupby(['Order','L3','L4'])[
            ["Main", "1st Comparison", "Var Comp&Main"]
        ].sum()

        # Add the current month's data to the combined dataframes
        if combined_L4_Fixed is None:
            combined_L4_Fixed = fix_data
        else:
            combined_L4_Fixed = combined_L4_Fixed.add(fix_data, fill_value=0)

        if combined_L4_Variable is None:
            combined_L4_Variable = var_data
        else:
            combined_L4_Variable = combined_L4_Variable.add(var_data, fill_value=0)

    # Resetting indices and rounding
    combined_L4_Fixed = combined_L4_Fixed.reset_index().round(2)
    combined_L4_Variable = combined_L4_Variable.reset_index()

    combined_L4_Fixed.columns = [
        "Order",
        "L3",
        "L4",
        "Total Main",
        "Total Budget",
        "Total Difference",
    ]
    combined_L4_Variable.columns = [
        "Order",
        "L3",
        "L4",
        "Total Main",
        "Total Budget",
        "Total Difference",
    ]

    return combined_L4_Fixed, combined_L4_Variable
