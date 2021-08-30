import pandas as pd
import os


directory = "data/"

def convert_to_list(x):
    #outdf = pd.DataFrame(columns= ["gene_id", "transcript_id","exon_number", "reference_id","ref_gene_id","cov", "FPKM", "TPM" ])
    
    tmp_dict = dict()

    split_key_val_pairs = x.split(";")

    split_key_val_pairs = [x.strip(" ") for x in split_key_val_pairs]

    for key_val_pair in split_key_val_pairs:

        key_val_arr = key_val_pair.split(" ")
        if(len(key_val_arr) >1):
            clean_key = key_val_arr[0].strip()
            clean_val = key_val_arr[1].strip('"').strip()
            tmp_dict[clean_key] = clean_val

    #outdf.append(tmp_dict, ignore_index=True)
    return pd.Series(tmp_dict)

for filename in os.listdir(directory):
    if filename.endswith(".tsv"):


        df = pd.read_csv(os.path.join(directory, filename),
        sep="\t", 
        skiprows=4, 
        header=0, 
        names=["seqname", "source", "feature",  "start",   "end",     "score",   "strand",  "frame", "attributes"])

        df = df.loc[df["feature"] == "transcript"]

        out =  pd.concat([df.drop(["attributes", "seqname", "source", "start", "end", "strand", "frame"], axis=1), df["attributes"].apply(convert_to_list)], axis=1)

        out = out[["TPM", "ref_gene_id"]]
        out_filename = filename.split(".")[0] + "_cleaned.csv"

        out.to_csv(os.path.join("out/", out_filename))