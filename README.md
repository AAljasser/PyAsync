# PyAsync: DeadLock

The following scenario highlights the importance of encapsulate multi-threaded functions to ensure corruption or misbehivors such as deadlock do not occur. Feature file ```PyAsync/Features/DeadLockExOne.feature & DeadLockExTwo.feature``` gluecode found at ```PyAsync/Features/Steps/glueCode.py``` illustrates fatal (System crash) and non-fatal (deadlock) if the solution introduced in ```PyAsync/main/Library.py``` has been commented out

#### Tool requirement
- Python 3
- Install [Behave](https://behave.readthedocs.io/en/latest/install.html) (Cucumber equivelant) 

#### Executing Feature File
```C:\...\PyAsync> behave --no-capture features\DeadLockExOne.feature``` would produce an obserable test (Printing out result etc...)

```C:\...\PyAsync> behave --no-capture features\DeadLockExTwo.feature``` 

```C:\...\PyAsync> behave features\DeadLockExOne.feature``` Would execute and only raise if the unwanted behavior is induced (Otherwise everything is logged at ```Logs/Library.log```)

```C:\...\PyAsync> behave features\DeadLockExTwo.feature``` 
