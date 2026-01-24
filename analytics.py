import pandas as pd 


def get_basic_status(df):
    status = {
        "Total_Sales_profits" :df['Profits'].sum(),
        "total Sales Count" : len(df),
         "average price" : df['Price'].mean()
    }
    return status 

def get_top_countries(df):
    return df.groupby("Country")["Profits"].sum().sort_values(ascending =False).head(5)

def get_gender_behevior(df):
    return df.groupby("Gender")["Profits"].mean()

def process_date_columns(df):
    
    if 'Date' in df.columns :
       df['Date'] = pd.to_datetime(df['Date'])
       df['Year'] = df['Date'].dt.year
       df['Month'] = df['Date'].dt.month_name()
       df['Day'] = df['Date'].dt.day_name()
    elif 'Data' in df.columns:
        df['Data'] = pd.to_datetime(df['Data'])
        df['Year'] = df['Data'].dt.year
        df['Month'] = df['Data'].dt.month_name()
        df['Day'] = df['Data'].dt.day_name()
    elif 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
        df['Year'] = df['date'].dt.year
        df['Month'] = df['date'].dt.month_name()
        df['Day'] = df['date'].dt.day_name()    
            
    else :
        print("No data column found in the dataset.")  
    return df    