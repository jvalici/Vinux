1) read trought install list

2) eclipse
- download master to the workspace
- open as pydev
- nice to have http://stackoverflow.com/questions/1672655/how-to-open-windows-explorer-on-selected-resource-in-eclipse
    in eclipse -> Run-> external tools ->  external tools configurations
    in program tree -> new
        name: OpenExplore
        localtion: C:\Windows\explorer.exe
        Arguments: /select,${selected_resource_loc}\
- in the Project exlporer
  1) rigt click Vinux->django->Make Django
  2) rigt click Vinux->django->Migrate Django
  3) rigt click Vinux->django->Run Django Tests should work




https://docs.djangoproject.com/en/1.10/intro/tutorial01/

python manage.py runserver

https://pypi.python.org/pypi/pytesseract