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
from Months.January_2025_Fixed import January_2025_Fixed
from Months.January_2025_Variable import January_2025_Variable
from Months.February_2025_Fixed import February_2025_Fixed
from Months.February_2025_Variable import February_2025_Variable
from Months.March_2025_Fixed import March_2025_Fixed
from Months.March_2025_Variable import March_2025_Variable
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
    Jan_2025 = sheets.get("Jan_2025")
    Feb_2025 = sheets.get("Feb_2025")
    Mar_2025 = sheets.get("Mar_2025")

    Jan_2025, Feb_2025, Mar_2025 = months_convert(Jan_2025, Feb_2025, Mar_2025)
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
                label="Select a Month", options=["January", "February", "March"]
            )
        with col_2:
            year = st.selectbox(label="Select Year", options=["2025", "2026"])
        with col_3:
            data = st.selectbox(
                label="Select Cost", options=["Fixed Costs", "Variable Costs"]
            )
        if (month == "January") & (year == "2025") & (data == "Fixed Costs"):
            January_2025_Fixed(Jan_2025)

        elif (month == "January") & (year == "2025") & (data == "Variable Costs"):
            January_2025_Variable(Jan_2025)

        elif (month == "February") & (year == "2025") & (data == "Fixed Costs"):
            February_2025_Fixed(Feb_2025)

        elif (month == "February") & (year == "2025") & (data == "Variable Costs"):
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
    with tab_2:
        (
            Year_To_Date_Total_Spent,
            Year_To_Date_Total_Budget,
            Year_To_Date_Total_Delta,
            delta,
            data,
        ) = YTD_KPI(Jan_2025,Feb_2025,Mar_2025)
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
                YTD_SunBurst(Jan_2025, Feb_2025, Mar_2025), use_container_width=True
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
        ) = YTD_Cost(Jan_2025, Feb_2025, Mar_2025)

        # This section handles the summation of data and uses a similar logic to the monthly view page
        filtered_result = filtered_months_data(Jan_2025, Feb_2025, Mar_2025)

        # Access filtered Fixed Costs and Variable Costs
        filtered_fixed_costs = filtered_result["Fixed Costs"]
        filtered_variable_costs = filtered_result["Variable Costs"]
        Jan_2025_filtered_Fixed, Feb_2025_filtered_Fixed, Mar_2025_filtered_Fixed = (
            filtered_fixed_costs[0],
            filtered_fixed_costs[1],
            filtered_fixed_costs[2],
        )
        (
            Jan_2025_filtered_Variable,
            Feb_2025_filtered_Variable,
            Mar_2025_filtered_Variable,
        ) = (
            filtered_variable_costs[0],
            filtered_variable_costs[1],
            filtered_variable_costs[2],
        )

        monthly_data = {
            "January": (Jan_2025_filtered_Fixed, Jan_2025_filtered_Variable),
            "February": (Feb_2025_filtered_Fixed, Feb_2025_filtered_Variable),
            "March": (Mar_2025_filtered_Fixed, Mar_2025_filtered_Variable),
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
                ],
                "Fixed Cost Budget": [
                    Jan_2025_filtered_Fixed["1st Comparison"].sum(),
                    Feb_2025_filtered_Fixed["1st Comparison"].sum(),
                    Mar_2025_filtered_Variable["1st Comparison"].sum(),
                ],
                "Month": ["January", "Feburary","March"],
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
                    Dataframes_ranked(filtered_df,"Order")

            with colswe12:
                with st.container(height=500, border=False):
                    fig = Levels_BarChart(filtered_df,'Order')
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
                        st.metric(
                            label="Delta",
                            value=f"£{filtered_df['Total Difference'].sum():,.2f}",
                            delta=f"{(((filtered_df['Total Budget'].sum()) - (filtered_df['Total Main'].sum()))/(filtered_df['Total Budget'].sum()))*100:.2f}%",
                        )
                    Dataframes_ranked(filtered_df,"L3")

            with col32:
                with st.container(height=500, border=False):
                    fig = Levels_BarChart(filtered_df,'L3')
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
                        combined_L4_Fixed
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
                        st.metric(
                            label="Delta",
                            value=f"£{filtered_df['Total Difference'].sum():,.2f}",
                            delta=f"{(((filtered_df['Total Budget'].sum()) - (filtered_df['Total Main'].sum()))/(filtered_df['Total Budget'].sum()))*100:.2f}%",
                        )
                    Dataframes_ranked(filtered_df,"L4")

            with col42:
                with st.container(height=500, border=False):
                    fig = Levels_BarChart(filtered_df,'L4')
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
                    filtered_df = L5_YTD_Filtered(selected_category_Order_L2,selected_category_L3,selected_category_L4,selected_category_L5,combined_L5_Fixed)
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
                        st.metric(
                            label="Delta",
                            value=f"£{filtered_df['Total Difference'].sum():,.2f}",
                            delta=f"{(((filtered_df['Total Budget'].sum()) - (filtered_df['Total Main'].sum()))/(filtered_df['Total Budget'].sum()))*100:.2f}%",
                        )
                    Dataframes_ranked(filtered_df,'AccountAndDescpription')

            with col52:
                with st.container(height=500, border=False):
                    fig = Levels_BarChart(filtered_df,'AccountAndDescpription')
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
                ],
                "Variable Cost Budget": [
                    Jan_2025_filtered_Variable["1st Comparison"].sum(),
                    Feb_2025_filtered_Variable["1st Comparison"].sum(),
                    Mar_2025_filtered_Variable["1st Comparison"].sum(),
                ],
                "Month": ["January", "Feburary","March"]}

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
                    Dataframes_ranked(filtered_df,"Order")

            with colswe12:
                with st.container(height=500, border=False):
                    fig = Levels_BarChart(filtered_df,'Order')
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
                        st.metric(
                            label="Delta",
                            value=f"£{filtered_df['Total Difference'].sum():,.2f}",
                            delta=f"{(((filtered_df['Total Budget'].sum()) - (filtered_df['Total Main'].sum()))/(filtered_df['Total Budget'].sum()))*100:.2f}%",
                        )
                    Dataframes_ranked(filtered_df,"L3")

            with col32:
                with st.container(height=500, border=False):
                    fig = Levels_BarChart(filtered_df,'L3')
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
                        combined_L4_Variable
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
                        st.metric(
                            label="Delta",
                            value=f"£{filtered_df['Total Difference'].sum():,.2f}",
                            delta=f"{(((filtered_df['Total Budget'].sum()) - (filtered_df['Total Main'].sum()))/(filtered_df['Total Budget'].sum()))*100:.2f}%",
                        )
                    Dataframes_ranked(filtered_df,"L4")

            with col42:
                with st.container(height=500, border=False):
                    fig = Levels_BarChart(filtered_df,'L4')
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
                    filtered_df = L5_YTD_Filtered(selected_category_Order_L2,selected_category_L3,selected_category_L4,selected_category_L5,combined_L5_Variable)
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
                        st.metric(
                            label="Delta",
                            value=f"£{filtered_df['Total Difference'].sum():,.2f}",
                            delta=f"{(((filtered_df['Total Budget'].sum()) - (filtered_df['Total Main'].sum()))/(filtered_df['Total Budget'].sum()))*100:.2f}%",
                        )
                    Dataframes_ranked(filtered_df,'AccountAndDescpription')

            with col52:
                with st.container(height=500, border=False):
                    fig = Levels_BarChart(filtered_df,'AccountAndDescpription')
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
