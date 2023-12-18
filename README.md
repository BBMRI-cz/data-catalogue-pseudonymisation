# data-catalogue-pseudonymisation
This is the repository for the pseudonymisation part of the BBMRI.cz data catalog.

## Pseudonymisation

### MiSEQ
Pseudonymizes predictive numbers, collects clinical data and removes unnecessary files before moving the data to SensitiveCloud at ICS-MUNI.

Pseudonymisation itself consists of multiple Python and Bash scripts, the whole pipeline is defined within **pseudonymize_pipeline.sh**:
  1. it sets paths to important folders and files,
  2. it ensures data (HIS exports) transfer from remote server,
  3. it looks for exports having "predictive number" value,
  4. it indentify and remove duplicates
  5. then it iterates through sequencing data folder (consisting of sequencing run output + following analysis output files) and runs scripts:
        - **remove_files.sh** - removes defined unnecessary files
        - **pseudonymisation.py** - performs pseudonymisation creating class **Pseudonymizer** and using function **pseudonymize_run()**  or **\_\_call\_\_()**. The function performs the following tasks:
            1. Pseudonymization of samplesheets
            2. Adding clinical and biobank data 
            3. Pseudonymizing file names
        - **clinical_finder.py**, this clinical_finder.py Python script contains:
          - class **Material** definition (with properties pseudo_ID, biopsy_number, sample_ID, sample_number, available_samples_number, material_type) 
          - The class **Material** has following subclasses:
            - **Tissue** (with properties material, pTNM, morphology, diagnosis, cut_time, freeze_time)
            - **Serum** (with properties material, diagnosis, taking_date)
            - **Genome** (with properties material, taking_date)
          - class **Patient** definition (with properties ID, birth, sex, samples)
          - class **FindClinicalInfo** definition (with properties export_path, predictive_numbers, pseudo_pred_table_path, pseudo_patient_table_path, pseudo_sample_table_path, run_path) and functions:
            - **\_\_call\_\_()** performs the following steps:
              1. Collects all clinical information in export and convert it to nicer json format
              2. Splits clinical info per patient and removes duplicated values
              3. Splits clinical info per pseudo_id and only takes one material per pseudo_id
            - **get_pseudo_ids()** returns all pseudo_ids generated in the search process.
      - **replace_predictive.sh** - replaces each predictive number appearance in all the files of sequencing data folder with created pseudo ID in previous step