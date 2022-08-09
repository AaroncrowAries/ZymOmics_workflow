configfile: "single.yaml"

rule all:
    input:
        expand("count/{sample}.count",sample=config["samples"]),

def get_input_fastqs(wildcards):
    return config["samples"][wildcards.sample]
rule fastp_trim:
    input:
        get_input_fastqs
    output:
        trimmed = "trim/{sample}_trimmed.fq.gz",
        html = "trim/{sample}.html",
        json = "trim/{sample}.json"
    log:
        "log/fastp_{sample}.log"
    threads: 4
    shell:
        "fastp --compression=6 --thread={threads} -R {wildcards.sample}_report --html {output.html} --json {output.json} -i {input} -o {output.trimmed}"

rule bwa_index:
    input:
        INDEX = config["reference"]["bwaRef"]
    output:
        expand("{INDEX}.{IDX}",IDX=["amb", "ann", "bwt", "pac", "sa"],INDEX = config["reference"]["bwaRef"])
    threads: 1
    shell:
        "bwa index {input}"

rule bwa_map:
    input:
        FILE = rules.fastp_trim.output.trimmed,
        INDEX= config["reference"]["bwaRef"],
        asd = expand("{INDEX}.{IDX}",IDX=["amb", "ann", "bwt", "pac", "sa"],INDEX = config["reference"]["bwaRef"])
    output:
        temp("bwa/{sample}.sam")
    log:
        "log/bwamap_{sample}.log"
    threads: 4
    shell:
        "bwa mem -t {threads} {input.INDEX}  {input.FILE} > {output}"

rule sam2bam:
    input:
        "bwa/{sample}.sam"
    output:
        "bam/{sample}.bam"
    log:
        "log/sam2bam_{sample}.log"
    threads: 4
    shell:
        "samtools view -@ {threads} -Sb {input} > {output}"

rule featurecounts_count:
    input:
        sample="bam/{sample}.bam"
    output:
        "count/{sample}.count"
    params:
        FEATURE=config["feature"]["features"],
        GTF=config["annotation"]["gtf"]
    log:
        "log/count_{sample}.log"
    threads: 4
    shell:
        "featureCounts -T {threads} -O -t {params.FEATURE}  -a {params.GTF} -o {output} {input.sample}"