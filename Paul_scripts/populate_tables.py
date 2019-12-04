#Dynamically populate the tables

import mysql.connector
from mysql.connector import Error


conn = mysql.connector.connect(host='localhost',
                                       database='genome_db',
                                       user='paul',
                                       password='***')#put your user and password


if conn.is_connected():
            print("Connected to Genome Database")

cursor = conn.cursor()


def insert_algorithm (_id, desc):
    query = "INSERT INTO algorithm(algorithm_id, algorithm_description) " \
            "VALUES(%s,%s)"
    args = (_id, desc)
    cursor.execute(query, args)

def insert_population (_id, desc):
    query = "INSERT INTO population(population_id, population_description) " \
            "VALUES(%s,%s)"
    args = (_id, desc)
    cursor.execute(query, args)

alg_dict = {"RF":"Random Forest", "SVR":"Support Vector Regression", "KNN":
            "K Nearest Neighbour"}

pop_dict = {"AFA":"African American", "CAU":"European American", "HIS":
            "Hispanic American"}

for keys, values in alg_dict.items():
	insert_algorithm(keys,values)
	print(keys, values)

print()

for keys, values in pop_dict.items():
	insert_population(keys,values)
	print(keys, values)

import pandas as pd
#gene annotation
geneanotfile = "/Users/okoro/OneDrive/Desktop/ml_predictdb/Paul_scripts/gencode.v18.annotation.parsed.txt"
anot = pd.read_csv(geneanotfile, sep = "\t")

anot_head = ["chr", "gene_id", "gene_name", "gene_type"]
anot = anot[anot_head]


def insert_gene (gene_id, gene_name, gene_type, gene_chr):
    query = "INSERT INTO gene(gene_id, gene_name, gene_type, chromosome_no) " \
            "VALUES(%s,%s,%s,%s)"
    args = (gene_id, gene_name, gene_type, gene_chr)
    cursor.execute(query, args)

for i in range(len(anot)):
	gene_id = anot.iloc[i,1]
	gene_name = anot.iloc[i,2]
	gene_type = anot.iloc[i,3]
	gene_chr = anot.iloc[i,0]
	insert_gene (gene_id, gene_name, gene_type, gene_chr)
	print(gene_id, gene_name, gene_type, gene_chr)


pops = ["AFA", "CAU", "HIS"]

#gene models
#KNN
def insert_knn (gene_id, pop_id, cross_val, neighbors, weight, p):
        query = "INSERT INTO knn_model(gene_id, population_id, cross_val_performance, neighbors, weight, p) " \
                "VALUES(%s,%s,%s,%s,%s,%s)"
        args = (gene_id, pop_id, cross_val, neighbors, weight, p)
        cursor.execute(query, args)


for pop in pops:
    knn_file = "/Users/okoro/OneDrive/Desktop/ml_predictdb/Paul_scripts/"+pop+"_best_grid_knn_all_chrom.txt"
    #knn_model = pd.read_csv(knn_file, sep = "\t")
    knn_head = ["Gene_ID", "CV_R2", "n_neigbors", "weights", "p"]
    #knn_model = afa_knn[knn_head]


    col_names = pd.read_csv(knn_file, nrows=0).columns
    types_dict = {"Gene_ID":str, "CV_R2":str, "n_neigbors":str, "weights":str, "p":str}
    types_dict.update({col: str for col in col_names if col not in types_dict})
    knn_model = pd.read_csv(knn_file, dtype=types_dict, sep="\t")
    knn_model = knn_model[knn_head]

    for i in range(4):
            gene_id = knn_model.iloc[i,0]
            pop_id = pop
            cross_val = (knn_model.iloc[i,1])
            neighbors = (knn_model.iloc[i,2])
            weight = knn_model.iloc[i,3]
            p = (knn_model.iloc[i,4])
            insert_knn (gene_id, pop_id, cross_val, neighbors, weight, p)
            print(gene_id, pop_id, cross_val, neighbors, weight, p)



#RF
#pop="AFA"
def insert_rf (gene_id, pop_id, cross_val, trees):
    query = "INSERT INTO rf_model(gene_id, population_id, cross_val_performance, trees) " \
            "VALUES(%s,%s,%s,%s)"
    args = (gene_id, pop_id, cross_val, trees)
    cursor.execute(query, args)

for pop in pops:
    
    rf_file = "/Users/okoro/OneDrive/Desktop/ml_predictdb/Paul_scripts/"+pop+"_best_grid_rf_all_chrom.txt"
    rf_head = ["Gene_ID", "CV_R2", "n_estimators"]

    col_names = pd.read_csv(rf_file, nrows=0).columns
    types_dict = {"Gene_ID":str, "CV_R2":str, "n_estimators":str}
    types_dict.update({col: str for col in col_names if col not in types_dict})
    rf_model = pd.read_csv(rf_file, dtype=types_dict, sep="\t")
    rf_model = rf_model[rf_head]

    for i in range(4):
        gene_id = rf_model.iloc[i,0]
        pop_id = pop
        cross_val = rf_model.iloc[i,1]
        trees = rf_model.iloc[i,2]
        insert_rf(gene_id, pop_id, cross_val, trees)
        print(gene_id, pop_id, cross_val, trees)


#SVR

#pop="AFA"
def insert_svr (gene_id, pop_id, cross_val, kernel, degree, c):
    query = "INSERT INTO svr_model(gene_id, population_id, cross_val_performance, kernel, degree, c) " \
            "VALUES(%s,%s,%s,%s,%s,%s)"
    args = (gene_id, pop_id, cross_val, kernel, degree, c)
    cursor.execute(query, args)

for pop in pops:
    
    svr_file = "/Users/okoro/OneDrive/Desktop/ml_predictdb/Paul_scripts/"+pop+"_best_grid_svr_all_chrom.txt"
    svr_head = ["Gene_ID", "CV_R2", "kernel", "degree", "C"]

    col_names = pd.read_csv(svr_file, nrows=0).columns
    #this is to force pandas to give the columns this specified data type in the dict below
    types_dict = {"Gene_ID":str, "CV_R2":str, "kernel":str, "degree":str, "C":str}
    types_dict.update({col: str for col in col_names if col not in types_dict})
    svr_model = pd.read_csv(svr_file, dtype=types_dict, sep="\t")
    svr_model = svr_model[svr_head]

    for i in range(4):
        gene_id = svr_model.iloc[i,0]
        pop_id = pop
        cross_val = svr_model.iloc[i,1]
        kernel = svr_model.iloc[i,2]
        degree = svr_model.iloc[i,3]
        c = svr_model.iloc[i,4]
        insert_svr(gene_id, pop_id, cross_val, kernel, degree, c)
        print(gene_id, pop_id, cross_val, kernel, degree, c)

conn.commit() #you can cmment it out just so that it won't run and populate database
conn.close()
