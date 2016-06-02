## What's it?
  A multi-purpose file directory search and manipulation tool called fdsm. 
  This tool can be invoked as follows on the command line:
```
  fdsm [ -b ] [-f] [-s <statementsfile>] [-i <instance>] [<directory>]
```
* **-b**: It will traverse the directory in breadth first.
* **-f**: Use full path name for statements.
* **-s**: Path of statements file.
* **-i**: Run on Amazon Cloud machine. <instance> is id of the machine.

Syntax for fdsm statement(s) is as follows:
```
  <fdsm expression> => <Unix/Python commands separated by comma> ;
  ....
  <fdsm expression> => <Unix/Python commands separated by comma> ;
```
