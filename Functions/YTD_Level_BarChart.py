import plotly.graph_objects as go

from Functions.YTD_Barcharts_color import Barcharts_YTD_Colors


def Levels_BarChart(data,column):
    # Create a grouped bar chart
    fig = go.Figure()

    # Add first column for Budget
    fig.add_trace(
        go.Bar(
            name="Budget",
            x=data[column],
            y=data["Total Budget"],
            marker_color="blue",  # Fixed color for Budget
        )
    )

    # Add second column for Spent with dynamic colors
    fig.add_trace(
        go.Bar(
            name="Spent",
            x=data[column],
            y=data["Total Main"],
            marker_color=Barcharts_YTD_Colors(data),  # Colors based on conditions
        )
    )

    # Update layout for better visualization
    fig.update_layout(
        xaxis_title="Categories",
        yaxis_title="Values",
        barmode="group",  # Group bars
    )
    return fig