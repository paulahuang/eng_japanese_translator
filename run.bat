@echo on
echo --- DEBUG: Starting BAT file ---

cd
echo --- DEBUG: Current directory before CD ---

cd /d "C:\Users\Owner\Documents\AI apps\Japanese translator"
echo --- DEBUG: Now in directory ---
cd

echo --- DEBUG: About to run python ---
python app.py

echo --- DEBUG: python command finished ---
pause



