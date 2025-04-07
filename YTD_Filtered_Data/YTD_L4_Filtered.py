def L4_YTD_Filtered(categpry_L4,category_L3,categoty_L2,data):
    # Apply the filter
    if category_L3 != "All":
        if categpry_L4 != "All":
            filtered_df = data[
                (data["L4"] == categpry_L4)
                & (data["L3"] == category_L3)
                & (data["Order"] == categoty_L2)
            ]
            filtered_df = filtered_df.sort_values(by="Total Difference", ascending=True)
        else:
            filtered_df = data[
                data["L3"] == category_L3
            ]
            filtered_df = filtered_df.sort_values(by="Total Difference", ascending=True)
    else:
        filtered_df = data[data["L3"] == category_L3]
        filtered_df = filtered_df.sort_values(by="Total Difference", ascending=True)
    return filtered_df