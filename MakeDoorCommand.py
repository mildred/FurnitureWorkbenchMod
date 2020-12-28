import os
import FreeCAD, FreeCADGui
from PySide.QtCore import QT_TRANSLATE_NOOP

class MakeDoorCommand:
    def __init__(self):
        pass

    def GetResources(self):
        return {'Pixmap': os.path.join(os.path.dirname(__file__), 'icons', 'MakeDoor.svg'),
                'MenuText': QT_TRANSLATE_NOOP("Furniture_MakeDoorComand", "Make Door"),
                'ToolTip': QT_TRANSLATE_NOOP("Furniture_MakeDoorCommand", "Make Door")}

    def Activated(self):
        print("Activated")

    def isActive(self):
        return True

FreeCADGui.addCommand('Furniture_MakeDoorCommand', MakeDoorCommand())
