# PyAsync: RaceCondition

The following scenario highlights the race condition in concurrent non-thread safe functions. Feature file ```PyAsync/Features/asyncBookBorrow.feature``` gluecode found at ```PyAsync/Features/Steps/glueCode.py``` illustrates race condition if the solution introduced in ```PyAsync/main/sServer.py``` has been commented out

#### Tool requirement
- Python 3
- Install [Behave](https://behave.readthedocs.io/en/latest/install.html) (Cucumber equivelant) 

#### Executing Feature File
```C:\...\PyAsync> behave --no-capture``` would produce an obserable test (Logs/Library.log can follow each step)

#### Termination
Due to the fact the server must be executed on the background for the test, to terminate completed test ```Ctrl``` + ```Pause/Break``` would terminate any background thread

#### Video Instructions
https://youtu.be/X70zyqZ9fsk
