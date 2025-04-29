This program is available for local use on GitHub, at https://github.com/k-atej/
smFRET. These instructions assume relatively minimal knowledge of how to run
a program sourced from Github. More experienced users are welcome to run the
program by whichever method they prefer.


In order to use this program, you will need some software installed on your
machine. First, navigate to Python’s website and download the latest version of
Python for your operating system. You will also likely want to use a visualizer.
Visual Studio Code (VS Code) is recommended as a free option in order to run
the program.

Download or clone the repository locally. To download, navigate to the repository,
click the green Code button in the top right and select Download Zip from the
menu. Once the zip file has been downloaded, extract the files to a specific folder on
your machine.

Open VS Code, or some other visualizer. Open all files in the folder that you
extracted from the zip file. Now that you have opened the files, you must now
download each of the external packages needed to run the program. These packages
do not need to be located externally and can be installed directly through VS Code.
Create a new terminal in VS Code, by navigating to Terminal and then New
Terminal. An optional but recommended step is to create a virtual environment.
There are many ways to set up a virtual environment, but one way to set up a virtual
environment for Python is by entering the following two lines. Press enter after each
line to execute the command. For alternative options, consult the documentation of
your visualizer.

python −m venv venv

source venv / bin / activate <−− On macOS/ Linux

venv \Scripts\activate <−− On Windows

The packages required for this program are tkinter, matplotlib, numPy, and Pan-
das. In order to install these packages, we must first install Pip. Create a new
terminal and type the following lines. Press enter to execute the command.

pip install

Your system may report that a new release of pip is available. To remedy this,
run the following line, or whatever line is prompted by the report.

python.exe −m pip install −−upgrade pip

Any further troubleshooting can be navigated by thoroughly reading the error
message for suggestions. It is also common to copy and paste error messages into a
search engine for further advice.

With Pip installed, you may now download the packages needed for the program.
The required packages are tkinter, matplotlib, numPy, and pandas. You may
do so by typing the following lines.

python −m pip install tk

python −m pip install numpy

python −m pip install matplotlib

python −m pip install pandas

Now that the necessary packages have been installed, you may attempt to run
main.py. Navigate to the main.py tab in VS Code and select Run (Run without
Debugging) from the toolbar. To open the main.py tab, it may be necessary to
double click the file in the file viewer on the left side. If prompted to select a
debugger, select Python Debugger. A new Python window should open, though it
may take a few seconds. If the window does not open, start by closing and restarting
the visualizer. If this does not alleviate the issue, read the error message listed in
the terminal and consult the documentation for your visualizer and/or your Python Version.
