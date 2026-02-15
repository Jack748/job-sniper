@echo off
REM 1. Activate your Conda environment
CALL C:\Users\giaco\miniconda3\condabin\conda.bat activate job_sniper

REM 2. Go to your project folder
cd /d C:\Users\giaco\Desktop\job_sniper

REM 3. Run the master script
python run_daily.py

REM 4. Pause so you can see if it worked (remove this line later if you want it silent)
pause