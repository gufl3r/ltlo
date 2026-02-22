call .\.venv\Scripts\activate

pyinstaller --onefile ^
  --noconsole ^
  --distpath build ^
  --workpath build\_work ^
  --add-data "game/assets;game/assets" ^
  --add-data "shared/libs;shared/libs" ^
  --add-data "shared/registry/storages;shared/registry/storages" ^
  --name leavethelightoff ^
  main.py