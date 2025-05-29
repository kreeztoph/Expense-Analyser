import pandas as pd

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
    combined_L5_Fixed = None
    combined_L5_Variable = None
    has_data = False

    for month, (fix_data, var_data) in monthly_data.items():
        if fix_data.empty and var_data.empty:
            continue

        has_data = True

        if not fix_data.empty:
            fix_data = fix_data.groupby(['Order', 'L3', 'L4', 'AccountAndDescpription'])[
                ["Main", "1st Comparison", "Var Comp&Main"]
            ].sum()
            combined_L5_Fixed = fix_data if combined_L5_Fixed is None else combined_L5_Fixed.add(fix_data, fill_value=0)

        if not var_data.empty:
            var_data = var_data.groupby(['Order', 'L3', 'L4', 'AccountAndDescpription'])[
                ["Main", "1st Comparison", "Var Comp&Main"]
            ].sum()
            combined_L5_Variable = var_data if combined_L5_Variable is None else combined_L5_Variable.add(var_data, fill_value=0)

    # Define output columns
    column_names = [
        "Order",
        "L3",
        "L4",
        "AccountAndDescpription",
        "Total Main",
        "Total Budget",
        "Total Difference",
    ]

    if not has_data:
        return (
            pd.DataFrame(columns=column_names),
            pd.DataFrame(columns=column_names)
        )

    if combined_L5_Fixed is not None:
        combined_L5_Fixed = combined_L5_Fixed.reset_index().round(2)
        combined_L5_Fixed.columns = column_names
    else:
        combined_L5_Fixed = pd.DataFrame(columns=column_names)

    if combined_L5_Variable is not None:
        combined_L5_Variable = combined_L5_Variable.reset_index().round(2)
        combined_L5_Variable.columns = column_names
    else:
        combined_L5_Variable = pd.DataFrame(columns=column_names)

    return combined_L5_Fixed.fillna(0), combined_L5_Variable.fillna(0)
