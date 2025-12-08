# 16s_Microbiome-Map_pipeline
Sample: [SAMN15860556](https://www.ncbi.nlm.nih.gov/biosample/SAMN15860556/)

## Sample Background
SAMN15860556 contains paired-end V4 regions of 16S rRNA sequences from stool samples [1]. Sequencing was done using Illumina MiSeq with targeted-capture.

During targeted capture, certain genomic regions (e.g. V4) or genes are captured via hybridization to target-specific biotinylated probes. The probe-sequence hybrid is then pulled down and sequenced with next-generation sequencing (NGS)

![Capture of targeted sequences (image source: https://www.bioarrow.com/en/page/long-read-sequencing)](./assets/ngs-target-capture-hybridization.png "Capture of targeted sequences (image source: https://www.bioarrow.com/en/page/long-read-sequencing)")

The associated sequence run of this sample, [SRR12479080](https://trace.ncbi.nlm.nih.gov/Traces/?view=run_browser&acc=SRR12479080&display=metadata), displays a Phred QS distribution that is negatively-skewed 

![SRR12479080 Phred Quality Score Distribution](/assets/phred_qs_dist.png)

Recall that the Phred quality score measures the quality (and thereby confidence) of the reported nucleobase inferred from sequencing. It's calculated as 
$$
Q = -10 log_{10}P
$$

where P is the probability of base-call error. That is, a base whose Phred QS is 30 has a $10^-3$ chance of being incorrect. Phred scores are reported in FASTQ files as ASCII characters signifying scores in the range of [0, 40] (see [here](https://en.wikipedia.org/wiki/Phred_quality_score#Symbols) for a map of ASCII character to score and associated base-call error probability). A negatively-skewed Phred QS distribution then is promising as it suggests that the average sequence is of high-quality for a reasonable QS cutoff, e.g. 30.

## Tools

### QC



## References
1.  Wu Z, Byrd DA, Wan Y, et al. The oral microbiome and breast cancer and nonmalignant breast disease, and its relationship with the fecal microbiome in the Ghana Breast Health Study. Int J Cancer. 2022; 151(8): 1248-1260. doi:[10.1002/ijc.34145](https://doi.org/10.1002/ijc.34145)
