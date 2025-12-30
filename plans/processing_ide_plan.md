## Objective

Generate a plan to use PySide6 to create a GUI that’s similar to the
IDE for the processing system. Processing (https://processing.org)
enables the creation of generative art.

There’s a screen capture of the ide in the file processing_ide.png
that can be examined for visual structure. 

The documentation for processing has an overview of the development
environment that you can read at: https://processing.org/environment

As opposed to editing Java-like processing code, this IDE should edit
Python in its code windows.

Eventually we will want to use the IDE like environment to launch an
instance of FramebufferWidget (in @src/peyote/smoke_subommand.py) for
code edited in the environment to draw against. 

Devise on offscreen widget class that can render into a GIF or PNG
file. Similar to FramebufferWidget use a shared Numpy ndarray for the
art code to manipulate with Numpy and a 2D vector library.

Define an appropriate class structure if needed, but don’t make a
complex object class hierarchy.

Plan out additional command groups and subcommands to launch the
IDE.

Break this down into multiple implementation phases if necessary.

If possible, create a test plan that uses the offscreen widget to do
simple drawing to generate an image file and run checks against the
rendered image.

If you’re not sure of something or there are 2 to 3 reasonable
implementation choices, be sure to ask clarifying questions. Do not
generate any new code. Simply generate a plan that can be passed for
future agents to work on.



