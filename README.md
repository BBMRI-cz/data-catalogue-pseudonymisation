# data-catalogue-pseudonymisation
This is the repository for the pseudonymisation part of the BBMRI.cz data catalog

## Pseudonymisation

### MiSEQ
Pseudonymizes predictive numbers before moving the data to SensitiveCloud at ICS-MUNI

Pseudonymisation itself consists of multiple Python and Bash scripts, the whole pipeline is defined within **pseudonymize_pipeline.sh**:
  1. it sets paths to important folders and files,
  2. it ensures data (HIS exports) transfer from remote server,
  3. it looks for exports having "predictive number" value,
  4. it indentify and remove duplicates
  5. then it iterates through sequencing data folder (consisting of sequencing run output + following analysis output files) and runs scripts:
        - **remove_files.sh** - removes defined unnecessary files,
        - **pseudonymisation.py** - performs pseudonymisation creating class *Pseudonymizer* and using function ***pseudonymize_run()*** consisting of:
          >   - ***pseudo_sample_sheet_and_get_clinical_data()*** - which performs pseudonymisation of "Sample Sheet" file carrying IDs of sequenced samples and collects clinical data using class *FindClinicalInfo* defined within **clinical_finder.py** consisting of:
          >>   - definition of the class *Material* (with properties pseudo_ID, biopsy_number, sample_ID, sample_number, available_samples_number, material_type) and function ***_generate_pseudo_sample_id()*** - which generates pseudo sample ID for selected predictive number in case it does not exist, otherwise it returns existing pseudo sample ID with subclasses:
          >>     - Tissue (with properties material, pTNM, morphology, diagnosis, cut_time, freeze_time)
          >>     - Serum (with properties material, diagnosis, taking_date)
          >>     - Genome (with properties material, taking_date)
          >>   - definition of class *Patient* (with properties ID, birth, sex, samples)
          >>   - definition of class *FindClinicalInfo* (with properties export_path, predictive_numbers, pseudo_pred_table_path, pseudo_patient_table_path, pseudo_sample_table_path, run_path) and functions:
          >>>   - ***_collect_clinical_data()***
          >>>    - ***_add_pseudo_ID()***
          >>>    - ***_check_for_predictive_number_in_export()***
          >>>      - ***_fix_predictive_number()***
          >>>      - ***_generate_pseudo_patient_id()***
          >>>    - ***_combine_patients_with_same_id()***
          >>>    - ***_remove_duplicates_from_list_and_sort_samples()***
          >>>  - ***_convert_collection_to_dict()***
          >>>    - ***_convert_samples_to_dict()***
          >>>  - ***_get_samples_with_unique_predictive_number()***
          >>>  - ***_convert_samples_to_dict***
          >   - ***create_temporary_pseudo_table()*** - temporarily stores predictiveID:pseudoID tuples of a current run in JSON format
          >   - ***locate_all_files_with_predictive_number()*** - locates all files in a run that contain a predictive number in the name and thanks to function ***rename_files_recursively()*** replaces it with pseudonymized predictive number
        - **replace_predictive.sh** - replaces each predictive number appearance in sequencing data folder with created pseudo ID in previous step
