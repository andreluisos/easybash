# About

easybash Basher helps you to easily and safely run BASH commands in a Python program using subprocess Popen.

It's basically a subprocess Popen wrapper.

The idea is to provide an easy way to execute shell commands without compromising safety. Even though it's possible to pass `shell=True` to Popen in order to execute complex commands, it's not recommended and it's mostly not needed with this package.

# Used libraries

```
shlex
subprocess
time
```

This package requires no Python third party libraries.

# Installation

You can install it directly from PyPi using pip:

`pip install easybash`

You can also install it directly from this repository:

`pip install git+https://github.com/andreluisos/easybash.git`

# Usage

## Importing
Basher is an object of easybash. So you can import it with the following code:

```python
from easybash import Basher
```

## Running a command and waiting for the execution to end

```python
from easybash import Basher

Basher('sleep 3')
```
## You can add a message 

```python
from easybash import Basher

Basher('sleep 3', msg='Sleeping for 3 seconds')
```
![msg example](https://github.com/andreluisos/easybash/raw/master/img/1.gif)

## You can debug the execution

```python
from easybash import Basher

Basher('sleep 3', msg='Sleeping for 3 seconds', debug=True)
```
![debug example](https://github.com/andreluisos/easybash/raw/master/img/2.gif)

## You can print the stdout/stderr of the command

```python
from easybash import Basher

print(Basher('ls', msg='Listing files in this dir').stdout)
```
![stdout1 example](https://github.com/andreluisos/easybash/raw/master/img/3.gif)

## You can do whatever you want with the output

```python
from easybash import Basher

[print(line) for line in Basher('ls').stdout.split()]
```
![stdout2 example](https://github.com/andreluisos/easybash/raw/master/img/4.gif)

## You don't have to wait for command execution to keep running your code

```python
from easybash import Basher

cmd = Basher('sleep 20', wait=False)
print(cmd.pid)
```
![wait example](https://github.com/andreluisos/easybash/raw/master/img/5.gif)

## Basher will automatically reconize pipes, so you can easily run commands
*Redirections are being implemented*.
```python
from easybash import Basher

print(Basher('ls | wc -l | wc -l').stdout)
```
![pipe example](https://github.com/andreluisos/easybash/raw/master/img/6.png)

## You can change the current working directory

```python
from easybash import Basher

print(Basher('ls', cwd='/home/andreluisos/test').stdout)
```
![cwd example](https://github.com/andreluisos/easybash/raw/master/img/7.png)

## You can pass shell=True, but it's not recomended!
The idea of the module is to provide an easy way to execute shell commands without compromising safety.
Redirections will be implemented soon.

```python
from easybash import Basher

Basher('ls', shell=True)
```
