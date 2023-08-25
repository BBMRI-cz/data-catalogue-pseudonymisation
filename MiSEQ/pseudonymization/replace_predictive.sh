echo "Replacing predictive numbers in files"
jq -r '.[] | .[] | .predictive_number + " " + .pseudo_number' $1 | while read -r pred_num pseudo_num; do
    grep -rlw "$2/InterOp/IndexMetricsOut.bin" -e $pred_num | xargs -i@ sed -i "s/$pred_num/$pseudo_num/g" @
    grep -rlw "$2/Data/Intensities/BaseCalls/Alignment/AdapterCounts.txt" -e $pred_num | xargs -i@ sed -i "s/$pred_num/$pseudo_num/g" @
    grep -rlw "$2/Data/Intensities/BaseCalls/Alignment/DemultiplexSummaryF1L1.txt" -e $pred_num | xargs -i@ sed -i "s/$pred_num/$pseudo_num/g" @
    grep -rlw "$2/GenerateFASTQRunStatistics.xml" -e $pred_num | xargs -i@ sed -i "s/$pred_num/$pseudo_num/g" @
    grep -rlw "$2/Analysis/${pseudo_num}_Output/${pseudo_num}/" -e $pred_num | xargs -i@ sed -i "s/$pred_num/$pseudo_num/g" @
    grep -rlw "$2/Analysis/BAM/${pseudo_num}.bam" -e $pred_num | xargs -i@ sed -i "s/$pred_num/$pseudo_num/g" @
done
echo "Replacement done"