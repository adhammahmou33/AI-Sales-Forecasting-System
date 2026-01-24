import pandas as pd 


def load_data(file_path):
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
        print("download CSV")
    elif file_path.endswith(".xlsx"):
        df =pd.read_excel(file_path)
        print("download Excel")
    else :
        print("NOT Uploaded File")
    return df
   
