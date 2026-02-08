call .\.venv\Scripts\activate

pyinstaller --onefile ^
  --distpath build ^
  --workpath build\_work ^
  --add-data "assets;assets" ^
  --add-data "libs;libs" ^
  --add-data "gameinfo.json;." ^
  --add-data "gamecapacities.json;." ^
  --add-data "runtimeconfig.json;." ^
  --name leavethelightoff ^
  main.py