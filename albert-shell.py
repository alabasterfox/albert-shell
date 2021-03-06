#!/usr/bin/env python3

import getpass
import os
import socket
import subprocess

"""ASH: a simple shell written in Python"""

# To run this file:
#
# > python3 albert-shell.py
#
#   runs the shell program
#

def execute_command(command):
    """execute commands and handle piping"""
    try:
        if "|" in command:
            # save for restoring later on
            s_in, s_out = (0, 0)
            s_in = os.dup(0)
            s_out = os.dup(1)

            # first command takes commandut from stdin
            fdin = os.dup(s_in)

            # iterate over all the commands that are piped
            for cmd in command.split("|"):
                # fdin will be stdin if it's the first iteration
                # and the readable end of the pipe if not.
                os.dup2(fdin, 0)
                os.close(fdin)

                # restore stdout if this is the last command
                if cmd == command.split("|")[-1]:
                    fdout = os.dup(s_out)
                else:
                    fdin, fdout = os.pipe()

                # redirect stdout to pipe
                os.dup2(fdout, 1)
                os.close(fdout)

                try:
                    subprocess.run(cmd.strip().split())
                except Exception:
                    print("ASH: command not found: {}".format(cmd.strip()))

            # restore stdout and stdin
            os.dup2(s_in, 0)
            os.dup2(s_out, 1)
            os.close(s_in)
            os.close(s_out)
        else:
            subprocess.run(command.split(" "))
    except Exception:
        print("ASH: command not found: {}".format(command))


def psh_cd(path):
    """convert to absolute path and change directory"""
    try:
        os.chdir(os.path.abspath(path))
    except Exception:
        print("cd: no such file or directory: {}".format(path))


def psh_help():
    print("""
Welcome to ASH 0.0.1's help utility!

(A)lbert (SH)ell is a basic shell implementation in Python written by Albert Willett Jr
based on an article by Danish Prakash.

Enter the name of any command in the format 

COMMAND [OPTIONS]

to execute it. To exit this shell utility,just type "exit".
""")


def main():

    # Print welcome/intro message
    print("""ASH 0.0.1 (v0.0.1.14, May 21, 2021).\nType "help" for more information.""")

    while True:

        # accept user input
        command = input("{}@{} {} > ".format(
            getpass.getuser(),
            socket.gethostname(),
            os.path.basename(os.getcwd())
            ))

        # exit the shell
        if command.lower() == "exit" or \
           command.lower() == "exit()" or \
           command.lower() == ".exit" or \
           command.lower() == "quit" or \
           command.lower() == "q":
            break
        # change directory
        elif command[:3].lower() == "cd ":
            psh_cd(command[3:])
        elif command.lower() == "help":
            psh_help()
        else:
            execute_command(command)


if '__main__' == __name__:
    main()