# EU Trade Analysis Dashboard

A project analyzing the European Union’s international trade in goods and services.

## 📊 About the Project

This project uses data from Eurostat (available on Kaggle):
https://www.kaggle.com/datasets/abidhussai512/exports-and-imports-dataset-eurostat

The goal is to explore and visualize trade dynamics across EU countries, focusing on:
- Exports and Imports
- Trade Balance
- Export-to-Import Ratio
- Country-level comparisons
- Trends over time (1995–2025)

# 🛠️ Technologies 

    Python 3 - Main Language

    Pandas 
    - Data cleaning and transformation
    - Creation of derived metrics (trade balance, ratios, YoY)
    - Aggregation for EU-level analysis
    
    Power BI - Data Visualization

    ---

## 📁 Project Structure

European-Union-Trade-in-Goods-and-Services-analysis/
<br>
 # data cleaning and transformation
<br>
├── src/data_processing.py                                      
<br>
 # data map with 2 letter country codes (information directly from eurostat)
<br>
├── data/raw/country_codes_UE.csv                               
<br>
#  data map with other complementary information (directly from eurostat)
<br>
├── data/raw/na_item.csv                                  
<br>
#  explanation on data maps and sources from all data utilized
<br>
├── data/raw/data_dictionary.txt                                
<br>
# original kaggle csv
<br>
├── data/raw/nama_10_exi_2026-04-01.csv                         
<br>
# Country level data
<br>
├── data/processed/nama_10_exi_2026-04-01_treated.csv           
<br>
# European Union Level data
<br>
├── data/processed/nama_10_exi_2026-04-01_EU_treated.csv        
<br>
# Power BI Dashboard
<br>
└── dashboard/eu_trade_dashboard.pbix                           
<br>


## 📈 Dashboard

The Power BI dashboard provides:
- EU-level overview (KPIs and trends)
- Country comparison (ranking and trade balance)
- Geographic visualization
- Detailed country analysis

---

## 🧠 Key Insights

- Germany dominates EU trade, representing the largest share
- Ireland shows the highest export-to-import ratio
- Southern and Eastern European countries tend to have trade deficits
- EU trade surplus is concentrated in a few countries

---

## 🚀 How to Run

1. Clone the repository  
2. Install dependencies:

pip install -r requirements.txt

3. Run the data processing script:

python src/data_processing.py

4. Open the Power BI file:

/dashboard/eu_trade_dashboard.pbix

