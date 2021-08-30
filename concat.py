import pandas as pd
import numpy as np
import os

# The input directory
directory = "../out/"

final_df = pd.DataFrame()

total_files = len(os.listdir(directory))
count = 1
for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        print("File {} of {}".format(count, total_files))
        count +=1


        joint = os.path.join(directory, filename)
        
        temp_df = pd.read_csv(joint)


        gene_name = filename.split("_")[0]
        temp_df = temp_df.reset_index()
        temp_df["sample"] = gene_name

        
        
        #temp_df = temp_df.rename(columns={"TPM":gene_name})
        # temp_df = temp_df.dropna(subset=["transcript_id"])
        # temp_df = temp_df.set_index("transcript_id")
        # temp_df = temp_df[[gene_name]]
        
        final_df = pd.concat([final_df, temp_df], axis=0)
               
    else:
        continue


# final_df = final_df.dropna(axis=0, how='all')
# final_df = final_df.fillna(value=0)


print(final_df.head())
print(final_df.tail())



final_df.to_csv("final.csv")

## We shouldn't need this cause there are no duplicates
pt = final_df.pivot_table(index="ref_gene_id", columns="sample", values="TPM", aggfunc=np.mean)


#pt = final_df.pivot(index=["ref_gene_id"], columns=["sample"], values="TPM")

pt.to_csv("pivot_table.csv")