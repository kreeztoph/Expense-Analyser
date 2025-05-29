import pandas as pd

def YTD_L3(monthly_data):
    """
    Combine fixed and variable costs for an arbitrary number of months.

    Args:
        monthly_data: A dictionary where keys are month names
                      and values are tuples of (fixed_data, variable_data).

    Returns:
        combined_L3_Fixed: Aggregated fixed data across all months.
        combined_L3_Variable: Aggregated variable data across all months.
    """
    combined_L3_Fixed = None
    combined_L3_Variable = None
    has_data = False

    for month, (fix_data, var_data) in monthly_data.items():
        # Skip if both are completely empty
        if fix_data.empty and var_data.empty:
            continue

        has_data = True

        if not fix_data.empty:
            fix_data = fix_data.groupby(["Order", "L3"])[
                ["Main", "1st Comparison", "Var Comp&Main"]
            ].sum()
            combined_L3_Fixed = fix_data if combined_L3_Fixed is None else combined_L3_Fixed.add(fix_data, fill_value=0)

        if not var_data.empty:
            var_data = var_data.groupby(["Order", "L3"])[
                ["Main", "1st Comparison", "Var Comp&Main"]
            ].sum()
            combined_L3_Variable = var_data if combined_L3_Variable is None else combined_L3_Variable.add(var_data, fill_value=0)

    # Define final column names
    column_names = ["Order", "L3", "Total Main", "Total Budget", "Total Difference"]

    if not has_data:
        # Return empty DataFrames with expected structure if no data at all
        return (
            pd.DataFrame(columns=column_names),
            pd.DataFrame(columns=column_names)
        )

    # Reset index and rename columns
    if combined_L3_Fixed is not None:
        combined_L3_Fixed = combined_L3_Fixed.reset_index().round(2)
        combined_L3_Fixed.columns = column_names
    else:
        combined_L3_Fixed = pd.DataFrame(columns=column_names)

    if combined_L3_Variable is not None:
        combined_L3_Variable = combined_L3_Variable.reset_index().round(2)
        combined_L3_Variable.columns = column_names
    else:
        combined_L3_Variable = pd.DataFrame(columns=column_names)

    return combined_L3_Fixed.fillna(0), combined_L3_Variable.fillna(0)
