# coding: utf-8

import argparse
import sys
import os
import subprocess
import time

def creat_folder(path):
    if not os.path.exists(path):
        os.mkdir(path)

def crisprcas_commands(crisprcas_file, crisprcas_dir):

    com1 = ("""singularity exec -B $PWD CrisprCasFinder.simg perl /usr/local/CRISPRCasFinder/CRISPRCasFinder.pl -so /usr/local/CRISPRCasFinder/sel392v2.so -cf /usr/local/CRISPRCasFinder/CasFinder-2.0.3 -drpt /usr/local/CRISPRCasFinder/supplementary_files/repeatDirection.tsv -copyCSS /usr/local/CRISPRCasFinder/supplementary_files/crispr.css -html -rpts /usr/local/CRISPRCasFinder/supplementary_files/Repeat_List.csv -cpuM 4 -cas -def G -out %s -in %s""") % (crisprcas_dir, crisprcas_file)
    res = subprocess.Popen(com1, shell=True)
    res.wait()
    print('CRISPR/Cas detction complete！')

def ta_commands(tarm_file, ta_dir, tarm_database):
    print("Enter Toxin-AntiToxin proteins detection!")
    if "Bacteria_TADB_202206.phr" not in os.listdir(tarm_database):
        print("There is no index files for database, please wait for a while to complete the index process.")
        com3 =  ("""singularity exec -B $PWD CrisprCasFinder.simg makeblastdb -in %s -dbtype prot -out %s """)\
                % (tarm_database+"Bacteria_TA_v1_202206_out.faa", tarm_database+"Bacteria_TADB_202206")
        res = subprocess.Popen(com3, shell=True)
        res.wait()
        print('TADB index complete！')
    com2 = ("""singularity exec -B $PWD CrisprCasFinder.simg psiblast -word_size 3 -outfmt 6 -num_threads 4 -db %s -query %s -out %s""") % (tarm_database+"Bacteria_TADB_202206", tarm_file, ta_dir+"TA_results")
    res = subprocess.Popen(com2, shell=True)
    res.wait()
    print('Toxin-AntiToxin proteins detction complete！')

def rm_commands(tarm_file, ta_dir, tarm_database):
    print("Enter Restriction-Modification proteins detection!")
    if "Bacteria_RMDB_202206.phr" not in os.listdir(tarm_database):
        print("There is no index files for database, please wait for a while to complete the index process.")
        com5 =  ("""singularity exec -B $PWD CrisprCasFinder.simg makeblastdb -in %s -dbtype prot -out %s """)\
                % (tarm_database+"Bacteria_RM_v1_202206_out.faa", tarm_database+"Bacteria_RMDB_202206")
        res = subprocess.Popen(com5, shell=True)
        res.wait()
        print('RMDB index complete！')
    com4 = ("""singularity exec -B $PWD CrisprCasFinder.simg psiblast -word_size 3 -outfmt 6 -num_threads 4 -db %s -query %s -out %s""") % (tarm_database+"Bacteria_RMDB_202206", tarm_file, ta_dir+"RM_results")
    res = subprocess.Popen(com4, shell=True)
    res.wait()
    print('Restriction-Modification proteins detction complete！')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = """Auto detect CRISPR arrays and Cas proteins, blast to get Toxin-
                                                Antitoxin protein homolog and Restriction/Methylation protein homolog.
                                                type -help or -h for help""")
    #add subparsers crisprcas
    parser.add_argument('-i', '--input_crisprcas', type=str, help='Input file for CRISPR/Cas detection, genome file in fasta format is recommended.')
    parser.add_argument('-I', '--input_tarm', type=str,
                        help='Input file for TA/RM detection, protein sequences in fasta format is recommended.')
    parser.add_argument('-o', '--outdir', type=str, default="./", help='Output dir path. Default:\"./\"')
    parser.add_argument('-db', '--database', type=str, help='TA and RM database dir path. Example: \"./TARM_Database\"')

    group = parser.add_argument_group('Debug option', description='When you need to skip steps, you can use '
                                                                  'these options separately.')
    group.add_argument('--CC', type=str, default='True', choices=['True', 'False'], help='Only to find CRISPR arrays and Cas proteins. Default: True.')
    group.add_argument('--TA', type=str, default='True', choices=['True', 'False'], help='Only to find Toxin-AntiToxin proteins. Default: True.')
    group.add_argument('--RM', type=str, default='True', choices=['True', 'False'], help='Only to find Restriction/Methylation proteins. Default: True.')

    #set default func
    args = parser.parse_args()
    if len(sys.argv) == 1:
        parser.print_help(file=sys.stderr)
        sys.exit(1)

    outdir = os.path.abspath(args.outdir)

    if outdir == "./":
        outdir = outdir + 'Results' + time.strftime('%Y%m%d%H%M%S') + "/"
        comd = ("mkdir %s" % (outdir))
        res = subprocess.Popen(comd, shell=True)
        res.wait()
    else:
        if not str(outdir).endswith("/") :
            outdir = outdir + '/Results' + time.strftime('%Y%m%d%H%M%S') + "/"
            comd = ("mkdir %s" % (outdir))
            res = subprocess.Popen(comd, shell=True)
            res.wait()
        else:
            outdir = outdir + 'Results' + time.strftime('%Y%m%d%H%M%S') + "/"
            comd = ("mkdir %s" % (outdir))
            res = subprocess.Popen(comd, shell=True)
            res.wait()


    group = parser.parse_args()
    crisprcas_bool = group.CC
    ta_bool = group.TA
    rm_bool = group.RM

    tarm_database = args.database
    if not os.path.isdir(tarm_database):
        print("The TARM_Database ir path specified does not exist")
        sys.exit(2)
    if not (tarm_database.endswith("/")):
        tarm_database = tarm_database + '/'
    crisprcas_file = args.input_crisprcas
    tarm_file = args.input_tarm

    crisprcas_dir = os.path.abspath(outdir + "CRISPRCas_results")
    ta_dir = os.path.abspath(outdir)
    if not str(ta_dir).endswith("/"):
        ta_dir += "/"
    rm_dir = os.path.abspath(outdir)
    if not str(rm_dir).endswith("/"):
        rm_dir += "/"

    if crisprcas_bool == 'True':
        if crisprcas_file:
            crisprcas_comds = crisprcas_commands(crisprcas_file, crisprcas_dir)
        else:
            sys.exit("Please input input_crisprcas file. If you don't need CC detection, Please input \"--CC False\"")

    if ta_bool == 'True':
        if args.database:
            if args.tarm_file:
                ta_comds = ta_commands(tarm_file, ta_dir, tarm_database)
            else:
                sys.exit(
                    "Please input input_tarm file path. If you don't need TA detection, Please input \"--TA False\"")
        else:
            sys.exit("Please input TARM_Databse dir path. If you don't need TA detection, Please input \"--TA False\"")

    if rm_bool == 'True':
        if args.database:
            if args.tarm_file:
                rm_comds = rm_commands(tarm_file, ta_dir, tarm_database)
            else:
                sys.exit(
                    "Please input input_tarm file path. If you don't need RM detection, Please input \"--RM False\"")
        else:
            sys.exit("Please input TARM_Databse dir path. If you don't need RM detection, Please input \"--RM False\"")