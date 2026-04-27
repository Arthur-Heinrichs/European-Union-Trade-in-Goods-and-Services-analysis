from pathlib import Path
import pandas as pd


# project root (one level above /src)
BASE_DIR = Path(__file__).resolve().parents[1]

# define directories
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

# read raw data
#three datasets: one with infos from eurostat and two with mapping tables that i have constructed.
#review data/raw/data_dictionary for more info.
df = pd.read_csv(RAW_DIR / "nama_10_exi_2026-04-01.csv")
country_codes_df = pd.read_csv(RAW_DIR /"country_codes_UE.csv")
na_item_df = pd.read_csv(RAW_DIR /"na_item.csv")



#adjusting from year based columns to one column with years
year_cols = [col for col in df.columns if col.isdigit()] 

df = df.melt(
    id_vars=["freq", "unit", "na_item", "geo\\TIME_PERIOD"],
    value_vars=year_cols,
    var_name="year",
    value_name="value"
)

#renaming field for corresponding country letter code
df.rename(columns={"geo\\TIME_PERIOD":"2_letter_code"}, inplace=True)

#transforming year and value(money) column in numbers
df["year"] = pd.to_numeric(df["year"], errors="coerce")
df["value"] = pd.to_numeric(df["value"], errors="coerce")*1000000

#keeping only current prices in million euros (original data, but we already multiplied by 1 million to display the original values)
df = df.loc[df["unit"]=="CP_MEUR"]

#transforming the variable from current prices in million euros to current prices in euros.
df["unit"] = df["unit"].replace("CP_MEUR", "CP_EUR")

#dropping null values
df = df.dropna(subset=["value"])



#Merging the country codes with the original dataset. 
# Data for EA21 and EA12 (EU aggregates) aren't mapped, 
# so I chose to remove them since their exact descriptions weren't available via Eurostat.
df = pd.merge(df, country_codes_df[["2_letter_code", "country"]], on="2_letter_code", how="inner")


#join with the table that has what type of operation it refers (export, import...)
df = pd.merge(df, na_item_df[["Label", "Notation"]], left_on="na_item", right_on="Notation", how="inner")
df = df.drop(columns="Notation")


#adjusting from operation lines to operation columns (one line per country per year)
df = df.pivot(
    index=["year", "country", "2_letter_code", "unit"], 
    columns="Label", 
    values="value"
).reset_index()


#dropping non total data from export and import of a country because we will not use it on the dashboard and not all of it is available.
df = df.drop(columns=['Exports of goods and services to members of the Monetary Union', 
                       'Exports of goods and services to non-members of the Monetary Union', 
                       'Exports of goods and services to the European Union', 
                       'Exports of goods and services to the institutions of the EU', 
                       'Exports of goods and services to third countries and international organisations',
                       'Imports of goods and services from members of the Monetary Union', 
                       'Imports of goods and services from non-members of the Monetary Union', 
                       'Imports of goods and services from the European Union', 
                       'Imports of goods and services from the institutions of the EU', 
                       'Imports of goods and services from third countries and international organisations'
                       ])

#creating custom fields for data
df["trade_balance"] = df["Exports of goods and services"]  - df ["Imports of goods and services"]
df["coverage_ratio"] = df["Exports of goods and services"] / df ["Imports of goods and services"] 
df["total_trade"] = df["Exports of goods and services"]    + df ["Imports of goods and services"]

#ordering data and creating a field for pct year year change
#using group by so first year by given country does not have a pct year change based on other country
df = df.sort_values(by=["country", "unit", "year"])
df["total_exports_yoy"] = df.groupby(["country", "unit"])["Exports of goods and services"].pct_change(periods=1)
df["total_imports_yoy"] = df.groupby(["country", "unit"])["Imports of goods and services"].pct_change(periods=1)

#creating a dataset that holds European union level data
df_total_ue = df[df["country"] == "European Union (27 countries)"].set_index("year")[['Exports of goods and services', 'Imports of goods and services', 
                                                                                      'trade_balance', 'coverage_ratio', 'total_trade', 'total_exports_yoy', 
                                                                                      'total_imports_yoy']]

#removing non country data
excluir = ['European Union (27 countries)',  'euro area (19 countries)', 'euro area (20 countries)', 'euro area']
df = df[~df["country"].isin(excluir)]

#creating custom fields that compare the country performance vs European Union
total_exports_por_ano = df["year"].map(df_total_ue["Exports of goods and services"])

df["%_Export_UE"] = (df["Exports of goods and services"]) / total_exports_por_ano

total_imports_por_ano = df["year"].map(df_total_ue["Imports of goods and services"])

df["%_Import_UE"] = (df["Imports of goods and services"]) / total_exports_por_ano

total_trade_por_ano = df["year"].map(df_total_ue["total_trade"])

df["%_total_trade_UE"] = (df["total_trade"]) / total_exports_por_ano

df_total_ue = df_total_ue.reset_index()


#exporting data
df.to_csv(PROCESSED_DIR  / "nama_10_exi_2026-04-01_treated.csv", index=False, encoding="utf-8")
df_total_ue.to_csv(PROCESSED_DIR / "nama_10_exi_2026-04-01_EU_treated.csv", index=False, encoding="utf-8")