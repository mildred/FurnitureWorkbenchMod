class ReloadCommand:
    def __init__(self):
        pass

    def Activated(self):
        from importlib import reload
        import Furniture_Door
        import Furniture_Annotation
        reload(Furniture_Door)
        reload(Furniture_Annotation)

    def GetResources(self):
        return {'Pixmap': 'icons/Reload.svg',
                'MenuText': "Reload",
                'ToolTip': "Reload"}

    def isActive(self):
        return True

FreeCADGui.addCommand('Furniture_ReloadCommand', ReloadCommand())

class FurnitureWorkbench ( Workbench ):
    "My workbench object"
    Icon = """
            /* XPM */
            static const char *test_icon[]={
            "16 16 2 1",
            "a c #000000",
            ". c None",
            "................",
            "................",
            "..############..",
            "..############..",
            "..############..",
            "..####..........",
            "..####..........",
            "..########......",
            "..########......",
            "..####..........",
            "..####..........",
            "..####..........",
            "..####..........",
            "..####..........",
            "................",
            "................"};
            """
    MenuText = "Furniture Workbench"
    ToolTip = "This is my extraordinary furniture workbench"

    def GetClassName(self):
        return "Gui::PythonWorkbench"

    def Initialize(self):
        import Furniture_Door
        self.appendToolbar("Furniture", ["Furniture_ReloadCommand", "Furniture_MakeDoorCommand"])
        self.appendMenu("Furniture", ["Furniture_ReloadCommand", "Furniture_MakeDoorCommand"])
        Log ("Loading Furniture... done\n")

    def Activated(self):
        # do something here if needed...
        Msg ("FurnitureWorkbench.Activated()\n")

    def Deactivated(self):
        # do something here if needed...
        Msg ("FurnitureWorkbench.Deactivated()\n")

FreeCADGui.addWorkbench(FurnitureWorkbench)
