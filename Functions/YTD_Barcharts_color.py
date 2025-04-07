import numpy as np

def Barcharts_YTD_Colors(data):
    colors = np.where(
        (data["Total Budget"] == 0),
        "orange",
        np.where(
            (data["Total Main"] > data["Total Budget"]),
            "red",
            "green",
        ),
    )
    return colors