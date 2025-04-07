import streamlit as st

from Functions.Color_code import color_code

def Dataframes_ranked(data,column):
    # Apply styling to the 'Order' column based on 'Delta'
    if "Total Difference" in data.columns:
        styled_df = data.style.apply(
            lambda row: [
                (color_code(row, "Total Difference") if col == column  else "")
                for col in data.columns
            ],
            axis=1,
        )
        # Display in Streamlit
        st.dataframe(
            styled_df,
            use_container_width=True,
            column_config={
                "Total Difference": st.column_config.NumberColumn(format="%.2f"),
                "Total Budget": st.column_config.NumberColumn(format="%.2f"),
                "Total Main": st.column_config.NumberColumn(format="%.2f"),
            },
        )
    else:
        st.error("Column 'Total Difference' is missing from the DataFrame")
