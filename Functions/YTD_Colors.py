import numpy as np

def YTD_Colors(data):
    # Assign colors to the bars based on your conditions
    colors = np.where(
        (data["Budget"] == 0),
        "orange",
        np.where(
            (data["Spent"] > data["Budget"]),
            "red",
            "green",
        ),
    )
    return colors