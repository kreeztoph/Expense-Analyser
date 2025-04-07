def L3_YTD_Filtered(category_L3,category_L2,data_L3):
    # Apply the filter
    if category_L2 != "All":
        if category_L3 != "All":
            filtered_df = data_L3[
                (data_L3["L3"] == category_L3)
                & (data_L3["Order"] == category_L2)
            ]
            filtered_df = filtered_df.sort_values(by="Total Difference", ascending=True)
        else:
            filtered_df = data_L3[
                data_L3["Order"] == category_L2
            ]
            filtered_df = filtered_df.sort_values(by="Total Difference", ascending=True)
    else:
        filtered_df = data_L3[
            data_L3["Order"] == category_L2
        ]
        filtered_df = filtered_df.sort_values(by="Total Difference", ascending=True)
    return filtered_df