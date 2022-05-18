## Python Template Repository

Setup with useful VSC, Git configuration and libraries. 

To start:
```
    ProjectRoot>python -m venv .
    ProjectRoot>.\Scipts\activate
    ProjectRoot>pip install -r requirements.txt
```

To test:
```
    ProjectRoot>pytest
```

To generate coverage documentation:
```
    ProjectRoot>coverage run -m pytest
```

To view coverage report as a HTML document:
```
    ProjectRoot>coverage html
```

Remember when revisiting after the IDE or terminal has been restarted, restart the env;
```
    ProjectRoot>.\Scipts\activate
```
When the env is active you should see the project name before the directory in ther terminal;
```
    (ProjectName) ProjectName>
```
