# data-catalogue-pseudonymisation
This is the repository for the pseudonymisation part of the BBMRI.cz data catalog.

## Pseudonymisation
Pseudonymizes predictive numbers, collects clinical data and removes unnecessary files before moving the data to SensitiveCloud at ICS-MUNI.

## Supported sequencing types
Miseq, New Miseq, MammaPrint

## How to run the scripts
### Locally - Development
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
docker-compose up -f compose.dev.yml -d --build
```
### In production
#### Using docker-compose
```bash
# connect to seq server
su export
cd /home/export/data-catalogue-pseudonymisation
docker-compose up -f compose.prod.yml -d
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

