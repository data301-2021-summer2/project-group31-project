import pandas as pd
import numpy as np


def load_and_process(path):

        # Method Chain 1, load data and drop and replace columns

    df = (pd.read_csv(path,sep=',')
          .drop(['Job Description',"Easy Apply","Competitors","Industry","Sector","Revenue","Type of ownership","Headquarters","Founded"],axis='columns') 
          .rename(columns = {"Rating" : "Company Rating","Size":"Company Size"})
         )

        # Method Chain 2   
        # Replace unknown data in Company Rating and Size Column 

        # Decided to kept -1 as -1 because when ploting with "Unknown" the plot is not ordered also changing it to -1 to 0 wouldn't also work because there might be a company rating with 0
#     df1 = (pd.DataFrame(data=df)
#            .loc[lambda x: x["Company Rating"]==-1]
#            .replace(-1,"Unknown")
#           )
#     df.update(df1)

    df1 = (pd.DataFrame(data=df)
           .loc[lambda x: x["Company Size"]=="-1"]
           .replace("-1","Unknown")
          )
    df.update(df1)


        # Method Chain 3, Remove new line("\n") in Company name column
        # Remove (Glassdoor est.) in Salary Estimate column and create new Min and Max column

    df2 = (pd.DataFrame(data=df["Company Name"])
          .replace(r'\n.*', '', regex=True)
         )
    df.update(df2)

    df2 = (pd.DataFrame(data=df["Salary Estimate"])
          .replace(r'\(.*', '', regex=True)
          .replace('[\$]', '', regex=True)
         )    
    df.update(df2)

    new = df["Salary Estimate"].str.split("-", n = 1, expand = True)
    df["Minimum Salary"]= new[0]
    df["Maximum Salary"]= new[1]
    df.drop(columns =["Salary Estimate"],inplace = True)

    df2 = (pd.DataFrame(data=df["Minimum Salary"])
          .replace('K', '', regex=True)
          .astype(int)
         )
    df2=df2*1000
    df.update(df2)

    df2 = (pd.DataFrame(data=df["Maximum Salary"])
          .replace('K', '', regex=True)
          .astype(int)
         )
    df2=df2*1000
    df.update(df2)
    df["Average Salary"] = (df["Maximum Salary"]+df["Minimum Salary"])/2


        # Cut down data size to only include Data Engineer, Software Engineer, and Big Data Engineer job title

    DataEng_data = df.loc[df["Job Title"]== "Data Engineer"] #469 rows
    SoftEng_data = df.loc[df["Job Title"]== "Software Engineer"] #93 rows
    BigDataEng_data = df.loc[df["Job Title"]== "Big Data Engineer"] #73 rows
    frames = [DataEng_data,SoftEng_data,BigDataEng_data]
    df = pd.concat(frames)
    df = df.reset_index()


        # Caterogized company size column

    df["Company Size"].loc[df["Company Size"] == "1 to 50 employees"] = "Small"
    df["Company Size"].loc[df["Company Size"] == "51 to 200 employees"] = "Small"
    df["Company Size"].loc[df["Company Size"] == "201 to 500 employees"] = "Medium"
    df["Company Size"].loc[df["Company Size"] == "501 to 1000 employees"] = "Large"
    df["Company Size"].loc[df["Company Size"] == "1001 to 5000 employees"] = "Large"
    df["Company Size"].loc[df["Company Size"] == "5001 to 10000 employees"] = "Large"
    df["Company Size"].loc[df["Company Size"] == "10000+ employees"] = "Large"
    
    return df