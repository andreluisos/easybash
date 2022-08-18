"""
A Python shell command helper using the subprocess Popen.
"""

from shlex import split as shsplit, join as shjoin
from subprocess import Popen, STDOUT, PIPE
from time import sleep, time


class Basher:
    """
    1. The __init__ method is used to initialize the class.
    """

    def __init__(
        self,
        cmd: str,
        cwd=None,
        msg=None,
        debug=False,
        shell=False,
        quiet=False,
        wait=True
    ) -> None:
        self.wait = wait
        if self.wait:
            self.timer_start = time()
        self.cmd, self.pipes = self.cmd_sanitizer(cmd)
        self.cwd = cwd
        self.quiet = quiet
        self.message = msg
        self.debug = debug
        self.shell = shell
        self.delay = 0.2
        self.yellow = "\033[93m"
        self.green = "\033[92m\033[1m"
        self.red = "\033[91m\033[1m"
        self.reset = "\033[0m"
        self.result = self.execute_command()
        self.pid = self.result.pid
        if self.wait:
            self.execution_stdout(self.result)
            self.return_code = self.result.returncode
            self.return_bool = bool(self.return_code)
            self.stdout, self.stderr = self.descriptor()
            self.timer_end = time()
            if self.debug:
                print(f'Command ran: {self.cmd_to_str()}')
                print(f'Return code: {self.return_code}')
                print(
                    f'Execution time (s): {self.timer_end - self.timer_start}')
                if self.stdout:
                    print('-----STDOUT-----')
                    print(self.stdout)
                    print('----------------')
                if self.stderr:
                    print('-----STDERR-----')
                    print(self.stderr)
                    print('----------------')
        else:
            if self.debug:
                print(f'Command ran: {self.cmd_to_str()}')
                print(f'PID: {self.pid}')

    def cmd_to_str(self) -> str:
        """
        1. Join the command with spaces.
        """
        cmd = f'{shjoin(self.cmd)}'
        pipes = f'{" | " + " | ".join([" ".join(pipe) for pipe in self.pipes]) if self.pipes else ""}'
        return cmd + pipes

    def cmd_sanitizer(self, cmd: str) -> tuple[list[str], list[list[str]] | None]:
        """
        1. If the input is not a list, then try to split it.
        2. If the input is a list, then do nothing.
        """
        if '>' in cmd:
            raise ValueError(
                f'Incorrect type for cmd: {type(cmd)}. Redirections are not yet supported.')
                
        if not isinstance(cmd, str):
            raise ValueError(
                f'Incorrect type for cmd: {type(cmd)}. Must be str.')

        if '|' in cmd:
            cmd_split = cmd.split('|')
            cmd_split = [shsplit(cmd) for cmd in cmd_split]
            return (cmd_split[0], cmd_split[1:])
        return (shsplit(cmd), None)

    def main_command(self) -> Popen:
        """
        1. self.cmd is the command that is going to be run.
        2. self.cwd is the working directory.
        3. stdin is the input that is going to be passed to the command.
        4. stdout is the output that is going to be printed.
        5. stderr is the error that is going to be printed.
        6. shell is whether the command is a shell command or not.
        """
        return Popen(
            self.cmd,
            cwd=self.cwd,
            stdin=PIPE,
            stdout=PIPE,
            stderr=STDOUT,
            shell=self.shell,
        )

    def pipe_command(self, previous: Popen, pipe: list[str]) -> Popen:
        """
        1. pipe is the command that we want to run.
        2. stdin is the output of the previous command.
        3. stdout is the output of the current command.
        4. stderr is the error output of the current command.
        5. shell is whether the command is a shell command or not.
        """
        return Popen(
            pipe,
            stdin=previous.stdout,
            stdout=PIPE,
            stderr=STDOUT,
            shell=self.shell,
        )

    def execution_stdout(self, result: Popen) -> None:
        """
        2. Use the poll() method to check if the code is still running.
        3. Use the debug variable to check if we want to see the output of the code.
        4. Use the message variable to print the message to the user.
        6. Use the print() method to print the message to the user."""
        if self.wait:
            while result.poll() is None:
                if self.message is not None:
                    print(f'[{self.yellow}. {self.reset}] {self.message}\r',
                          end='', flush=True)
                    sleep(self.delay)
                    print(f'[{self.yellow} .{self.reset}] {self.message}\r',
                          end='', flush=True)
                sleep(self.delay)

    def execute_command(self) -> Popen:
        """
        1. The main_command() method is used to create the main command.
        2. The pipe_command() method is used to create the pipe command.
        3. The execute() method is used to execute the command.
        """
        if self.pipes:
            main_command = self.main_command()
            pipe_command = None
            previous = main_command
            for index, pipe in enumerate(self.pipes):
                if index == len(self.pipes):
                    pipe_command = self.pipe_command(previous, pipe)
                else:
                    pipe_command = self.pipe_command(previous, pipe)
                previous = pipe_command
            return pipe_command  # type: ignore
        return self.main_command()

    def descriptor(self) -> tuple:
        """
        1. The execution_stdout() function is used to get the output of the command.
        2. The .decode("UTF-8") is used to decode the output of the command.
        3. The .strip() is used to remove the extra spaces from the output.
        """
        if self.return_code == 0:
            self.return_bool = True
            if self.message is not None:
                print(f'[{self.green}OK{self.reset}] {self.message}\n')
        else:
            self.return_bool = False
            if self.message is not None:
                print(f'[{self.red}--{self.reset}] {self.message}\n')

        descriptor = self.result.communicate()
        stdout, stderr = None, None
        if descriptor[0]:
            stdout = descriptor[0].decode("UTF-8").strip()
        if descriptor[1]:
            stderr = descriptor[1].decode("UTF-8").strip()
        return (stdout, stderr)
