#!/bin/sh

echo "Replacing predictive numbers in files"

pred_num=$2
pseudo_num=$3

grep -rlw "$1/InterOp/IndexMetricsOut.bin" -e $pred_num | xargs -i@ sed -i "s/$pred_num/$pseudo_num/g" @
grep -rlw "$1/Data/Intensities/BaseCalls/Alignment/AdapterCounts.txt" -e $pred_num | xargs -i@ sed -i "s/$pred_num/$pseudo_num/g" @
grep -rlw "$1/Data/Intensities/BaseCalls/Alignment/DemultiplexSummaryF1L1.txt" -e $pred_num | xargs -i@ sed -i "s/$pred_num/$pseudo_num/g" @
grep -rlw "$1/GenerateFASTQRunStatistics.xml" -e $pred_num | xargs -i@ sed -i "s/$pred_num/$pseudo_num/g" @
grep -rlw "$1/Analysis/${pseudo_num}_Output/${pseudo_num}/" -e $pred_num | xargs -i@ sed -i "s/$pred_num/$pseudo_num/g" @
grep -rlw "$1/Analysis/BAM/${pseudo_num}.bam" -e $pred_num | xargs -i@ sed -i "s/$pred_num/$pseudo_num/g" @
echo "Replacement done"