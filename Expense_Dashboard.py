import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import numpy as np
import plotly.express as px

# Page Imports
from Functions.Dataframes_color import Dataframes_ranked
from Functions.YTD_Cost import YTD_Cost
from Functions.YTD_Level_BarChart import Levels_BarChart
from Functions.YTD_SunBurst import YTD_SunBurst
from Functions.YTD_Line_chart import YTD_LineChart
from Functions.Months_Definition_file import months_convert
from Level_data.YTD_L2 import YTD_L2
from Level_data.YTD_L3 import YTD_L3
from Level_data.YTD_L4 import YTD_L4
from Level_data.YTD_L5 import YTD_L5
from Months.December_2024_Fixed import December_2024_Fixed
from Months.December_2024_Variable import December_2024_Variable
from Months.January_2025_Fixed import January_2025_Fixed
from Months.January_2025_Variable import January_2025_Variable
from Months.February_2025_Fixed import February_2025_Fixed
from Months.February_2025_Variable import February_2025_Variable
from Months.March_2025_Fixed import March_2025_Fixed
from Months.March_2025_Variable import March_2025_Variable
from Months.April_2025_Fixed import April_2025_Fixed
from Months.April_2025_Variable import April_2025_Variable
from Months.May_2025_Fixed import May_2025_Fixed
from Months.May_2025_Variable import May_2025_Variable
from Months.June_2025_Fixed import June_2025_Fixed
from Months.June_2025_Variable import June_2025_Variable
from Months.July_2025_Fixed import July_2025_Fixed
from Months.July_2025_Variable import July_2025_Variable
from Months.August_2025_Fixed import August_2025_Fixed
from Months.August_2025_Variable import August_2025_Variable
from Months.November_2024_Variable import November_2024_Variable
from Months.October_2024_Fixed import October_2024_Fixed
from Months.October_2024_Variable import October_2024_Variable
from Months.September_2024_Fixed import September_2024_Fixed
from Months.September_2024_Variable import September_2024_Variable
from Months.September_2025_Fixed import September_2025_Fixed
from Months.September_2025_Variable import September_2025_Variable
from Months.October_2025_Fixed import October_2025_Fixed
from Months.October_2025_Variable import October_2025_Variable
from Months.November_2025_Fixed import November_2024_Fixed
from Months.November_2025_Variable import November_2025_Variable
from Months.December_2025_Fixed import December_2025_Fixed
from Months.December_2025_Variable import December_2025_Variable
from Functions.YTD_KPI import YTD_KPI
from Functions.filtered_cost import filtered_months_data
from Functions.YTD_Barchart import YTD_Barchart
from Functions.YTD_Colors import YTD_Colors
from YTD_Filtered_Data.YTD_L2_Filtered import L2_Filtered_data
from YTD_Filtered_Data.YTD_L3_Filtered import L3_YTD_Filtered
from YTD_Filtered_Data.YTD_L4_Filtered import L4_YTD_Filtered
from YTD_Filtered_Data.YTD_L5_Filtered import L5_YTD_Filtered


# Centralized Streamlit Configuration and Introduction
logo_url = "Images/LCY3 Logo.png"
logo_url_2 = "Images/Amazon RME Logo.png"
st.set_page_config(
    page_title="Amazon RME Expense",
    page_icon=logo_url,
    layout="wide",
    menu_items={
        "Get Help": "mailto:aakalkri@amazon.co.uk",
        "Report a bug": "mailto:aakalkri@amazon.co.uk",
        "About": "Developed for LCY3 RME. Managed by @aakalkri.",
    },
)
cols1, cols2, cols3 = st.columns(
    [3, 4, 3], vertical_alignment="center", gap="small"
)  # This creates a 10% and 80% split
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
    st.image(logo_url_2, width=200)

with st.expander(label="Click here to open upload tab!"):
    head_1, head_2, head_3 = st.columns([0.2, 0.6, 0.2])
    with head_2:
        # File uploader
        uploaded_file = st.file_uploader("Upload an Excel File", type="xlsx")


if uploaded_file is not None:
    # Load the uploaded Excel file
    try:
        xls = pd.ExcelFile(uploaded_file)
        sheets = {}

        # Iterate through sheets and store DataFrames in a dictionary
        for sheet in xls.sheet_names:
            clean_name = sheet.replace(" ", "_").replace("-", "_")  # Clean up names
            if not clean_name.isidentifier():
                clean_name = f"df_{clean_name}"  # Ensure valid dictionary keys

            sheets[clean_name] = xls.parse(sheet)  # Store DataFrame in the dictionary

    except Exception as e:
        st.error(f"An error occurred while loading the Excel file: {e}")

    ####=============Month========###############
    Sep_2024 = sheets.get("Sep_2024")
    Oct_2024 = sheets.get("Oct_2024")
    Nov_2024 = sheets.get("Nov_2024")
    Dec_2024 = sheets.get("Dec_2024")
    Jan_2025 = sheets.get("Jan_2025")
    Feb_2025 = sheets.get("Feb_2025")
    Mar_2025 = sheets.get("Mar_2025")
    Apr_2025 = sheets.get("Apr_2025")
    May_2025 = sheets.get("May_2025")
    Jun_2025 = sheets.get("Jun_2025")
    Jul_2025 = sheets.get("Jul_2025")
    Aug_2025 = sheets.get("Aug_2025")
    Sep_2025 = sheets.get("Sep_2025")
    Oct_2025 = sheets.get("Oct_2025")
    Nov_2025 = sheets.get("Nov_2025")
    Dec_2025 = sheets.get("Dec_2025")

    (
        Sep_2024,
        Oct_2024,
        Nov_2024,
        Dec_2024,
        Jan_2025,
        Feb_2025,
        Mar_2025,
        Apr_2025,
        May_2025,
        Jun_2025,
        Jul_2025,
        Aug_2025,
        Sep_2025,
        Oct_2025,
        Nov_2025,
        Dec_2025,
    ) = months_convert(
        Sep_2024,
        Oct_2024,
        Nov_2024,
        Dec_2024,
        Jan_2025,
        Feb_2025,
        Mar_2025,
        Apr_2025,
        May_2025,
        Jun_2025,
        Jul_2025,
        Aug_2025,
        Sep_2025,
        Oct_2025,
        Nov_2025,
        Dec_2025,
    )
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
        unsafe_allow_html=True,
    )

    with tab_1:
        col_1, col_2, col_3 = st.columns(3)
        with col_1:
            month = st.selectbox(
                label="Select a Month",
                options=[
                    "January",
                    "February",
                    "March",
                    "April",
                    "May",
                    "June",
                    "July",
                    "August",
                    "September",
                    "October",
                    "November",
                    "December",
                ],
            )
        with col_2:
            year = st.selectbox(label="Select Year", options=["2024", "2025", "2026"])
        with col_3:
            data = st.selectbox(
                label="Select Cost", options=["Fixed Costs", "Variable Costs"]
            )
        if (month == "September") & (year == "2024") & (data == "Fixed Costs"):
            if Sep_2024.empty:
                st.info(f"No data available fot this {month}.")
            else:
                September_2024_Fixed(Sep_2024)

        elif (month == "September") & (year == "2024") & (data == "Variable Costs"):
            if Sep_2024.empty:
                st.info(f"No data available fot this {month}.")
            else:
                September_2024_Variable(Sep_2024)

        elif (month == "October") & (year == "2024") & (data == "Fixed Costs"):
            if Oct_2024.empty:
                st.info(f"No data available fot this {month}.")
            else:
                October_2024_Fixed(Oct_2024)

        elif (month == "October") & (year == "2024") & (data == "Variable Costs"):
            if Oct_2024.empty:
                st.info(f"No data available fot this {month}.")
            else:
                October_2024_Variable(Oct_2024)

        elif (month == "November") & (year == "2024") & (data == "Fixed Costs"):
            if Nov_2024.empty:
                st.info("No data available fot this month.")
            else:
                November_2024_Fixed(Nov_2024)

        elif (month == "November") & (year == "2024") & (data == "Variable Costs"):
            if Nov_2024.empty:
                st.info("No data available for this month.")
            else:
                November_2024_Variable(Nov_2024)

        elif (month == "December") & (year == "2024") & (data == "Fixed Costs"):
            if Dec_2024.empty:
                st.info(f"No data available fot this {month}.")
            else:
                December_2024_Fixed(Dec_2024)

        elif (month == "December") & (year == "2024") & (data == "Variable Costs"):
            if Dec_2024.empty:
                st.info(f"No data available fot this {month}.")
            else:
                December_2024_Variable(Dec_2024)
        elif (month == "January") & (year == "2025") & (data == "Fixed Costs"):
            if Jan_2025.empty:
                st.info(f"No data available fot this {month}.")
            else:
                January_2025_Fixed(Jan_2025)

        elif (month == "January") & (year == "2025") & (data == "Variable Costs"):
            if Jan_2025.empty:
                st.info(f"No data available fot this {month}.")
            else:
                January_2025_Variable(Jan_2025)

        elif (month == "February") & (year == "2025") & (data == "Fixed Costs"):
            if Feb_2025.empty:
                st.info(f"No data available fot this {month}.")
            else:
                February_2025_Fixed(Feb_2025)

        elif (month == "February") & (year == "2025") & (data == "Variable Costs"):
            if Feb_2025.empty:
                st.info(f"No data available fot this {month}.")
            else:
                February_2025_Variable(Feb_2025)

        elif (month == "March") & (year == "2025") & (data == "Fixed Costs"):
            if Mar_2025.empty:
                st.info("No data available fot this month.")
            else:
                March_2025_Fixed(Mar_2025)

        elif (month == "March") & (year == "2025") & (data == "Variable Costs"):
            if Mar_2025.empty:
                st.info("No data available for this month.")
            else:
                March_2025_Variable(Mar_2025)

        elif (month == "April") & (year == "2025") & (data == "Fixed Costs"):
            if Apr_2025.empty:
                st.info(f"No data available fot this {month}.")
            else:
                April_2025_Fixed(Apr_2025)

        elif (month == "April") & (year == "2025") & (data == "Variable Costs"):
            if Apr_2025.empty:
                st.info(f"No data available fot this {month}.")
            else:
                April_2025_Variable(Apr_2025)
        else:
            st.info("No data for the month selected")

    with tab_2:
        (
            Year_To_Date_Total_Spent,
            Year_To_Date_Total_Budget,
            Year_To_Date_Total_Delta,
            delta,
            data,
        ) = YTD_KPI(
            Jan_2025,
            Feb_2025,
            Mar_2025,
            Apr_2025,
            May_2025,
            Jun_2025,
            Jul_2025,
            Aug_2025,
            Sep_2025,
            Oct_2025,
            Nov_2025,
            Dec_2025,
        )
        cols1, cols2, cols3 = st.columns(3, vertical_alignment="center", border=True)
        with cols1:
            st.metric(
                value=f"£{Year_To_Date_Total_Spent:,.2f}",
                label="Year to Date Total (Spent)",
            )
        with cols2:
            st.metric(
                value=f"£{Year_To_Date_Total_Budget:,.2f}",
                label="Year to Date Total (Budget)",
            )
        with cols3:
            st.metric(
                value=f"£{Year_To_Date_Total_Delta:,.2f}",
                label="Year to Date Total (Delta)",
                delta=f"{delta:.2f}%",
            )

        colss1, cols22, cols23 = st.columns(3, vertical_alignment="center")
        colors = YTD_Colors(data)
        with colss1:
            # Display the chart in Streamlit
            st.subheader("Spend by Month Bar Chart")
            st.plotly_chart(YTD_Barchart(data, colors), key="wferfwwewew")
        with cols22:
            # Display Plotly chart in Streamlit
            st.plotly_chart(YTD_LineChart(data))
        with cols23:
            # Display chart in Streamlit
            st.plotly_chart(
                YTD_SunBurst(
                    Jan_2025,
                    Feb_2025,
                    Mar_2025,
                    Apr_2025,
                    May_2025,
                    Jun_2025,
                    Jul_2025,
                    Aug_2025,
                    Sep_2025,
                    Oct_2025,
                    Nov_2025,
                    Dec_2025,
                ),
                use_container_width=True,
            )
        (
            Fixed_cost_YTD_spent,
            Fixed_cost_YTD_Budget,
            Fixed_cost_YTD_Delta,
            Fixed_Cost_YTD_Delta_Percent,
            Variable_cost_YTD_spent,
            Variable_cost_YTD_Budget,
            Variable_cost_YTD_Delta,
            Variable_Cost_YTD_Delta_Percent,
        ) = YTD_Cost(
            Jan_2025,
            Feb_2025,
            Mar_2025,
            Apr_2025,
            May_2025,
            Jun_2025,
            Jul_2025,
            Aug_2025,
            Sep_2025,
            Oct_2025,
            Nov_2025,
            Dec_2025,
        )

        # This section handles the summation of data and uses a similar logic to the monthly view page
        filtered_result = filtered_months_data(
            Jan_2025,
            Feb_2025,
            Mar_2025,
            Apr_2025,
            May_2025,
            Jun_2025,
            Jul_2025,
            Aug_2025,
            Sep_2025,
            Oct_2025,
            Nov_2025,
            Dec_2025,
        )
        # Access filtered Fixed Costs and Variable Costs
        filtered_fixed_costs = filtered_result["Fixed Costs"]
        filtered_variable_costs = filtered_result["Variable Costs"]
        (
            Jan_2025_filtered_Fixed,
            Feb_2025_filtered_Fixed,
            Mar_2025_filtered_Fixed,
            Apr_2025_filtered_Fixed,
            May_2025_filtered_Fixed,
            Jun_2025_filtered_Fixed,
            Jul_2025_filtered_Fixed,
            Aug_2025_filtered_Fixed,
            Sep_2025_filtered_Fixed,
            Oct_2025_filtered_Fixed,
            Nov_2025_filtered_Fixed,
            Dec_2025_filtered_Fixed,
        ) = (
            filtered_fixed_costs[0],
            filtered_fixed_costs[1],
            filtered_fixed_costs[2],
            filtered_fixed_costs[3],
            filtered_fixed_costs[4],
            filtered_fixed_costs[5],
            filtered_fixed_costs[6],
            filtered_fixed_costs[7],
            filtered_fixed_costs[8],
            filtered_fixed_costs[9],
            filtered_fixed_costs[10],
            filtered_fixed_costs[11],
        )
        (
            Jan_2025_filtered_Variable,
            Feb_2025_filtered_Variable,
            Mar_2025_filtered_Variable,
            Apr_2025_filtered_Variable,
            May_2025_filtered_Variable,
            Jun_2025_filtered_Variable,
            Jul_2025_filtered_Variable,
            Aug_2025_filtered_Variable,
            Sep_2025_filtered_Variable,
            Oct_2025_filtered_Variable,
            Nov_2025_filtered_Variable,
            Dec_2025_filtered_Variable,
        ) = (
            filtered_variable_costs[0],
            filtered_variable_costs[1],
            filtered_variable_costs[2],
            filtered_variable_costs[3],
            filtered_variable_costs[4],
            filtered_variable_costs[5],
            filtered_variable_costs[6],
            filtered_variable_costs[7],
            filtered_variable_costs[8],
            filtered_variable_costs[9],
            filtered_variable_costs[10],
            filtered_variable_costs[11],
        )

        monthly_data = {
            "January": (Jan_2025_filtered_Fixed, Jan_2025_filtered_Variable),
            "February": (Feb_2025_filtered_Fixed, Feb_2025_filtered_Variable),
            "March": (Mar_2025_filtered_Fixed, Mar_2025_filtered_Variable),
            "April": (Apr_2025_filtered_Fixed, Apr_2025_filtered_Variable),
            "May": (May_2025_filtered_Fixed, May_2025_filtered_Variable),
            "June": (Jun_2025_filtered_Fixed, Jun_2025_filtered_Variable),
            "July": (Jul_2025_filtered_Fixed, Jul_2025_filtered_Variable),
            "August": (Aug_2025_filtered_Fixed, Aug_2025_filtered_Variable),
            "September": (Sep_2025_filtered_Fixed, Sep_2025_filtered_Variable),
            "October": (Oct_2025_filtered_Fixed, Oct_2025_filtered_Variable),
            "November": (Nov_2025_filtered_Fixed, Nov_2025_filtered_Variable),
            "December": (Dec_2025_filtered_Fixed, Dec_2025_filtered_Variable),
            # Add future months here
        }
        combined_L2_Fixed, combined_L2_Variable = YTD_L2(monthly_data)
        combined_L3_Fixed, combined_L3_Variable = YTD_L3(monthly_data)
        combined_L4_Fixed, combined_L4_Variable = YTD_L4(monthly_data)
        combined_L5_Fixed, combined_L5_Variable = YTD_L5(monthly_data)

        selected_cost_YTD = st.selectbox(
            label="Select Cost To Analyse", options=["Fixed Cost", "Variable Cost"]
        )

        if selected_cost_YTD == "Fixed Cost":
            #######################----------------------------------------------#####################################
            data_L2 = {
                "Fixed Cost Spent": [
                    Jan_2025_filtered_Fixed["Main"].sum(),
                    Feb_2025_filtered_Fixed["Main"].sum(),
                    Mar_2025_filtered_Fixed["Main"].sum(),
                    Apr_2025_filtered_Fixed["Main"].sum(),
                    May_2025_filtered_Fixed["Main"].sum(),
                    Jun_2025_filtered_Fixed["Main"].sum(),
                    Jul_2025_filtered_Fixed["Main"].sum(),
                    Aug_2025_filtered_Fixed["Main"].sum(),
                    Sep_2025_filtered_Fixed["Main"].sum(),
                    Oct_2025_filtered_Fixed["Main"].sum(),
                    Nov_2025_filtered_Fixed["Main"].sum(),
                    Dec_2025_filtered_Fixed["Main"].sum(),
                ],
                "Fixed Cost Budget": [
                    Jan_2025_filtered_Fixed["1st Comparison"].sum(),
                    Feb_2025_filtered_Fixed["1st Comparison"].sum(),
                    Mar_2025_filtered_Fixed["1st Comparison"].sum(),
                    Apr_2025_filtered_Fixed["1st Comparison"].sum(),
                    May_2025_filtered_Fixed["1st Comparison"].sum(),
                    Jun_2025_filtered_Fixed["1st Comparison"].sum(),
                    Jul_2025_filtered_Fixed["1st Comparison"].sum(),
                    Aug_2025_filtered_Fixed["1st Comparison"].sum(),
                    Sep_2025_filtered_Fixed["1st Comparison"].sum(),
                    Oct_2025_filtered_Fixed["1st Comparison"].sum(),
                    Nov_2025_filtered_Fixed["1st Comparison"].sum(),
                    Dec_2025_filtered_Fixed["1st Comparison"].sum(),
                ],
                "Month": [
                    "January",
                    "February",
                    "March",
                    "April",
                    "May",
                    "June",
                    "July",
                    "August",
                    "September",
                    "October",
                    "November",
                    "December",
                ],
            }

            colsss1, colsss2 = st.columns(2)
            with colsss1:
                st.header("Fixed Cost Analysis (Year To Date)")
            with colsss2:
                st.header("Fixed Cost Analysis Trend by Month (Year To Date)")

            with st.container(height=500, border=False):
                cols1, cols2, cols3, cols4 = st.columns(
                    [0.15, 0.15, 0.15, 0.55], vertical_alignment="center"
                )

                with cols1:
                    st.metric(
                        value=f"£{Fixed_cost_YTD_Budget:,.2f}",
                        label="Fixed Cost Year To Date Budget",
                        border=True,
                    )
                with cols2:
                    st.metric(
                        value=f"£{Fixed_cost_YTD_spent:,.2f}",
                        label="Fixed Cost Year To Date Spent",
                        border=True,
                    )
                with cols3:
                    st.metric(
                        value=f"£{Fixed_cost_YTD_Delta:,.2f}",
                        label="Fixed Cost Year To Date Delta",
                        border=True,
                        delta=f"{Fixed_Cost_YTD_Delta_Percent:.2f}%",
                    )

                with cols4:
                    fig = px.line(
                        data_L2,
                        x="Month",
                        y=["Fixed Cost Spent", "Fixed Cost Budget"],
                        title="Budget vs. Spent Over Months",
                        labels={"value": "Amount", "Month": "Month"},
                        color_discrete_sequence=[
                            "red",
                            "green",
                        ],  # Optional customization for colors
                    )

                    # Display Plotly chart in Streamlit
                    st.plotly_chart(fig)

            clswe11, colswe12 = st.columns(2)
            with clswe11:
                with st.container(height=500, border=False):
                    # User filter input
                    selected_category_Order_L2 = st.selectbox(
                        "Filter by Order:",
                        ["All"] + list(combined_L2_Fixed["Order"].unique()),
                        key="FI5656dby Order",
                    )
                    filtered_df = L2_Filtered_data(
                        selected_category_Order_L2, combined_L2_Fixed
                    )

                    coli1, coli2, coli3 = st.columns(
                        3, border=True, vertical_alignment="center"
                    )
                    with coli1:
                        st.metric(
                            label="Total Budget",
                            value=f"£{filtered_df['Total Budget'].sum():,.2f}",
                        )
                    with coli2:
                        st.metric(
                            label="Total Spent",
                            value=f"£{filtered_df['Total Main'].sum():,.2f}",
                        )
                    with coli3:
                        st.metric(
                            label="Total Difference",
                            value=f"£{filtered_df['Total Difference'].sum():,.2f}",
                            delta=f"{(((filtered_df['Total Budget'].sum()) - (filtered_df['Total Main'].sum()))/(filtered_df['Total Budget'].sum()))*100:.2f}%",
                        )
                    Dataframes_ranked(filtered_df, "Order")

            with colswe12:
                with st.container(height=500, border=False):
                    fig = Levels_BarChart(filtered_df, "Order")
                    st.subheader("Cost by Order Bar Chart")
                    st.plotly_chart(fig, key="45hgfhe")

            col31, col32 = st.columns(2, gap="medium", vertical_alignment="center")
            new_data_454 = combined_L3_Fixed[
                combined_L3_Fixed["Order"] == selected_category_Order_L2
            ]
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
                    filtered_df = L3_YTD_Filtered(
                        selected_category_L3,
                        selected_category_Order_L2,
                        combined_L3_Fixed,
                    )
                    coli31, coli32, coli33 = st.columns(
                        3, border=True, vertical_alignment="center"
                    )
                    with coli31:
                        st.metric(
                            label="Budget",
                            value=f"£{filtered_df['Total Budget'].sum():,.2f}",
                        )
                    with coli32:
                        st.metric(
                            label="Spent",
                            value=f"£{filtered_df['Total Main'].sum():,.2f}",
                        )
                    with coli33:
                        budget_sum = filtered_df["Total Budget"].sum()
                        main_sum = filtered_df["Total Main"].sum()
                        if pd.notna(budget_sum) and budget_sum != 0:
                            delta_value = ((budget_sum - main_sum) / budget_sum) * 100
                            delta = f"{delta_value:.2f}%"
                        else:
                            delta = 0
                        st.metric(
                            label="Delta",
                            value=f"£{filtered_df['Total Difference'].sum():,.2f}",
                            delta=delta,
                        )
                    Dataframes_ranked(filtered_df, "L3")

            with col32:
                with st.container(height=500, border=False):
                    fig = Levels_BarChart(filtered_df, "L3")
                    # Display the chart in Streamlit
                    st.subheader("Cost by L3 Bar Chart")
                    st.plotly_chart(fig, key="kfmmfem")

            col41, col42 = st.columns(2, gap="medium", vertical_alignment="center")
            new_data_4154 = combined_L4_Fixed[
                combined_L4_Fixed["L3"] == selected_category_L3
            ]
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
                    filtered_df = L4_YTD_Filtered(
                        selected_category_L4,
                        selected_category_L3,
                        selected_category_Order_L2,
                        combined_L4_Fixed,
                    )
                    coli31, coli32, coli33 = st.columns(
                        3, border=True, vertical_alignment="center"
                    )
                    with coli31:
                        st.metric(
                            label="Budget",
                            value=f"£{filtered_df['Total Budget'].sum():,.2f}",
                        )
                    with coli32:
                        st.metric(
                            label="Spent",
                            value=f"£{filtered_df['Total Main'].sum():,.2f}",
                        )
                    with coli33:
                        budget_sum = filtered_df["Total Budget"].sum()
                        main_sum = filtered_df["Total Main"].sum()
                        if pd.notna(budget_sum) and budget_sum != 0:
                            delta_value = ((budget_sum - main_sum) / budget_sum) * 100
                            delta = f"{delta_value:.2f}%"
                        else:
                            delta = 0
                        st.metric(
                            label="Delta",
                            value=f"£{filtered_df['Total Difference'].sum():,.2f}",
                            delta=delta,
                        )
                    Dataframes_ranked(filtered_df, "L4")

            with col42:
                with st.container(height=500, border=False):
                    fig = Levels_BarChart(filtered_df, "L4")
                    # Display the chart in Streamlit
                    st.subheader("Cost by L4 Bar Chart")
                    st.plotly_chart(fig, key="efeef22efrvbg")
            col51, col52 = st.columns(2, gap="medium", vertical_alignment="center")
            new_data_41154 = combined_L5_Fixed[
                combined_L5_Fixed["L4"] == selected_category_L4
            ]
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
                        ["All"]
                        + list(new_data_41154["AccountAndDescpription"].unique()),
                        key="4r34rf34rf44gtrfghtertger",
                    )
                    filtered_df = L5_YTD_Filtered(
                        selected_category_Order_L2,
                        selected_category_L3,
                        selected_category_L4,
                        selected_category_L5,
                        combined_L5_Fixed,
                    )
                    coli31, coli32, coli33 = st.columns(
                        3, border=True, vertical_alignment="center"
                    )
                    with coli31:
                        st.metric(
                            label="Budget",
                            value=f"£{filtered_df['Total Budget'].sum():,.2f}",
                        )
                    with coli32:
                        st.metric(
                            label="Spent",
                            value=f"£{filtered_df['Total Main'].sum():,.2f}",
                        )
                    with coli33:
                        budget_sum = filtered_df["Total Budget"].sum()
                        main_sum = filtered_df["Total Main"].sum()
                        if pd.notna(budget_sum) and budget_sum != 0:
                            delta_value = ((budget_sum - main_sum) / budget_sum) * 100
                            delta = f"{delta_value:.2f}%"
                        else:
                            delta = 0
                        st.metric(
                            label="Delta",
                            value=f"£{filtered_df['Total Difference'].sum():,.2f}",
                            delta=delta,
                        )
                    Dataframes_ranked(filtered_df, "AccountAndDescpription")

            with col52:
                with st.container(height=500, border=False):
                    fig = Levels_BarChart(filtered_df, "AccountAndDescpription")
                    # Display the chart in Streamlit
                    st.subheader("Cost by Account Bar Chart")
                    st.plotly_chart(fig, key="435253wewew")

        if selected_cost_YTD == "Variable Cost":
            #######################----------------------------------------------#####################################
            data_L22 = {
                "Variable Cost Spent": [
                    Jan_2025_filtered_Variable["Main"].sum(),
                    Feb_2025_filtered_Variable["Main"].sum(),
                    Mar_2025_filtered_Variable["Main"].sum(),
                    Apr_2025_filtered_Variable["Main"].sum(),
                    May_2025_filtered_Variable["Main"].sum(),
                    Jun_2025_filtered_Variable["Main"].sum(),
                    Jul_2025_filtered_Variable["Main"].sum(),
                    Aug_2025_filtered_Variable["Main"].sum(),
                    Sep_2025_filtered_Variable["Main"].sum(),
                    Oct_2025_filtered_Variable["Main"].sum(),
                    Nov_2025_filtered_Variable["Main"].sum(),
                    Dec_2025_filtered_Variable["Main"].sum(),
                ],
                "Variable Cost Budget": [
                    Jan_2025_filtered_Variable["1st Comparison"].sum(),
                    Feb_2025_filtered_Variable["1st Comparison"].sum(),
                    Mar_2025_filtered_Variable["1st Comparison"].sum(),
                    Apr_2025_filtered_Variable["1st Comparison"].sum(),
                    May_2025_filtered_Variable["1st Comparison"].sum(),
                    Jun_2025_filtered_Variable["1st Comparison"].sum(),
                    Jul_2025_filtered_Variable["1st Comparison"].sum(),
                    Aug_2025_filtered_Variable["1st Comparison"].sum(),
                    Sep_2025_filtered_Variable["1st Comparison"].sum(),
                    Oct_2025_filtered_Variable["1st Comparison"].sum(),
                    Nov_2025_filtered_Variable["1st Comparison"].sum(),
                    Dec_2025_filtered_Variable["1st Comparison"].sum(),
                ],
                "Month": [
                    "January",
                    "February",
                    "March",
                    "April",
                    "May",
                    "June",
                    "July",
                    "August",
                    "September",
                    "October",
                    "November",
                    "December",
                ],
            }

            colsss1, colsss2 = st.columns(2)
            with colsss1:
                st.header("Variable Cost Analysis (Year To Date)")
            with colsss2:
                st.header("Variable Cost Analysis Trend by Month (Year To Date)")

            with st.container(height=500, border=False):
                cols1, cols2, cols3, cols4 = st.columns(
                    [0.15, 0.15, 0.15, 0.55], vertical_alignment="center"
                )

                with cols1:
                    st.metric(
                        value=f"£{Variable_cost_YTD_Budget:,.2f}",
                        label="Variable Cost Year To Date Budget",
                        border=True,
                    )
                with cols2:
                    st.metric(
                        value=f"£{Variable_cost_YTD_spent:,.2f}",
                        label="Variable Cost Year To Date Spent",
                        border=True,
                    )
                with cols3:
                    st.metric(
                        value=f"£{Variable_cost_YTD_Delta:,.2f}",
                        label="Variable Cost Year To Date Delta",
                        border=True,
                        delta=f"{Variable_Cost_YTD_Delta_Percent:.2f}%",
                    )
                with cols4:
                    fig = px.line(
                        data_L22,
                        x="Month",
                        y=["Variable Cost Spent", "Variable Cost Budget"],
                        title="Budget vs. Spent Over Months",
                        labels={"value": "Amount", "Month": "Month"},
                        color_discrete_sequence=[
                            "red",
                            "green",
                        ],  # Optional customization for colors
                    )

                    # Display Plotly chart in Streamlit
                    st.plotly_chart(fig)

            clswe11, colswe12 = st.columns(2)
            with clswe11:
                with st.container(height=500, border=False):
                    # User filter input
                    selected_category_Order_L2 = st.selectbox(
                        "Filter by Order:",
                        ["All"] + list(combined_L2_Variable["Order"].unique()),
                        key="FI5656dby Order",
                    )
                    filtered_df = L2_Filtered_data(
                        selected_category_Order_L2, combined_L2_Variable
                    )

                    coli1, coli2, coli3 = st.columns(
                        3, border=True, vertical_alignment="center"
                    )
                    with coli1:
                        st.metric(
                            label="Total Budget",
                            value=f"£{filtered_df['Total Budget'].sum():,.2f}",
                        )
                    with coli2:
                        st.metric(
                            label="Total Spent",
                            value=f"£{filtered_df['Total Main'].sum():,.2f}",
                        )
                    with coli3:
                        st.metric(
                            label="Total Difference",
                            value=f"£{filtered_df['Total Difference'].sum():,.2f}",
                            delta=f"{(((filtered_df['Total Budget'].sum()) - (filtered_df['Total Main'].sum()))/(filtered_df['Total Budget'].sum()))*100:.2f}%",
                        )
                    Dataframes_ranked(filtered_df, "Order")

            with colswe12:
                with st.container(height=500, border=False):
                    fig = Levels_BarChart(filtered_df, "Order")
                    st.subheader("Cost by Order Bar Chart")
                    st.plotly_chart(fig, key="45hgfhe")

            col31, col32 = st.columns(2, gap="medium", vertical_alignment="center")
            new_data_454 = combined_L3_Variable[
                combined_L3_Variable["Order"] == selected_category_Order_L2
            ]
            combined_L3_Variable = combined_L3_Variable.rename(
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
                    filtered_df = L3_YTD_Filtered(
                        selected_category_L3,
                        selected_category_Order_L2,
                        combined_L3_Variable,
                    )
                    coli31, coli32, coli33 = st.columns(
                        3, border=True, vertical_alignment="center"
                    )
                    with coli31:
                        st.metric(
                            label="Budget",
                            value=f"£{filtered_df['Total Budget'].sum():,.2f}",
                        )
                    with coli32:
                        st.metric(
                            label="Spent",
                            value=f"£{filtered_df['Total Main'].sum():,.2f}",
                        )
                    with coli33:
                        budget_sum = filtered_df["Total Budget"].sum()
                        main_sum = filtered_df["Total Main"].sum()
                        if pd.notna(budget_sum) and budget_sum != 0:
                            delta_value = ((budget_sum - main_sum) / budget_sum) * 100
                            delta = f"{delta_value:.2f}%"
                        else:
                            delta = 0
                        st.metric(
                            label="Delta",
                            value=f"£{filtered_df['Total Difference'].sum():,.2f}",
                            delta=delta,
                        )
                    Dataframes_ranked(filtered_df, "L3")

            with col32:
                with st.container(height=500, border=False):
                    fig = Levels_BarChart(filtered_df, "L3")
                    # Display the chart in Streamlit
                    st.subheader("Cost by L3 Bar Chart")
                    st.plotly_chart(fig, key="kfmmfem")

            col41, col42 = st.columns(2, gap="medium", vertical_alignment="center")
            new_data_4154 = combined_L4_Variable[
                combined_L4_Variable["L3"] == selected_category_L3
            ]
            combined_L4_Variable = combined_L4_Variable.rename(
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
                    filtered_df = L4_YTD_Filtered(
                        selected_category_L4,
                        selected_category_L3,
                        selected_category_Order_L2,
                        combined_L4_Variable,
                    )
                    coli31, coli32, coli33 = st.columns(
                        3, border=True, vertical_alignment="center"
                    )
                    with coli31:
                        st.metric(
                            label="Budget",
                            value=f"£{filtered_df['Total Budget'].sum():,.2f}",
                        )
                    with coli32:
                        st.metric(
                            label="Spent",
                            value=f"£{filtered_df['Total Main'].sum():,.2f}",
                        )
                    with coli33:
                        budget_sum = filtered_df["Total Budget"].sum()
                        main_sum = filtered_df["Total Main"].sum()
                        if pd.notna(budget_sum) and budget_sum != 0:
                            delta_value = ((budget_sum - main_sum) / budget_sum) * 100
                            delta = f"{delta_value:.2f}%"
                        else:
                            delta = 0
                        st.metric(
                            label="Delta",
                            value=f"£{filtered_df['Total Difference'].sum():,.2f}",
                            delta=delta,
                        )
                    Dataframes_ranked(filtered_df, "L4")

            with col42:
                with st.container(height=500, border=False):
                    fig = Levels_BarChart(filtered_df, "L4")
                    # Display the chart in Streamlit
                    st.subheader("Cost by L4 Bar Chart")
                    st.plotly_chart(fig, key="efeef22efrvbg")
            col51, col52 = st.columns(2, gap="medium", vertical_alignment="center")
            new_data_41154 = combined_L5_Variable[
                combined_L5_Variable["L4"] == selected_category_L4
            ]
            combined_L5_Variable = combined_L5_Variable.rename(
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
                        ["All"]
                        + list(new_data_41154["AccountAndDescpription"].unique()),
                        key="4r34rf34rf44gtrfghtertger",
                    )
                    filtered_df = L5_YTD_Filtered(
                        selected_category_Order_L2,
                        selected_category_L3,
                        selected_category_L4,
                        selected_category_L5,
                        combined_L5_Variable,
                    )
                    coli31, coli32, coli33 = st.columns(
                        3, border=True, vertical_alignment="center"
                    )
                    with coli31:
                        st.metric(
                            label="Budget",
                            value=f"£{filtered_df['Total Budget'].sum():,.2f}",
                        )
                    with coli32:
                        st.metric(
                            label="Spent",
                            value=f"£{filtered_df['Total Main'].sum():,.2f}",
                        )
                    with coli33:
                        budget_sum = filtered_df["Total Budget"].sum()
                        main_sum = filtered_df["Total Main"].sum()
                        if pd.notna(budget_sum) and budget_sum != 0:
                            delta_value = ((budget_sum - main_sum) / budget_sum) * 100
                            delta = f"{delta_value:.2f}%"
                        else:
                            delta = 0
                        st.metric(
                            label="Delta",
                            value=f"£{filtered_df['Total Difference'].sum():,.2f}",
                            delta=delta,
                        )
                    Dataframes_ranked(filtered_df, "AccountAndDescpription")

            with col52:
                with st.container(height=500, border=False):
                    fig = Levels_BarChart(filtered_df, "AccountAndDescpription")
                    # Display the chart in Streamlit
                    st.subheader("Cost by Account Bar Chart")
                    st.plotly_chart(fig, key="435253wewew")
    with tab_3:
        st.info(
            "This feature will be launched in future version of this dashboard. Dashboard is designed by @aakalkri for Amazon LCY3 Reliability and Maintenance Engineering Automations Engineering Team under supervision of @didymiod and @sherress.",
            icon="ℹ️",
        )
else:
    st.info("Please upload an Excel file to proceed.")
