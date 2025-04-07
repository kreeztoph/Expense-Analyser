import plotly.graph_objects as go

def YTD_Barchart(data,colors):
    # Create a grouped bar chart
    fig = go.Figure()

    # Add first column for Budget
    fig.add_trace(
        go.Bar(
            name="Budget",
            x=data["Month"],
            y=data["Budget"],
            marker_color="blue",  # Variable color for Budget
        )
    )

    # Add second column for Spent with dynamic colors
    fig.add_trace(
        go.Bar(
            name="Spent",
            x=data["Month"],
            y=data["Spent"],
            marker_color=colors,  # Colors based on conditions
        )
    )

    # Update layout for better visualization
    fig.update_layout(
        xaxis_title="Months",
        yaxis_title="Values",
        barmode="group",  # Group bars
    )
    return fig
