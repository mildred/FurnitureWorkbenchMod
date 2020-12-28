import os
import FreeCAD, FreeCADGui
from PySide.QtCore import QT_TRANSLATE_NOOP
from pivy import coin
from Furniture_Annotation import Annotation, annotate, findRole

class Door:
    def __init__(self, obj):
        '''Add some custom properties to our box feature'''
        obj.addProperty("App::PropertyLength","Thickness","Door","Thickness of the door").Thickness=20.0
        obj.addProperty("App::PropertyLength","Width","Door","Width of the door").Width=300.0
        obj.addProperty("App::PropertyLength","Height","Door", "Height of the door").Height=500.0
        obj.addProperty("App::PropertyLength","FrameWidth","Door", "Frame width").FrameWidth=50.0
        obj.addProperty("App::PropertyLength","ProfondeurMortaise","Door", "Profondeur de mortaise").ProfondeurMortaise=35.0
        obj.addProperty("App::PropertyLength","EpaisseurMortaise","Door", "Epaisseur de mortaise").EpaisseurMortaise=10.0
        obj.addProperty("App::PropertyLength","LargeurMortaise","Door", "Largeur de mortaise").LargeurMortaise=30.0
        obj.addProperty("App::PropertyLength","EpaisseurRainure","Door", "Epaisseur de rainure").EpaisseurRainure=8.0
        obj.addProperty("App::PropertyLength","ProfondeurRainure","Door", "Profondeur de rainure").ProfondeurRainure=10.0
        obj.addProperty("App::PropertyLink","MontantG","Door", "Montant gauche")
        obj.addProperty("App::PropertyLink","MontantD","Door", "Montant droit")
        obj.addProperty("App::PropertyLink","TraverseH","Door", "Traverse haute")
        obj.addProperty("App::PropertyLink","TraverseB","Door", "Traverse basse")
        obj.MontantG=obj.Document.addObject("PartDesign::Body", "MontantGauche")
        obj.MontantD=obj.Document.addObject("PartDesign::Body", "MontantDroit")
        obj.TraverseH=obj.Document.addObject("PartDesign::Body", "TraverseHaute")
        obj.TraverseB=obj.Document.addObject("PartDesign::Body", "TraverseBasse")
        obj.MontantG.addObject(annotate(obj.Document.addObject("PartDesign::AdditiveBox", "Montant"), Role = 'piece'))
        obj.MontantG.addObject(annotate(obj.Document.addObject("PartDesign::SubtractiveBox", "Mortaise"), Role = 'mortaise-h'))
        obj.MontantG.addObject(annotate(obj.Document.addObject("PartDesign::SubtractiveBox", "Mortaise"), Role = 'mortaise-b'))
        obj.MontantG.addObject(annotate(obj.Document.addObject("PartDesign::SubtractiveBox", "Rainure"), Role = 'rainure'))
        obj.MontantD.addObject(annotate(obj.Document.addObject("PartDesign::AdditiveBox", "Montant"), Role = 'piece'))
        obj.MontantD.addObject(annotate(obj.Document.addObject("PartDesign::SubtractiveBox", "Mortaise"), Role = 'mortaise-h'))
        obj.MontantD.addObject(annotate(obj.Document.addObject("PartDesign::SubtractiveBox", "Mortaise"), Role = 'mortaise-b'))
        obj.MontantD.addObject(annotate(obj.Document.addObject("PartDesign::SubtractiveBox", "Rainure"), Role = 'rainure'))
        obj.TraverseH.addObject(annotate(obj.Document.addObject("PartDesign::AdditiveBox", "Traverse"), Role = 'piece'))
        obj.TraverseH.addObject(annotate(obj.Document.addObject("PartDesign::SubtractiveBox", "Rainure"), Role = 'rainure'))
        obj.TraverseB.addObject(annotate(obj.Document.addObject("PartDesign::AdditiveBox", "Traverse"), Role = 'piece'))
        obj.TraverseB.addObject(annotate(obj.Document.addObject("PartDesign::SubtractiveBox", "Rainure"), Role = 'rainure'))
        obj.Proxy = self
        self.recomputeChildren(obj, {'FrameWidth', 'Thickness', 'Height',
            'Width', 'ProfondeurMortaise', 'EpaisseurMortaise',
            'LargeurMortaise', 'EpaisseurRainure', 'ProfondeurRainure'})

    def getSubpart(self, obj, part, subpart):
        return findRole(getattr(obj, part).Group, Role = subpart)

    def recomputeChildren(self, obj, props):
        rainure_g = self.getSubpart(obj, 'MontantG', 'rainure')
        rainure_g.Length = obj.Height
        rainure_g.Width  = obj.ProfondeurRainure
        rainure_g.Height = obj.EpaisseurRainure
        rainure_g.Placement = FreeCAD.Placement(
                FreeCAD.Vector(0, 0,
                    (obj.Thickness - obj.EpaisseurRainure) / 2.0),
                FreeCAD.Rotation(0, 0, 0))

        rainure_d = self.getSubpart(obj, 'MontantD', 'rainure')
        rainure_d.Length = obj.Height
        rainure_d.Width  = obj.ProfondeurRainure
        rainure_d.Height = obj.EpaisseurRainure
        rainure_d.Placement = FreeCAD.Placement(
                FreeCAD.Vector(0,
                    obj.FrameWidth - obj.ProfondeurRainure,
                    (obj.Thickness - obj.EpaisseurRainure) / 2.0),
                FreeCAD.Rotation(0, 0, 0))

        rainure_h = self.getSubpart(obj, 'TraverseH', 'rainure')
        rainure_h.Length = obj.Width - 2 * obj.FrameWidth
        rainure_h.Width  = obj.ProfondeurRainure
        rainure_h.Height = obj.EpaisseurRainure
        rainure_h.Placement = FreeCAD.Placement(
                FreeCAD.Vector(0, 0,
                    (obj.Thickness - obj.EpaisseurRainure) / 2.0),
                FreeCAD.Rotation(0, 0, 0))

        rainure_b = self.getSubpart(obj, 'TraverseB', 'rainure')
        rainure_b.Length = obj.Width - 2 * obj.FrameWidth
        rainure_b.Width  = obj.ProfondeurRainure
        rainure_b.Height = obj.EpaisseurRainure
        rainure_b.Placement = FreeCAD.Placement(
                FreeCAD.Vector(0,
                    obj.FrameWidth - obj.ProfondeurRainure,
                    (obj.Thickness - obj.EpaisseurRainure) / 2.0),
                FreeCAD.Rotation(0, 0, 0))

        if not {'ProfondeurMortaise', 'EpaisseurMortaise', 'LargeurMortaise'}.isdisjoint(props):
            for mortaise in [
                    self.getSubpart(obj, 'MontantG', 'mortaise-h'),
                    self.getSubpart(obj, 'MontantG', 'mortaise-b'),
                    self.getSubpart(obj, 'MontantD', 'mortaise-h'),
                    self.getSubpart(obj, 'MontantD', 'mortaise-b')]:
                mortaise.Width = obj.ProfondeurMortaise
                mortaise.Height = obj.EpaisseurMortaise
                mortaise.Length = obj.LargeurMortaise
        if not {'Thickness', 'Height', 'FrameWidth', 'EpaisseurMortaise',
                'LargeurMortaise', 'ProfondeurMortaise'}.isdisjoint(props):
            self.getSubpart(obj, 'MontantG', 'mortaise-h').Placement = FreeCAD.Placement(
                    FreeCAD.Vector(
                        obj.Height - (obj.FrameWidth - obj.LargeurMortaise) / 2.0 - obj.LargeurMortaise,
                        0,
                        (obj.Thickness - obj.EpaisseurMortaise) / 2.0),
                    FreeCAD.Rotation(0, 0, 0))
            self.getSubpart(obj, 'MontantG', 'mortaise-b').Placement = FreeCAD.Placement(
                    FreeCAD.Vector(
                        (obj.FrameWidth - obj.LargeurMortaise) / 2.0,
                        0,
                        (obj.Thickness - obj.EpaisseurMortaise) / 2.0),
                    FreeCAD.Rotation(0, 0, 0))
            self.getSubpart(obj, 'MontantD', 'mortaise-h').Placement = FreeCAD.Placement(
                    FreeCAD.Vector(
                        obj.Height - (obj.FrameWidth - obj.LargeurMortaise) / 2.0 - obj.LargeurMortaise,
                        obj.FrameWidth - obj.ProfondeurMortaise,
                        (obj.Thickness - obj.EpaisseurMortaise) / 2.0),
                    FreeCAD.Rotation(0, 0, 0))
            self.getSubpart(obj, 'MontantD', 'mortaise-b').Placement = FreeCAD.Placement(
                    FreeCAD.Vector(
                        (obj.FrameWidth - obj.LargeurMortaise) / 2.0,
                        obj.FrameWidth - obj.ProfondeurMortaise,
                        (obj.Thickness - obj.EpaisseurMortaise) / 2.0),
                    FreeCAD.Rotation(0, 0, 0))
        if not {'FrameWidth'}.isdisjoint(props):
            mortaise_b = findRole(obj.MontantG.Group, Role = 'mortaise-b')
            obj.MontantG.Group[0].Width = obj.FrameWidth
            obj.MontantD.Group[0].Width = obj.FrameWidth
            obj.TraverseB.Group[0].Width = obj.FrameWidth
            obj.TraverseH.Group[0].Width = obj.FrameWidth
        if not {'Thickness'}.isdisjoint(props):
            obj.MontantG.Group[0].Height = obj.Thickness
            obj.MontantD.Group[0].Height = obj.Thickness
            obj.TraverseH.Group[0].Height = obj.Thickness
            obj.TraverseB.Group[0].Height = obj.Thickness
        if not {'Height'}.isdisjoint(props):
            obj.MontantG.Group[0].Length = obj.Height
            obj.MontantD.Group[0].Length = obj.Height
        if not {'Width', 'FrameWidth', 'MontantG', 'MontantD'}.isdisjoint(props):
            obj.MontantG.Placement = FreeCAD.Placement(
                    FreeCAD.Vector(obj.MontantG.Group[0].Width, 0, 0),
                    FreeCAD.Rotation(90, 0, 0))
            obj.MontantD.Placement = FreeCAD.Placement(
                    FreeCAD.Vector(obj.Width, 0, 0),
                    FreeCAD.Rotation(90, 0, 0))
            obj.TraverseH.Group[0].Length = obj.Width - obj.MontantG.Group[0].Width - obj.MontantD.Group[0].Width
            obj.TraverseB.Group[0].Length = obj.Width - obj.MontantG.Group[0].Width - obj.MontantD.Group[0].Width
        if not {'FrameWidth', 'MontantG', 'MontantD'}.isdisjoint(props):
            obj.TraverseB.Placement = FreeCAD.Placement(
                    FreeCAD.Vector(obj.MontantG.Group[0].Width, 0, 0),
                    FreeCAD.Rotation(0, 0, 0))
            obj.TraverseH.Placement = FreeCAD.Placement(
                    FreeCAD.Vector(obj.MontantG.Group[0].Width, obj.Height - obj.FrameWidth, 0),
                    FreeCAD.Rotation(0, 0, 0))

    def onChanged(self, fp, prop):
        '''Do something when a property has changed'''
        FreeCAD.Console.PrintMessage("Change property: " + str(prop) + "\n")
        self.recomputeChildren(fp, {str(prop)})

    def execute(self, fp):
        '''Do something when doing a recomputation, this method is mandatory'''
        FreeCAD.Console.PrintMessage("Recompute Python Door feature\n")

class ViewProviderDoor:
    def __init__(self, obj):
        '''Set this object to the proxy object of the actual view provider'''
        obj.Proxy = self
        self.ViewObject = obj
 
    def attach(self, obj):
        '''Setup the scene sub-graph of the view provider, this method is mandatory'''
        self.ViewObject = obj
        self.Object = obj.Object

    def claimChildren(self):
        return [self.Object.MontantG, self.Object.MontantD,
                self.Object.TraverseH, self.Object.TraverseB]

    def updateData(self, fp, prop):
        '''If a property of the handled feature has changed we have the chance to handle this here'''
        # fp is the handled feature, prop is the name of the property that has changed
        pass

    def onChanged(self, vp, prop):
        '''Here we can do something when a single property got changed'''
        pass

    def getIcon(self):
        '''Return the icon in XPM format which will appear in the tree view. This method is\
                optional and if not defined a default icon is shown.'''
        return ":/icons/MakeDoor.svg"

    def __getstate__(self):
        '''When saving the document this object gets stored using Python's json module.\
                Since we have some un-serializable parts here -- the Coin stuff -- we must define this method\
                to return a tuple of all serializable objects or None.'''
        return None

    def __setstate__(self,state):
        '''When restoring the serialized object from document we have the chance to set some internals here.\
                Since no data were serialized nothing needs to be done here.'''
        return None


class MakeDoorCommand:
    def __init__(self):
        pass

    def GetResources(self):
        return {'Pixmap': os.path.join(os.path.dirname(__file__), 'icons', 'MakeDoor.svg'),
                'MenuText': QT_TRANSLATE_NOOP("Furniture_MakeDoorComand", "Make Door"),
                'ToolTip': QT_TRANSLATE_NOOP("Furniture_MakeDoorCommand", "Make Door")}

    def Activated(self):
        a=FreeCAD.ActiveDocument.addObject("App::FeaturePython", "Door")
        Door(a)
        ViewProviderDoor(a.ViewObject)
        FreeCAD.ActiveDocument.recompute()

    def isActive(self):
        return True

FreeCADGui.addCommand('Furniture_MakeDoorCommand', MakeDoorCommand())
