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
  1) rigt click Vinux->django->Migrate
  2) rigt click Vinux->django->Make Migration (Vinux as argument)
  3) rigt click Vinux->django->Run Django Tests should work




https://docs.djangoproject.com/en/1.10/intro/tutorial01/