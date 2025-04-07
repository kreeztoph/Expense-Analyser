def L5_YTD_Filtered(category_L2, category_L3, category_L4, category_L5, data):
    # Apply the filter
    if category_L4 != "All":
        if category_L5 != "All":
            filtered_df = data[
                (data["L4"] == category_L4)
                & (data["L3"] == category_L3)
                & (data["Order"] == category_L2)
                & (data["AccountAndDescpription"] == category_L5)
            ]
            filtered_df = filtered_df.sort_values(by="Total Difference", ascending=True)
        else:
            filtered_df = data[
                data["L4"] == category_L4
            ]
            filtered_df = filtered_df.sort_values(by="Total Difference", ascending=True)
    else:
        filtered_df = data[data["L4"] == category_L4]
        filtered_df = filtered_df.sort_values(by="Total Difference", ascending=True)
    return filtered_df