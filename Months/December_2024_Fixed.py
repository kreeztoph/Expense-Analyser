import pandas as pd
import streamlit as st
import numpy as np
import plotly.graph_objects as go
from Functions.Color_code import color_code


def December_2024_Fixed(data):
    data_complete = data.groupby(["Category"]).sum(list).reset_index()
    data_2024_Fixed_Cost_Data = data[(data["Category"] == "Fixed Costs")]
    L1_Grouped = (
        data_2024_Fixed_Cost_Data.groupby(["Category"]).sum(list).reset_index()
    )
    L2_Grouped = (
        data_2024_Fixed_Cost_Data.groupby(["Category", "Order"])
        .sum(list)
        .reset_index()
    )
    L3_Grouped = (
        data_2024_Fixed_Cost_Data.groupby(["Category", "Order", "L3"])
        .sum(list)
        .reset_index()
    )
    L4_Grouped = (
        data_2024_Fixed_Cost_Data.groupby(["Category", "Order", "L3", "L4"])
        .sum(list)
        .reset_index()
    )
    L5_Grouped = (
        data_2024_Fixed_Cost_Data.groupby(
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

    data_Budget = float(data_complete["1st Comparison"].sum())
    data_spent = float(data_complete["Main"].sum())
    data_Delta = float(data_complete["Var Comp&Main"].sum())
    data_delta_percent = (((data_Budget) - (data_spent)) / (data_Budget)) * 100
    data_Fixed_Budget = float(df_parsed_1["Budget"].iloc[0])
    data_Fixed_Spent = float(df_parsed_1["Main"].iloc[0])
    data_Fixed_Delta = float(df_parsed_1["Delta"].iloc[0])
    data_Fixed_Delta_Percent = (
        ((data_Fixed_Budget) - (data_Fixed_Spent)) / (data_Fixed_Budget)
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
            "December Budget",
            value=f"£{data_Budget:,.2f}",
            border=True,
            help="This is the total budget for December.",
        )
    with col2:
        st.metric(
            "December Spent",
            value=f"£{data_spent:,.2f}",
            border=True,
            help="This is the total amount of funds spent in December.",
        )
    with col3:
        st.metric(
            "December Delta",
            value=f"£{data_Delta:,.2f}",
            border=True,
            delta=f"{data_delta_percent:,.2f} %",
            help="This is the difference in the amount budgeted and the amount spent for December.",
        )
    with col4:
        st.metric(
            "December Fixed Cost Budget",
            value=f"£{data_Fixed_Budget:,.2f}",
            border=True,
            help="This is the total amount budgeted to be spent for Fixed Costs in December.",
        )
    with col5:
        st.metric(
            "December Fixed Cost Spent",
            value=f"£{data_Fixed_Spent:,.2f}",
            border=True,
            help="This is the total amount spent for Fixed Cost inDecember.",
        )
    with col6:
        st.metric(
            "December Fixed Cost Delta",
            value=f"£{data_Fixed_Delta:,.2f}",
            border=True,
            delta=f"{data_Fixed_Delta_Percent:,.2f}%",
            help="This is the difference in the budgeted amount and Spent amount for Fixed Costs in December.",
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
                        color_code(row,'Delta') if col == "Order" else ""
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
                budget_sum = filtered_df['Budget'].sum()
                main_sum = filtered_df['Spent'].sum()
                if pd.notna(budget_sum) and budget_sum != 0:
                    delta_value = ((budget_sum - main_sum) / budget_sum) * 100
                    delta = f"{delta_value:.2f}%"
                else:
                    delta = 0
                st.metric(
                    label="Delta",
                    value=f"£{filtered_df['Delta'].sum():,.2f}",
                    delta=delta,
                )
            # Apply styling to the 'Order' column based on 'Delta'
            if "Delta" in filtered_df.columns:
                styled_df = filtered_df.style.apply(
                    lambda row: [
                        color_code(row,'Delta') if col == "L3" else ""
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
                budget_sum = filtered_df['Budget'].sum()
                main_sum = filtered_df['Spent'].sum()
                if pd.notna(budget_sum) and budget_sum != 0:
                    delta_value = ((budget_sum - main_sum) / budget_sum) * 100
                    delta = f"{delta_value:.2f}%"
                else:
                    delta = 0
                st.metric(
                    label="Delta",
                    value=f"£{filtered_df['Delta'].sum():,.2f}",
                    delta=delta,
                )
            # Apply styling to the 'Order' column based on 'Delta'
            if "Delta" in filtered_df.columns:
                styled_df = filtered_df.style.apply(
                    lambda row: [
                        color_code(row,'Delta') if col == "L4" else ""
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
                budget_sum = filtered_df['Budget'].sum()
                main_sum = filtered_df['Spent'].sum()
                if pd.notna(budget_sum) and budget_sum != 0:
                    delta_value = ((budget_sum - main_sum) / budget_sum) * 100
                    delta = f"{delta_value:.2f}%"
                else:
                    delta = 0
                st.metric(
                    label="Delta",
                    value=f"£{filtered_df['Delta'].sum():,.2f}",
                    delta=delta,
                )
            # Apply styling to the 'Order' column based on 'Delta'
            if "Delta" in filtered_df.columns:
                styled_df = filtered_df.style.apply(
                    lambda row: [
                        (
                            color_code(row,'Delta')
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