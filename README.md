# 16s_Microbiome-Map_pipeline
Sample: [SAMN15860556](https://www.ncbi.nlm.nih.gov/biosample/SAMN15860556/)

## Sample Background
SAMN15860556 contains **paired-end V4 regions of 16S rRNA** sequences from stool samples [1]. Sequencing was done using Illumina MiSeq with targeted-capture.

During targeted capture, certain genomic regions (e.g. V4) or genes are captured via hybridization to target-specific biotinylated probes. The probe-sequence hybrid is then pulled down and sequenced with next-generation sequencing (NGS)

![Capture of targeted sequences (image source: https://www.bioarrow.com/en/page/long-read-sequencing)](./assets/ngs-target-capture-hybridization_50.png "Capture of targeted sequences (image source: https://www.bioarrow.com/en/page/long-read-sequencing)")

The associated sequence run of this sample, [SRR12479080](https://trace.ncbi.nlm.nih.gov/Traces/?view=run_browser&acc=SRR12479080&display=metadata), displays a Phred QS distribution that is negatively-skewed 

![SRR12479080 Phred Quality Score Distribution](/assets/phred_qs_dist.png)

Recall that the Phred quality score measures the quality (and thereby confidence) of the reported nucleobase inferred from sequencing. It's calculated as $Q = -10 log_{10}P$ where $P$ is the probability of base-call error. That is, a base whose Phred QS is 30 has a $10^{-3}$ chance of being incorrect. Phred scores are reported in FASTQ files as ASCII characters signifying scores in the range of [0, 40] (see [here](https://en.wikipedia.org/wiki/Phred_quality_score#Symbols) for a map of ASCII character to score and associated base-call error probability). A negatively-skewed Phred QS distribution then is promising as it suggests that the average sequence is of high-quality for a reasonable QS cutoff, e.g. 30.

## Tools
For each tool, follow your OS's installation instructions:
1. Data fetching: [SRA toolkit](https://github.com/ncbi/sra-tools/wiki/01.-Downloading-SRA-Toolkit)
2. Preprocessing: FLASh, Cutadapt, FASTQC, MultiQC, Trimmomatic
3. Identification of V4/clustering into OTUs: USEARCH alignment vs MAFFT vs DADA2
4. OTU Counting: USEARCH
5. Taxonomic Profiling: RDP classifier vs `phyloseq` vs SILVA vs Greengenes


## Workflow
### Repo structure
```
- /
|_ assets/
|_ raw_data/
|_ qc_reports/
|_ processed_data
|_ results/
|_ scripts/
|_ metadata/
```

where:
- `assets` contains images for README.md
- `raw_data` contains all FASTQ files
- `qc_reports` contains quality data of raw sequences
- `processed_data` contains FASTQ files after QC trimming, and filtering
- `results` contains feature tables, clusters, taxonomy, etc.
- `scripts` contains analysis scripts
- `metadata` contains samples' metadata

### Getting the Data
Using SRA Toolkit's fasterq-dump, fetch SRR12479080 with
```bash
cd raw_data && mkdir SRR12479080 && fasterq-dump SRR12479080
```

`fasterq-dump` automatically splits paired-end FASTQ files into 2 read files labelled `[ID]_1.fastq` and `[ID]_2.fastq` for forward and reverse, respectively. Each entry in the file is organized as 
```
@[sequence identifier] [ID] [length]
[raw sequence nucloetides]
+[sequence identifier] [ID] [length]
[ASCII quality score for each NT in the raw sequence]
```
e.g.
```
@SRR12479080.36137 36137 length=150
CCTGTTTGCTACCCACACTTTCGAGCCTCAGCGTCAGTTGGTGCCCAGTAGGCCGCCTTCGCCACTGGTGTTCCTCCCGATATCTACGCATTCCACCGCTACACCGGGAATTCCGCCTACCTCTGCACTACTCAAGAAAAACAGTTTTGA
+SRR12479080.36137 36137 length=150
AAAAAF@CFFFFGGGGGGFGFEEAGGGH4F3BE2EE2FGFCEFHGCEABF5FD3A0EAAGGEFEEFC2BBGGG4FHFGE?EEEGHGFGEEFEHHGHCEEFEEFGC/>///BFDFC/AA/FGBFHFF<C1<FGHFFDDGFHHG.0F1F1<.
```
If `fasterq-dump` can't find the paired read for a sequence, it will output that in a separate file. We'll ignore such reads from this analysis for now.

### QC
#### Contig Assembly
The first step is to assemble contigs from the raw reads to reconstruct the 16S rRNA gene. We do this because:
1. each read is 150 bp in length but the V4 region of 16S rRNA is 250-255bp long
2. our data is paired-end suggesting that there is ~95-100bp overlap between the 2 reads. 

To build contigs we can use [FLASh](https://ccb.jhu.edu/software/FLASH/) [2]
```bash
cd SRR12479080
flash SRR12479080_1.fastq SRR12479080_2.fastq
```
with default paramters. The output of FLASh is as follows:
- `out.extendedFrags.fastq`: merged reads
- `out.notCombined_1.fastq`: read 1 of mate pairs that were not merged.
- `out.notCombined_2.fastq`: read 2 of mate pairs that were not merged.
- `out.hist`: numeric histogram of merged read lengths
- `out.histogram`: visual representation of the numeric hisogram of merged read lengths.

It's a good spot to pause here and inspect how many of each read failed to assemble into contigs. For example, the `SRR12479080` data had 1,115 forward and reverse reads that failed to assembly

```bash
# get sequence identifiers from each not combined set
perl -lne '@f = /^@(\S+)\s+/ and print join "\t", @f;' out.notCombined_1.fastq > ids_gene_ids_1.tsv

perl -lne '@f = /^@(\S+)\s+/ and print join "\t", @f;' out.notCombined_2.fastq > ids_gene_ids_2.tsv

# check if they correspond to the same pairs
cmp --silent ids_gene_ids_1.tsv ids_gene_ids_2.tsv||echo "There are different identifiers"
```

Since identifiers are identical here, we can try relaxing the default arguments of `flash` if their inspected alignments seem to have a good similarity or identity scores. Candidate options:
- `-O, --allow-outies`: combine read pairs in the "outie" orientation

If the similarity/identity scores aren't good and we have enough contigs assembled, we can also discard them. In the case of `SRR12479080`, there are 35,021 assembled contigs. The failed-to-assemble group is ~3.2% of the pairs.

#### Filtering and Trimming

#### Dereplication

### Alignment

#### QC 
1. remove non-V4 overlapping regions
2. pre-clustering
3. remove chimera

### Taxonomic Profiling

#### QC 
remove contaminants, e.g. 18S rRNA, mitochondrial/chloroplast/Archaeal 16S rRNA, etc.

### Clutsering and Counting OTUs

### Diversity & Statistical Analysis

## References
1.  Wu Z, Byrd DA, Wan Y, et al. The oral microbiome and breast cancer and nonmalignant breast disease, and its relationship with the fecal microbiome in the Ghana Breast Health Study. Int J Cancer. 2022; 151(8): 1248-1260. doi:[10.1002/ijc.34145](https://doi.org/10.1002/ijc.34145)
2. Tanja Magoč, Steven L. Salzberg, FLASH: fast length adjustment of short reads to improve genome assemblies, Bioinformatics, Volume 27, Issue 21, November 2011, Pages 2957–2963, [https://doi.org/10.1093/bioinformatics/btr507](https://doi.org/10.1093/bioinformatics/btr507)
