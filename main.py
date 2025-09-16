import argparse

from pseudonymization.process.processor import Processor


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="Sequencing Pseudonymization",
                                     description="This script pseudonymized the data,"
                                                 " deletes unimportant data and sends them to SensitiveCloud")
    parser.add_argument("-s", "--source_folder", type=str, required=True)
    parser.add_argument("-d", "--destination_folder", type=str, required=True)
    parser.add_argument("-t", "--pseudo_tables_folder", type=str, required=True)
    parser.add_argument("-l", "--sequencing_libraries", type=str, required=True)
    parser.add_argument("-lsc", "--sequencing_libraries_sc", type=str, required=True)
    parser.add_argument("--log_dir", type=str, required=True)
    
    args = parser.parse_args()


    processor = Processor(
        args.source_folder,
        args.destination_folder,
        args.pseudo_tables_folder,
        args.sequencing_libraries,
        args.sequencing_libraries_sc,
        args.log_dir
    )

    processor.copy_libraries()
    processor.process_runs()
