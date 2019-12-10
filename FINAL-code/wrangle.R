afa_knn <- read.table(file = "/Users/okoro/Onedrive/Desktop/ml_predictdb/Paul_scripts/AFA_best_grid_knn_all_chrom.txt", header = T)
gencode <- read.table(file = "/Users/okoro/Onedrive/Desktop/ml_predictdb/Paul_scripts/gencode.v18.annotation.parsed.txt", header = T)

gencode <- subset(gencode, gene_type == c("protein_coding", "pseudogene", "lincRNA"))
#gencode <- subset(gencode, chr != c("X", "Y", "M"))

library(dplyr)

gencode$gene_id <- as.character(gencode$gene_id)

for (i in 1:length(gencode$gene_id)){
  gencode$gene_id[i] <- gsub('\\.[0-9]+','',gencode$gene_id[i])
} #just to remove the decimal places in the gene_id

#write.table(gencode, file = "/Users/okoro/Onedrive/Desktop/ml_predictdb/Paul_scripts/gencode.v18.annotation.parsed.txt", row.names = F, quote = F, sep = "\t")


afa_knn$Gene_ID <- as.character(afa_knn$Gene_ID)
for (i in 1:length(afa_knn$Gene_ID)){
  afa_knn$Gene_ID[i] <- gsub('\\.[0-9]+','',afa_knn$Gene_ID[i])
} #just to remove the decimal places in the gene_id
afa_knn <- subset(afa_knn, CV_R2 > 0.3)

write.table(afa_knn, file = "/Users/okoro/Onedrive/Desktop/ml_predictdb/Paul_scripts/AFA_best_grid_knn_all_chrom.txt", row.names = F, quote = F, sep = "\t")

afa_rf <- read.table(file = "/Users/okoro/Onedrive/Desktop/ml_predictdb/Paul_scripts/AFA_best_grid_rf_all_chrom.txt", header = T)
afa_rf$Gene_ID <- as.character(afa_rf$Gene_ID)
dup <- c('ENSG00000020633.14', 'ENSG00000162390.13', 'ENSG00000121940.11', 'ENSG00000118217.5', 'ENSG00000123684.8', 'ENSG00000030110.8', 'ENSG00000111640.10', 'ENSG00000064763.5', 'ENSG00000139637.9', 'ENSG00000139318.7', 'ENSG00000111361.8', 'ENSG00000198718.8', 'ENSG00000178974.5', 'ENSG00000100601.5', 'ENSG00000140740.6', 'ENSG00000102974.10', 'ENSG00000103168.12', 'ENSG00000129245.7', 'ENSG00000108306.7', 'ENSG00000178307.5', 'ENSG00000070540.8', 'ENSG00000141552.13', 'ENSG00000104980.3', 'ENSG00000099330.4', 'ENSG00000105656.7', 'ENSG00000167380.12', 'ENSG00000160439.10', 'ENSG00000089050.10', 'ENSG00000125843.6', 'ENSG00000078804.8', 'ENSG00000172315.5', 'ENSG00000130699.11', 'ENSG00000128322.6', 'ENSG00000099977.9', 'ENSG00000128335.9', 'ENSG00000196576.10', 'ENSG00000100316.11')

for (i in 1:length(dup)){
  dup[i] <- gsub('\\.[0-9]+','',dup[i])
} #just to remove the decimal places in the gene_id

afa_rf <- subset(afa_rf, Gene_ID == dup)

for (i in 1:length(afa_rf$Gene_ID)){
  afa_rf$Gene_ID[i] <- gsub('\\.[0-9]+','',afa_rf$Gene_ID[i])
} #just to remove the decimal places in the gene_id
afa_rf <- subset(afa_rf, CV_R2 > 0.6)



write.table(afa_rf, file = "/Users/okoro/Onedrive/Desktop/ml_predictdb/Paul_scripts/AFA_best_grid_rf_all_chrom.txt", row.names = F, quote = F, sep = "\t")


afa_svr <- read.table(file = "/Users/okoro/Onedrive/Desktop/ml_predictdb/Paul_scripts/AFA_best_grid_svr_all_chrom.txt", header = T)
afa_svr$Gene_ID <- as.character(afa_svr$Gene_ID)
for (i in 1:length(afa_svr$Gene_ID)){
  afa_svr$Gene_ID[i] <- gsub('\\.[0-9]+','',afa_svr$Gene_ID[i])
} #just to remove the decimal places in the gene_id
afa_svr <- subset(afa_svr, CV_R2 > 0.5)
write.table(afa_svr, file = "/Users/okoro/Onedrive/Desktop/ml_predictdb/Paul_scripts/AFA_best_grid_svr_all_chrom.txt", row.names = F, quote = F, sep = "\t")



#CAU
cau_knn <- read.table(file = "/Users/okoro/Onedrive/Desktop/ml_predictdb/Paul_scripts/CAU_best_grid_knn_all_chrom.txt", header = T)
cau_knn$Gene_ID <- as.character(cau_knn$Gene_ID)
for (i in 1:length(cau_knn$Gene_ID)){
  cau_knn$Gene_ID[i] <- gsub('\\.[0-9]+','',cau_knn$Gene_ID[i])
} #just to remove the decimal places in the gene_id
cau_knn <- subset(cau_knn, CV_R2 > 0.5)
write.table(cau_knn, file = "/Users/okoro/Onedrive/Desktop/ml_predictdb/Paul_scripts/CAU_best_grid_knn_all_chrom.txt", row.names = F, quote = F, sep = "\t")


cau_rf <- read.table(file = "/Users/okoro/Onedrive/Desktop/ml_predictdb/Paul_scripts/CAU_best_grid_rf_all_chrom.txt", header = T)
cau_rf$Gene_ID <- as.character(cau_rf$Gene_ID)
for (i in 1:length(cau_rf$Gene_ID)){
  cau_rf$Gene_ID[i] <- gsub('\\.[0-9]+','',cau_rf$Gene_ID[i])
} #just to remove the decimal places in the gene_id
cau_rf <- subset(cau_rf, CV_R2 > 0.70)
write.table(cau_rf, file = "/Users/okoro/Onedrive/Desktop/ml_predictdb/Paul_scripts/CAU_best_grid_rf_all_chrom.txt", row.names = F, quote = F, sep = "\t")


cau_svr <- read.table(file = "/Users/okoro/Onedrive/Desktop/ml_predictdb/Paul_scripts/CAU_best_grid_svr_all_chrom.txt", header = T)
cau_svr$Gene_ID <- as.character(cau_svr$Gene_ID)
for (i in 1:length(cau_svr$Gene_ID)){
  cau_svr$Gene_ID[i] <- gsub('\\.[0-9]+','',cau_svr$Gene_ID[i])
} #just to remove the decimal places in the gene_id
cau_svr <- subset(cau_svr, CV_R2 > 0.70)
write.table(cau_svr, file = "/Users/okoro/Onedrive/Desktop/ml_predictdb/Paul_scripts/CAU_best_grid_svr_all_chrom.txt", row.names = F, quote = F, sep = "\t")



#HIS
his_knn <- read.table(file = "/Users/okoro/Onedrive/Desktop/ml_predictdb/Paul_scripts/HIS_best_grid_knn_all_chrom.txt", header = T)
his_knn$Gene_ID <- as.character(his_knn$Gene_ID)
for (i in 1:length(his_knn$Gene_ID)){
  his_knn$Gene_ID[i] <- gsub('\\.[0-9]+','',his_knn$Gene_ID[i])
} #just to remove the decimal places in the gene_id
his_knn <- subset(his_knn, CV_R2 > 0.5)
write.table(his_knn, file = "/Users/okoro/Onedrive/Desktop/ml_predictdb/Paul_scripts/HIS_best_grid_knn_all_chrom.txt", row.names = F, quote = F, sep = "\t")



his_rf <- read.table(file = "/Users/okoro/Onedrive/Desktop/ml_predictdb/Paul_scripts/HIS_best_grid_rf_all_chrom.txt", header = T)
his_rf$Gene_ID <- as.character(his_rf$Gene_ID)
for (i in 1:length(his_rf$Gene_ID)){
  his_rf$Gene_ID[i] <- gsub('\\.[0-9]+','',his_rf$Gene_ID[i])
} #just to remove the decimal places in the gene_id
his_rf <- subset(his_rf, CV_R2 > 0.72)
write.table(his_rf, file = "/Users/okoro/Onedrive/Desktop/ml_predictdb/Paul_scripts/HIS_best_grid_rf_all_chrom.txt", row.names = F, quote = F, sep = "\t")



his_svr <- read.table(file = "/Users/okoro/Onedrive/Desktop/ml_predictdb/Paul_scripts/HIS_best_grid_svr_all_chrom.txt", header = T)
his_svr$Gene_ID <- as.character(his_svr$Gene_ID)
for (i in 1:length(his_svr$Gene_ID)){
  his_svr$Gene_ID[i] <- gsub('\\.[0-9]+','',his_svr$Gene_ID[i])
} #just to remove the decimal places in the gene_id
his_svr <- subset(his_svr, CV_R2 > 0.72)
write.table(his_svr, file = "/Users/okoro/Onedrive/Desktop/ml_predictdb/Paul_scripts/HIS_best_grid_svr_all_chrom.txt", row.names = F, quote = F, sep = "\t")


unik <- as.data.frame(unique(his_svr$Gene_ID))
