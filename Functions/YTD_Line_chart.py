import plotly.express as px

def YTD_LineChart(data):
    fig = px.line(
        data,
        x="Month",
        y=["Spent", "Budget"],
        title="Budget vs. Spent Over Months",
        labels={"value": "Amount", "Month": "Month"},
        color_discrete_sequence=["red", "green"],  # Optional customization for colors
    )
    return fig