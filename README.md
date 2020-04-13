# PyAsync: DeadLock

The following scenario highlights the importance of encapsulate multi-threaded functions to ensure corruption or misbehivors such as deadlock do not occur. Feature file ```PyAsync/Features/DeadLockExOne.feature & DeadLockExTwo.feature``` gluecode found at ```PyAsync/Features/Steps/glueCode.py``` illustrates fatal (System crash) and non-fatal (deadlock) if the solution introduced in ```PyAsync/main/Library.py``` has been commented out

#### Tool requirement
- Python 3
- Install [Behave](https://behave.readthedocs.io/en/latest/install.html) (Cucumber equivelant) 

#### Executing Feature File
```C:\...\PyAsync> behave --no-capture features\DeadLockExOne.feature``` (fatal) would produce an obserable test (Logs/Library.log can follow each step)

```C:\...\PyAsync> behave --no-capture features\DeadLockExTwo.feature``` (Non-fatal) deadlock

#### Termination
Due to the fact the server must be executed on the background for the test, to terminate completed test ```Ctrl``` + ```Pause/Break``` would terminate any background thread


