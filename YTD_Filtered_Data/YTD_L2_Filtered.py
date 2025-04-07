import pandas as pd

def L2_Filtered_data(category,data):
    # Apply the filter
    if category != "All":
        filtered_df = data[
            (data["Order"] == category)
            & (data["Order"] == category)
        ]
        filtered_df = filtered_df.sort_values(
            by="Total Difference", ascending=True
        )
    else:
        filtered_df = data
        filtered_df = filtered_df.sort_values(
            by="Total Difference", ascending=True
        )
    filtered_df.columns = filtered_df.columns.str.strip()
    filtered_df[["Total Main", "Total Budget", "Total Difference"]] = (
        filtered_df[
            ["Total Main", "Total Budget", "Total Difference"]
        ].apply(pd.to_numeric, errors="coerce")
    )
    
    return filtered_df