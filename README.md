# CrisprCas_TA_RM
A Workflow that integrates the CRISPRCasFinder and library of toxin-antitoxins and Restriction-modification proteins we build to find CRISPR arrays, Cas proteins, toxin-antitoxins and Restriction-modification proteins.

## User Mannul
### Install
Before using, you need to install **Singularity**, a Docker like container software that does not require complex dependencies. 
```
apt-get update
apt-get install singularity
```
Decompress the compressed data file
```
cd TARM_Database
cat Bacteria_RM_v1_202206_out.faa.gz.* > Bacteria_RM_v1_202206_out.faa.gz
gunzip Bacteria_RM_v1_202206_out.faa.gz
gunzip Bacteria_TA_v1_202206_out.faa.gz
```

### Use
Enter the project folder
```
cd CRISPR_TA_RM
```
Use python3 to run start.py
Enter the project folder
Example:
```
python3 start.py -i test_file1.fasta -I test_file2.faa -o ./ -db TARM_Database/
```
