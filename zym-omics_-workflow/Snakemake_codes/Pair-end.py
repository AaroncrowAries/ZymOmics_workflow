configfile: "paired.yaml"

rule all:
    input:
        expand("count/Result.count",sample=config["samples"])

rule fastp_trim:
    input:
        fq_1 = config["samples"]["paired_fq_1"],
        fq_2 = config["samples"]["paired_fq_2"]
    output:
        trimmed_1 = "trim/trimmed_R1.fq.gz",
        trimmed_2 = "trim/trimmed_R2.fq.gz",
        html = "trim/fastp.html",
        json = "trim/fastp.json"
    log:
        "log/fastp.log"
    threads: 4
    shell:
        "fastp --compression=6 --thread={threads} -R Trim_report --html {output.html} --json {output.json} -i {input.fq_1} -I {input.fq_2} -o {output.trimmed_1} -O {output.trimmed_2}"

rule subread_buildindex:
    input:
        INDEX = config["reference"]["bwaRef"]
    output:
        index_files = expand("ind.{IDX}",IDX=["00.b.array", "00.b.tab", "files", "log", "reads"])
    threads: 1
    shell:
        "subread-buildindex -o ind {input}"

rule subread_map:
    input:
        trim_1 = rules.fastp_trim.output.trimmed_1,
        trim_2 = rules.fastp_trim.output.trimmed_2,
        INDEX= config["reference"]["bwaRef"]
    output:
        temp("map/mapped.sam")
    log:
        "log/bwamap.log"
    threads: 4
    shell:
        "subjunc -T {threads} -i ind -r {input.trim_1} -R {input.trim_2} -o {output}"

rule sam2bam:
    input:
        "map/mapped.sam"
    output:
        "bam/mapped.bam"
    log:
        "log/sam2bam.log"
    threads: 4
    shell:
        "samtools view -@ {threads} -Sb {input} > {output}"

rule featurecounts_count:
    input:
        sample="bam/mapped.bam"
    output:
        "count/Result.count"
    params:
        FEATURE=config["feature"]["features"],
        GTF=config["annotation"]["gtf"]
    log:
        "log/count.log"
    threads: 4
    shell:
        "featureCounts -T {threads} -O -t {params.FEATURE}  -a {params.GTF} -o {output} {input.sample}"