import pandas as pd

def YTD_L2(monthly_data):
    """
    Combine fixed and variable costs for an arbitrary number of months.
    
    Args:
        monthly_data: A dictionary where keys are month names
                      and values are tuples of (fixed_data, variable_data).
    
    Returns:
        combined_L2_Fixed: Aggregated fixed data across all months.
        combined_L2_Variable: Aggregated variable data across all months.
    """
    combined_L2_Fixed = None
    combined_L2_Variable = None
    has_data = False

    for month, (fix_data, var_data) in monthly_data.items():
        # Skip if both datasets are completely empty
        if fix_data.empty and var_data.empty:
            continue
        
        has_data = True

        # Group and sum the data (only if not empty)
        if not fix_data.empty:
            fix_data = fix_data.groupby("Order")[["Main", "1st Comparison", "Var Comp&Main"]].sum()
            combined_L2_Fixed = fix_data if combined_L2_Fixed is None else combined_L2_Fixed.add(fix_data, fill_value=0)

        if not var_data.empty:
            var_data = var_data.groupby("Order")[["Main", "1st Comparison", "Var Comp&Main"]].sum()
            combined_L2_Variable = var_data if combined_L2_Variable is None else combined_L2_Variable.add(var_data, fill_value=0)

    # Create empty default DataFrame with zero values if no data exists
    if not has_data:
        empty_df = pd.DataFrame(columns=["Order", "Total Main", "Total Budget", "Total Difference"])
        return (
            pd.DataFrame(columns=empty_df.columns).assign(**{
                "Order": [],
                "Total Main": [],
                "Total Budget": [],
                "Total Difference": [],
            }).fillna(0),
            pd.DataFrame(columns=empty_df.columns).assign(**{
                "Order": [],
                "Total Main": [],
                "Total Budget": [],
                "Total Difference": [],
            }).fillna(0),
        )

    # Final formatting
    if combined_L2_Fixed is not None:
        combined_L2_Fixed = combined_L2_Fixed.reset_index().round(2)
        combined_L2_Fixed.columns = ["Order", "Total Main", "Total Budget", "Total Difference"]
    else:
        combined_L2_Fixed = pd.DataFrame(columns=["Order", "Total Main", "Total Budget", "Total Difference"])

    if combined_L2_Variable is not None:
        combined_L2_Variable = combined_L2_Variable.reset_index().round(2)
        combined_L2_Variable.columns = ["Order", "Total Main", "Total Budget", "Total Difference"]
    else:
        combined_L2_Variable = pd.DataFrame(columns=["Order", "Total Main", "Total Budget", "Total Difference"])

    return combined_L2_Fixed.fillna(0), combined_L2_Variable.fillna(0)
