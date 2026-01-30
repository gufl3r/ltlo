call .\.venv\Scripts\activate

pyinstaller --onefile ^
  --distpath build ^
  --workpath build\_work ^
  --add-data "assets;assets" ^
  --add-data "version_info.json;." ^
  --add-data "config.json;." ^
  --add-data "libs;libs" ^
  --name leavethelightoff ^
  main.py