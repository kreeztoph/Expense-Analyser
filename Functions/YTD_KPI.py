import pandas as pd


def YTD_KPI(
    jan=None,
    feb=None,
    mar=None,
    apr=None,
    may=None,
    jun=None,
    jul=None,
    aug=None,
    sep=None,
    oct=None,
    nov=None,
    dec=None,
):
    if jan is None:
        jan = pd.DataFrame({"Main": [0], "1st Comparison": [0], "Var Comp&Main": [0]})
    if feb is None:
        feb = pd.DataFrame({"Main": [0], "1st Comparison": [0], "Var Comp&Main": [0]})
    if mar is None:
        mar = pd.DataFrame({"Main": [0], "1st Comparison": [0], "Var Comp&Main": [0]})
    if (apr is None) or (apr.empty):
        apr = pd.DataFrame({"Main": [0], "1st Comparison": [0], "Var Comp&Main": [0]})
    if (may is None) or (may.empty):
        may = pd.DataFrame({"Main": [0], "1st Comparison": [0], "Var Comp&Main": [0]})
    if (jun is None) or (jun.empty):
        jun = pd.DataFrame({"Main": [0], "1st Comparison": [0], "Var Comp&Main": [0]})
    if (jul is None) or (jul.empty):
        jul = pd.DataFrame({"Main": [0], "1st Comparison": [0], "Var Comp&Main": [0]})
    if (aug is None) or (aug.empty):
        aug = pd.DataFrame({"Main": [0], "1st Comparison": [0], "Var Comp&Main": [0]})
    if (sep is None) or (sep.empty):
        sep = pd.DataFrame({"Main": [0], "1st Comparison": [0], "Var Comp&Main": [0]})
    if (oct is None) or (oct.empty):
        oct = pd.DataFrame({"Main": [0], "1st Comparison": [0], "Var Comp&Main": [0]})
    if (nov is None) or (nov.empty):
        nov = pd.DataFrame({"Main": [0], "1st Comparison": [0], "Var Comp&Main": [0]})
    if (dec is None) or (dec.empty):
        dec = pd.DataFrame({"Main": [0], "1st Comparison": [0], "Var Comp&Main": [0]})

    Year_To_Date_Total_Spent = (
        jan["Main"].sum()
        + feb["Main"].sum()
        + mar["Main"].sum()
        + apr["Main"].sum()
        + may["Main"].sum()
        + jun["Main"].sum()
        + jul["Main"].sum()
        + aug["Main"].sum()
        + sep["Main"].sum()
        + oct["Main"].sum()
        + nov["Main"].sum()
        + dec["Main"].sum()
    )
    Year_To_Date_Total_Budget = (
        jan["1st Comparison"].sum()
        + feb["1st Comparison"].sum()
        + mar["1st Comparison"].sum()
        + apr["1st Comparison"].sum()
        + may["1st Comparison"].sum()
        + jun["1st Comparison"].sum()
        + jul["1st Comparison"].sum()
        + aug["1st Comparison"].sum()
        + sep["1st Comparison"].sum()
        + oct["1st Comparison"].sum()
        + nov["1st Comparison"].sum()
        + dec["1st Comparison"].sum()
    )
    Year_To_Date_Total_Delta = (
        jan["Var Comp&Main"].sum()
        + feb["Var Comp&Main"].sum()
        + mar["Var Comp&Main"].sum()
        + apr["Var Comp&Main"].sum()
        + may["Var Comp&Main"].sum()
        + jun["Var Comp&Main"].sum()
        + jul["Var Comp&Main"].sum()
        + aug["Var Comp&Main"].sum()
        + sep["Var Comp&Main"].sum()
        + oct["Var Comp&Main"].sum()
        + nov["Var Comp&Main"].sum()
        + dec["Var Comp&Main"].sum()
    )
    
    delta_percent = (
        (Year_To_Date_Total_Budget - Year_To_Date_Total_Spent)
        / (Year_To_Date_Total_Budget)
    ) * 100

    # Create sample data
    data = pd.DataFrame(
        {
            "Month": ["January", "February", "March", "April", "May","June","July", "August", "September","October", "November", "December"],
            "Spent": [
                jan["Main"].sum(),
                feb["Main"].sum(),
                mar["Main"].sum(),
                apr["Main"].sum(),
                may["Main"].sum(),
                jun["Main"].sum(),
                jul["Main"].sum(),
                aug["Main"].sum(),
                sep["Main"].sum(),
                oct["Main"].sum(),
                nov["Main"].sum(),
                dec["Main"].sum(),
            ],
            "Budget": [
                jan["1st Comparison"].sum(),
                feb["1st Comparison"].sum(),
                mar["1st Comparison"].sum(),
                apr["1st Comparison"].sum(),
                may["1st Comparison"].sum(),
                jun["1st Comparison"].sum(),
                jul["1st Comparison"].sum(),
                aug["1st Comparison"].sum(),
                sep["1st Comparison"].sum(),
                oct["1st Comparison"].sum(),
                nov["1st Comparison"].sum(),
                dec["1st Comparison"].sum(),
            ],
        }
    )
    return (
        Year_To_Date_Total_Spent,
        Year_To_Date_Total_Budget,
        Year_To_Date_Total_Delta,
        delta_percent,
        data,
    )
