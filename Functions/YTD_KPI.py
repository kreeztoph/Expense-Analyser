import pandas as pd

def YTD_KPI(jan=None, feb=None, mar=None, apr=None):
    if jan is None:
        jan = pd.DataFrame({"Main": [0], "1st Comparison": [0], "Var Comp&Main": [0]})
    if feb is None:
        feb = pd.DataFrame({"Main": [0], "1st Comparison": [0], "Var Comp&Main": [0]})
    if mar is None:
        mar = pd.DataFrame({"Main": [0], "1st Comparison": [0], "Var Comp&Main": [0]})
    if apr is None:
        apr = pd.DataFrame({"Main": [0], "1st Comparison": [0], "Var Comp&Main": [0]})
    Year_To_Date_Total_Spent = (
        jan["Main"].sum() + feb["Main"].sum() + mar["Main"].sum() + apr["Main"].sum()
    )
    Year_To_Date_Total_Budget = (
        jan["1st Comparison"].sum()
        + feb["1st Comparison"].sum()
        + mar["1st Comparison"].sum()
        + apr["1st Comparison"].sum()
    )
    Year_To_Date_Total_Delta = (
        jan["Var Comp&Main"].sum()
        + feb["Var Comp&Main"].sum()
        + mar["Var Comp&Main"].sum()
        + apr["Var Comp&Main"].sum()
    )
    delta_percent = (
        (Year_To_Date_Total_Budget - Year_To_Date_Total_Spent)
        / (Year_To_Date_Total_Budget)
    ) * 100

    # Create sample data
    data = pd.DataFrame(
        {
            "Month": ["January", "February", "March", "April"],
            "Spent": [
                jan["Main"].sum(),
                feb["Main"].sum(),
                mar["Main"].sum(),
                apr["Main"].sum(),
            ],
            "Budget": [
                jan["1st Comparison"].sum(),
                feb["1st Comparison"].sum(),
                mar["1st Comparison"].sum(),
                apr["1st Comparison"].sum(),
            ],
        }
    )
    return Year_To_Date_Total_Spent,Year_To_Date_Total_Budget,Year_To_Date_Total_Delta,delta_percent,data