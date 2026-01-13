[![DOI](https://zenodo.org/badge/682956470.svg)](https://doi.org/10.5281/zenodo.10408797)
# data-catalogue-pseudonymisation
This is the repository for the pseudonymisation part of the BBMRI.cz data catalog.

## Pseudonymisation
Pseudonymizes predictive numbers, collects clinical data and removes unnecessary files before moving the data to SensitiveCloud at ICS-MUNI.

## Supported sequencing types
Miseq, New Miseq, MammaPrint

## How to run the scripts
### Dev environment
#### Using main.py
1. Install requirements
```bash
pip install -r requiremenents.txt
```
2. Run main.py
```bash
python main.py -s /path/to/runs/for/pseudonymization -d /path/to/sensitive/cloud/destination 
               -t /path/to/pseudonymisation/tables/folder -l /path/to/libraries 
               -lsc /path/to/sensitive/cloud/libraries"
```
#### Using docker-compose
```bash
docker compose up -f compose.dev.yml -d --build
```
### Test environment
#### Folder structure
/seq/NO-BACKUP-SPACE/test/\
├── Libraries/     # Required library files for pseudonymisation\
├── logs/          # Logs from test runs\
└── TRANSFER/      # Input data to be pseudonymized


#### Running a Test
1. Copy the run you want to test into */test/TRANSFER/:
```
cp -a /path/to/original/run/ /seq/NO-BACKUP-SPACE/test/TRANSFER/
```
2. Switch to export user and navigate to script folder:
```
su export
cd ~/data-catalogue-pseudonymisation
```
3. Start the pseudonymization script:
```
docker compose -f compose.test.yml up --build 
```
#### Viewing logs
Logs for each run are in the `/seq/NO-BACKUP-SPACE/test/logs` directory.
To view all service logs:
```
docker compose -f compose.test.yml logs
```

### In production
#### Using docker-compose
```bash
# connect to seq server
su export
cd /home/export/data-catalogue-pseudonymisation
docker compose up -f compose.prod.yml --build -d
```
#### Deployment in cron
```bash
# connect to seq serve
su export
crontab -e
# setting cron to run every Monday, Wednesday, Friday at 22:00
0 22 * * 1,3,5 /usr/local/bin/docker-compose -f /home/export/data-catalogue-pseudonymisation/compose.prod.yml up -d &>> /home/export/logs/`date +\%Y\%m\%d\%H\%M\%S`.log
```
## Deploying new version in production
```bash
su export
cd /home/export/data-catalogue-pseudonymization
git switch main
git pull
```
The new version shouldthe new version should automatically start in production once the cronjob is run automatically start in production once the cronjob is run.

