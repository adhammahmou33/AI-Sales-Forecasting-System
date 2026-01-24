import pandas as pd 
from tkinter import filedialog
import tkinter as tk 
from  sklearn.linear_model import LinearRegression
from analytics import get_basic_status, process_date_columns
from data_loader import load_data
import matplotlib.pyplot as plt



def main ():
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost" ,True)
    
    file_path =filedialog.askopenfilename(
        title ="Select file",
        filetypes=[("Excel Files" , "*.xlsx *.xls") , ("CSV Files" , "*.csv")]
    )
    

    if file_path :
        try :
            df = load_data(file_path)
            print(df.head())
            print(df.describe())
            print(df.info())
            print("Load File Successfuly")
        except Exception as e :
            print(f"ُError load data{e}")  
            
    else :
        print("No File Selected")    
        
    print("The Big Numbers \n") 
    
    results = get_basic_status(df)   
    
    print("Total_Sales_profits : " , results["Total_Sales_profits"])
    print("total Sales Count is : ",results["total Sales Count"])
    print("average price is :" , results["average price"])

    df =process_date_columns(df) 
        
        
    plt.figure(figsize=(10, 5))
    df_chart =df.groupby("Country")["Profits"].sum().sort_values(ascending =False).head(4).plot(kind = "bar" ,fontsize=16)
    print("\n Top 4 Countries by Profits : \n ",df_chart )
    plt.title("Top 4 Countries by Profits",fontsize=18)
    
    plt.figure(figsize=(10, 5))
    df_chart2 =df.groupby("Type")["Profits"].sum().sort_values(ascending =False).head(5).plot(kind ="bar" ,fontsize=16)
    print("\n Top 5 Countries by Profits : \n ",df_chart2)
    plt.title("Top 5 Types by Profits",fontsize=18)
    
    plt.figure(figsize=(10, 5))
    df_chart3 =df.groupby("Gender")["Profits"].sum().sort_values(ascending =False).head(5).plot(kind="pie" , autopct ="%1.1f%%"  ,fontsize=16)
    print("\n Top 5 Genders : \n ",df_chart3)
    plt.title("Top 5 Genders",fontsize=18)
    plt.ylabel("")
    
    
    plt.figure(figsize=(10, 5))
    df_chart3 =df.groupby(["Year" ,"Day"])["Profits"].sum().sort_values(ascending =False).head(5).plot(kind="pie" , autopct ="%1.1f%%"  ,fontsize=16)
    print("\n  years of day by Profits : \n ",df_chart3)
    plt.title("years of day by Profits",fontsize=18)
    plt.ylabel("")
    
    plt.show()

  
    
    
    
    

if __name__ =='__main__'  :            
        main()     