import pandas as pd
import plotly.express as px

def YTD_SunBurst(*months):
    # Initialize empty lists for Cost, Month, and Values
    costs = []
    months_list = []
    values = []

    # Iterate over each month provided in the arguments
    month_names = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

    for i, month in enumerate(months):
        if i < len(month_names):
            month_name = month_names[i]  # Get the corresponding month name
        else:
            month_name = f"Month {i + 1}"  # Fallback for additional months without a predefined name

        # Append fixed and variable costs for the current month
        costs.append("Fixed Cost")
        months_list.append(month_name)
        values.append(month[month["Category"] == "Fixed Costs"]["Main"].sum())

        costs.append("Variable Cost")
        months_list.append(month_name)
        values.append(month[month["Category"] == "Variable Costs"]["Main"].sum())

    # Create the data dictionary dynamically
    data = {
        "Cost": costs,
        "Month": months_list,
        "Values": values,
    }

    # Convert the data dictionary into a DataFrame
    sun_burst_df = pd.DataFrame(data)

    # Create sunburst chart with Plotly
    fig = px.sunburst(
        sun_burst_df,
        path=["Month", "Cost"],
        values="Values",
        title="Monthly Spending",
    )

    # Customize hover information
    fig.update_traces(
        hovertemplate="<b>%{label}</b><br>Value: £%{value}",
    )

    # Adjust chart size
    fig.update_layout(
        width=500,  # Set the width (adjust as needed)
        height=500,  # Set the height (adjust as needed)
    )

    return fig
