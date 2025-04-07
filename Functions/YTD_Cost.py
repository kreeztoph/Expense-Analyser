def YTD_Cost(*months):
    # Initialize variables for totals
    Fixed_cost_YTD_spent = 0
    Fixed_cost_YTD_Budget = 0
    Fixed_cost_YTD_Delta = 0
    Variable_cost_YTD_spent = 0
    Variable_cost_YTD_Budget = 0
    Variable_cost_YTD_Delta = 0

    # Loop through each month to calculate cumulative values
    for month in months:
        Fixed_cost_YTD_spent += month[month["Category"] == "Fixed Costs"]["Main"].sum()
        Fixed_cost_YTD_Budget += month[month["Category"] == "Fixed Costs"][
            "1st Comparison"
        ].sum()
        Fixed_cost_YTD_Delta += month[month["Category"] == "Fixed Costs"][
            "Var Comp&Main"
        ].sum()
        Variable_cost_YTD_spent += month[month["Category"] == "Variable Costs"][
            "Main"
        ].sum()
        Variable_cost_YTD_Budget += month[month["Category"] == "Variable Costs"][
            "1st Comparison"
        ].sum()
        Variable_cost_YTD_Delta += month[month["Category"] == "Variable Costs"][
            "Var Comp&Main"
        ].sum()

    # Calculate percentage deltas
    Fixed_Cost_YTD_Delta_Percent = (
        (Fixed_cost_YTD_Budget - Fixed_cost_YTD_spent) / Fixed_cost_YTD_Budget
    ) * 100
    Variable_Cost_YTD_Delta_Percent = (
        (Variable_cost_YTD_Budget - Variable_cost_YTD_spent) / Variable_cost_YTD_Budget
    ) * 100

    # Return results as a dictionary or tuple
    return (
        Fixed_cost_YTD_spent,
        Fixed_cost_YTD_Budget,
        Fixed_cost_YTD_Delta,
        Fixed_Cost_YTD_Delta_Percent,
        Variable_cost_YTD_spent,
        Variable_cost_YTD_Budget,
        Variable_cost_YTD_Delta,
        Variable_Cost_YTD_Delta_Percent,
    )
