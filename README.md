# PyAsync: QueueRace

The following branch highlights behaviors in the introduction of for-ever waiting (To enter lab) state of threads and exploring solution to implement thread safe queue by allowing a correct output (Users entered in lab) when executing multiple threads entering and simulatenously wait for the lab to open. Feature file ```PyAsync/Feature/QueueRace.feature``` gluecode found at ```PyAsync/Feature/Steps/glueCode.py```

#### Tool requirement
- Python 3
- Install [Behave](https://behave.readthedocs.io/en/latest/install.html) (Cucumber equivelant) 

#### Executing Feature File
```C:\...\PyAsync> behave --no-capture``` would produce an obserable test (Backed by Logs/Library.logs)

#### Termination
Due to the fact the server must be executed on the background for the test, to terminate completed test ```Ctrl``` + ```Pause/Break``` would terminate any background thread
