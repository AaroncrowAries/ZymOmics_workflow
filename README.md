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
cd CRISPR_TA_RM
cat CrisprCasFinder.simg.gz.* > CrisprCasFinder.simg.gz
gunzip CrisprCasFinder.simg.gz
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

For the skilled, you can use CRISPRCasFinder and psiblastp directly for more personalized operations.
CRISPRCasFinder is under the CrisprCasFinder /usr/local/CRISPRCasFinder directory. Blast is already in the system environment.
```
singularity exec -B $PWD CrisprCasFinder.simg perl /usr/local/CRISPRCasFinder/CRISPRCasFinder.pl -so /usr/local/CRISPRCasFinder/sel392v2.so -cf /usr/local/CRISPRCasFinder/CasFinder-2.0.3 -drpt /usr/local/CRISPRCasFinder/supplementary_files/repeatDirection.tsv -rpts /usr/local/CRISPRCasFinder/supplementary_files/Repeat_List.csv -cas -def G -out RES21092020_2 -in sequence.fasta

singularity exec -B $PWD CrisprCasFinder.simg psiblastp -h
```
