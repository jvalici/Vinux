1) read trought install list

2) eclipse
- download master to the workspace
- open as pydev
- nice to have http://stackoverflow.com/questions/1672655/how-to-open-windows-explorer-on-selected-resource-in-eclipse
    in eclipse -> Run-> external tools ->  external tools configurations
    in program tree -> new
        name: OpenInExplorer
        localtion: C:\Windows\explorer.exe
        Arguments: /select,${selected_resource_loc}\
- nice to have: http://stackoverflow.com/questions/25594935/where-is-classical-vertical-scrollbar-in-pydev
- in the Project exlporer

  a) rigt click Vinux->django->Make Migration (Vinux as argument)
  IMPORTANT: check migrations.accent_and_trigram.toAdd and copy the operations as the first operations of the initial migration created at the previous command (0001_initial.py?)
  this is for the companyName__unaccent__lower__trigram_similar==hint search in Vinux.controllerCellar
  b) rigt click Vinux->django->Migrate
  c) rigt click Vinux->django->Run Django Tests should work


3) read through USEFUL COMMANDS

