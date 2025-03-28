import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import numpy as np
import plotly.express as px

pd.options.display.float_format = "{:.2f}".format

# Centralized Streamlit Configuration and Introduction
logo_url = "Images/LCY3 Logo.png"
logo_url_2 = "Images/Amazon RME Logo.png"
st.set_page_config(page_title="Amazon RME Expense", page_icon=logo_url, layout="wide",menu_items={'Get Help': 'mailto:aakalkri@amazon.co.uk','Report a bug': "mailto:aakalkri@amazon.co.uk",'About': "Developed for LCY3 RME. Managed by @aakalkri."})
cols1, cols2,cols3 = st.columns([3,4,3],vertical_alignment="center",gap= 'small')  # This creates a 10% and 80% split
with cols1:
    st.image(logo_url, width=200)
with cols2:
    # Vertically center title
    title_html = """
    <div style="justify-content:bottom; align-items:center;">
        <h1 style='font-size: 40px; margin-left: 10%;'>
            <span style='color: #6CB4EE;'>Amazon LCY3</span> 
            <span style='color: #1D2951;'>Expenses Analysis</span>
        </h1>
    </div>
    """
    st.markdown(title_html, unsafe_allow_html=True)
with cols3:
    st.image(logo_url_2,width=200)
    
with st.expander(label='Click here to open upload tab!'):
    head_1,head_2,head_3 = st.columns([0.2,0.6,0.2])
    with head_2:
        # File uploader
        uploaded_file = st.file_uploader("Upload an Excel File", type="xlsx")

# Function to apply color coding
def color_code(row):
    if pd.isna(row["Delta"]) or row["Delta"] == 0:
        return "background-color: orange"  # Neutral
    elif row["Delta"] > 0:
        return "background-color: green"  # Positive delta
    else:
        return "background-color: red"  # Negative delta
       
# Function to apply color coding
def color_code_new(row,color_column):
    if pd.isna(row[color_column]) or row[color_column] == 0:
        return "background-color: orange"  # Neutral
    elif row[color_column] > 0:
        return "background-color: green"  # Positive delta
    else:
        return "background-color: red"  # Negative delta

if uploaded_file is not None:
    # Load the uploaded Excel file
    try:
        xls = pd.ExcelFile(uploaded_file)
        sheets = []

        # Iterate through sheets and create variables
        for sheet in xls.sheet_names:
            clean_name = sheet.replace(" ", "_").replace(
                "-", "_"
            )  # Replace spaces and dashes with underscores
            if not clean_name.isidentifier():
                clean_name = f"df_{clean_name}"  # Ensure valid variable names

            globals()[clean_name] = xls.parse(
                sheet
            )  # Create a global variable for the DataFrame
            sheets.append(clean_name)

        # Display the parsed sheets and their names
        # st.write("Sheets have been loaded successfully!")
        # st.write("Loaded sheet names:", sheets)

    except Exception as e:
        st.error(f"An error occurred while loading the Excel file: {e}")

    tab_1, tab_2, tab_3 = st.tabs(
        ["Monthly Analysis", "Yearly Analysis", "Comparative Analysis"]
    )
    # Inject CSS to evenly spread tabs
    st.markdown(
        """
        <style>
        .stTabs [data-baseweb="tab"] {
            flex: 1;
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    with tab_1:
        col_1, col_2, col_3 = st.columns(3)
        with col_1:
            month = st.selectbox(
                label="Select a Month", options=["January", "February","March"]
            )
        with col_2:
            year = st.selectbox(label="Select Year", options=["2025", "2026"])
        with col_3:
            data = st.selectbox(
                label="Select Cost", options=["Fixed Costs", "Variable Costs"]
            )
        if (month == "January") & (year == "2025") & (data == "Fixed Costs"):
            Jan_2025 = Jan_2025.iloc[:, 0:8]
            Jan_2025 = Jan_2025.fillna(0)
            jan_2025_complete = Jan_2025.groupby(["Category"]).sum(list).reset_index()
            Jan_2025_Fixed_Cost_Data = Jan_2025[(Jan_2025["Category"] == "Fixed Costs")]
            L1_Grouped = (
                Jan_2025_Fixed_Cost_Data.groupby(["Category"]).sum(list).reset_index()
            )
            L2_Grouped = (
                Jan_2025_Fixed_Cost_Data.groupby(["Category", "Order"])
                .sum(list)
                .reset_index()
            )
            L3_Grouped = (
                Jan_2025_Fixed_Cost_Data.groupby(["Category", "Order", "L3"])
                .sum(list)
                .reset_index()
            )
            L4_Grouped = (
                Jan_2025_Fixed_Cost_Data.groupby(["Category", "Order", "L3", "L4"])
                .sum(list)
                .reset_index()
            )
            L5_Grouped = (
                Jan_2025_Fixed_Cost_Data.groupby(
                    ["Category", "Order", "L3", "L4", "AccountAndDescpription"]
                )
                .sum(list)
                .reset_index()
            )

            grouped_dfs = {
                "L1_Grouped": ("Category", L1_Grouped),
                "L2_Grouped": ("Order", L2_Grouped),
                "L3_Grouped": ("L3", L3_Grouped),
                "L4_Grouped": ("L4", L4_Grouped),
                "L5_Grouped": ("AccountAndDescpription", L5_Grouped),
            }
            # Dictionary to store parsed DataFrames
            parsed_dfs = {}

            # Loop through each grouped DataFrame
            for key, (category_column, df) in grouped_dfs.items():
                data = []

                for _, row in df.iterrows():
                    budget, spent, delta = (
                        row["1st Comparison"],
                        row["Main"],
                        row["Var Comp&Main"],
                    )
                    data.append(
                        [row[category_column], budget, spent, delta]
                    )  # Dynamically get category column

                # Convert to DataFrame and store in dictionary
                parsed_dfs[key] = pd.DataFrame(
                    data, columns=["Category", "Budget", "Main", "Delta"]
                )
            # Access parsed DataFrames, e.g.:
            df_parsed_1 = parsed_dfs["L1_Grouped"]
            df_parsed_2 = parsed_dfs["L2_Grouped"]
            df_parsed_3 = parsed_dfs["L3_Grouped"]
            df_parsed_4 = parsed_dfs["L4_Grouped"]
            df_parsed_5 = parsed_dfs["L5_Grouped"]

            Jan_Budget = float(jan_2025_complete["1st Comparison"].sum())
            Jan_spent = float(jan_2025_complete["Main"].sum())
            Jan_Delta = float(jan_2025_complete["Var Comp&Main"].sum())
            Jan_delta_percent = (((Jan_Budget) - (Jan_spent)) / (Jan_Budget)) * 100
            Jan_Fixed_Budget = float(df_parsed_1["Budget"].iloc[0])
            Jan_Fixed_Spent = float(df_parsed_1["Main"].iloc[0])
            Jan_Fixed_Delta = float(df_parsed_1["Delta"].iloc[0])
            Jan_Fixed_Delta_Percent = (
                ((Jan_Fixed_Budget) - (Jan_Fixed_Spent)) / (Jan_Fixed_Budget)
            ) * 100
            cols1, cols2 = st.columns(2)
            with cols1:
                st.header("Monthly Summary")
            with cols2:
                st.header("Cost Summary")
            col1, col2, col3, col4, col5, col6 = st.columns(
                6, gap="medium", vertical_alignment="center"
            )
            with col1:
                st.metric(
                    "January Budget",
                    value=f"£{Jan_Budget:,.2f}",
                    border=True,
                    help="This is the total budget for January.",
                )
            with col2:
                st.metric(
                    "January Spent",
                    value=f"£{Jan_spent:,.2f}",
                    border=True,
                    help="This is the total amount of funds spent in January.",
                )
            with col3:
                st.metric(
                    "January Delta",
                    value=f"£{Jan_Delta:,.2f}",
                    border=True,
                    delta=f"{Jan_delta_percent:,.2f} %",
                    help="This is the difference in the amount budgeted and the amount spent for Janauary.",
                )
            with col4:
                st.metric(
                    "January Fixed Cost Budget",
                    value=f"£{Jan_Fixed_Budget:,.2f}",
                    border=True,
                    help="This is the total amount budgeted to be spent for Fixed Costs in January.",
                )
            with col5:
                st.metric(
                    "January Fixed Cost Spent",
                    value=f"£{Jan_Fixed_Spent:,.2f}",
                    border=True,
                    help="This is the total amount spent for Fixed Cost in Janauary.",
                )
            with col6:
                st.metric(
                    "January Fixed Cost Delta",
                    value=f"£{Jan_Fixed_Delta:,.2f}",
                    border=True,
                    delta=f"{Jan_Fixed_Delta_Percent:,.2f}%",
                    help="This is the difference in the budgeted amount and Spent amount for Fixed Costs in January.",
                )

            col21, col22 = st.columns(2, gap="medium", vertical_alignment="center")
            with col21:
                with st.container(height=500, border=False):
                    L2_Grouped = L2_Grouped.rename(
                        columns={
                            "Main": "Spent",
                            "1st Comparison": "Budget",
                            "Var Comp&Main": "Delta",
                        }
                    )
                    # User filter input
                    selected_category_Order = st.selectbox(
                        "Filter by Order:",
                        ["All"] + list(L2_Grouped["Order"].unique()),
                        key="FIlter by Order",
                    )

                    # Apply the filter
                    if selected_category_Order != "All":
                        filtered_df = L2_Grouped[
                            (L2_Grouped["Order"] == selected_category_Order)
                            & (L2_Grouped["Order"] == selected_category_Order)
                        ]
                        filtered_df = filtered_df.sort_values(
                            by="Delta", ascending=True
                        )
                    else:
                        filtered_df = L2_Grouped
                        filtered_df = filtered_df.sort_values(
                            by="Delta", ascending=True
                        )
                    filtered_df.columns = filtered_df.columns.str.strip()
                    filtered_df[["Spent", "Budget", "Delta"]] = filtered_df[
                        ["Spent", "Budget", "Delta"]
                    ].apply(pd.to_numeric, errors="coerce")
                    coli1, coli2, coli3 = st.columns(
                        3, border=True, vertical_alignment="center"
                    )
                    with coli1:
                        st.metric(
                            label="Budget", value=f"£{filtered_df['Budget'].sum():,.2f}"
                        )
                    with coli2:
                        st.metric(
                            label="Spent", value=f"£{filtered_df['Spent'].sum():,.2f}"
                        )
                    with coli3:
                        st.metric(
                            label="Delta",
                            value=f"£{filtered_df['Delta'].sum():,.2f}",
                            delta=f"{(((filtered_df['Budget'].sum()) - (filtered_df['Spent'].sum()))/(filtered_df['Budget'].sum()))*100:.2f}%",
                        )
                    # Apply styling to the 'Order' column based on 'Delta'
                    if "Delta" in filtered_df.columns:
                        styled_df = filtered_df.style.apply(
                            lambda row: [
                                color_code(row) if col == "Order" else ""
                                for col in filtered_df.columns
                            ],
                            axis=1,
                        )
                        # Display in Streamlit
                        st.dataframe(styled_df, use_container_width=True)
                    else:
                        st.error("Column 'Delta' is missing from the DataFrame")

            with col22:
                with st.container(height=500, border=False):
                    # Assign colors to the bars based on your conditions
                    colors = np.where(
                        (filtered_df["Budget"] == 0),
                        "orange",
                        np.where(
                            (filtered_df["Spent"] > filtered_df["Budget"]),
                            "red",
                            "green",
                        ),
                    )

                    # Create a grouped bar chart
                    fig = go.Figure()

                    # Add first column for Budget
                    fig.add_trace(
                        go.Bar(
                            name="Budget",
                            x=filtered_df["Order"],
                            y=filtered_df["Budget"],
                            marker_color="blue",  # Fixed color for Budget
                        )
                    )

                    # Add second column for Spent with dynamic colors
                    fig.add_trace(
                        go.Bar(
                            name="Spent",
                            x=filtered_df["Order"],
                            y=filtered_df["Spent"],
                            marker_color=colors,  # Colors based on conditions
                        )
                    )

                    # Update layout for better visualization
                    fig.update_layout(
                        xaxis_title="Categories",
                        yaxis_title="Values",
                        barmode="group",  # Group bars
                    )

                    # Display the chart in Streamlit
                    st.subheader("Cost by Order Bar Chart")
                    st.plotly_chart(fig, key="weerwewew")
                    

            col31, col32 = st.columns(2, gap="medium",vertical_alignment='center')
            new_data_45 = L3_Grouped[L3_Grouped["Order"] == selected_category_Order]
            L3_Grouped = L3_Grouped.rename(
                columns={
                    "Main": "Spent",
                    "1st Comparison": "Budget",
                    "Var Comp&Main": "Delta",
                }
            )
            with col31:
                with st.container(height=500, border=False):
                    # User filter input
                    selected_category = st.selectbox(
                        "Filter by Level 3:",
                        ["All"] + list(new_data_45["L3"].unique()),
                        key="wew2feefef",
                    )
                    # Apply the filter
                    if selected_category_Order != "All":
                        if selected_category != "All":
                            filtered_df = L3_Grouped[
                                (L3_Grouped["L3"] == selected_category)
                                & (L3_Grouped["Order"] == selected_category_Order)
                            ]
                            filtered_df = filtered_df.sort_values(
                                by="Delta", ascending=True
                            )
                        else:
                            filtered_df = L3_Grouped[
                                L3_Grouped["Order"] == selected_category_Order
                            ]
                            filtered_df = filtered_df.sort_values(
                                by="Delta", ascending=True
                            )
                    else:
                        filtered_df = L3_Grouped[
                            L3_Grouped["Order"] == selected_category_Order
                        ]
                        filtered_df = filtered_df.sort_values(
                            by="Delta", ascending=True
                        )
                    coli31, coli32, coli33 = st.columns(
                        3, border=True, vertical_alignment="center"
                    )
                    with coli31:
                        st.metric(
                            label="Budget", value=f"£{filtered_df['Budget'].sum():,.2f}"
                        )
                    with coli32:
                        st.metric(
                            label="Spent", value=f"£{filtered_df['Spent'].sum():,.2f}"
                        )
                    with coli33:
                        st.metric(
                            label="Delta",
                            value=f"£{filtered_df['Delta'].sum():,.2f}",
                            delta=f"{(((filtered_df['Budget'].sum()) - (filtered_df['Spent'].sum()))/(filtered_df['Budget'].sum()))*100:.2f}%",
                        )
                    # Apply styling to the 'Order' column based on 'Delta'
                    if "Delta" in filtered_df.columns:
                        styled_df = filtered_df.style.apply(
                            lambda row: [
                                color_code(row) if col == "L3" else ""
                                for col in filtered_df.columns
                            ],
                            axis=1,
                        )
                        # Display in Streamlit
                        st.dataframe(styled_df, use_container_width=True)
                    else:
                        st.error("Column 'Delta' is missing from the DataFrame")

            with col32:
                with st.container(height=500, border=False):
                    # Assign colors to the bars based on your conditions
                    colors = np.where(
                        (filtered_df["Budget"] == 0),
                        "orange",
                        np.where(
                            (filtered_df["Spent"] > filtered_df["Budget"]),
                            "red",
                            "green",
                        ),
                    )
                    # Create a grouped bar chart
                    fig = go.Figure()

                    # Add first column for Budget
                    fig.add_trace(
                        go.Bar(
                            name="Budget",
                            x=filtered_df["L3"],
                            y=filtered_df["Budget"],
                            marker_color="blue",  # Fixed color for Budget
                        )
                    )

                    # Add second column for Spent with dynamic colors
                    fig.add_trace(
                        go.Bar(
                            name="Spent",
                            x=filtered_df["L3"],
                            y=filtered_df["Spent"],
                            marker_color=colors,  # Colors based on conditions
                        )
                    )

                    # Update layout for better visualization
                    fig.update_layout(
                        xaxis_title="Categories",
                        yaxis_title="Values",
                        barmode="group",  # Group bars
                    )

                    # Display the chart in Streamlit
                    st.subheader("Cost by L3 Bar Chart")
                    st.plotly_chart(fig, key="we3refewfefdwewew")

            col41, col42 = st.columns(2, gap="medium",vertical_alignment='center')
            new_data_46 = L4_Grouped[L4_Grouped["L3"] == selected_category]
            L4_Grouped = L4_Grouped.rename(
                columns={
                    "Main": "Spent",
                    "1st Comparison": "Budget",
                    "Var Comp&Main": "Delta",
                }
            )
            with col41:
                with st.container(height=500, border=False):
                    # User filter input
                    selected_category_L4 = st.selectbox(
                        "Filter by L4:",
                        ["All"] + list(new_data_46["L4"].unique()),
                        key="2f44343r34353535356fef",
                    )
                    # Apply the filter
                    if selected_category != "All":
                        if selected_category_L4 != "All":
                            filtered_df = L4_Grouped[
                                (L4_Grouped["L4"] == selected_category_L4)
                                & (L4_Grouped["Order"] == selected_category_Order)
                                & (L4_Grouped["L3"] == selected_category)
                            ]
                            filtered_df = filtered_df.sort_values(
                                by="Delta", ascending=True
                            )
                        else:
                            filtered_df = L4_Grouped[
                                L4_Grouped["L3"] == selected_category
                            ]
                            filtered_df = filtered_df.sort_values(
                                by="Delta", ascending=True
                            )
                    else:
                        filtered_df = L4_Grouped[L4_Grouped["L3"] == selected_category]
                        filtered_df = filtered_df.sort_values(
                            by="Delta", ascending=True
                        )
                    coli31, coli32, coli33 = st.columns(
                        3, border=True, vertical_alignment="center"
                    )
                    with coli31:
                        st.metric(
                            label="Budget", value=f"£{filtered_df['Budget'].sum():,.2f}"
                        )
                    with coli32:
                        st.metric(
                            label="Spent", value=f"£{filtered_df['Spent'].sum():,.2f}"
                        )
                    with coli33:
                        st.metric(
                            label="Delta",
                            value=f"£{filtered_df['Delta'].sum():,.2f}",
                            delta=f"{(((filtered_df['Budget'].sum()) - (filtered_df['Spent'].sum()))/(filtered_df['Budget'].sum()))*100:.2f}%",
                        )
                    # Apply styling to the 'Order' column based on 'Delta'
                    if "Delta" in filtered_df.columns:
                        styled_df = filtered_df.style.apply(
                            lambda row: [
                                color_code(row) if col == "L4" else ""
                                for col in filtered_df.columns
                            ],
                            axis=1,
                        )
                        # Display in Streamlit
                        st.dataframe(styled_df, use_container_width=True)
                    else:
                        st.error("Column 'Delta' is missing from the DataFrame")
            with col42:
                with st.container(height=500, border=False):
                    # Assign colors to the bars based on your conditions
                    colors = np.where(
                        (filtered_df["Budget"] == 0),
                        "orange",
                        np.where(
                            (filtered_df["Spent"] > filtered_df["Budget"]),
                            "red",
                            "green",
                        ),
                    )

                    # Create a grouped bar chart
                    fig = go.Figure()

                    # Add first column for Budget
                    fig.add_trace(
                        go.Bar(
                            name="Budget",
                            x=filtered_df["L4"],
                            y=filtered_df["Budget"],
                            marker_color="blue",  # Fixed color for Budget
                        )
                    )

                    # Add second column for Spent with dynamic colors
                    fig.add_trace(
                        go.Bar(
                            name="Spent",
                            x=filtered_df["L4"],
                            y=filtered_df["Spent"],
                            marker_color=colors,  # Colors based on conditions
                        )
                    )

                    # Update layout for better visualization
                    fig.update_layout(
                        xaxis_title="Categories",
                        yaxis_title="Values",
                        barmode="group",  # Group bars
                    )

                    # Display the chart in Streamlit
                    st.subheader("Cost by L4 Chart")
                    st.plotly_chart(fig, key="we3dffewfefdwewew")

            col51, col52 = st.columns(2, gap="medium",vertical_alignment='center')
            new_data_47 = L5_Grouped[L5_Grouped["L4"] == selected_category_L4]
            L5_Grouped = L5_Grouped.rename(
                columns={
                    "Main": "Spent",
                    "1st Comparison": "Budget",
                    "Var Comp&Main": "Delta",
                }
            )
            with col51:
                with st.container(height=500, border=False):
                    # User filter input
                    selected_category_L5 = st.selectbox(
                        "Filter by Order:",
                        ["All"] + list(new_data_47["AccountAndDescpription"].unique()),
                        key="2ff5frtgr445gg4gdr45ef",
                    )
                    # Apply the filter
                    if selected_category_L4 != "All":
                        if selected_category_L5 != "All":
                            filtered_df = L5_Grouped[
                                (
                                    L5_Grouped["AccountAndDescpription"]
                                    == selected_category_L5
                                )
                                & (L5_Grouped["Order"] == selected_category_Order)
                                & (L5_Grouped["L3"] == selected_category)
                                & (L5_Grouped["L4"] == selected_category_L4)
                            ]
                            filtered_df = filtered_df.sort_values(
                                by="Delta", ascending=True
                            )
                        else:
                            filtered_df = L5_Grouped[
                                L5_Grouped["L4"] == selected_category_L4
                            ]
                            filtered_df = filtered_df.sort_values(
                                by="Delta", ascending=True
                            )
                    else:
                        filtered_df = L5_Grouped[
                            L5_Grouped["L4"] == selected_category_L4
                        ]
                        filtered_df = filtered_df.sort_values(
                            by="Delta", ascending=True
                        )
                    coli31, coli32, coli33 = st.columns(
                        3, border=True, vertical_alignment="center"
                    )
                    with coli31:
                        st.metric(
                            label="Budget", value=f"£{filtered_df['Budget'].sum():,.2f}"
                        )
                    with coli32:
                        st.metric(
                            label="Spent", value=f"£{filtered_df['Spent'].sum():,.2f}"
                        )
                    with coli33:
                        st.metric(
                            label="Delta",
                            value=f"£{filtered_df['Delta'].sum():,.2f}",
                            delta=f"{(((filtered_df['Budget'].sum()) - (filtered_df['Spent'].sum()))/(filtered_df['Budget'].sum()))*100:.2f}%",
                        )
                    # Apply styling to the 'Order' column based on 'Delta'
                    if "Delta" in filtered_df.columns:
                        styled_df = filtered_df.style.apply(
                            lambda row: [
                                (
                                    color_code(row)
                                    if col == "AccountAndDescpription"
                                    else ""
                                )
                                for col in filtered_df.columns
                            ],
                            axis=1,
                        )
                        # Display in Streamlit
                        st.dataframe(styled_df, use_container_width=True)
                    else:
                        st.error("Column 'Delta' is missing from the DataFrame")

            with col52:
                with st.container(height=500, border=False):
                    # Assign colors to the bars based on your conditions
                    colors = np.where(
                        (filtered_df["Budget"] == 0),
                        "orange",
                        np.where(
                            (filtered_df["Spent"] > filtered_df["Budget"]),
                            "red",
                            "green",
                        ),
                    )

                    # Create a grouped bar chart
                    fig = go.Figure()

                    # Add first column for Budget
                    fig.add_trace(
                        go.Bar(
                            name="Budget",
                            x=filtered_df["AccountAndDescpription"],
                            y=filtered_df["Budget"],
                            marker_color="blue",  # Fixed color for Budget
                        )
                    )

                    # Add second column for Spent with dynamic colors
                    fig.add_trace(
                        go.Bar(
                            name="Spent",
                            x=filtered_df["AccountAndDescpription"],
                            y=filtered_df["Spent"],
                            marker_color=colors,  # Colors based on conditions
                        )
                    )

                    # Update layout for better visualization
                    fig.update_layout(
                        xaxis_title="Categories",
                        yaxis_title="Values",
                        barmode="group",  # Group bars
                    )

                    # Display the chart in Streamlit
                    st.subheader("Cost by Account Bar Chart")
                    st.plotly_chart(fig, key="we3redwededffewfefdwewew")

        if (month == "January") & (year == "2025") & (data == "Variable Costs"):
            Jan_2025 = Jan_2025.iloc[:, 0:8]
            Jan_2025 = Jan_2025.fillna(0)
            jan_2025_complete = Jan_2025.groupby(["Category"]).sum(list).reset_index()
            Jan_2025_Variable_Cost_Data = Jan_2025[(Jan_2025["Category"] == "Variable Costs")]
            L1_Grouped = (
                Jan_2025_Variable_Cost_Data.groupby(["Category"]).sum(list).reset_index()
            )
            L2_Grouped = (
                Jan_2025_Variable_Cost_Data.groupby(["Category", "Order"])
                .sum(list)
                .reset_index()
            )
            L3_Grouped = (
                Jan_2025_Variable_Cost_Data.groupby(["Category", "Order", "L3"])
                .sum(list)
                .reset_index()
            )
            L4_Grouped = (
                Jan_2025_Variable_Cost_Data.groupby(["Category", "Order", "L3", "L4"])
                .sum(list)
                .reset_index()
            )
            L5_Grouped = (
                Jan_2025_Variable_Cost_Data.groupby(
                    ["Category", "Order", "L3", "L4", "AccountAndDescpription"]
                )
                .sum(list)
                .reset_index()
            )

            grouped_dfs = {
                "L1_Grouped": ("Category", L1_Grouped),
                "L2_Grouped": ("Order", L2_Grouped),
                "L3_Grouped": ("L3", L3_Grouped),
                "L4_Grouped": ("L4", L4_Grouped),
                "L5_Grouped": ("AccountAndDescpription", L5_Grouped),
            }
            # Dictionary to store parsed DataFrames
            parsed_dfs = {}

            # Loop through each grouped DataFrame
            for key, (category_column, df) in grouped_dfs.items():
                data = []

                for _, row in df.iterrows():
                    budget, spent, delta = (
                        row["1st Comparison"],
                        row["Main"],
                        row["Var Comp&Main"],
                    )
                    data.append(
                        [row[category_column], budget, spent, delta]
                    )  # Dynamically get category column

                # Convert to DataFrame and store in dictionary
                parsed_dfs[key] = pd.DataFrame(
                    data, columns=["Category", "Budget", "Main", "Delta"]
                )
            # Access parsed DataFrames, e.g.:
            df_parsed_1 = parsed_dfs["L1_Grouped"]
            df_parsed_2 = parsed_dfs["L2_Grouped"]
            df_parsed_3 = parsed_dfs["L3_Grouped"]
            df_parsed_4 = parsed_dfs["L4_Grouped"]
            df_parsed_5 = parsed_dfs["L5_Grouped"]

            Jan_Budget = float(jan_2025_complete["1st Comparison"].sum())
            Jan_spent = float(jan_2025_complete["Main"].sum())
            Jan_Delta = float(jan_2025_complete["Var Comp&Main"].sum())
            Jan_delta_percent = (((Jan_Budget) - (Jan_spent)) / (Jan_Budget)) * 100
            Jan_Variable_Budget = float(df_parsed_1["Budget"].iloc[0])
            Jan_Variable_Spent = float(df_parsed_1["Main"].iloc[0])
            Jan_Variable_Delta = float(df_parsed_1["Delta"].iloc[0])
            Jan_Variable_Delta_Percent = (
                ((Jan_Variable_Budget) - (Jan_Variable_Spent)) / (Jan_Variable_Budget)
            ) * 100
            cols1, cols2 = st.columns(2)
            with cols1:
                st.header("Monthly Summary")
            with cols2:
                st.header("Cost Summary")
            col1, col2, col3, col4, col5, col6 = st.columns(
                6, gap="medium", vertical_alignment="center"
            )
            with col1:
                st.metric(
                    "January Budget",
                    value=f"£{Jan_Budget:,.2f}",
                    border=True,
                    help="This is the total budget for January.",
                )
            with col2:
                st.metric(
                    "January Spent",
                    value=f"£{Jan_spent:,.2f}",
                    border=True,
                    help="This is the total amount of funds spent in January.",
                )
            with col3:
                st.metric(
                    "January Delta",
                    value=f"£{Jan_Delta:,.2f}",
                    border=True,
                    delta=f"{Jan_delta_percent:,.2f} %",
                    help="This is the difference in the amount budgeted and the amount spent for Janauary.",
                )
            with col4:
                st.metric(
                    "January Variable Cost Budget",
                    value=f"£{Jan_Variable_Budget:,.2f}",
                    border=True,
                    help="This is the total amount budgeted to be spent for Variable Costs in January.",
                )
            with col5:
                st.metric(
                    "January Variable Cost Spent",
                    value=f"£{Jan_Variable_Spent:,.2f}",
                    border=True,
                    help="This is the total amount spent for Variable Cost in Janauary.",
                )
            with col6:
                st.metric(
                    "January Variable Cost Delta",
                    value=f"£{Jan_Variable_Delta:,.2f}",
                    border=True,
                    delta=f"{Jan_Variable_Delta_Percent:,.2f}%",
                    help="This is the difference in the budgeted amount and Spent amount for Variable Costs in January.",
                )

            col21, col22 = st.columns(2, gap="medium", vertical_alignment="center")
            with col21:
                with st.container(height=500, border=False):
                    L2_Grouped = L2_Grouped.rename(
                        columns={
                            "Main": "Spent",
                            "1st Comparison": "Budget",
                            "Var Comp&Main": "Delta",
                        }
                    )
                    # User filter input
                    selected_category_Order = st.selectbox(
                        "Filter by Order:",
                        ["All"] + list(L2_Grouped["Order"].unique()),
                        key="FIlter by Order",
                    )

                    # Apply the filter
                    if selected_category_Order != "All":
                        filtered_df = L2_Grouped[
                            (L2_Grouped["Order"] == selected_category_Order)
                            & (L2_Grouped["Order"] == selected_category_Order)
                        ]
                        filtered_df = filtered_df.sort_values(
                            by="Delta", ascending=True
                        )
                    else:
                        filtered_df = L2_Grouped
                        filtered_df = filtered_df.sort_values(
                            by="Delta", ascending=True
                        )
                    filtered_df.columns = filtered_df.columns.str.strip()
                    filtered_df[["Spent", "Budget", "Delta"]] = filtered_df[
                        ["Spent", "Budget", "Delta"]
                    ].apply(pd.to_numeric, errors="coerce")
                    coli1, coli2, coli3 = st.columns(
                        3, border=True, vertical_alignment="center"
                    )
                    with coli1:
                        st.metric(
                            label="Budget", value=f"£{filtered_df['Budget'].sum():,.2f}"
                        )
                    with coli2:
                        st.metric(
                            label="Spent", value=f"£{filtered_df['Spent'].sum():,.2f}"
                        )
                    with coli3:
                        st.metric(
                            label="Delta",
                            value=f"£{filtered_df['Delta'].sum():,.2f}",
                            delta=f"{(((filtered_df['Budget'].sum()) - (filtered_df['Spent'].sum()))/(filtered_df['Budget'].sum()))*100:.2f}%",
                        )
                    # Apply styling to the 'Order' column based on 'Delta'
                    if "Delta" in filtered_df.columns:
                        styled_df = filtered_df.style.apply(
                            lambda row: [
                                color_code(row) if col == "Order" else ""
                                for col in filtered_df.columns
                            ],
                            axis=1,
                        )
                        # Display in Streamlit
                        st.dataframe(styled_df, use_container_width=True)
                    else:
                        st.error("Column 'Delta' is missing from the DataFrame")

            with col22:
                with st.container(height=500, border=False):
                    # Assign colors to the bars based on your conditions
                    colors = np.where(
                        (filtered_df["Budget"] == 0),
                        "orange",
                        np.where(
                            (filtered_df["Spent"] > filtered_df["Budget"]),
                            "red",
                            "green",
                        ),
                    )

                    # Create a grouped bar chart
                    fig = go.Figure()

                    # Add first column for Budget
                    fig.add_trace(
                        go.Bar(
                            name="Budget",
                            x=filtered_df["Order"],
                            y=filtered_df["Budget"],
                            marker_color="blue",  # Variable color for Budget
                        )
                    )

                    # Add second column for Spent with dynamic colors
                    fig.add_trace(
                        go.Bar(
                            name="Spent",
                            x=filtered_df["Order"],
                            y=filtered_df["Spent"],
                            marker_color=colors,  # Colors based on conditions
                        )
                    )

                    # Update layout for better visualization
                    fig.update_layout(
                        xaxis_title="Categories",
                        yaxis_title="Values",
                        barmode="group",  # Group bars
                    )

                    # Display the chart in Streamlit
                    st.subheader("Cost by Order Bar Chart")
                    st.plotly_chart(fig, key="weerwewew")

            col31, col32 = st.columns(2, gap="medium",vertical_alignment='center')
            new_data_45 = L3_Grouped[L3_Grouped["Order"] == selected_category_Order]
            L3_Grouped = L3_Grouped.rename(
                columns={
                    "Main": "Spent",
                    "1st Comparison": "Budget",
                    "Var Comp&Main": "Delta",
                }
            )
            with col31:
                with st.container(height=500, border=False):
                    # User filter input
                    selected_category = st.selectbox(
                        "Filter by Level 3:",
                        ["All"] + list(new_data_45["L3"].unique()),
                        key="2feefeewef",
                    )
                    # Apply the filter
                    if selected_category_Order != "All":
                        if selected_category != "All":
                            filtered_df = L3_Grouped[
                                (L3_Grouped["L3"] == selected_category)
                                & (L3_Grouped["Order"] == selected_category_Order)
                            ]
                            filtered_df = filtered_df.sort_values(
                                by="Delta", ascending=True
                            )
                        else:
                            filtered_df = L3_Grouped[
                                L3_Grouped["Order"] == selected_category_Order
                            ]
                            filtered_df = filtered_df.sort_values(
                                by="Delta", ascending=True
                            )
                    else:
                        filtered_df = L3_Grouped[
                            L3_Grouped["Order"] == selected_category_Order
                        ]
                        filtered_df = filtered_df.sort_values(
                            by="Delta", ascending=True
                        )
                    coli31, coli32, coli33 = st.columns(
                        3, border=True, vertical_alignment="center"
                    )
                    with coli31:
                        st.metric(
                            label="Budget", value=f"£{filtered_df['Budget'].sum():,.2f}"
                        )
                    with coli32:
                        st.metric(
                            label="Spent", value=f"£{filtered_df['Spent'].sum():,.2f}"
                        )
                    with coli33:
                        st.metric(
                            label="Delta",
                            value=f"£{filtered_df['Delta'].sum():,.2f}",
                            delta=f"{(((filtered_df['Budget'].sum()) - (filtered_df['Spent'].sum()))/(filtered_df['Budget'].sum()))*100:.2f}%",
                        )
                    # Apply styling to the 'Order' column based on 'Delta'
                    if "Delta" in filtered_df.columns:
                        styled_df = filtered_df.style.apply(
                            lambda row: [
                                color_code(row) if col == "L3" else ""
                                for col in filtered_df.columns
                            ],
                            axis=1,
                        )
                        # Display in Streamlit
                        st.dataframe(styled_df, use_container_width=True)
                    else:
                        st.error("Column 'Delta' is missing from the DataFrame")

            with col32:
                with st.container(height=500, border=False):
                    # Assign colors to the bars based on your conditions
                    colors = np.where(
                        (filtered_df["Budget"] == 0),
                        "orange",
                        np.where(
                            (filtered_df["Spent"] > filtered_df["Budget"]),
                            "red",
                            "green",
                        ),
                    )
                    # Create a grouped bar chart
                    fig = go.Figure()

                    # Add first column for Budget
                    fig.add_trace(
                        go.Bar(
                            name="Budget",
                            x=filtered_df["L3"],
                            y=filtered_df["Budget"],
                            marker_color="blue",  # Variable color for Budget
                        )
                    )

                    # Add second column for Spent with dynamic colors
                    fig.add_trace(
                        go.Bar(
                            name="Spent",
                            x=filtered_df["L3"],
                            y=filtered_df["Spent"],
                            marker_color=colors,  # Colors based on conditions
                        )
                    )

                    # Update layout for better visualization
                    fig.update_layout(
                        xaxis_title="Categories",
                        yaxis_title="Values",
                        barmode="group",  # Group bars
                    )

                    # Display the chart in Streamlit
                    st.subheader("Cost by L3 Bar Chart")
                    st.plotly_chart(fig, key="we3refewfefdwewew")

            col41, col42 = st.columns(2, gap="medium",vertical_alignment='center')
            new_data_46 = L4_Grouped[L4_Grouped["L3"] == selected_category]
            L4_Grouped = L4_Grouped.rename(
                columns={
                    "Main": "Spent",
                    "1st Comparison": "Budget",
                    "Var Comp&Main": "Delta",
                }
            )
            with col41:
                with st.container(height=500, border=False):
                    # User filter input
                    selected_category_L4 = st.selectbox(
                        "Filter by L4:",
                        ["All"] + list(new_data_46["L4"].unique()),
                        key="2f44343r34353535356fef",
                    )
                    # Apply the filter
                    if selected_category != "All":
                        if selected_category_L4 != "All":
                            filtered_df = L4_Grouped[
                                (L4_Grouped["L4"] == selected_category_L4)
                                & (L4_Grouped["Order"] == selected_category_Order)
                                & (L4_Grouped["L3"] == selected_category)
                            ]
                            filtered_df = filtered_df.sort_values(
                                by="Delta", ascending=True
                            )
                        else:
                            filtered_df = L4_Grouped[
                                L4_Grouped["L3"] == selected_category
                            ]
                            filtered_df = filtered_df.sort_values(
                                by="Delta", ascending=True
                            )
                    else:
                        filtered_df = L4_Grouped[L4_Grouped["L3"] == selected_category]
                        filtered_df = filtered_df.sort_values(
                            by="Delta", ascending=True
                        )
                    coli31, coli32, coli33 = st.columns(
                        3, border=True, vertical_alignment="center"
                    )
                    with coli31:
                        st.metric(
                            label="Budget", value=f"£{filtered_df['Budget'].sum():,.2f}"
                        )
                    with coli32:
                        st.metric(
                            label="Spent", value=f"£{filtered_df['Spent'].sum():,.2f}"
                        )
                    with coli33:
                        st.metric(
                            label="Delta",
                            value=f"£{filtered_df['Delta'].sum():,.2f}",
                            delta=f"{(((filtered_df['Budget'].sum()) - (filtered_df['Spent'].sum()))/(filtered_df['Budget'].sum()))*100:.2f}%",
                        )
                    # Apply styling to the 'Order' column based on 'Delta'
                    if "Delta" in filtered_df.columns:
                        styled_df = filtered_df.style.apply(
                            lambda row: [
                                color_code(row) if col == "L4" else ""
                                for col in filtered_df.columns
                            ],
                            axis=1,
                        )
                        # Display in Streamlit
                        st.dataframe(styled_df, use_container_width=True)
                    else:
                        st.error("Column 'Delta' is missing from the DataFrame")
            with col42:
                with st.container(height=500, border=False):
                    # Assign colors to the bars based on your conditions
                    colors = np.where(
                        (filtered_df["Budget"] == 0),
                        "orange",
                        np.where(
                            (filtered_df["Spent"] > filtered_df["Budget"]),
                            "red",
                            "green",
                        ),
                    )

                    # Create a grouped bar chart
                    fig = go.Figure()

                    # Add first column for Budget
                    fig.add_trace(
                        go.Bar(
                            name="Budget",
                            x=filtered_df["L4"],
                            y=filtered_df["Budget"],
                            marker_color="blue",  # Variable color for Budget
                        )
                    )

                    # Add second column for Spent with dynamic colors
                    fig.add_trace(
                        go.Bar(
                            name="Spent",
                            x=filtered_df["L4"],
                            y=filtered_df["Spent"],
                            marker_color=colors,  # Colors based on conditions
                        )
                    )

                    # Update layout for better visualization
                    fig.update_layout(
                        xaxis_title="Categories",
                        yaxis_title="Values",
                        barmode="group",  # Group bars
                    )

                    # Display the chart in Streamlit
                    st.subheader("Cost by L4 Chart")
                    st.plotly_chart(fig, key="we3dffewfefdwewew")

            col51, col52 = st.columns(2, gap="medium",vertical_alignment='center')
            new_data_47 = L5_Grouped[L5_Grouped["L4"] == selected_category_L4]
            L5_Grouped = L5_Grouped.rename(
                columns={
                    "Main": "Spent",
                    "1st Comparison": "Budget",
                    "Var Comp&Main": "Delta",
                }
            )
            with col51:
                with st.container(height=500, border=False):
                    # User filter input
                    selected_category_L5 = st.selectbox(
                        "Filter by Order:",
                        ["All"] + list(new_data_47["AccountAndDescpription"].unique()),
                        key="2ff5frtgr445gg4gdr45ef",
                    )
                    # Apply the filter
                    if selected_category_L4 != "All":
                        if selected_category_L5 != "All":
                            filtered_df = L5_Grouped[
                                (
                                    L5_Grouped["AccountAndDescpription"]
                                    == selected_category_L5
                                )
                                & (L5_Grouped["Order"] == selected_category_Order)
                                & (L5_Grouped["L3"] == selected_category)
                                & (L5_Grouped["L4"] == selected_category_L4)
                            ]
                            filtered_df = filtered_df.sort_values(
                                by="Delta", ascending=True
                            )
                        else:
                            filtered_df = L5_Grouped[
                                L5_Grouped["L4"] == selected_category_L4
                            ]
                            filtered_df = filtered_df.sort_values(
                                by="Delta", ascending=True
                            )
                    else:
                        filtered_df = L5_Grouped[
                            L5_Grouped["L4"] == selected_category_L4
                        ]
                        filtered_df = filtered_df.sort_values(
                            by="Delta", ascending=True
                        )
                    coli31, coli32, coli33 = st.columns(
                        3, border=True, vertical_alignment="center"
                    )
                    with coli31:
                        st.metric(
                            label="Budget", value=f"£{filtered_df['Budget'].sum():,.2f}"
                        )
                    with coli32:
                        st.metric(
                            label="Spent", value=f"£{filtered_df['Spent'].sum():,.2f}"
                        )
                    with coli33:
                        st.metric(
                            label="Delta",
                            value=f"£{filtered_df['Delta'].sum():,.2f}",
                            delta=f"{(((filtered_df['Budget'].sum()) - (filtered_df['Spent'].sum()))/(filtered_df['Budget'].sum()))*100:.2f}%",
                        )
                    # Apply styling to the 'Order' column based on 'Delta'
                    if "Delta" in filtered_df.columns:
                        styled_df = filtered_df.style.apply(
                            lambda row: [
                                (
                                    color_code(row)
                                    if col == "AccountAndDescpription"
                                    else ""
                                )
                                for col in filtered_df.columns
                            ],
                            axis=1,
                        )
                        # Display in Streamlit
                        st.dataframe(styled_df, use_container_width=True)
                    else:
                        st.error("Column 'Delta' is missing from the DataFrame")

            with col52:
                with st.container(height=500, border=False):
                    # Assign colors to the bars based on your conditions
                    colors = np.where(
                        (filtered_df["Budget"] == 0),
                        "orange",
                        np.where(
                            (filtered_df["Spent"] > filtered_df["Budget"]),
                            "red",
                            "green",
                        ),
                    )

                    # Create a grouped bar chart
                    fig = go.Figure()

                    # Add first column for Budget
                    fig.add_trace(
                        go.Bar(
                            name="Budget",
                            x=filtered_df["AccountAndDescpription"],
                            y=filtered_df["Budget"],
                            marker_color="blue",  # Variable color for Budget
                        )
                    )

                    # Add second column for Spent with dynamic colors
                    fig.add_trace(
                        go.Bar(
                            name="Spent",
                            x=filtered_df["AccountAndDescpription"],
                            y=filtered_df["Spent"],
                            marker_color=colors,  # Colors based on conditions
                        )
                    )

                    # Update layout for better visualization
                    fig.update_layout(
                        xaxis_title="Categories",
                        yaxis_title="Values",
                        barmode="group",  # Group bars
                    )

                    # Display the chart in Streamlit
                    st.subheader("Cost by Account Bar Chart")
                    st.plotly_chart(fig, key="we3redwededffewfefdwewew")

        if (month == "February") & (year == "2025") & (data == "Fixed Costs"):
            Feb_2025 = Feb_2025.iloc[:, 0:8]
            Feb_2025 = Feb_2025.fillna(0)
            Feb_2025_complete = Feb_2025.groupby(["Category"]).sum(list).reset_index()
            Feb_2025_Fixed_Cost_Data = Feb_2025[(Feb_2025["Category"] == "Fixed Costs")]
            L1_Grouped = (
                Feb_2025_Fixed_Cost_Data.groupby(["Category"]).sum(list).reset_index()
            )
            L2_Grouped = (
                Feb_2025_Fixed_Cost_Data.groupby(["Category", "Order"])
                .sum(list)
                .reset_index()
            )
            L3_Grouped = (
                Feb_2025_Fixed_Cost_Data.groupby(["Category", "Order", "L3"])
                .sum(list)
                .reset_index()
            )
            L4_Grouped = (
                Feb_2025_Fixed_Cost_Data.groupby(["Category", "Order", "L3", "L4"])
                .sum(list)
                .reset_index()
            )
            L5_Grouped = (
                Feb_2025_Fixed_Cost_Data.groupby(
                    ["Category", "Order", "L3", "L4", "AccountAndDescpription"]
                )
                .sum(list)
                .reset_index()
            )

            grouped_dfs = {
                "L1_Grouped": ("Category", L1_Grouped),
                "L2_Grouped": ("Order", L2_Grouped),
                "L3_Grouped": ("L3", L3_Grouped),
                "L4_Grouped": ("L4", L4_Grouped),
                "L5_Grouped": ("AccountAndDescpription", L5_Grouped),
            }
            # Dictionary to store parsed DataFrames
            parsed_dfs = {}

            # Loop through each grouped DataFrame
            for key, (category_column, df) in grouped_dfs.items():
                data = []

                for _, row in df.iterrows():
                    budget, spent, delta = (
                        row["1st Comparison"],
                        row["Main"],
                        row["Var Comp&Main"],
                    )
                    data.append(
                        [row[category_column], budget, spent, delta]
                    )  # Dynamically get category column

                # Convert to DataFrame and store in dictionary
                parsed_dfs[key] = pd.DataFrame(
                    data, columns=["Category", "Budget", "Main", "Delta"]
                )
            # Access parsed DataFrames, e.g.:
            df_parsed_1 = parsed_dfs["L1_Grouped"]
            df_parsed_2 = parsed_dfs["L2_Grouped"]
            df_parsed_3 = parsed_dfs["L3_Grouped"]
            df_parsed_4 = parsed_dfs["L4_Grouped"]
            df_parsed_5 = parsed_dfs["L5_Grouped"]

            Feb_Budget = float(Feb_2025_complete["1st Comparison"].sum())
            Feb_spent = float(Feb_2025_complete["Main"].sum())
            Feb_Delta = float(Feb_2025_complete["Var Comp&Main"].sum())
            Feb_delta_percent = (((Feb_Budget) - (Feb_spent)) / (Feb_Budget)) * 100
            Feb_Fixed_Budget = float(df_parsed_1["Budget"].iloc[0])
            Feb_Fixed_Spent = float(df_parsed_1["Main"].iloc[0])
            Feb_Fixed_Delta = float(df_parsed_1["Delta"].iloc[0])
            Feb_Fixed_Delta_Percent = (
                ((Feb_Fixed_Budget) - (Feb_Fixed_Spent)) / (Feb_Fixed_Budget)
            ) * 100
            cols1, cols2 = st.columns(2)
            with cols1:
                st.header("Monthly Summary")
            with cols2:
                st.header("Cost Summary")
            col1, col2, col3, col4, col5, col6 = st.columns(
                6, gap="medium", vertical_alignment="center"
            )
            with col1:
                st.metric(
                    "Feburary Budget",
                    value=f"£{Feb_Budget:,.2f}",
                    border=True,
                    help="This is the total budget for Feburary.",
                )
            with col2:
                st.metric(
                    "Feburary Spent",
                    value=f"£{Feb_spent:,.2f}",
                    border=True,
                    help="This is the total amount of funds spent in Feburary.",
                )
            with col3:
                st.metric(
                    "Feburary Delta",
                    value=f"£{Feb_Delta:,.2f}",
                    border=True,
                    delta=f"{Feb_delta_percent:,.2f} %",
                    help="This is the difference in the amount budgeted and the amount spent for Febauary.",
                )
            with col4:
                st.metric(
                    "Feburary Fixed Cost Budget",
                    value=f"£{Feb_Fixed_Budget:,.2f}",
                    border=True,
                    help="This is the total amount budgeted to be spent for Fixed Costs in Feburary.",
                )
            with col5:
                st.metric(
                    "Feburary Fixed Cost Spent",
                    value=f"£{Feb_Fixed_Spent:,.2f}",
                    border=True,
                    help="This is the total amount spent for Fixed Cost in Febauary.",
                )
            with col6:
                st.metric(
                    "Feburary Fixed Cost Delta",
                    value=f"£{Feb_Fixed_Delta:,.2f}",
                    border=True,
                    delta=f"{Feb_Fixed_Delta_Percent:,.2f}%",
                    help="This is the difference in the budgeted amount and Spent amount for Fixed Costs in Feburary.",
                )

            col21, col22 = st.columns(2, gap="medium", vertical_alignment="center")
            with col21:
                with st.container(height=500, border=False):
                    L2_Grouped = L2_Grouped.rename(
                        columns={
                            "Main": "Spent",
                            "1st Comparison": "Budget",
                            "Var Comp&Main": "Delta",
                        }
                    )
                    # User filter input
                    selected_category_Order = st.selectbox(
                        "Filter by Order:",
                        ["All"] + list(L2_Grouped["Order"].unique()),
                        key="FIlter by Order",
                    )

                    # Apply the filter
                    if selected_category_Order != "All":
                        filtered_df = L2_Grouped[
                            (L2_Grouped["Order"] == selected_category_Order)
                            & (L2_Grouped["Order"] == selected_category_Order)
                        ]
                        filtered_df = filtered_df.sort_values(
                            by="Delta", ascending=True
                        )
                    else:
                        filtered_df = L2_Grouped
                        filtered_df = filtered_df.sort_values(
                            by="Delta", ascending=True
                        )
                    filtered_df.columns = filtered_df.columns.str.strip()
                    filtered_df[["Spent", "Budget", "Delta"]] = filtered_df[
                        ["Spent", "Budget", "Delta"]
                    ].apply(pd.to_numeric, errors="coerce")
                    coli1, coli2, coli3 = st.columns(
                        3, border=True, vertical_alignment="center"
                    )
                    with coli1:
                        st.metric(
                            label="Budget", value=f"£{filtered_df['Budget'].sum():,.2f}"
                        )
                    with coli2:
                        st.metric(
                            label="Spent", value=f"£{filtered_df['Spent'].sum():,.2f}"
                        )
                    with coli3:
                        st.metric(
                            label="Delta",
                            value=f"£{filtered_df['Delta'].sum():,.2f}",
                            delta=f"{(((filtered_df['Budget'].sum()) - (filtered_df['Spent'].sum()))/(filtered_df['Budget'].sum()))*100:.2f}%",
                        )
                    # Apply styling to the 'Order' column based on 'Delta'
                    if "Delta" in filtered_df.columns:
                        styled_df = filtered_df.style.apply(
                            lambda row: [
                                color_code(row) if col == "Order" else ""
                                for col in filtered_df.columns
                            ],
                            axis=1,
                        )
                        # Display in Streamlit
                        st.dataframe(styled_df, use_container_width=True)
                    else:
                        st.error("Column 'Delta' is missing from the DataFrame")

            with col22:
                with st.container(height=500, border=False):
                    # Assign colors to the bars based on your conditions
                    colors = np.where(
                        (filtered_df["Budget"] == 0),
                        "orange",
                        np.where(
                            (filtered_df["Spent"] > filtered_df["Budget"]),
                            "red",
                            "green",
                        ),
                    )

                    # Create a grouped bar chart
                    fig = go.Figure()

                    # Add first column for Budget
                    fig.add_trace(
                        go.Bar(
                            name="Budget",
                            x=filtered_df["Order"],
                            y=filtered_df["Budget"],
                            marker_color="blue",  # Fixed color for Budget
                        )
                    )

                    # Add second column for Spent with dynamic colors
                    fig.add_trace(
                        go.Bar(
                            name="Spent",
                            x=filtered_df["Order"],
                            y=filtered_df["Spent"],
                            marker_color=colors,  # Colors based on conditions
                        )
                    )

                    # Update layout for better visualization
                    fig.update_layout(
                        xaxis_title="Categories",
                        yaxis_title="Values",
                        barmode="group",  # Group bars
                    )

                    # Display the chart in Streamlit
                    st.subheader("Cost by Order Bar Chart")
                    st.plotly_chart(fig, key="weerwewew")

            col31, col32 = st.columns(2, gap="medium",vertical_alignment='center')
            new_data_45 = L3_Grouped[L3_Grouped["Order"] == selected_category_Order]
            L3_Grouped = L3_Grouped.rename(
                columns={
                    "Main": "Spent",
                    "1st Comparison": "Budget",
                    "Var Comp&Main": "Delta",
                }
            )
            with col31:
                with st.container(height=500, border=False):
                    # User filter input
                    selected_category = st.selectbox(
                        "Filter by Level 3:",
                        ["All"] + list(new_data_45["L3"].unique()),
                        key="2feefbgtbef",
                    )
                    # Apply the filter
                    if selected_category_Order != "All":
                        if selected_category != "All":
                            filtered_df = L3_Grouped[
                                (L3_Grouped["L3"] == selected_category)
                                & (L3_Grouped["Order"] == selected_category_Order)
                            ]
                            filtered_df = filtered_df.sort_values(
                                by="Delta", ascending=True
                            )
                        else:
                            filtered_df = L3_Grouped[
                                L3_Grouped["Order"] == selected_category_Order
                            ]
                            filtered_df = filtered_df.sort_values(
                                by="Delta", ascending=True
                            )
                    else:
                        filtered_df = L3_Grouped[
                            L3_Grouped["Order"] == selected_category_Order
                        ]
                        filtered_df = filtered_df.sort_values(
                            by="Delta", ascending=True
                        )
                    coli31, coli32, coli33 = st.columns(
                        3, border=True, vertical_alignment="center"
                    )
                    with coli31:
                        st.metric(
                            label="Budget", value=f"£{filtered_df['Budget'].sum():,.2f}"
                        )
                    with coli32:
                        st.metric(
                            label="Spent", value=f"£{filtered_df['Spent'].sum():,.2f}"
                        )
                    with coli33:
                        st.metric(
                            label="Delta",
                            value=f"£{filtered_df['Delta'].sum():,.2f}",
                            delta=f"{(((filtered_df['Budget'].sum()) - (filtered_df['Spent'].sum()))/(filtered_df['Budget'].sum()))*100:.2f}%",
                        )
                    # Apply styling to the 'Order' column based on 'Delta'
                    if "Delta" in filtered_df.columns:
                        styled_df = filtered_df.style.apply(
                            lambda row: [
                                color_code(row) if col == "L3" else ""
                                for col in filtered_df.columns
                            ],
                            axis=1,
                        )
                        # Display in Streamlit
                        st.dataframe(styled_df, use_container_width=True)
                    else:
                        st.error("Column 'Delta' is missing from the DataFrame")

            with col32:
                with st.container(height=500, border=False):
                    # Assign colors to the bars based on your conditions
                    colors = np.where(
                        (filtered_df["Budget"] == 0),
                        "orange",
                        np.where(
                            (filtered_df["Spent"] > filtered_df["Budget"]),
                            "red",
                            "green",
                        ),
                    )
                    # Create a grouped bar chart
                    fig = go.Figure()

                    # Add first column for Budget
                    fig.add_trace(
                        go.Bar(
                            name="Budget",
                            x=filtered_df["L3"],
                            y=filtered_df["Budget"],
                            marker_color="blue",  # Fixed color for Budget
                        )
                    )

                    # Add second column for Spent with dynamic colors
                    fig.add_trace(
                        go.Bar(
                            name="Spent",
                            x=filtered_df["L3"],
                            y=filtered_df["Spent"],
                            marker_color=colors,  # Colors based on conditions
                        )
                    )

                    # Update layout for better visualization
                    fig.update_layout(
                        xaxis_title="Categories",
                        yaxis_title="Values",
                        barmode="group",  # Group bars
                    )

                    # Display the chart in Streamlit
                    st.subheader("Cost by L3 Bar Chart")
                    st.plotly_chart(fig, key="we3refewfefdwewew")

            col41, col42 = st.columns(2, gap="medium",vertical_alignment='center')
            new_data_46 = L4_Grouped[L4_Grouped["L3"] == selected_category]
            L4_Grouped = L4_Grouped.rename(
                columns={
                    "Main": "Spent",
                    "1st Comparison": "Budget",
                    "Var Comp&Main": "Delta",
                }
            )
            with col41:
                with st.container(height=500, border=False):
                    # User filter input
                    selected_category_L4 = st.selectbox(
                        "Filter by L4:",
                        ["All"] + list(new_data_46["L4"].unique()),
                        key="2f44343r34353535356fef",
                    )
                    # Apply the filter
                    if selected_category != "All":
                        if selected_category_L4 != "All":
                            filtered_df = L4_Grouped[
                                (L4_Grouped["L4"] == selected_category_L4)
                                & (L4_Grouped["Order"] == selected_category_Order)
                                & (L4_Grouped["L3"] == selected_category)
                            ]
                            filtered_df = filtered_df.sort_values(
                                by="Delta", ascending=True
                            )
                        else:
                            filtered_df = L4_Grouped[
                                L4_Grouped["L3"] == selected_category
                            ]
                            filtered_df = filtered_df.sort_values(
                                by="Delta", ascending=True
                            )
                    else:
                        filtered_df = L4_Grouped[L4_Grouped["L3"] == selected_category]
                        filtered_df = filtered_df.sort_values(
                            by="Delta", ascending=True
                        )
                    coli31, coli32, coli33 = st.columns(
                        3, border=True, vertical_alignment="center"
                    )
                    with coli31:
                        st.metric(
                            label="Budget", value=f"£{filtered_df['Budget'].sum():,.2f}"
                        )
                    with coli32:
                        st.metric(
                            label="Spent", value=f"£{filtered_df['Spent'].sum():,.2f}"
                        )
                    with coli33:
                        st.metric(
                            label="Delta",
                            value=f"£{filtered_df['Delta'].sum():,.2f}",
                            delta=f"{(((filtered_df['Budget'].sum()) - (filtered_df['Spent'].sum()))/(filtered_df['Budget'].sum()))*100:.2f}%",
                        )
                    # Apply styling to the 'Order' column based on 'Delta'
                    if "Delta" in filtered_df.columns:
                        styled_df = filtered_df.style.apply(
                            lambda row: [
                                color_code(row) if col == "L4" else ""
                                for col in filtered_df.columns
                            ],
                            axis=1,
                        )
                        # Display in Streamlit
                        st.dataframe(styled_df, use_container_width=True)
                    else:
                        st.error("Column 'Delta' is missing from the DataFrame")
            with col42:
                with st.container(height=500, border=False):
                    # Assign colors to the bars based on your conditions
                    colors = np.where(
                        (filtered_df["Budget"] == 0),
                        "orange",
                        np.where(
                            (filtered_df["Spent"] > filtered_df["Budget"]),
                            "red",
                            "green",
                        ),
                    )

                    # Create a grouped bar chart
                    fig = go.Figure()

                    # Add first column for Budget
                    fig.add_trace(
                        go.Bar(
                            name="Budget",
                            x=filtered_df["L4"],
                            y=filtered_df["Budget"],
                            marker_color="blue",  # Fixed color for Budget
                        )
                    )

                    # Add second column for Spent with dynamic colors
                    fig.add_trace(
                        go.Bar(
                            name="Spent",
                            x=filtered_df["L4"],
                            y=filtered_df["Spent"],
                            marker_color=colors,  # Colors based on conditions
                        )
                    )

                    # Update layout for better visualization
                    fig.update_layout(
                        xaxis_title="Categories",
                        yaxis_title="Values",
                        barmode="group",  # Group bars
                    )

                    # Display the chart in Streamlit
                    st.subheader("Cost by L4 Chart")
                    st.plotly_chart(fig, key="we3dffewfefdwewew")

            col51, col52 = st.columns(2, gap="medium",vertical_alignment='center')
            new_data_47 = L5_Grouped[L5_Grouped["L4"] == selected_category_L4]
            L5_Grouped = L5_Grouped.rename(
                columns={
                    "Main": "Spent",
                    "1st Comparison": "Budget",
                    "Var Comp&Main": "Delta",
                }
            )
            with col51:
                with st.container(height=500, border=False):
                    # User filter input
                    selected_category_L5 = st.selectbox(
                        "Filter by Order:",
                        ["All"] + list(new_data_47["AccountAndDescpription"].unique()),
                        key="2ff5frtgr445gg4gdr45ef",
                    )
                    # Apply the filter
                    if selected_category_L4 != "All":
                        if selected_category_L5 != "All":
                            filtered_df = L5_Grouped[
                                (
                                    L5_Grouped["AccountAndDescpription"]
                                    == selected_category_L5
                                )
                                & (L5_Grouped["Order"] == selected_category_Order)
                                & (L5_Grouped["L3"] == selected_category)
                                & (L5_Grouped["L4"] == selected_category_L4)
                            ]
                            filtered_df = filtered_df.sort_values(
                                by="Delta", ascending=True
                            )
                        else:
                            filtered_df = L5_Grouped[
                                L5_Grouped["L4"] == selected_category_L4
                            ]
                            filtered_df = filtered_df.sort_values(
                                by="Delta", ascending=True
                            )
                    else:
                        filtered_df = L5_Grouped[
                            L5_Grouped["L4"] == selected_category_L4
                        ]
                        filtered_df = filtered_df.sort_values(
                            by="Delta", ascending=True
                        )
                    coli31, coli32, coli33 = st.columns(
                        3, border=True, vertical_alignment="center"
                    )
                    with coli31:
                        st.metric(
                            label="Budget", value=f"£{filtered_df['Budget'].sum():,.2f}"
                        )
                    with coli32:
                        st.metric(
                            label="Spent", value=f"£{filtered_df['Spent'].sum():,.2f}"
                        )
                    with coli33:
                        st.metric(
                            label="Delta",
                            value=f"£{filtered_df['Delta'].sum():,.2f}",
                            delta=f"{(((filtered_df['Budget'].sum()) - (filtered_df['Spent'].sum()))/(filtered_df['Budget'].sum()))*100:.2f}%",
                        )
                    # Apply styling to the 'Order' column based on 'Delta'
                    if "Delta" in filtered_df.columns:
                        styled_df = filtered_df.style.apply(
                            lambda row: [
                                (
                                    color_code(row)
                                    if col == "AccountAndDescpription"
                                    else ""
                                )
                                for col in filtered_df.columns
                            ],
                            axis=1,
                        )
                        # Display in Streamlit
                        st.dataframe(styled_df, use_container_width=True)
                    else:
                        st.error("Column 'Delta' is missing from the DataFrame")

            with col52:
                with st.container(height=500, border=False):
                    # Assign colors to the bars based on your conditions
                    colors = np.where(
                        (filtered_df["Budget"] == 0),
                        "orange",
                        np.where(
                            (filtered_df["Spent"] > filtered_df["Budget"]),
                            "red",
                            "green",
                        ),
                    )

                    # Create a grouped bar chart
                    fig = go.Figure()

                    # Add first column for Budget
                    fig.add_trace(
                        go.Bar(
                            name="Budget",
                            x=filtered_df["AccountAndDescpription"],
                            y=filtered_df["Budget"],
                            marker_color="blue",  # Fixed color for Budget
                        )
                    )

                    # Add second column for Spent with dynamic colors
                    fig.add_trace(
                        go.Bar(
                            name="Spent",
                            x=filtered_df["AccountAndDescpription"],
                            y=filtered_df["Spent"],
                            marker_color=colors,  # Colors based on conditions
                        )
                    )

                    # Update layout for better visualization
                    fig.update_layout(
                        xaxis_title="Categories",
                        yaxis_title="Values",
                        barmode="group",  # Group bars
                    )

                    # Display the chart in Streamlit
                    st.subheader("Cost by Account Bar Chart")
                    st.plotly_chart(fig, key="we3redwededffewfefdwewew")

        if (month == "February") & (year == "2025") & (data == "Variable Costs"):
            Feb_2025 = Feb_2025.iloc[:, 0:8]
            Feb_2025 = Feb_2025.fillna(0)
            Feb_2025_complete = Feb_2025.groupby(["Category"]).sum(list).reset_index()
            Feb_2025_Variable_Cost_Data = Feb_2025[(Feb_2025["Category"] == "Variable Costs")]
            L1_Grouped = (
                Feb_2025_Variable_Cost_Data.groupby(["Category"]).sum(list).reset_index()
            )
            L2_Grouped = (
                Feb_2025_Variable_Cost_Data.groupby(["Category", "Order"])
                .sum(list)
                .reset_index()
            )
            L3_Grouped = (
                Feb_2025_Variable_Cost_Data.groupby(["Category", "Order", "L3"])
                .sum(list)
                .reset_index()
            )
            L4_Grouped = (
                Feb_2025_Variable_Cost_Data.groupby(["Category", "Order", "L3", "L4"])
                .sum(list)
                .reset_index()
            )
            L5_Grouped = (
                Feb_2025_Variable_Cost_Data.groupby(
                    ["Category", "Order", "L3", "L4", "AccountAndDescpription"]
                )
                .sum(list)
                .reset_index()
            )

            grouped_dfs = {
                "L1_Grouped": ("Category", L1_Grouped),
                "L2_Grouped": ("Order", L2_Grouped),
                "L3_Grouped": ("L3", L3_Grouped),
                "L4_Grouped": ("L4", L4_Grouped),
                "L5_Grouped": ("AccountAndDescpription", L5_Grouped),
            }
            # Dictionary to store parsed DataFrames
            parsed_dfs = {}

            # Loop through each grouped DataFrame
            for key, (category_column, df) in grouped_dfs.items():
                data = []

                for _, row in df.iterrows():
                    budget, spent, delta = (
                        row["1st Comparison"],
                        row["Main"],
                        row["Var Comp&Main"],
                    )
                    data.append(
                        [row[category_column], budget, spent, delta]
                    )  # Dynamically get category column

                # Convert to DataFrame and store in dictionary
                parsed_dfs[key] = pd.DataFrame(
                    data, columns=["Category", "Budget", "Main", "Delta"]
                )
            # Access parsed DataFrames, e.g.:
            df_parsed_1 = parsed_dfs["L1_Grouped"]
            df_parsed_2 = parsed_dfs["L2_Grouped"]
            df_parsed_3 = parsed_dfs["L3_Grouped"]
            df_parsed_4 = parsed_dfs["L4_Grouped"]
            df_parsed_5 = parsed_dfs["L5_Grouped"]

            Feb_Budget = float(Feb_2025_complete["1st Comparison"].sum())
            Feb_spent = float(Feb_2025_complete["Main"].sum())
            Feb_Delta = float(Feb_2025_complete["Var Comp&Main"].sum())
            Feb_delta_percent = (((Feb_Budget) - (Feb_spent)) / (Feb_Budget)) * 100
            Feb_Variable_Budget = float(df_parsed_1["Budget"].iloc[0])
            Feb_Variable_Spent = float(df_parsed_1["Main"].iloc[0])
            Feb_Variable_Delta = float(df_parsed_1["Delta"].iloc[0])
            Feb_Variable_Delta_Percent = (
                ((Feb_Variable_Budget) - (Feb_Variable_Spent)) / (Feb_Variable_Budget)
            ) * 100
            cols1, cols2 = st.columns(2)
            with cols1:
                st.header("Monthly Summary")
            with cols2:
                st.header("Cost Summary")
            col1, col2, col3, col4, col5, col6 = st.columns(
                6, gap="medium", vertical_alignment="center"
            )
            with col1:
                st.metric(
                    "Feburary Budget",
                    value=f"£{Feb_Budget:,.2f}",
                    border=True,
                    help="This is the total budget for Feburary.",
                )
            with col2:
                st.metric(
                    "Feburary Spent",
                    value=f"£{Feb_spent:,.2f}",
                    border=True,
                    help="This is the total amount of funds spent in Feburary.",
                )
            with col3:
                st.metric(
                    "Feburary Delta",
                    value=f"£{Feb_Delta:,.2f}",
                    border=True,
                    delta=f"{Feb_delta_percent:,.2f} %",
                    help="This is the difference in the amount budgeted and the amount spent for Febauary.",
                )
            with col4:
                st.metric(
                    "Feburary Variable Cost Budget",
                    value=f"£{Feb_Variable_Budget:,.2f}",
                    border=True,
                    help="This is the total amount budgeted to be spent for Variable Costs in Feburary.",
                )
            with col5:
                st.metric(
                    "Feburary Variable Cost Spent",
                    value=f"£{Feb_Variable_Spent:,.2f}",
                    border=True,
                    help="This is the total amount spent for Variable Cost in Febauary.",
                )
            with col6:
                st.metric(
                    "Feburary Variable Cost Delta",
                    value=f"£{Feb_Variable_Delta:,.2f}",
                    border=True,
                    delta=f"{Feb_Variable_Delta_Percent:,.2f}%",
                    help="This is the difference in the budgeted amount and Spent amount for Variable Costs in Feburary.",
                )

            col21, col22 = st.columns(2, gap="medium", vertical_alignment="center")
            with col21:
                with st.container(height=500, border=False):
                    L2_Grouped = L2_Grouped.rename(
                        columns={
                            "Main": "Spent",
                            "1st Comparison": "Budget",
                            "Var Comp&Main": "Delta",
                        }
                    )
                    # User filter input
                    selected_category_Order = st.selectbox(
                        "Filter by Order:",
                        ["All"] + list(L2_Grouped["Order"].unique()),
                        key="FIlter by Order",
                    )

                    # Apply the filter
                    if selected_category_Order != "All":
                        filtered_df = L2_Grouped[
                            (L2_Grouped["Order"] == selected_category_Order)
                            & (L2_Grouped["Order"] == selected_category_Order)
                        ]
                        filtered_df = filtered_df.sort_values(
                            by="Delta", ascending=True
                        )
                    else:
                        filtered_df = L2_Grouped
                        filtered_df = filtered_df.sort_values(
                            by="Delta", ascending=True
                        )
                    filtered_df.columns = filtered_df.columns.str.strip()
                    filtered_df[["Spent", "Budget", "Delta"]] = filtered_df[
                        ["Spent", "Budget", "Delta"]
                    ].apply(pd.to_numeric, errors="coerce")
                    coli1, coli2, coli3 = st.columns(
                        3, border=True, vertical_alignment="center"
                    )
                    with coli1:
                        st.metric(
                            label="Budget", value=f"£{filtered_df['Budget'].sum():,.2f}"
                        )
                    with coli2:
                        st.metric(
                            label="Spent", value=f"£{filtered_df['Spent'].sum():,.2f}"
                        )
                    with coli3:
                        st.metric(
                            label="Delta",
                            value=f"£{filtered_df['Delta'].sum():,.2f}",
                            delta=f"{(((filtered_df['Budget'].sum()) - (filtered_df['Spent'].sum()))/(filtered_df['Budget'].sum()))*100:.2f}%",
                        )
                    # Apply styling to the 'Order' column based on 'Delta'
                    if "Delta" in filtered_df.columns:
                        styled_df = filtered_df.style.apply(
                            lambda row: [
                                color_code(row) if col == "Order" else ""
                                for col in filtered_df.columns
                            ],
                            axis=1,
                        )
                        # Display in Streamlit
                        st.dataframe(styled_df, use_container_width=True)
                    else:
                        st.error("Column 'Delta' is missing from the DataFrame")

            with col22:
                with st.container(height=500, border=False):
                    # Assign colors to the bars based on your conditions
                    colors = np.where(
                        (filtered_df["Budget"] == 0),
                        "orange",
                        np.where(
                            (filtered_df["Spent"] > filtered_df["Budget"]),
                            "red",
                            "green",
                        ),
                    )

                    # Create a grouped bar chart
                    fig = go.Figure()

                    # Add first column for Budget
                    fig.add_trace(
                        go.Bar(
                            name="Budget",
                            x=filtered_df["Order"],
                            y=filtered_df["Budget"],
                            marker_color="blue",  # Variable color for Budget
                        )
                    )

                    # Add second column for Spent with dynamic colors
                    fig.add_trace(
                        go.Bar(
                            name="Spent",
                            x=filtered_df["Order"],
                            y=filtered_df["Spent"],
                            marker_color=colors,  # Colors based on conditions
                        )
                    )

                    # Update layout for better visualization
                    fig.update_layout(
                        xaxis_title="Categories",
                        yaxis_title="Values",
                        barmode="group",  # Group bars
                    )

                    # Display the chart in Streamlit
                    st.subheader("Cost by Order Bar Chart")
                    st.plotly_chart(fig, key="weerwewew")

            col31, col32 = st.columns(2, gap="medium",vertical_alignment='center')
            new_data_45 = L3_Grouped[L3_Grouped["Order"] == selected_category_Order]
            L3_Grouped = L3_Grouped.rename(
                columns={
                    "Main": "Spent",
                    "1st Comparison": "Budget",
                    "Var Comp&Main": "Delta",
                }
            )
            with col31:
                with st.container(height=500, border=False):
                    # User filter input
                    selected_category = st.selectbox(
                        "Filter by Level 3:",
                        ["All"] + list(new_data_45["L3"].unique()),
                        key="thrgreg",
                    )
                    # Apply the filter
                    if selected_category_Order != "All":
                        if selected_category != "All":
                            filtered_df = L3_Grouped[
                                (L3_Grouped["L3"] == selected_category)
                                & (L3_Grouped["Order"] == selected_category_Order)
                            ]
                            filtered_df = filtered_df.sort_values(
                                by="Delta", ascending=True
                            )
                        else:
                            filtered_df = L3_Grouped[
                                L3_Grouped["Order"] == selected_category_Order
                            ]
                            filtered_df = filtered_df.sort_values(
                                by="Delta", ascending=True
                            )
                    else:
                        filtered_df = L3_Grouped[
                            L3_Grouped["Order"] == selected_category_Order
                        ]
                        filtered_df = filtered_df.sort_values(
                            by="Delta", ascending=True
                        )
                    coli31, coli32, coli33 = st.columns(
                        3, border=True, vertical_alignment="center"
                    )
                    with coli31:
                        st.metric(
                            label="Budget", value=f"£{filtered_df['Budget'].sum():,.2f}"
                        )
                    with coli32:
                        st.metric(
                            label="Spent", value=f"£{filtered_df['Spent'].sum():,.2f}"
                        )
                    with coli33:
                        st.metric(
                            label="Delta",
                            value=f"£{filtered_df['Delta'].sum():,.2f}",
                            delta=f"{(((filtered_df['Budget'].sum()) - (filtered_df['Spent'].sum()))/(filtered_df['Budget'].sum()))*100:.2f}%",
                        )
                    # Apply styling to the 'Order' column based on 'Delta'
                    if "Delta" in filtered_df.columns:
                        styled_df = filtered_df.style.apply(
                            lambda row: [
                                color_code(row) if col == "L3" else ""
                                for col in filtered_df.columns
                            ],
                            axis=1,
                        )
                        # Display in Streamlit
                        st.dataframe(styled_df, use_container_width=True)
                    else:
                        st.error("Column 'Delta' is missing from the DataFrame")

            with col32:
                with st.container(height=500, border=False):
                    # Assign colors to the bars based on your conditions
                    colors = np.where(
                        (filtered_df["Budget"] == 0),
                        "orange",
                        np.where(
                            (filtered_df["Spent"] > filtered_df["Budget"]),
                            "red",
                            "green",
                        ),
                    )
                    # Create a grouped bar chart
                    fig = go.Figure()

                    # Add first column for Budget
                    fig.add_trace(
                        go.Bar(
                            name="Budget",
                            x=filtered_df["L3"],
                            y=filtered_df["Budget"],
                            marker_color="blue",  # Variable color for Budget
                        )
                    )

                    # Add second column for Spent with dynamic colors
                    fig.add_trace(
                        go.Bar(
                            name="Spent",
                            x=filtered_df["L3"],
                            y=filtered_df["Spent"],
                            marker_color=colors,  # Colors based on conditions
                        )
                    )

                    # Update layout for better visualization
                    fig.update_layout(
                        xaxis_title="Categories",
                        yaxis_title="Values",
                        barmode="group",  # Group bars
                    )

                    # Display the chart in Streamlit
                    st.subheader("Cost by L3 Bar Chart")
                    st.plotly_chart(fig, key="we3refewfefdwewew")

            col41, col42 = st.columns(2, gap="medium",vertical_alignment='center')
            new_data_46 = L4_Grouped[L4_Grouped["L3"] == selected_category]
            L4_Grouped = L4_Grouped.rename(
                columns={
                    "Main": "Spent",
                    "1st Comparison": "Budget",
                    "Var Comp&Main": "Delta",
                }
            )
            with col41:
                with st.container(height=500, border=False):
                    # User filter input
                    selected_category_L4 = st.selectbox(
                        "Filter by L4:",
                        ["All"] + list(new_data_46["L4"].unique()),
                        key="2f44343r34353535356fef",
                    )
                    # Apply the filter
                    if selected_category != "All":
                        if selected_category_L4 != "All":
                            filtered_df = L4_Grouped[
                                (L4_Grouped["L4"] == selected_category_L4)
                                & (L4_Grouped["Order"] == selected_category_Order)
                                & (L4_Grouped["L3"] == selected_category)
                            ]
                            filtered_df = filtered_df.sort_values(
                                by="Delta", ascending=True
                            )
                        else:
                            filtered_df = L4_Grouped[
                                L4_Grouped["L3"] == selected_category
                            ]
                            filtered_df = filtered_df.sort_values(
                                by="Delta", ascending=True
                            )
                    else:
                        filtered_df = L4_Grouped[L4_Grouped["L3"] == selected_category]
                        filtered_df = filtered_df.sort_values(
                            by="Delta", ascending=True
                        )
                    coli31, coli32, coli33 = st.columns(
                        3, border=True, vertical_alignment="center"
                    )
                    with coli31:
                        st.metric(
                            label="Budget", value=f"£{filtered_df['Budget'].sum():,.2f}"
                        )
                    with coli32:
                        st.metric(
                            label="Spent", value=f"£{filtered_df['Spent'].sum():,.2f}"
                        )
                    with coli33:
                        st.metric(
                            label="Delta",
                            value=f"£{filtered_df['Delta'].sum():,.2f}",
                            delta=f"{(((filtered_df['Budget'].sum()) - (filtered_df['Spent'].sum()))/(filtered_df['Budget'].sum()))*100:.2f}%",
                        )
                    # Apply styling to the 'Order' column based on 'Delta'
                    if "Delta" in filtered_df.columns:
                        styled_df = filtered_df.style.apply(
                            lambda row: [
                                color_code(row) if col == "L4" else ""
                                for col in filtered_df.columns
                            ],
                            axis=1,
                        )
                        # Display in Streamlit
                        st.dataframe(styled_df, use_container_width=True)
                    else:
                        st.error("Column 'Delta' is missing from the DataFrame")
            with col42:
                with st.container(height=500, border=False):
                    # Assign colors to the bars based on your conditions
                    colors = np.where(
                        (filtered_df["Budget"] == 0),
                        "orange",
                        np.where(
                            (filtered_df["Spent"] > filtered_df["Budget"]),
                            "red",
                            "green",
                        ),
                    )

                    # Create a grouped bar chart
                    fig = go.Figure()

                    # Add first column for Budget
                    fig.add_trace(
                        go.Bar(
                            name="Budget",
                            x=filtered_df["L4"],
                            y=filtered_df["Budget"],
                            marker_color="blue",  # Variable color for Budget
                        )
                    )

                    # Add second column for Spent with dynamic colors
                    fig.add_trace(
                        go.Bar(
                            name="Spent",
                            x=filtered_df["L4"],
                            y=filtered_df["Spent"],
                            marker_color=colors,  # Colors based on conditions
                        )
                    )

                    # Update layout for better visualization
                    fig.update_layout(
                        xaxis_title="Categories",
                        yaxis_title="Values",
                        barmode="group",  # Group bars
                    )

                    # Display the chart in Streamlit
                    st.subheader("Cost by L4 Chart")
                    st.plotly_chart(fig, key="we3dffewfefdwewew")

            col51, col52 = st.columns(2, gap="medium",vertical_alignment='center')
            new_data_47 = L5_Grouped[L5_Grouped["L4"] == selected_category_L4]
            L5_Grouped = L5_Grouped.rename(
                columns={
                    "Main": "Spent",
                    "1st Comparison": "Budget",
                    "Var Comp&Main": "Delta",
                }
            )
            with col51:
                with st.container(height=500, border=False):
                    # User filter input
                    selected_category_L5 = st.selectbox(
                        "Filter by Order:",
                        ["All"] + list(new_data_47["AccountAndDescpription"].unique()),
                        key="2ff5frtgr445gg4gdr45ef",
                    )
                    # Apply the filter
                    if selected_category_L4 != "All":
                        if selected_category_L5 != "All":
                            filtered_df = L5_Grouped[
                                (
                                    L5_Grouped["AccountAndDescpription"]
                                    == selected_category_L5
                                )
                                & (L5_Grouped["Order"] == selected_category_Order)
                                & (L5_Grouped["L3"] == selected_category)
                                & (L5_Grouped["L4"] == selected_category_L4)
                            ]
                            filtered_df = filtered_df.sort_values(
                                by="Delta", ascending=True
                            )
                        else:
                            filtered_df = L5_Grouped[
                                L5_Grouped["L4"] == selected_category_L4
                            ]
                            filtered_df = filtered_df.sort_values(
                                by="Delta", ascending=True
                            )
                    else:
                        filtered_df = L5_Grouped[
                            L5_Grouped["L4"] == selected_category_L4
                        ]
                        filtered_df = filtered_df.sort_values(
                            by="Delta", ascending=True
                        )
                    coli31, coli32, coli33 = st.columns(
                        3, border=True, vertical_alignment="center"
                    )
                    with coli31:
                        st.metric(
                            label="Budget", value=f"£{filtered_df['Budget'].sum():,.2f}"
                        )
                    with coli32:
                        st.metric(
                            label="Spent", value=f"£{filtered_df['Spent'].sum():,.2f}"
                        )
                    with coli33:
                        st.metric(
                            label="Delta",
                            value=f"£{filtered_df['Delta'].sum():,.2f}",
                            delta=f"{(((filtered_df['Budget'].sum()) - (filtered_df['Spent'].sum()))/(filtered_df['Budget'].sum()))*100:.2f}%",
                        )
                    # Apply styling to the 'Order' column based on 'Delta'
                    if "Delta" in filtered_df.columns:
                        styled_df = filtered_df.style.apply(
                            lambda row: [
                                (
                                    color_code(row)
                                    if col == "AccountAndDescpription"
                                    else ""
                                )
                                for col in filtered_df.columns
                            ],
                            axis=1,
                        )
                        # Display in Streamlit
                        st.dataframe(styled_df, use_container_width=True)
                    else:
                        st.error("Column 'Delta' is missing from the DataFrame")

            with col52:
                with st.container(height=500, border=False):
                    # Assign colors to the bars based on your conditions
                    colors = np.where(
                        (filtered_df["Budget"] == 0),
                        "orange",
                        np.where(
                            (filtered_df["Spent"] > filtered_df["Budget"]),
                            "red",
                            "green",
                        ),
                    )

                    # Create a grouped bar chart
                    fig = go.Figure()

                    # Add first column for Budget
                    fig.add_trace(
                        go.Bar(
                            name="Budget",
                            x=filtered_df["AccountAndDescpription"],
                            y=filtered_df["Budget"],
                            marker_color="blue",  # Variable color for Budget
                        )
                    )

                    # Add second column for Spent with dynamic colors
                    fig.add_trace(
                        go.Bar(
                            name="Spent",
                            x=filtered_df["AccountAndDescpription"],
                            y=filtered_df["Spent"],
                            marker_color=colors,  # Colors based on conditions
                        )
                    )

                    # Update layout for better visualization
                    fig.update_layout(
                        xaxis_title="Months",
                        yaxis_title="Values",
                        barmode="group",  # Group bars
                    )

                    # Display the chart in Streamlit
                    st.subheader("Cost by Account Bar Chart")
                    st.plotly_chart(fig, key="we3redwededffewfefdwewew")
        
        if (month == "March") & (year == "2025") & (data == "Fixed Costs"):
            if Mar_2025.empty:
                st.info('No data available fot this month.')
            else:
                Mar_2025 = Mar_2025.iloc[:, 0:8]
                Mar_2025 = Mar_2025.fillna(0)
                Mar_2025_complete = Mar_2025.groupby(["Category"]).sum(list).reset_index()
                Mar_2025_Fixed_Cost_Data = Mar_2025[(Mar_2025["Category"] == "Fixed Costs")]
                L1_Grouped = Mar_2025_Fixed_Cost_Data.groupby(["Category"]).sum(list).reset_index()
                L2_Grouped = (
                    Mar_2025_Fixed_Cost_Data.groupby(["Category", "Order"]).sum(list).reset_index()
                )
                L3_Grouped = (
                    Mar_2025_Fixed_Cost_Data.groupby(["Category", "Order", "L3"])
                    .sum(list)
                    .reset_index()
                )
                L4_Grouped = (
                    Mar_2025_Fixed_Cost_Data.groupby(["Category", "Order", "L3", "L4"])
                    .sum(list)
                    .reset_index()
                )
                L5_Grouped = (
                    Mar_2025_Fixed_Cost_Data.groupby(
                        ["Category", "Order", "L3", "L4", "AccountAndDescpription"]
                    )
                    .sum(list)
                    .reset_index()
                )

                grouped_dfs = {
                    "L1_Grouped": ("Category", L1_Grouped),
                    "L2_Grouped": ("Order", L2_Grouped),
                    "L3_Grouped": ("L3", L3_Grouped),
                    "L4_Grouped": ("L4", L4_Grouped),
                    "L5_Grouped": ("AccountAndDescpription", L5_Grouped),
                }
                # Dictionary to store parsed DataFrames
                parsed_dfs = {}

                # Loop through each grouped DataFrame
                for key, (category_column, df) in grouped_dfs.items():
                    data = []

                    for _, row in df.iterrows():
                        budget, spent, delta = (
                            row["1st Comparison"],
                            row["Main"],
                            row["Var Comp&Main"],
                        )
                        data.append(
                            [row[category_column], budget, spent, delta]
                        )  # Dynamically get category column

                    # Convert to DataFrame and store in dictionary
                    parsed_dfs[key] = pd.DataFrame(
                        data, columns=["Category", "Budget", "Main", "Delta"]
                    )
                # Access parsed DataFrames, e.g.:
                df_parsed_1 = parsed_dfs["L1_Grouped"]
                df_parsed_2 = parsed_dfs["L2_Grouped"]
                df_parsed_3 = parsed_dfs["L3_Grouped"]
                df_parsed_4 = parsed_dfs["L4_Grouped"]
                df_parsed_5 = parsed_dfs["L5_Grouped"]

                Mar_Budget = float(Mar_2025_complete["1st Comparison"].sum())
                Mar_spent = float(Mar_2025_complete["Main"].sum())
                Mar_Delta = float(Mar_2025_complete["Var Comp&Main"].sum())
                Mar_delta_percent = (((Mar_Budget) - (Mar_spent)) / (Mar_Budget)) * 100
                Mar_Fixed_Budget = float(df_parsed_1["Budget"].iloc[0])
                Mar_Fixed_Spent = float(df_parsed_1["Main"].iloc[0])
                Mar_Fixed_Delta = float(df_parsed_1["Delta"].iloc[0])
                Mar_Fixed_Delta_Percent = (
                    ((Mar_Fixed_Budget) - (Mar_Fixed_Spent)) / (Mar_Fixed_Budget)
                ) * 100
                cols1, cols2 = st.columns(2)
                with cols1:
                    st.header("Monthly Summary")
                with cols2:
                    st.header("Cost Summary")
                col1, col2, col3, col4, col5, col6 = st.columns(
                    6, gap="medium", vertical_alignment="center"
                )
                with col1:
                    st.metric(
                        "March Budget",
                        value=f"£{Mar_Budget:,.2f}",
                        border=True,
                        help="This is the total budget for March.",
                    )
                with col2:
                    st.metric(
                        "March Spent",
                        value=f"£{Mar_spent:,.2f}",
                        border=True,
                        help="This is the total amount of funds spent in March.",
                    )
                with col3:
                    st.metric(
                        "March Delta",
                        value=f"£{Mar_Delta:,.2f}",
                        border=True,
                        delta=f"{Mar_delta_percent:,.2f} %",
                        help="This is the difference in the amount budgeted and the amount spent for Marauary.",
                    )
                with col4:
                    st.metric(
                        "March Fixed Cost Budget",
                        value=f"£{Mar_Fixed_Budget:,.2f}",
                        border=True,
                        help="This is the total amount budgeted to be spent for Fixed Costs in March.",
                    )
                with col5:
                    st.metric(
                        "March Fixed Cost Spent",
                        value=f"£{Mar_Fixed_Spent:,.2f}",
                        border=True,
                        help="This is the total amount spent for Fixed Cost in Marauary.",
                    )
                with col6:
                    st.metric(
                        "March Fixed Cost Delta",
                        value=f"£{Mar_Fixed_Delta:,.2f}",
                        border=True,
                        delta=f"{Mar_Fixed_Delta_Percent:,.2f}%",
                        help="This is the difference in the budgeted amount and Spent amount for Fixed Costs in March.",
                    )

                col21, col22 = st.columns(2, gap="medium", vertical_alignment="center")
                with col21:
                    with st.container(height=500, border=False):
                        L2_Grouped = L2_Grouped.rename(
                            columns={
                                "Main": "Spent",
                                "1st Comparison": "Budget",
                                "Var Comp&Main": "Delta",
                            }
                        )
                        # User filter input
                        selected_category_Order = st.selectbox(
                            "Filter by Order:",
                            ["All"] + list(L2_Grouped["Order"].unique()),
                            key="FIlter by Order",
                        )

                        # Apply the filter
                        if selected_category_Order != "All":
                            filtered_df = L2_Grouped[
                                (L2_Grouped["Order"] == selected_category_Order)
                                & (L2_Grouped["Order"] == selected_category_Order)
                            ]
                            filtered_df = filtered_df.sort_values(by="Delta", ascending=True)
                        else:
                            filtered_df = L2_Grouped
                            filtered_df = filtered_df.sort_values(by="Delta", ascending=True)
                        filtered_df.columns = filtered_df.columns.str.strip()
                        filtered_df[["Spent", "Budget", "Delta"]] = filtered_df[
                            ["Spent", "Budget", "Delta"]
                        ].apply(pd.to_numeric, errors="coerce")
                        coli1, coli2, coli3 = st.columns(
                            3, border=True, vertical_alignment="center"
                        )
                        with coli1:
                            st.metric(label="Budget", value=f"£{filtered_df['Budget'].sum():,.2f}")
                        with coli2:
                            st.metric(label="Spent", value=f"£{filtered_df['Spent'].sum():,.2f}")
                        with coli3:
                            st.metric(
                                label="Delta",
                                value=f"£{filtered_df['Delta'].sum():,.2f}",
                                delta=f"{(((filtered_df['Budget'].sum()) - (filtered_df['Spent'].sum()))/(filtered_df['Budget'].sum()))*100:.2f}%",
                            )
                        # Apply styling to the 'Order' column based on 'Delta'
                        if "Delta" in filtered_df.columns:
                            styled_df = filtered_df.style.apply(
                                lambda row: [
                                    color_code(row) if col == "Order" else ""
                                    for col in filtered_df.columns
                                ],
                                axis=1,
                            )
                            # Display in Streamlit
                            st.dataframe(styled_df, use_container_width=True)
                        else:
                            st.error("Column 'Delta' is missing from the DataFrame")

                with col22:
                    with st.container(height=500, border=False):
                        # Assign colors to the bars based on your conditions
                        colors = np.where(
                            (filtered_df["Budget"] == 0),
                            "orange",
                            np.where(
                                (filtered_df["Spent"] > filtered_df["Budget"]),
                                "red",
                                "green",
                            ),
                        )

                        # Create a grouped bar chart
                        fig = go.Figure()

                        # Add first column for Budget
                        fig.add_trace(
                            go.Bar(
                                name="Budget",
                                x=filtered_df["Order"],
                                y=filtered_df["Budget"],
                                marker_color="blue",  # Fixed color for Budget
                            )
                        )

                        # Add second column for Spent with dynamic colors
                        fig.add_trace(
                            go.Bar(
                                name="Spent",
                                x=filtered_df["Order"],
                                y=filtered_df["Spent"],
                                marker_color=colors,  # Colors based on conditions
                            )
                        )

                        # Update layout for better visualization
                        fig.update_layout(
                            xaxis_title="Categories",
                            yaxis_title="Values",
                            barmode="group",  # Group bars
                        )

                        # Display the chart in Streamlit
                        st.subheader("Cost by Order Bar Chart")
                        st.plotly_chart(fig, key="weerwewew")

                col31, col32 = st.columns(2, gap="medium", vertical_alignment="center")
                new_data_45 = L3_Grouped[L3_Grouped["Order"] == selected_category_Order]
                L3_Grouped = L3_Grouped.rename(
                    columns={
                        "Main": "Spent",
                        "1st Comparison": "Budget",
                        "Var Comp&Main": "Delta",
                    }
                )
                with col31:
                    with st.container(height=500, border=False):
                        # User filter input
                        selected_category = st.selectbox(
                            "Filter by Level 3:",
                            ["All"] + list(new_data_45["L3"].unique()),
                            key="2feefbgtbef",
                        )
                        # Apply the filter
                        if selected_category_Order != "All":
                            if selected_category != "All":
                                filtered_df = L3_Grouped[
                                    (L3_Grouped["L3"] == selected_category)
                                    & (L3_Grouped["Order"] == selected_category_Order)
                                ]
                                filtered_df = filtered_df.sort_values(by="Delta", ascending=True)
                            else:
                                filtered_df = L3_Grouped[
                                    L3_Grouped["Order"] == selected_category_Order
                                ]
                                filtered_df = filtered_df.sort_values(by="Delta", ascending=True)
                        else:
                            filtered_df = L3_Grouped[L3_Grouped["Order"] == selected_category_Order]
                            filtered_df = filtered_df.sort_values(by="Delta", ascending=True)
                        coli31, coli32, coli33 = st.columns(
                            3, border=True, vertical_alignment="center"
                        )
                        with coli31:
                            st.metric(label="Budget", value=f"£{filtered_df['Budget'].sum():,.2f}")
                        with coli32:
                            st.metric(label="Spent", value=f"£{filtered_df['Spent'].sum():,.2f}")
                        with coli33:
                            st.metric(
                                label="Delta",
                                value=f"£{filtered_df['Delta'].sum():,.2f}",
                                delta=f"{(((filtered_df['Budget'].sum()) - (filtered_df['Spent'].sum()))/(filtered_df['Budget'].sum()))*100:.2f}%",
                            )
                        # Apply styling to the 'Order' column based on 'Delta'
                        if "Delta" in filtered_df.columns:
                            styled_df = filtered_df.style.apply(
                                lambda row: [
                                    color_code(row) if col == "L3" else ""
                                    for col in filtered_df.columns
                                ],
                                axis=1,
                            )
                            # Display in Streamlit
                            st.dataframe(styled_df, use_container_width=True)
                        else:
                            st.error("Column 'Delta' is missing from the DataFrame")

                with col32:
                    with st.container(height=500, border=False):
                        # Assign colors to the bars based on your conditions
                        colors = np.where(
                            (filtered_df["Budget"] == 0),
                            "orange",
                            np.where(
                                (filtered_df["Spent"] > filtered_df["Budget"]),
                                "red",
                                "green",
                            ),
                        )
                        # Create a grouped bar chart
                        fig = go.Figure()

                        # Add first column for Budget
                        fig.add_trace(
                            go.Bar(
                                name="Budget",
                                x=filtered_df["L3"],
                                y=filtered_df["Budget"],
                                marker_color="blue",  # Fixed color for Budget
                            )
                        )

                        # Add second column for Spent with dynamic colors
                        fig.add_trace(
                            go.Bar(
                                name="Spent",
                                x=filtered_df["L3"],
                                y=filtered_df["Spent"],
                                marker_color=colors,  # Colors based on conditions
                            )
                        )

                        # Update layout for better visualization
                        fig.update_layout(
                            xaxis_title="Categories",
                            yaxis_title="Values",
                            barmode="group",  # Group bars
                        )

                        # Display the chart in Streamlit
                        st.subheader("Cost by L3 Bar Chart")
                        st.plotly_chart(fig, key="we3refewfefdwewew")

                col41, col42 = st.columns(2, gap="medium", vertical_alignment="center")
                new_data_46 = L4_Grouped[L4_Grouped["L3"] == selected_category]
                L4_Grouped = L4_Grouped.rename(
                    columns={
                        "Main": "Spent",
                        "1st Comparison": "Budget",
                        "Var Comp&Main": "Delta",
                    }
                )
                with col41:
                    with st.container(height=500, border=False):
                        # User filter input
                        selected_category_L4 = st.selectbox(
                            "Filter by L4:",
                            ["All"] + list(new_data_46["L4"].unique()),
                            key="2f44343r34353535356fef",
                        )
                        # Apply the filter
                        if selected_category != "All":
                            if selected_category_L4 != "All":
                                filtered_df = L4_Grouped[
                                    (L4_Grouped["L4"] == selected_category_L4)
                                    & (L4_Grouped["Order"] == selected_category_Order)
                                    & (L4_Grouped["L3"] == selected_category)
                                ]
                                filtered_df = filtered_df.sort_values(by="Delta", ascending=True)
                            else:
                                filtered_df = L4_Grouped[L4_Grouped["L3"] == selected_category]
                                filtered_df = filtered_df.sort_values(by="Delta", ascending=True)
                        else:
                            filtered_df = L4_Grouped[L4_Grouped["L3"] == selected_category]
                            filtered_df = filtered_df.sort_values(by="Delta", ascending=True)
                        coli31, coli32, coli33 = st.columns(
                            3, border=True, vertical_alignment="center"
                        )
                        with coli31:
                            st.metric(label="Budget", value=f"£{filtered_df['Budget'].sum():,.2f}")
                        with coli32:
                            st.metric(label="Spent", value=f"£{filtered_df['Spent'].sum():,.2f}")
                        with coli33:
                            st.metric(
                                label="Delta",
                                value=f"£{filtered_df['Delta'].sum():,.2f}",
                                delta=f"{(((filtered_df['Budget'].sum()) - (filtered_df['Spent'].sum()))/(filtered_df['Budget'].sum()))*100:.2f}%",
                            )
                        # Apply styling to the 'Order' column based on 'Delta'
                        if "Delta" in filtered_df.columns:
                            styled_df = filtered_df.style.apply(
                                lambda row: [
                                    color_code(row) if col == "L4" else ""
                                    for col in filtered_df.columns
                                ],
                                axis=1,
                            )
                            # Display in Streamlit
                            st.dataframe(styled_df, use_container_width=True)
                        else:
                            st.error("Column 'Delta' is missing from the DataFrame")
                with col42:
                    with st.container(height=500, border=False):
                        # Assign colors to the bars based on your conditions
                        colors = np.where(
                            (filtered_df["Budget"] == 0),
                            "orange",
                            np.where(
                                (filtered_df["Spent"] > filtered_df["Budget"]),
                                "red",
                                "green",
                            ),
                        )

                        # Create a grouped bar chart
                        fig = go.Figure()

                        # Add first column for Budget
                        fig.add_trace(
                            go.Bar(
                                name="Budget",
                                x=filtered_df["L4"],
                                y=filtered_df["Budget"],
                                marker_color="blue",  # Fixed color for Budget
                            )
                        )

                        # Add second column for Spent with dynamic colors
                        fig.add_trace(
                            go.Bar(
                                name="Spent",
                                x=filtered_df["L4"],
                                y=filtered_df["Spent"],
                                marker_color=colors,  # Colors based on conditions
                            )
                        )

                        # Update layout for better visualization
                        fig.update_layout(
                            xaxis_title="Categories",
                            yaxis_title="Values",
                            barmode="group",  # Group bars
                        )

                        # Display the chart in Streamlit
                        st.subheader("Cost by L4 Chart")
                        st.plotly_chart(fig, key="we3dffewfefdwewew")

                col51, col52 = st.columns(2, gap="medium", vertical_alignment="center")
                new_data_47 = L5_Grouped[L5_Grouped["L4"] == selected_category_L4]
                L5_Grouped = L5_Grouped.rename(
                    columns={
                        "Main": "Spent",
                        "1st Comparison": "Budget",
                        "Var Comp&Main": "Delta",
                    }
                )
                with col51:
                    with st.container(height=500, border=False):
                        # User filter input
                        selected_category_L5 = st.selectbox(
                            "Filter by Order:",
                            ["All"] + list(new_data_47["AccountAndDescpription"].unique()),
                            key="2ff5frtgr445gg4gdr45ef",
                        )
                        # Apply the filter
                        if selected_category_L4 != "All":
                            if selected_category_L5 != "All":
                                filtered_df = L5_Grouped[
                                    (L5_Grouped["AccountAndDescpription"] == selected_category_L5)
                                    & (L5_Grouped["Order"] == selected_category_Order)
                                    & (L5_Grouped["L3"] == selected_category)
                                    & (L5_Grouped["L4"] == selected_category_L4)
                                ]
                                filtered_df = filtered_df.sort_values(by="Delta", ascending=True)
                            else:
                                filtered_df = L5_Grouped[L5_Grouped["L4"] == selected_category_L4]
                                filtered_df = filtered_df.sort_values(by="Delta", ascending=True)
                        else:
                            filtered_df = L5_Grouped[L5_Grouped["L4"] == selected_category_L4]
                            filtered_df = filtered_df.sort_values(by="Delta", ascending=True)
                        coli31, coli32, coli33 = st.columns(
                            3, border=True, vertical_alignment="center"
                        )
                        with coli31:
                            st.metric(label="Budget", value=f"£{filtered_df['Budget'].sum():,.2f}")
                        with coli32:
                            st.metric(label="Spent", value=f"£{filtered_df['Spent'].sum():,.2f}")
                        with coli33:
                            st.metric(
                                label="Delta",
                                value=f"£{filtered_df['Delta'].sum():,.2f}",
                                delta=f"{(((filtered_df['Budget'].sum()) - (filtered_df['Spent'].sum()))/(filtered_df['Budget'].sum()))*100:.2f}%",
                            )
                        # Apply styling to the 'Order' column based on 'Delta'
                        if "Delta" in filtered_df.columns:
                            styled_df = filtered_df.style.apply(
                                lambda row: [
                                    (color_code(row) if col == "AccountAndDescpription" else "")
                                    for col in filtered_df.columns
                                ],
                                axis=1,
                            )
                            # Display in Streamlit
                            st.dataframe(styled_df, use_container_width=True)
                        else:
                            st.error("Column 'Delta' is missing from the DataFrame")

                with col52:
                    with st.container(height=500, border=False):
                        # Assign colors to the bars based on your conditions
                        colors = np.where(
                            (filtered_df["Budget"] == 0),
                            "orange",
                            np.where(
                                (filtered_df["Spent"] > filtered_df["Budget"]),
                                "red",
                                "green",
                            ),
                        )

                        # Create a grouped bar chart
                        fig = go.Figure()

                        # Add first column for Budget
                        fig.add_trace(
                            go.Bar(
                                name="Budget",
                                x=filtered_df["AccountAndDescpription"],
                                y=filtered_df["Budget"],
                                marker_color="blue",  # Fixed color for Budget
                            )
                        )

                        # Add second column for Spent with dynamic colors
                        fig.add_trace(
                            go.Bar(
                                name="Spent",
                                x=filtered_df["AccountAndDescpription"],
                                y=filtered_df["Spent"],
                                marker_color=colors,  # Colors based on conditions
                            )
                        )

                        # Update layout for better visualization
                        fig.update_layout(
                            xaxis_title="Categories",
                            yaxis_title="Values",
                            barmode="group",  # Group bars
                        )

                        # Display the chart in Streamlit
                        st.subheader("Cost by Account Bar Chart")
                        st.plotly_chart(fig, key="we3redwededffewfefdwewew")

        if (month == "March") & (year == "2025") & (data == "Variable Costs"):
            if Mar_2025.empty:
                st.info('No data available for this month.')
            else:
                Mar_2025 = Mar_2025.iloc[:, 0:8]
                Mar_2025 = Mar_2025.fillna(0)
                Mar_2025_complete = Mar_2025.groupby(["Category"]).sum(list).reset_index()
                Mar_2025_Variable_Cost_Data = Mar_2025[(Mar_2025["Category"] == "Variable Costs")]
                L1_Grouped = (
                    Mar_2025_Variable_Cost_Data.groupby(["Category"]).sum(list).reset_index()
                )
                L2_Grouped = (
                    Mar_2025_Variable_Cost_Data.groupby(["Category", "Order"])
                    .sum(list)
                    .reset_index()
                )
                L3_Grouped = (
                    Mar_2025_Variable_Cost_Data.groupby(["Category", "Order", "L3"])
                    .sum(list)
                    .reset_index()
                )
                L4_Grouped = (
                    Mar_2025_Variable_Cost_Data.groupby(["Category", "Order", "L3", "L4"])
                    .sum(list)
                    .reset_index()
                )
                L5_Grouped = (
                    Mar_2025_Variable_Cost_Data.groupby(
                        ["Category", "Order", "L3", "L4", "AccountAndDescpription"]
                    )
                    .sum(list)
                    .reset_index()
                )

                grouped_dfs = {
                    "L1_Grouped": ("Category", L1_Grouped),
                    "L2_Grouped": ("Order", L2_Grouped),
                    "L3_Grouped": ("L3", L3_Grouped),
                    "L4_Grouped": ("L4", L4_Grouped),
                    "L5_Grouped": ("AccountAndDescpription", L5_Grouped),
                }
                # Dictionary to store parsed DataFrames
                parsed_dfs = {}

                # Loop through each grouped DataFrame
                for key, (category_column, df) in grouped_dfs.items():
                    data = []

                    for _, row in df.iterrows():
                        budget, spent, delta = (
                            row["1st Comparison"],
                            row["Main"],
                            row["Var Comp&Main"],
                        )
                        data.append(
                            [row[category_column], budget, spent, delta]
                        )  # Dynamically get category column

                    # Convert to DataFrame and store in dictionary
                    parsed_dfs[key] = pd.DataFrame(
                        data, columns=["Category", "Budget", "Main", "Delta"]
                    )
                # Access parsed DataFrames, e.g.:
                df_parsed_1 = parsed_dfs["L1_Grouped"]
                df_parsed_2 = parsed_dfs["L2_Grouped"]
                df_parsed_3 = parsed_dfs["L3_Grouped"]
                df_parsed_4 = parsed_dfs["L4_Grouped"]
                df_parsed_5 = parsed_dfs["L5_Grouped"]

                Mar_Budget = float(Mar_2025_complete["1st Comparison"].sum())
                Mar_spent = float(Mar_2025_complete["Main"].sum())
                Mar_Delta = float(Mar_2025_complete["Var Comp&Main"].sum())
                Mar_delta_percent = (((Mar_Budget) - (Mar_spent)) / (Mar_Budget)) * 100
                Mar_Variable_Budget = float(df_parsed_1["Budget"].iloc[0])
                Mar_Variable_Spent = float(df_parsed_1["Main"].iloc[0])
                Mar_Variable_Delta = float(df_parsed_1["Delta"].iloc[0])
                Mar_Variable_Delta_Percent = (
                    ((Mar_Variable_Budget) - (Mar_Variable_Spent)) / (Mar_Variable_Budget)
                ) * 100
                cols1, cols2 = st.columns(2)
                with cols1:
                    st.header("Monthly Summary")
                with cols2:
                    st.header("Cost Summary")
                col1, col2, col3, col4, col5, col6 = st.columns(
                    6, gap="medium", vertical_alignment="center"
                )
                with col1:
                    st.metric(
                        "March Budget",
                        value=f"£{Mar_Budget:,.2f}",
                        border=True,
                        help="This is the total budget for March.",
                    )
                with col2:
                    st.metric(
                        "March Spent",
                        value=f"£{Mar_spent:,.2f}",
                        border=True,
                        help="This is the total amount of funds spent in March.",
                    )
                with col3:
                    st.metric(
                        "March Delta",
                        value=f"£{Mar_Delta:,.2f}",
                        border=True,
                        delta=f"{Mar_delta_percent:,.2f} %",
                        help="This is the difference in the amount budgeted and the amount spent for Marauary.",
                    )
                with col4:
                    st.metric(
                        "March Variable Cost Budget",
                        value=f"£{Mar_Variable_Budget:,.2f}",
                        border=True,
                        help="This is the total amount budgeted to be spent for Variable Costs in March.",
                    )
                with col5:
                    st.metric(
                        "March Variable Cost Spent",
                        value=f"£{Mar_Variable_Spent:,.2f}",
                        border=True,
                        help="This is the total amount spent for Variable Cost in Marauary.",
                    )
                with col6:
                    st.metric(
                        "March Variable Cost Delta",
                        value=f"£{Mar_Variable_Delta:,.2f}",
                        border=True,
                        delta=f"{Mar_Variable_Delta_Percent:,.2f}%",
                        help="This is the difference in the budgeted amount and Spent amount for Variable Costs in March.",
                    )

                col21, col22 = st.columns(2, gap="medium", vertical_alignment="center")
                with col21:
                    with st.container(height=500, border=False):
                        L2_Grouped = L2_Grouped.rename(
                            columns={
                                "Main": "Spent",
                                "1st Comparison": "Budget",
                                "Var Comp&Main": "Delta",
                            }
                        )
                        # User filter input
                        selected_category_Order = st.selectbox(
                            "Filter by Order:",
                            ["All"] + list(L2_Grouped["Order"].unique()),
                            key="FIlter by Order",
                        )

                        # Apply the filter
                        if selected_category_Order != "All":
                            filtered_df = L2_Grouped[
                                (L2_Grouped["Order"] == selected_category_Order)
                                & (L2_Grouped["Order"] == selected_category_Order)
                            ]
                            filtered_df = filtered_df.sort_values(by="Delta", ascending=True)
                        else:
                            filtered_df = L2_Grouped
                            filtered_df = filtered_df.sort_values(by="Delta", ascending=True)
                        filtered_df.columns = filtered_df.columns.str.strip()
                        filtered_df[["Spent", "Budget", "Delta"]] = filtered_df[
                            ["Spent", "Budget", "Delta"]
                        ].apply(pd.to_numeric, errors="coerce")
                        coli1, coli2, coli3 = st.columns(
                            3, border=True, vertical_alignment="center"
                        )
                        with coli1:
                            st.metric(label="Budget", value=f"£{filtered_df['Budget'].sum():,.2f}")
                        with coli2:
                            st.metric(label="Spent", value=f"£{filtered_df['Spent'].sum():,.2f}")
                        with coli3:
                            st.metric(
                                label="Delta",
                                value=f"£{filtered_df['Delta'].sum():,.2f}",
                                delta=f"{(((filtered_df['Budget'].sum()) - (filtered_df['Spent'].sum()))/(filtered_df['Budget'].sum()))*100:.2f}%",
                            )
                        # Apply styling to the 'Order' column based on 'Delta'
                        if "Delta" in filtered_df.columns:
                            styled_df = filtered_df.style.apply(
                                lambda row: [
                                    color_code(row) if col == "Order" else ""
                                    for col in filtered_df.columns
                                ],
                                axis=1,
                            )
                            # Display in Streamlit
                            st.dataframe(styled_df, use_container_width=True)
                        else:
                            st.error("Column 'Delta' is missing from the DataFrame")

                with col22:
                    with st.container(height=500, border=False):
                        # Assign colors to the bars based on your conditions
                        colors = np.where(
                            (filtered_df["Budget"] == 0),
                            "orange",
                            np.where(
                                (filtered_df["Spent"] > filtered_df["Budget"]),
                                "red",
                                "green",
                            ),
                        )

                        # Create a grouped bar chart
                        fig = go.Figure()

                        # Add first column for Budget
                        fig.add_trace(
                            go.Bar(
                                name="Budget",
                                x=filtered_df["Order"],
                                y=filtered_df["Budget"],
                                marker_color="blue",  # Variable color for Budget
                            )
                        )

                        # Add second column for Spent with dynamic colors
                        fig.add_trace(
                            go.Bar(
                                name="Spent",
                                x=filtered_df["Order"],
                                y=filtered_df["Spent"],
                                marker_color=colors,  # Colors based on conditions
                            )
                        )

                        # Update layout for better visualization
                        fig.update_layout(
                            xaxis_title="Categories",
                            yaxis_title="Values",
                            barmode="group",  # Group bars
                        )

                        # Display the chart in Streamlit
                        st.subheader("Cost by Order Bar Chart")
                        st.plotly_chart(fig, key="weerwewew")

                col31, col32 = st.columns(2, gap="medium", vertical_alignment="center")
                new_data_45 = L3_Grouped[L3_Grouped["Order"] == selected_category_Order]
                L3_Grouped = L3_Grouped.rename(
                    columns={
                        "Main": "Spent",
                        "1st Comparison": "Budget",
                        "Var Comp&Main": "Delta",
                    }
                )
                with col31:
                    with st.container(height=500, border=False):
                        # User filter input
                        selected_category = st.selectbox(
                            "Filter by Level 3:",
                            ["All"] + list(new_data_45["L3"].unique()),
                            key="thrgreg",
                        )
                        # Apply the filter
                        if selected_category_Order != "All":
                            if selected_category != "All":
                                filtered_df = L3_Grouped[
                                    (L3_Grouped["L3"] == selected_category)
                                    & (L3_Grouped["Order"] == selected_category_Order)
                                ]
                                filtered_df = filtered_df.sort_values(by="Delta", ascending=True)
                            else:
                                filtered_df = L3_Grouped[
                                    L3_Grouped["Order"] == selected_category_Order
                                ]
                                filtered_df = filtered_df.sort_values(by="Delta", ascending=True)
                        else:
                            filtered_df = L3_Grouped[L3_Grouped["Order"] == selected_category_Order]
                            filtered_df = filtered_df.sort_values(by="Delta", ascending=True)
                        coli31, coli32, coli33 = st.columns(
                            3, border=True, vertical_alignment="center"
                        )
                        with coli31:
                            st.metric(label="Budget", value=f"£{filtered_df['Budget'].sum():,.2f}")
                        with coli32:
                            st.metric(label="Spent", value=f"£{filtered_df['Spent'].sum():,.2f}")
                        with coli33:
                            st.metric(
                                label="Delta",
                                value=f"£{filtered_df['Delta'].sum():,.2f}",
                                delta=f"{(((filtered_df['Budget'].sum()) - (filtered_df['Spent'].sum()))/(filtered_df['Budget'].sum()))*100:.2f}%",
                            )
                        # Apply styling to the 'Order' column based on 'Delta'
                        if "Delta" in filtered_df.columns:
                            styled_df = filtered_df.style.apply(
                                lambda row: [
                                    color_code(row) if col == "L3" else ""
                                    for col in filtered_df.columns
                                ],
                                axis=1,
                            )
                            # Display in Streamlit
                            st.dataframe(styled_df, use_container_width=True)
                        else:
                            st.error("Column 'Delta' is missing from the DataFrame")

                with col32:
                    with st.container(height=500, border=False):
                        # Assign colors to the bars based on your conditions
                        colors = np.where(
                            (filtered_df["Budget"] == 0),
                            "orange",
                            np.where(
                                (filtered_df["Spent"] > filtered_df["Budget"]),
                                "red",
                                "green",
                            ),
                        )
                        # Create a grouped bar chart
                        fig = go.Figure()

                        # Add first column for Budget
                        fig.add_trace(
                            go.Bar(
                                name="Budget",
                                x=filtered_df["L3"],
                                y=filtered_df["Budget"],
                                marker_color="blue",  # Variable color for Budget
                            )
                        )

                        # Add second column for Spent with dynamic colors
                        fig.add_trace(
                            go.Bar(
                                name="Spent",
                                x=filtered_df["L3"],
                                y=filtered_df["Spent"],
                                marker_color=colors,  # Colors based on conditions
                            )
                        )

                        # Update layout for better visualization
                        fig.update_layout(
                            xaxis_title="Categories",
                            yaxis_title="Values",
                            barmode="group",  # Group bars
                        )

                        # Display the chart in Streamlit
                        st.subheader("Cost by L3 Bar Chart")
                        st.plotly_chart(fig, key="we3refewfefdwewew")

                col41, col42 = st.columns(2, gap="medium", vertical_alignment="center")
                new_data_46 = L4_Grouped[L4_Grouped["L3"] == selected_category]
                L4_Grouped = L4_Grouped.rename(
                    columns={
                        "Main": "Spent",
                        "1st Comparison": "Budget",
                        "Var Comp&Main": "Delta",
                    }
                )
                with col41:
                    with st.container(height=500, border=False):
                        # User filter input
                        selected_category_L4 = st.selectbox(
                            "Filter by L4:",
                            ["All"] + list(new_data_46["L4"].unique()),
                            key="2f44343r34353535356fef",
                        )
                        # Apply the filter
                        if selected_category != "All":
                            if selected_category_L4 != "All":
                                filtered_df = L4_Grouped[
                                    (L4_Grouped["L4"] == selected_category_L4)
                                    & (L4_Grouped["Order"] == selected_category_Order)
                                    & (L4_Grouped["L3"] == selected_category)
                                ]
                                filtered_df = filtered_df.sort_values(by="Delta", ascending=True)
                            else:
                                filtered_df = L4_Grouped[L4_Grouped["L3"] == selected_category]
                                filtered_df = filtered_df.sort_values(by="Delta", ascending=True)
                        else:
                            filtered_df = L4_Grouped[L4_Grouped["L3"] == selected_category]
                            filtered_df = filtered_df.sort_values(by="Delta", ascending=True)
                        coli31, coli32, coli33 = st.columns(
                            3, border=True, vertical_alignment="center"
                        )
                        with coli31:
                            st.metric(label="Budget", value=f"£{filtered_df['Budget'].sum():,.2f}")
                        with coli32:
                            st.metric(label="Spent", value=f"£{filtered_df['Spent'].sum():,.2f}")
                        with coli33:
                            st.metric(
                                label="Delta",
                                value=f"£{filtered_df['Delta'].sum():,.2f}",
                                delta=f"{(((filtered_df['Budget'].sum()) - (filtered_df['Spent'].sum()))/(filtered_df['Budget'].sum()))*100:.2f}%",
                            )
                        # Apply styling to the 'Order' column based on 'Delta'
                        if "Delta" in filtered_df.columns:
                            styled_df = filtered_df.style.apply(
                                lambda row: [
                                    color_code(row) if col == "L4" else ""
                                    for col in filtered_df.columns
                                ],
                                axis=1,
                            )
                            # Display in Streamlit
                            st.dataframe(styled_df, use_container_width=True)
                        else:
                            st.error("Column 'Delta' is missing from the DataFrame")
                with col42:
                    with st.container(height=500, border=False):
                        # Assign colors to the bars based on your conditions
                        colors = np.where(
                            (filtered_df["Budget"] == 0),
                            "orange",
                            np.where(
                                (filtered_df["Spent"] > filtered_df["Budget"]),
                                "red",
                                "green",
                            ),
                        )

                        # Create a grouped bar chart
                        fig = go.Figure()

                        # Add first column for Budget
                        fig.add_trace(
                            go.Bar(
                                name="Budget",
                                x=filtered_df["L4"],
                                y=filtered_df["Budget"],
                                marker_color="blue",  # Variable color for Budget
                            )
                        )

                        # Add second column for Spent with dynamic colors
                        fig.add_trace(
                            go.Bar(
                                name="Spent",
                                x=filtered_df["L4"],
                                y=filtered_df["Spent"],
                                marker_color=colors,  # Colors based on conditions
                            )
                        )

                        # Update layout for better visualization
                        fig.update_layout(
                            xaxis_title="Categories",
                            yaxis_title="Values",
                            barmode="group",  # Group bars
                        )

                        # Display the chart in Streamlit
                        st.subheader("Cost by L4 Chart")
                        st.plotly_chart(fig, key="we3dffewfefdwewew")

                col51, col52 = st.columns(2, gap="medium", vertical_alignment="center")
                new_data_47 = L5_Grouped[L5_Grouped["L4"] == selected_category_L4]
                L5_Grouped = L5_Grouped.rename(
                    columns={
                        "Main": "Spent",
                        "1st Comparison": "Budget",
                        "Var Comp&Main": "Delta",
                    }
                )
                with col51:
                    with st.container(height=500, border=False):
                        # User filter input
                        selected_category_L5 = st.selectbox(
                            "Filter by Order:",
                            ["All"] + list(new_data_47["AccountAndDescpription"].unique()),
                            key="2ff5frtgr445gg4gdr45ef",
                        )
                        # Apply the filter
                        if selected_category_L4 != "All":
                            if selected_category_L5 != "All":
                                filtered_df = L5_Grouped[
                                    (L5_Grouped["AccountAndDescpription"] == selected_category_L5)
                                    & (L5_Grouped["Order"] == selected_category_Order)
                                    & (L5_Grouped["L3"] == selected_category)
                                    & (L5_Grouped["L4"] == selected_category_L4)
                                ]
                                filtered_df = filtered_df.sort_values(by="Delta", ascending=True)
                            else:
                                filtered_df = L5_Grouped[L5_Grouped["L4"] == selected_category_L4]
                                filtered_df = filtered_df.sort_values(by="Delta", ascending=True)
                        else:
                            filtered_df = L5_Grouped[L5_Grouped["L4"] == selected_category_L4]
                            filtered_df = filtered_df.sort_values(by="Delta", ascending=True)
                        coli31, coli32, coli33 = st.columns(
                            3, border=True, vertical_alignment="center"
                        )
                        with coli31:
                            st.metric(label="Budget", value=f"£{filtered_df['Budget'].sum():,.2f}")
                        with coli32:
                            st.metric(label="Spent", value=f"£{filtered_df['Spent'].sum():,.2f}")
                        with coli33:
                            st.metric(
                                label="Delta",
                                value=f"£{filtered_df['Delta'].sum():,.2f}",
                                delta=f"{(((filtered_df['Budget'].sum()) - (filtered_df['Spent'].sum()))/(filtered_df['Budget'].sum()))*100:.2f}%",
                            )
                        # Apply styling to the 'Order' column based on 'Delta'
                        if "Delta" in filtered_df.columns:
                            styled_df = filtered_df.style.apply(
                                lambda row: [
                                    (color_code(row) if col == "AccountAndDescpription" else "")
                                    for col in filtered_df.columns
                                ],
                                axis=1,
                            )
                            # Display in Streamlit
                            st.dataframe(styled_df, use_container_width=True)
                        else:
                            st.error("Column 'Delta' is missing from the DataFrame")

                with col52:
                    with st.container(height=500, border=False):
                        # Assign colors to the bars based on your conditions
                        colors = np.where(
                            (filtered_df["Budget"] == 0),
                            "orange",
                            np.where(
                                (filtered_df["Spent"] > filtered_df["Budget"]),
                                "red",
                                "green",
                            ),
                        )

                        # Create a grouped bar chart
                        fig = go.Figure()

                        # Add first column for Budget
                        fig.add_trace(
                            go.Bar(
                                name="Budget",
                                x=filtered_df["AccountAndDescpription"],
                                y=filtered_df["Budget"],
                                marker_color="blue",  # Variable color for Budget
                            )
                        )

                        # Add second column for Spent with dynamic colors
                        fig.add_trace(
                            go.Bar(
                                name="Spent",
                                x=filtered_df["AccountAndDescpription"],
                                y=filtered_df["Spent"],
                                marker_color=colors,  # Colors based on conditions
                            )
                        )

                        # Update layout for better visualization
                        fig.update_layout(
                            xaxis_title="Months",
                            yaxis_title="Values",
                            barmode="group",  # Group bars
                        )

                        # Display the chart in Streamlit
                        st.subheader("Cost by Account Bar Chart")
                        st.plotly_chart(fig, key="we3redwededffewfefdwewew")   
    
    with tab_2:
        Year_To_Date_Total_Spent = Jan_2025['Main'].sum() + Feb_2025['Main'].sum()
        Year_To_Date_Total_Budget = Jan_2025['1st Comparison'].sum() + Feb_2025['1st Comparison'].sum()
        Year_To_Date_Total_Delta = Jan_2025['Var Comp&Main'].sum() + Feb_2025['Var Comp&Main'].sum()
        delta = ((Year_To_Date_Total_Budget - Year_To_Date_Total_Spent)/(Year_To_Date_Total_Budget))*100
        #Create sample data
        data = pd.DataFrame({'Month': ['January', 'February'],
                'Spent': [Jan_2025['Main'].sum(), Feb_2025['Main'].sum()],
                'Budget': [Jan_2025['1st Comparison'].sum(), Feb_2025['1st Comparison'].sum()]})
        cols1,cols2,cols3 = st.columns(3, vertical_alignment='center',border=True)
        with cols1:
            st.metric(value=f"£{Year_To_Date_Total_Spent:,.2f}",label = 'Year to Date Total (Spent)')
        with cols2:
            st.metric(value=f"£{Year_To_Date_Total_Budget:,.2f}",label = 'Year to Date Total (Budget)')
        with cols3:
            st.metric(value=f"£{Year_To_Date_Total_Delta:,.2f}",label = 'Year to Date Total (Delta)', delta = f"{delta:.2f}%")
        
        colss1,cols22,cols23 = st.columns(3,vertical_alignment='center')
        with colss1:
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

            # Display the chart in Streamlit
            st.subheader("Spend by Month Bar Chart")
            st.plotly_chart(fig, key="wferfwwewew")
        with cols22:

            fig = px.line(
                data,
                x='Month',
                y=['Spent', 'Budget'],
                title='Budget vs. Spent Over Months',
                labels={'value': 'Amount', 'Month': 'Month'},
                color_discrete_sequence=['red', 'green']  # Optional customization for colors
            )

            # Display Plotly chart in Streamlit
            st.plotly_chart(fig)
        with cols23:
            # Sample data
                data = {
                    "Cost": [
                        "Fixed Cost",
                        "Variable Cost",
                        "Fixed Cost",
                        "Variable Cost",
                    ],
                    "Month": ["January", "January", "Feburary", "Feburary"],
                    "Values": [
                        Jan_2025[Jan_2025["Category"] == "Fixed Costs"]["Main"].sum(),
                        Jan_2025[Jan_2025["Category"] == "Variable Costs"]["Main"].sum(),
                        Feb_2025[Feb_2025["Category"] == "Fixed Costs"]["Main"].sum(),
                        Feb_2025[Feb_2025["Category"] == "Variable Costs"]["Main"].sum(),
                    ],
                }

                sun_burst_df = pd.DataFrame(data)
                
                # Calculate total value for percentages
                total_value = sun_burst_df['Values'].sum()

                # Create sunburst chart with custom hovertemplate
                fig = px.sunburst(
                    sun_burst_df,
                    path=["Month", "Cost"],
                    values="Values",
                    title="Monthly Spending",
                )

                # Customize hover information
                fig.update_traces(
                    hovertemplate="<b>%{label}</b><br>Value: £%{value}",
                )
                # Adjust chart size
                fig.update_layout(
                    width=500,  # Set the width (increase as needed)
                    height=500  # Set the height (increase as needed)
                )

                # Display chart in Streamlit
                st.plotly_chart(fig, use_container_width=True)
        
        # This section handles the total cost for fixed and variable from beginning of the year to date
        Fixed_cost_YTD_spent = Jan_2025[Jan_2025['Category'] == 'Fixed Costs']['Main'].sum() + Feb_2025[Feb_2025['Category'] == 'Fixed Costs']['Main'].sum()
        Fixed_cost_YTD_Budget = Jan_2025[Jan_2025['Category'] == 'Fixed Costs']['1st Comparison'].sum() + Feb_2025[Feb_2025['Category'] == 'Fixed Costs']['1st Comparison'].sum()
        Fixed_cost_YTD_Delta = Jan_2025[Jan_2025['Category'] == 'Fixed Costs']['Var Comp&Main'].sum() + Feb_2025[Feb_2025['Category'] == 'Fixed Costs']['Var Comp&Main'].sum()
        Fixed_Cost_YTD_Delta_Percent = ((Fixed_cost_YTD_Budget - Fixed_cost_YTD_spent)/Fixed_cost_YTD_Budget ) * 100
        Variable_cost_YTD_spent = Jan_2025[Jan_2025['Category'] == 'Variable Costs']['Main'].sum() + Feb_2025[Feb_2025['Category'] == 'Variable Costs']['Main'].sum()
        Variable_cost_YTD_Budget = Jan_2025[Jan_2025['Category'] == 'Variable Costs']['1st Comparison'].sum() + Feb_2025[Feb_2025['Category'] == 'Variable Costs']['1st Comparison'].sum()
        Variable_cost_YTD_Delta = Jan_2025[Jan_2025['Category'] == 'Variable Costs']['Var Comp&Main'].sum() + Feb_2025[Feb_2025['Category'] == 'Variable Costs']['Var Comp&Main'].sum()
        Variable_Cost_YTD_Delta_Percent = ((Variable_cost_YTD_Budget - Variable_cost_YTD_spent)/Variable_cost_YTD_Budget ) * 100


        #This section handles the summation of data and uses a similar logic to the monthly view page
        #Variables
        # Filter rows where Category is 'Fixed Costs' for both DataFrames
        Jan_2025_filtered_Fixed = Jan_2025[Jan_2025['Category'] == 'Fixed Costs']
        Jan_2025_filtered_Variable = Jan_2025[Jan_2025['Category'] == 'Variable Costs']
        Feb_2025_filtered_Fixed = Feb_2025[Feb_2025['Category'] == 'Fixed Costs']
        Feb_2025_filtered_Variable = Feb_2025[Feb_2025['Category'] == 'Variable Costs']
        
        
        #####################################################################################################
        ############################## L2 Data Variables ####################################################
        #####################################################################################################
        Jan_grouped_Fixed_L2 = Jan_2025_filtered_Fixed.groupby(['Order'])[['Main','1st Comparison', 'Var Comp&Main']].sum()
        Feb_grouped_Fixed_L2 = Feb_2025_filtered_Fixed.groupby(['Order'])[['Main','1st Comparison', 'Var Comp&Main']].sum()
        Jan_grouped_Variable_L2 = Jan_2025_filtered_Variable.groupby(['Order'])[['Main','1st Comparison', 'Var Comp&Main']].sum()
        Feb_grouped_Variable_L2 = Feb_2025_filtered_Variable.groupby(['Order'])[['Main','1st Comparison', 'Var Comp&Main']].sum()
        
        combined_L2_Fixed = Jan_grouped_Fixed_L2.add(Feb_grouped_Fixed_L2, fill_value=0).reset_index().round(2)
        combined_L2_Variable = Jan_grouped_Variable_L2.add(Feb_grouped_Variable_L2, fill_value=0).reset_index()
        
        combined_L2_Fixed.columns = ['Order', 'Total Main', 'Total Budget', 'Total Difference']
        combined_L2_Variable.columns = ['Order', 'Total Main', 'Total Budget', 'Total Difference']
        
        
        #####################################################################################################
        ############################## L3 Data Variables ####################################################
        #####################################################################################################
              
        Jan_grouped_Fixed_L3 = Jan_2025_filtered_Fixed.groupby(['Order','L3'])[['Main','1st Comparison', 'Var Comp&Main']].sum()
        Feb_grouped_Fixed_L3 = Feb_2025_filtered_Fixed.groupby(['Order','L3'])[['Main','1st Comparison', 'Var Comp&Main']].sum()
        Jan_grouped_Variable_L3 = Jan_2025_filtered_Variable.groupby(['Order','L3'])[['Main','1st Comparison', 'Var Comp&Main']].sum()
        Feb_grouped_Variable_L3 = Feb_2025_filtered_Variable.groupby(['Order','L3'])[['Main','1st Comparison', 'Var Comp&Main']].sum()

        combined_L3_Fixed = Jan_grouped_Fixed_L3.add(Feb_grouped_Fixed_L3, fill_value=0).reset_index()
        combined_L3_Variable = Jan_grouped_Variable_L3.add(Feb_grouped_Variable_L3, fill_value=0).reset_index()

        combined_L3_Fixed.columns = ['Order','L3', 'Total Main', 'Total Budget', 'Total Difference']
        combined_L3_Variable.columns = ['Order','L3', 'Total Main', 'Total Budget', 'Total Difference']
        
        
        
        #####################################################################################################
        ############################## L4 Data Variables ####################################################
        #####################################################################################################

        Jan_grouped_Fixed_L4 = Jan_2025_filtered_Fixed.groupby(['Order','L3','L4'])[['Main','1st Comparison', 'Var Comp&Main']].sum()
        Feb_grouped_Fixed_L4 = Feb_2025_filtered_Fixed.groupby(['Order','L3','L4'])[['Main','1st Comparison', 'Var Comp&Main']].sum()
        Jan_grouped_Variable_L4 = Jan_2025_filtered_Variable.groupby(['Order','L3','L4'])[['Main','1st Comparison', 'Var Comp&Main']].sum()
        Feb_grouped_Variable_L4 = Feb_2025_filtered_Variable.groupby(['Order','L3','L4'])[['Main','1st Comparison', 'Var Comp&Main']].sum()

        combined_L4_Fixed = Jan_grouped_Fixed_L4.add(Feb_grouped_Fixed_L4, fill_value=0).reset_index()
        combined_L4_Variable = Jan_grouped_Variable_L4.add(Feb_grouped_Variable_L4, fill_value=0).reset_index()

        combined_L4_Fixed.columns = ['Order','L3','L4', 'Total Main', 'Total Budget', 'Total Difference']
        combined_L4_Variable.columns = ['Order','L3','L4', 'Total Main', 'Total Budget', 'Total Difference']
        
        
        #####################################################################################################
        ############################## L5 Data Variables ####################################################
        #####################################################################################################

        Jan_grouped_Fixed_L5 = Jan_2025_filtered_Fixed.groupby(['Order','L3','L4','AccountAndDescpription'])[['Main','1st Comparison', 'Var Comp&Main']].sum()
        Feb_grouped_Fixed_L5 = Feb_2025_filtered_Fixed.groupby(['Order','L3','L4','AccountAndDescpription'])[['Main','1st Comparison', 'Var Comp&Main']].sum()
        Jan_grouped_Variable_L5 = Jan_2025_filtered_Variable.groupby(['Order','L3','L4','AccountAndDescpription'])[['Main','1st Comparison', 'Var Comp&Main']].sum()
        Feb_grouped_Variable_L5 = Feb_2025_filtered_Variable.groupby(['Order','L3','L4','AccountAndDescpription'])[['Main','1st Comparison', 'Var Comp&Main']].sum()

        combined_L5_Fixed = Jan_grouped_Fixed_L5.add(Feb_grouped_Fixed_L5, fill_value=0).reset_index()
        combined_L5_Variable = Jan_grouped_Variable_L5.add(Feb_grouped_Variable_L5, fill_value=0).reset_index()

        combined_L5_Fixed.columns = ['Order','L3','L4','AccountAndDescpription', 'Total Main', 'Total Budget', 'Total Difference']
        combined_L5_Variable.columns = ['Order','L3','L4','AccountAndDescpription', 'Total Main', 'Total Budget', 'Total Difference']
        
        selected_cost_YTD = st.selectbox(label="Select Cost To Analyse", options=["Fixed Cost", "Variable Cost"])
        
        if selected_cost_YTD == 'Fixed Cost':
            #######################----------------------------------------------#####################################
            data_L2 = {
                        "Fixed Cost Spent": [
                            Jan_grouped_Fixed_L2['Main'].sum(),
                            Feb_grouped_Fixed_L2['Main'].sum(),
                        ],
                        "Fixed Cost Budget": [
                            Jan_grouped_Fixed_L2['1st Comparison'].sum(),
                            Feb_grouped_Fixed_L2['1st Comparison'].sum(),
                        ],
                        "Month": ["January", "Feburary"],

                    }
            
            colsss1,colsss2 = st.columns(2)
            with colsss1:
                st.header('Fixed Cost Analysis (Year To Date)')
            with colsss2:
                st.header('Fixed Cost Analysis Trend by Month (Year To Date)')
            
            with st.container(height=500, border=False):   
                cols1,cols2,cols3,cols4 = st.columns([0.15,0.15,0.15,0.55], vertical_alignment='center')
        
                with cols1:
                    st.metric(value=f"£{Fixed_cost_YTD_Budget:,.2f}",label = 'Fixed Cost Year To Date Budget', border=True)
                with cols2:
                    st.metric(value=f"£{Fixed_cost_YTD_spent:,.2f}",label = 'Fixed Cost Year To Date Spent', border=True)
                with cols3:
                    st.metric(value=f"£{Fixed_cost_YTD_Delta:,.2f}",label = 'Fixed Cost Year To Date Delta', border=True, delta=f"{Fixed_Cost_YTD_Delta_Percent:.2f}%")
                with cols4:
                    fig = px.line(
                        data_L2,
                        x='Month',
                        y=['Fixed Cost Spent', 'Fixed Cost Budget'],
                        title='Budget vs. Spent Over Months',
                        labels={'value': 'Amount', 'Month': 'Month'},
                        color_discrete_sequence=['red', 'green']  # Optional customization for colors
                    )

                    # Display Plotly chart in Streamlit
                    st.plotly_chart(fig)
            # with cols4:
            #     st.metric(value=f"£{Variable_cost_YTD_Budget:,.2f}",label = 'Variable Cost Year To Date Budget', border=True)
            # with cols5:
            #     st.metric(value=f"£{Variable_cost_YTD_spent:,.2f}",label = 'Variable Cost Year To Date Spent', border=True)
            # with cols6:
            #     st.metric(value=f"£{Variable_cost_YTD_Delta:,.2f}",label = 'Variable Cost Year To Date Delta', border=True,delta=f"{Variable_Cost_YTD_Delta_Percent:.2f}%")
                
            clswe11,colswe12 = st.columns(2)
            with clswe11:
                with st.container(height=500, border=False):
                    # User filter input
                    selected_category_Order_L2 = st.selectbox(
                        "Filter by Order:",
                        ["All"] + list(combined_L2_Fixed["Order"].unique()),
                        key="FI5656dby Order",
                    )

                    # Apply the filter
                    if selected_category_Order_L2 != "All":
                        filtered_df = combined_L2_Fixed[
                            (combined_L2_Fixed["Order"] == selected_category_Order_L2)
                            & (combined_L2_Fixed["Order"] == selected_category_Order_L2)
                        ]
                        filtered_df = filtered_df.sort_values(
                            by="Total Difference", ascending=True
                        )
                    else:
                        filtered_df = combined_L2_Fixed
                        filtered_df = filtered_df.sort_values(
                            by='Total Difference', ascending=True
                        )
                    filtered_df.columns = filtered_df.columns.str.strip()
                    filtered_df[['Total Main', 'Total Budget', 'Total Difference']] = filtered_df[
                        ['Total Main', 'Total Budget', 'Total Difference']
                    ].apply(pd.to_numeric, errors="coerce")
                    coli1, coli2, coli3 = st.columns(
                        3, border=True, vertical_alignment="center"
                    )
                    with coli1:
                        st.metric(
                            label="Total Budget", value=f"£{filtered_df['Total Budget'].sum():,.2f}"
                        )
                    with coli2:
                        st.metric(
                            label="Total Spent", value=f"£{filtered_df['Total Main'].sum():,.2f}"
                        )
                    with coli3:
                        st.metric(
                            label="Total Difference",
                            value=f"£{filtered_df['Total Difference'].sum():,.2f}",
                            delta=f"{(((filtered_df['Total Budget'].sum()) - (filtered_df['Total Main'].sum()))/(filtered_df['Total Budget'].sum()))*100:.2f}%",
                        )
                    # Apply styling to the 'Order' column based on 'Delta'
                    if "Total Difference" in filtered_df.columns:
                        styled_df = filtered_df.style.apply(
                            lambda row: [
                                color_code_new(row,"Total Difference") if col == "Order" else ""
                                for col in filtered_df.columns
                            ],
                            axis=1,
                        )
                        # Display in Streamlit
                        st.dataframe(styled_df, use_container_width=True,column_config={"Total Difference": st.column_config.NumberColumn(format="%.2f"),"Total Budget": st.column_config.NumberColumn(format="%.2f"),"Total Main": st.column_config.NumberColumn(format="%.2f")})
                    else:
                        st.error("Column 'Total Difference' is missing from the DataFrame")
                        
            with colswe12:
                with st.container(height=500, border=False):
                        # Assign colors to the bars based on your conditions
                        colors = np.where(
                            (filtered_df["Total Budget"] == 0),
                            "orange",
                            np.where(
                                (filtered_df["Total Main"] > filtered_df["Total Budget"]),
                                "red",
                                "green",
                            ),
                        )

                        # Create a grouped bar chart
                        fig = go.Figure()

                        # Add first column for Budget
                        fig.add_trace(
                            go.Bar(
                                name="Budget",
                                x=filtered_df["Order"],
                                y=filtered_df["Total Budget"],
                                marker_color="blue",  # Fixed color for Budget
                            )
                        )

                        # Add second column for Spent with dynamic colors
                        fig.add_trace(
                            go.Bar(
                                name="Spent",
                                x=filtered_df["Order"],
                                y=filtered_df["Total Main"],
                                marker_color=colors,  # Colors based on conditions
                            )
                        )

                        # Update layout for better visualization
                        fig.update_layout(
                            xaxis_title="Categories",
                            yaxis_title="Values",
                            barmode="group",  # Group bars
                        )

                        # Display the chart in Streamlit
                        st.subheader("Cost by Order Bar Chart")
                        st.plotly_chart(fig, key="45hgfhe")
                        
            col31, col32 = st.columns(2, gap="medium",vertical_alignment='center')
            new_data_454 = combined_L3_Fixed[combined_L3_Fixed["Order"] == selected_category_Order_L2]
            combined_L3_Fixed = combined_L3_Fixed.rename(
                columns={
                    "Main": "Spent",
                    "1st Comparison": "Budget",
                    "Var Comp&Main": "Delta",
                }
            )
            with col31:
                with st.container(height=500, border=False):
                    # User filter input
                    selected_category_L3 = st.selectbox(
                        "Filter by Level 3:",
                        ["All"] + list(new_data_454["L3"].unique()),
                        key="lvllv",
                    )
                    # Apply the filter
                    if selected_category_Order_L2 != "All":
                        if selected_category_L3 != "All":
                            filtered_df = combined_L3_Fixed[
                                (combined_L3_Fixed["L3"] == selected_category_L3)
                                & (combined_L3_Fixed["Order"] == selected_category_Order_L2)
                            ]
                            filtered_df = filtered_df.sort_values(
                                by="Total Difference", ascending=True
                            )
                        else:
                            filtered_df = combined_L3_Fixed[
                                combined_L3_Fixed["Order"] == selected_category_Order_L2
                            ]
                            filtered_df = filtered_df.sort_values(
                                by="Total Difference", ascending=True
                            )
                    else:
                        filtered_df = combined_L3_Fixed[
                            combined_L3_Fixed["Order"] == selected_category_Order_L2
                        ]
                        filtered_df = filtered_df.sort_values(
                            by="Total Difference", ascending=True
                        )
                    coli31, coli32, coli33 = st.columns(
                        3, border=True, vertical_alignment="center"
                    )
                    with coli31:
                        st.metric(
                            label="Budget", value=f"£{filtered_df['Total Budget'].sum():,.2f}"
                        )
                    with coli32:
                        st.metric(
                            label="Spent", value=f"£{filtered_df['Total Main'].sum():,.2f}"
                        )
                    with coli33:
                        st.metric(
                            label="Delta",
                            value=f"£{filtered_df['Total Difference'].sum():,.2f}",
                            delta=f"{(((filtered_df['Total Budget'].sum()) - (filtered_df['Total Main'].sum()))/(filtered_df['Total Budget'].sum()))*100:.2f}%",
                        )
                    # Apply styling to the 'Order' column based on 'Delta'
                    if "Total Difference" in filtered_df.columns:
                        styled_df = filtered_df.style.apply(
                            lambda row: [
                                color_code_new(row,'Total Difference') if col == "L3" else ""
                                for col in filtered_df.columns
                            ],
                            axis=1,
                        )
                        # Display in Streamlit
                        st.dataframe(styled_df, use_container_width=True)
                    else:
                        st.error("Column 'Delta' is missing from the DataFrame")

            with col32:
                with st.container(height=500, border=False):
                    # Assign colors to the bars based on your conditions
                    colors = np.where(
                        (filtered_df["Total Budget"] == 0),
                        "orange",
                        np.where(
                            (filtered_df["Total Main"] > filtered_df["Total Budget"]),
                            "red",
                            "green",
                        ),
                    )
                    # Create a grouped bar chart
                    fig = go.Figure()

                    # Add first column for Budget
                    fig.add_trace(
                        go.Bar(
                            name="Budget",
                            x=filtered_df["L3"],
                            y=filtered_df["Total Budget"],
                            marker_color="blue",  # Fixed color for Budget
                        )
                    )

                    # Add second column for Spent with dynamic colors
                    fig.add_trace(
                        go.Bar(
                            name="Spent",
                            x=filtered_df["L3"],
                            y=filtered_df["Total Main"],
                            marker_color=colors,  # Colors based on conditions
                        )
                    )

                    # Update layout for better visualization
                    fig.update_layout(
                        xaxis_title="Categories",
                        yaxis_title="Values",
                        barmode="group",  # Group bars
                    )

                    # Display the chart in Streamlit
                    st.subheader("Cost by L3 Bar Chart")
                    st.plotly_chart(fig, key="kfmmfem")
                    
            col41, col42 = st.columns(2, gap="medium",vertical_alignment='center')
            new_data_4154 = combined_L4_Fixed[combined_L4_Fixed["L3"] == selected_category_L3]
            combined_L4_Fixed = combined_L4_Fixed.rename(
                columns={
                    "Main": "Spent",
                    "1st Comparison": "Budget",
                    "Var Comp&Main": "Delta",
                }
            )
            with col41:
                with st.container(height=500, border=False):
                    # User filter input
                    selected_category_L4 = st.selectbox(
                        "Filter by Level 4:",
                        ["All"] + list(new_data_4154["L4"].unique()),
                        key="gggnneejmfedf",
                    )               
                    # Apply the filter
                    if selected_category_L3 != "All":
                        if selected_category_L4 != "All":
                            filtered_df = combined_L4_Fixed[
                                (combined_L4_Fixed["L4"] == selected_category_L4)
                                & (combined_L4_Fixed["L3"] == selected_category_L3) & (combined_L4_Fixed["Order"] == selected_category_Order_L2)
                            ]
                            filtered_df = filtered_df.sort_values(
                                by="Total Difference", ascending=True
                            )
                        else:
                            filtered_df = combined_L4_Fixed[
                                combined_L4_Fixed["L3"] == selected_category_L3
                            ]
                            filtered_df = filtered_df.sort_values(
                                by="Total Difference", ascending=True
                            )
                    else:
                        filtered_df = combined_L4_Fixed[
                            combined_L4_Fixed["L3"] == selected_category_L3
                        ]
                        filtered_df = filtered_df.sort_values(
                            by="Total Difference", ascending=True
                        )
                    coli31, coli32, coli33 = st.columns(
                        3, border=True, vertical_alignment="center"
                    )
                    with coli31:
                        st.metric(
                            label="Budget", value=f"£{filtered_df['Total Budget'].sum():,.2f}"
                        )
                    with coli32:
                        st.metric(
                            label="Spent", value=f"£{filtered_df['Total Main'].sum():,.2f}"
                        )
                    with coli33:
                        st.metric(
                            label="Delta",
                            value=f"£{filtered_df['Total Difference'].sum():,.2f}",
                            delta=f"{(((filtered_df['Total Budget'].sum()) - (filtered_df['Total Main'].sum()))/(filtered_df['Total Budget'].sum()))*100:.2f}%",
                        )
                    # Apply styling to the 'Order' column based on 'Delta'
                    if "Total Difference" in filtered_df.columns:
                        styled_df = filtered_df.style.apply(
                            lambda row: [
                                color_code_new(row,'Total Difference') if col == "L4" else ""
                                for col in filtered_df.columns
                            ],
                            axis=1,
                        )
                        # Display in Streamlit
                        st.dataframe(styled_df, use_container_width=True)
                    else:
                        st.error("Column 'Delta' is missing from the DataFrame")

            with col42:
                with st.container(height=500, border=False):
                    # Assign colors to the bars based on your conditions
                    colors = np.where(
                        (filtered_df["Total Budget"] == 0),
                        "orange",
                        np.where(
                            (filtered_df["Total Main"] > filtered_df["Total Budget"]),
                            "red",
                            "green",
                        ),
                    )
                    # Create a grouped bar chart
                    fig = go.Figure()

                    # Add first column for Budget
                    fig.add_trace(
                        go.Bar(
                            name="Budget",
                            x=filtered_df["L4"],
                            y=filtered_df["Total Budget"],
                            marker_color="blue",  # Fixed color for Budget
                        )
                    )

                    # Add second column for Spent with dynamic colors
                    fig.add_trace(
                        go.Bar(
                            name="Spent",
                            x=filtered_df["L4"],
                            y=filtered_df["Total Main"],
                            marker_color=colors,  # Colors based on conditions
                        )
                    )

                    # Update layout for better visualization
                    fig.update_layout(
                        xaxis_title="Categories",
                        yaxis_title="Values",
                        barmode="group",  # Group bars
                    )

                    # Display the chart in Streamlit
                    st.subheader("Cost by L4 Bar Chart")
                    st.plotly_chart(fig, key="efeef22efrvbg")
            col51, col52 = st.columns(2, gap="medium",vertical_alignment='center')
            new_data_41154 = combined_L5_Fixed[combined_L5_Fixed["L4"] == selected_category_L4]
            combined_L5_Fixed = combined_L5_Fixed.rename(
                columns={
                    "Main": "Spent",
                    "1st Comparison": "Budget",
                    "Var Comp&Main": "Delta",
                }
            )
            with col51:
                with st.container(height=500, border=False):
                    # User filter input
                    selected_category_L5 = st.selectbox(
                        "Filter by Account:",
                        ["All"] + list(new_data_41154["AccountAndDescpription"].unique()),
                        key="4r34rf34rf44gtrfghtertger",
                    )               
                    # Apply the filter
                    if selected_category_L4 != "All":
                        if selected_category_L5 != "All":
                            filtered_df = combined_L5_Fixed[
                                (combined_L5_Fixed["L4"] == selected_category_L4)
                                & (combined_L5_Fixed["L3"] == selected_category_L3) & (combined_L5_Fixed["Order"] == selected_category_Order_L2) & (combined_L5_Fixed["AccountAndDescpription"] == selected_category_L5)
                            ]
                            filtered_df = filtered_df.sort_values(
                                by="Total Difference", ascending=True
                            )
                        else:
                            filtered_df = combined_L5_Fixed[
                                combined_L5_Fixed["L4"] == selected_category_L4
                            ]   
                            filtered_df = filtered_df.sort_values(
                                by="Total Difference", ascending=True
                            )
                    else:
                        filtered_df = combined_L5_Fixed[
                            combined_L5_Fixed["L4"] == selected_category_L4
                        ]
                        filtered_df = filtered_df.sort_values(
                            by="Total Difference", ascending=True
                        )
                    coli31, coli32, coli33 = st.columns(
                        3, border=True, vertical_alignment="center"
                    )
                    with coli31:
                        st.metric(
                            label="Budget", value=f"£{filtered_df['Total Budget'].sum():,.2f}"
                        )
                    with coli32:
                        st.metric(
                            label="Spent", value=f"£{filtered_df['Total Main'].sum():,.2f}"
                        )
                    with coli33:
                        st.metric(
                            label="Delta",
                            value=f"£{filtered_df['Total Difference'].sum():,.2f}",
                            delta=f"{(((filtered_df['Total Budget'].sum()) - (filtered_df['Total Main'].sum()))/(filtered_df['Total Budget'].sum()))*100:.2f}%",
                        )
                    # Apply styling to the 'Order' column based on 'Delta'
                    if "Total Difference" in filtered_df.columns:
                        styled_df = filtered_df.style.apply(
                            lambda row: [
                                color_code_new(row,'Total Difference') if col == "AccountAndDescpription" else ""
                                for col in filtered_df.columns
                            ],
                            axis=1,
                        )
                        # Display in Streamlit
                        st.dataframe(styled_df, use_container_width=True)
                    else:
                        st.error("Column 'Delta' is missing from the DataFrame")

            with col52:
                with st.container(height=500, border=False):
                    # Assign colors to the bars based on your conditions
                    colors = np.where(
                        (filtered_df["Total Budget"] == 0),
                        "orange",
                        np.where(
                            (filtered_df["Total Main"] > filtered_df["Total Budget"]),
                            "red",
                            "green",
                        ),
                    )
                    # Create a grouped bar chart
                    fig = go.Figure()

                    # Add first column for Budget
                    fig.add_trace(
                        go.Bar(
                            name="Budget",
                            x=filtered_df["L4"],
                            y=filtered_df["Total Budget"],
                            marker_color="blue",  # Fixed color for Budget
                        )
                    )

                    # Add second column for Spent with dynamic colors
                    fig.add_trace(
                        go.Bar(
                            name="Spent",
                            x=filtered_df["L4"],
                            y=filtered_df["Total Main"],
                            marker_color=colors,  # Colors based on conditions
                        )
                    )

                    # Update layout for better visualization
                    fig.update_layout(
                        xaxis_title="Categories",
                        yaxis_title="Values",
                        barmode="group",  # Group bars
                    )

                    # Display the chart in Streamlit
                    st.subheader("Cost by Account Bar Chart")
                    st.plotly_chart(fig, key="435253wewew")
                
        if selected_cost_YTD == 'Variable Cost':
            #######################----------------------------------------------#####################################
            data_L2 = {
                        "Variable Cost Spent": [
                            Jan_grouped_Variable_L2['Main'].sum(),
                            Feb_grouped_Variable_L2['Main'].sum(),
                        ],
                        "Variable Cost Budget": [
                            Jan_grouped_Variable_L2['1st Comparison'].sum(),
                            Feb_grouped_Variable_L2['1st Comparison'].sum(),
                        ],
                        "Month": ["January", "Feburary"],

                    }
            
            colsss1,colsss2 = st.columns([0.45,0.55], border=True)
            with colsss1:
                st.subheader('Variable Cost Analysis (Year To Date)')
            with colsss2:
                st.subheader('Variable Cost Analysis Trend by Month (Year To Date)')
            
            colx1,colx2 = st.columns([0.45,0.55], border=True)
            with colx1:
                with st.container(height=500, border=False):   
                    cols1,cols2,cols3= st.columns((3), vertical_alignment='center')
                    with cols1:
                        st.metric(value=f"£{Variable_cost_YTD_Budget:,.2f}",label = 'Variable Cost Year To Date Budget', border=True)
                    with cols2:
                        st.metric(value=f"£{Variable_cost_YTD_spent:,.2f}",label = 'Variable Cost Year To Date Spent', border=True)
                    with cols3:
                        st.metric(value=f"£{Variable_cost_YTD_Delta:,.2f}",label = 'Variable Cost Year To Date Delta', border=True, delta=f"{Variable_Cost_YTD_Delta_Percent:.2f}%")
            with colx2:
                with st.container(height=500, border=False): 
                    fig = px.line(
                        data_L2,
                        x='Month',
                        y=['Variable Cost Spent', 'Variable Cost Budget'],
                        title='Budget vs. Spent Over Months',
                        labels={'value': 'Amount', 'Month': 'Month'},
                        color_discrete_sequence=['red', 'green']  # Optional customization for colors
                    )

                    # Display Plotly chart in Streamlit
                    st.plotly_chart(fig)
                    
                
                
            clswe11,colswe12 = st.columns(2)
            with clswe11:
                with st.container(height=500):
                    # User filter input
                    selected_category_Order_L2 = st.selectbox(
                        "Filter by Order:",
                        ["All"] + list(combined_L2_Variable["Order"].unique()),
                        key="FIlt44646rgrgrder",
                    )

                    # Apply the filter
                    if selected_category_Order_L2 != "All":
                        filtered_df = combined_L2_Variable[
                            (combined_L2_Variable["Order"] == selected_category_Order_L2)
                            & (combined_L2_Variable["Order"] == selected_category_Order_L2)
                        ]
                        filtered_df = filtered_df.sort_values(
                            by="Total Difference", ascending=True
                        )
                    else:
                        filtered_df = combined_L2_Variable
                        filtered_df = filtered_df.sort_values(
                            by='Total Difference', ascending=True
                        )
                    filtered_df.columns = filtered_df.columns.str.strip()
                    filtered_df[['Total Main', 'Total Budget', 'Total Difference']] = filtered_df[
                        ['Total Main', 'Total Budget', 'Total Difference']
                    ].apply(pd.to_numeric, errors="coerce")
                    coli1, coli2, coli3 = st.columns(
                        3, border=True, vertical_alignment="center"
                    )
                    with coli1:
                        st.metric(
                            label="Total Budget", value=f"£{filtered_df['Total Budget'].sum():,.2f}"
                        )
                    with coli2:
                        st.metric(
                            label="Total Spent", value=f"£{filtered_df['Total Main'].sum():,.2f}"
                        )
                    with coli3:
                        st.metric(
                            label="Total Difference",
                            value=f"£{filtered_df['Total Difference'].sum():,.2f}",
                            delta=f"{(((filtered_df['Total Budget'].sum()) - (filtered_df['Total Main'].sum()))/(filtered_df['Total Budget'].sum()))*100:.2f}%",
                        )
                    # Apply styling to the 'Order' column based on 'Delta'
                    if "Total Difference" in filtered_df.columns:
                        styled_df = filtered_df.style.apply(
                            lambda row: [
                                color_code_new(row,"Total Difference") if col == "Order" else ""
                                for col in filtered_df.columns
                            ],
                            axis=1,
                        )
                        # Display in Streamlit
                        st.dataframe(styled_df, use_container_width=True,column_config={"Total Difference": st.column_config.NumberColumn(format="%.2f"),"Total Budget": st.column_config.NumberColumn(format="%.2f"),"Total Main": st.column_config.NumberColumn(format="%.2f")})
                    else:
                        st.error("Column 'Total Difference' is missing from the DataFrame")
                        
            with colswe12:
                with st.container(height=500):
                        # Assign colors to the bars based on your conditions
                        colors = np.where(
                            (filtered_df["Total Budget"] == 0),
                            "orange",
                            np.where(
                                (filtered_df["Total Main"] > filtered_df["Total Budget"]),
                                "red",
                                "green",
                            ),
                        )

                        # Create a grouped bar chart
                        fig = go.Figure()

                        # Add first column for Budget
                        fig.add_trace(
                            go.Bar(
                                name="Budget",
                                x=filtered_df["Order"],
                                y=filtered_df["Total Budget"],
                                marker_color="blue",  # Variable color for Budget
                            )
                        )

                        # Add second column for Spent with dynamic colors
                        fig.add_trace(
                            go.Bar(
                                name="Spent",
                                x=filtered_df["Order"],
                                y=filtered_df["Total Main"],
                                marker_color=colors,  # Colors based on conditions
                            )
                        )

                        # Update layout for better visualization
                        fig.update_layout(
                            xaxis_title="Categories",
                            yaxis_title="Values",
                            barmode="group",  # Group bars
                        )

                        # Display the chart in Streamlit
                        st.subheader("Cost by Order Bar Chart")
                        st.plotly_chart(fig, key="57843wewew")
                        
            col31, col32 = st.columns(2, gap="medium",vertical_alignment='center')
            new_data_454 = combined_L3_Variable[combined_L3_Variable["Order"] == selected_category_Order_L2]
            combined_L3_Variable = combined_L3_Variable.rename(
                columns={
                    "Main": "Spent",
                    "1st Comparison": "Budget",
                    "Var Comp&Main": "Delta",
                }
            )
            with col31:
                with st.container(height=500):
                    # User filter input
                    selected_category_L3 = st.selectbox(
                        "Filter by Level 3:",
                        ["All"] + list(new_data_454["L3"].unique()),
                        key="v,cpwdmv",
                    )
                    # Apply the filter
                    if selected_category_Order_L2 != "All":
                        if selected_category_L3 != "All":
                            filtered_df = combined_L3_Variable[
                                (combined_L3_Variable["L3"] == selected_category_L3)
                                & (combined_L3_Variable["Order"] == selected_category_Order_L2)
                            ]
                            filtered_df = filtered_df.sort_values(
                                by="Total Difference", ascending=True
                            )
                        else:
                            filtered_df = combined_L3_Variable[
                                combined_L3_Variable["Order"] == selected_category_Order_L2
                            ]
                            filtered_df = filtered_df.sort_values(
                                by="Total Difference", ascending=True
                            )
                    else:
                        filtered_df = combined_L3_Variable[
                            combined_L3_Variable["Order"] == selected_category_Order_L2
                        ]
                        filtered_df = filtered_df.sort_values(
                            by="Total Difference", ascending=True
                        )
                    coli31, coli32, coli33 = st.columns(
                        3, border=True, vertical_alignment="center"
                    )
                    with coli31:
                        st.metric(
                            label="Budget", value=f"£{filtered_df['Total Budget'].sum():,.2f}"
                        )
                    with coli32:
                        st.metric(
                            label="Spent", value=f"£{filtered_df['Total Main'].sum():,.2f}"
                        )
                    with coli33:
                        st.metric(
                            label="Delta",
                            value=f"£{filtered_df['Total Difference'].sum():,.2f}",
                            delta=f"{(((filtered_df['Total Budget'].sum()) - (filtered_df['Total Main'].sum()))/(filtered_df['Total Budget'].sum()))*100:.2f}%",
                        )
                    # Apply styling to the 'Order' column based on 'Delta'
                    if "Total Difference" in filtered_df.columns:
                        styled_df = filtered_df.style.apply(
                            lambda row: [
                                color_code_new(row,'Total Difference') if col == "L3" else ""
                                for col in filtered_df.columns
                            ],
                            axis=1,
                        )
                        # Display in Streamlit
                        st.dataframe(styled_df, use_container_width=True)
                    else:
                        st.error("Column 'Delta' is missing from the DataFrame")

            with col32:
                with st.container(height=500):
                    # Assign colors to the bars based on your conditions
                    colors = np.where(
                        (filtered_df["Total Budget"] == 0),
                        "orange",
                        np.where(
                            (filtered_df["Total Main"] > filtered_df["Total Budget"]),
                            "red",
                            "green",
                        ),
                    )
                    # Create a grouped bar chart
                    fig = go.Figure()

                    # Add first column for Budget
                    fig.add_trace(
                        go.Bar(
                            name="Budget",
                            x=filtered_df["L3"],
                            y=filtered_df["Total Budget"],
                            marker_color="blue",  # Variable color for Budget
                        )
                    )

                    # Add second column for Spent with dynamic colors
                    fig.add_trace(
                        go.Bar(
                            name="Spent",
                            x=filtered_df["L3"],
                            y=filtered_df["Total Main"],
                            marker_color=colors,  # Colors based on conditions
                        )
                    )

                    # Update layout for better visualization
                    fig.update_layout(
                        xaxis_title="Categories",
                        yaxis_title="Values",
                        barmode="group",  # Group bars
                    )

                    # Display the chart in Streamlit
                    st.subheader("Cost by L3 Bar Chart")
                    st.plotly_chart(fig, key="dfbv53wewew")
                    
            col41, col42 = st.columns(2, gap="medium",vertical_alignment='center')
            new_data_4154 = combined_L4_Variable[combined_L4_Variable["L3"] == selected_category_L3]
            combined_L4_Variable = combined_L4_Variable.rename(
                columns={
                    "Main": "Spent",
                    "1st Comparison": "Budget",
                    "Var Comp&Main": "Delta",
                }
            )
            with col41:
                with st.container(height=500):
                    # User filter input
                    selected_category_L4 = st.selectbox(
                        "Filter by Level 4:",
                        ["All"] + list(new_data_4154["L4"].unique()),
                        key="dfmekfmkefe",
                    )               
                    # Apply the filter
                    if selected_category_L3 != "All":
                        if selected_category_L4 != "All":
                            filtered_df = combined_L4_Variable[
                                (combined_L4_Variable["L4"] == selected_category_L4)
                                & (combined_L4_Variable["L3"] == selected_category_L3) & (combined_L4_Variable["Order"] == selected_category_Order_L2)
                            ]
                            filtered_df = filtered_df.sort_values(
                                by="Total Difference", ascending=True
                            )
                        else:
                            filtered_df = combined_L4_Variable[
                                combined_L4_Variable["L3"] == selected_category_L3
                            ]
                            filtered_df = filtered_df.sort_values(
                                by="Total Difference", ascending=True
                            )
                    else:
                        filtered_df = combined_L4_Variable[
                            combined_L4_Variable["L3"] == selected_category_L3
                        ]
                        filtered_df = filtered_df.sort_values(
                            by="Total Difference", ascending=True
                        )
                    coli31, coli32, coli33 = st.columns(
                        3, border=True, vertical_alignment="center"
                    )
                    with coli31:
                        st.metric(
                            label="Budget", value=f"£{filtered_df['Total Budget'].sum():,.2f}"
                        )
                    with coli32:
                        st.metric(
                            label="Spent", value=f"£{filtered_df['Total Main'].sum():,.2f}"
                        )
                    with coli33:
                        st.metric(
                            label="Delta",
                            value=f"£{filtered_df['Total Difference'].sum():,.2f}",
                            delta=f"{(((filtered_df['Total Budget'].sum()) - (filtered_df['Total Main'].sum()))/(filtered_df['Total Budget'].sum()))*100:.2f}%",
                        )
                    # Apply styling to the 'Order' column based on 'Delta'
                    if "Total Difference" in filtered_df.columns:
                        styled_df = filtered_df.style.apply(
                            lambda row: [
                                color_code_new(row,'Total Difference') if col == "L4" else ""
                                for col in filtered_df.columns
                            ],
                            axis=1,
                        )
                        # Display in Streamlit
                        st.dataframe(styled_df, use_container_width=True)
                    else:
                        st.error("Column 'Delta' is missing from the DataFrame")

            with col42:
                with st.container(height=500):
                    # Assign colors to the bars based on your conditions
                    colors = np.where(
                        (filtered_df["Total Budget"] == 0),
                        "orange",
                        np.where(
                            (filtered_df["Total Main"] > filtered_df["Total Budget"]),
                            "red",
                            "green",
                        ),
                    )
                    # Create a grouped bar chart
                    fig = go.Figure()

                    # Add first column for Budget
                    fig.add_trace(
                        go.Bar(
                            name="Budget",
                            x=filtered_df["L4"],
                            y=filtered_df["Total Budget"],
                            marker_color="blue",  # Variable color for Budget
                        )
                    )

                    # Add second column for Spent with dynamic colors
                    fig.add_trace(
                        go.Bar(
                            name="Spent",
                            x=filtered_df["L4"],
                            y=filtered_df["Total Main"],
                            marker_color=colors,  # Colors based on conditions
                        )
                    )

                    # Update layout for better visualization
                    fig.update_layout(
                        xaxis_title="Categories",
                        yaxis_title="Values",
                        barmode="group",  # Group bars
                    )

                    # Display the chart in Streamlit
                    st.subheader("Cost by L4 Bar Chart")
                    st.plotly_chart(fig, key="efefppefe")
                                 
            col51, col52 = st.columns(2, gap="medium",vertical_alignment='center')
            new_data_41154 = combined_L5_Variable[combined_L5_Variable["L4"] == selected_category_L4]
            combined_L5_Variable = combined_L5_Variable.rename(
                columns={
                    "Main": "Spent",
                    "1st Comparison": "Budget",
                    "Var Comp&Main": "Delta",
                }
            )
            with col51:
                with st.container(height=500):
                    # User filter input
                    selected_category_L5 = st.selectbox(
                        "Filter by Account:",
                        ["All"] + list(new_data_41154["AccountAndDescpription"].unique()),
                        key="f3ef3efff44523",
                    )               
                    # Apply the filter
                    if selected_category_L4 != "All":
                        if selected_category_L5 != "All":
                            filtered_df = combined_L5_Variable[
                                (combined_L5_Variable["L4"] == selected_category_L4)
                                & (combined_L5_Variable["L3"] == selected_category_L3) & (combined_L5_Variable["Order"] == selected_category_Order_L2) & (combined_L5_Variable["AccountAndDescpription"] == selected_category_L5)
                            ]
                            filtered_df = filtered_df.sort_values(
                                by="Total Difference", ascending=True
                            )
                        else:
                            filtered_df = combined_L5_Variable[
                                combined_L5_Variable["L4"] == selected_category_L4
                            ]   
                            filtered_df = filtered_df.sort_values(
                                by="Total Difference", ascending=True
                            )
                    else:
                        filtered_df = combined_L5_Variable[
                            combined_L5_Variable["L4"] == selected_category_L4
                        ]
                        filtered_df = filtered_df.sort_values(
                            by="Total Difference", ascending=True
                        )
                    coli31, coli32, coli33 = st.columns(
                        3, border=True, vertical_alignment="center"
                    )
                    with coli31:
                        st.metric(
                            label="Budget", value=f"£{filtered_df['Total Budget'].sum():,.2f}"
                        )
                    with coli32:
                        st.metric(
                            label="Spent", value=f"£{filtered_df['Total Main'].sum():,.2f}"
                        )
                    with coli33:
                        st.metric(
                            label="Delta",
                            value=f"£{filtered_df['Total Difference'].sum():,.2f}",
                            delta=f"{(((filtered_df['Total Budget'].sum()) - (filtered_df['Total Main'].sum()))/(filtered_df['Total Budget'].sum()))*100:.2f}%",
                        )
                    # Apply styling to the 'Order' column based on 'Delta'
                    if "Total Difference" in filtered_df.columns:
                        styled_df = filtered_df.style.apply(
                            lambda row: [
                                color_code_new(row,'Total Difference') if col == "AccountAndDescpription" else ""
                                for col in filtered_df.columns
                            ],
                            axis=1,
                        )
                        # Display in Streamlit
                        st.dataframe(styled_df, use_container_width=True)
                    else:
                        st.error("Column 'Delta' is missing from the DataFrame")

            with col52:
                with st.container(height=500):
                    # Assign colors to the bars based on your conditions
                    colors = np.where(
                        (filtered_df["Total Budget"] == 0),
                        "orange",
                        np.where(
                            (filtered_df["Total Main"] > filtered_df["Total Budget"]),
                            "red",
                            "green",
                        ),
                    )
                    # Create a grouped bar chart
                    fig = go.Figure()

                    # Add first column for Budget
                    fig.add_trace(
                        go.Bar(
                            name="Budget",
                            x=filtered_df["L4"],
                            y=filtered_df["Total Budget"],
                            marker_color="blue",  # Variable color for Budget
                        )
                    )

                    # Add second column for Spent with dynamic colors
                    fig.add_trace(
                        go.Bar(
                            name="Spent",
                            x=filtered_df["L4"],
                            y=filtered_df["Total Main"],
                            marker_color=colors,  # Colors based on conditions
                        )
                    )

                    # Update layout for better visualization
                    fig.update_layout(
                        xaxis_title="Categories",
                        yaxis_title="Values",
                        barmode="group",  # Group bars
                    )

                    # Display the chart in Streamlit
                    st.subheader("Cost by Account Bar Chart")
                    st.plotly_chart(fig, key="43525343wewew")
    with tab_3:
        st.info('This feature will be launched in future version of this dashboard. Dashboard is designed by @aakalkri for Amazon LCY3 Reliability and Maintenance Engineering Automations Engineering Team under supervision of @didymiod and @sherress.', icon="ℹ️")
else:   
    st.info("Please upload an Excel file to proceed.")
