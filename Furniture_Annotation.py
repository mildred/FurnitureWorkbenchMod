import os
import FreeCAD, FreeCADGui

class ViewProviderAnnotation:
    def __init__(self, obj):
        obj.Proxy = self
        self.ViewObject = obj

    def attach(self, obj):
        '''Setup the scene sub-graph of the view provider, this method is mandatory'''
        self.ViewObject = obj
        self.Object = obj.Object

    def claimChildren(self):
        return [self.Object.Link]

class Annotation:
    def __init__(self, obj):
        obj.addProperty("App::PropertyString", "Role", "Annotation", "Role")
        obj.addProperty("App::PropertyLink", "Link", "Annotation", "Linked object")
        obj.Proxy = self

def annotate(obj, **kwargs):
    a = obj.Document.addObject("App::FeaturePython", "Annotation")
    ann = Annotation(a)
    a.Link = obj
    a.ViewObject.Proxy = 0
    #ViewProviderAnnotation(a.ViewObject)
    for k, v in kwargs.items():
        setattr(a, k, v)
    return obj

def findAnnotation(obj):
    for o in obj.InList:
        if o.TypeId == 'App::FeaturePython' and o.Proxy.__class__ == Annotation:
            return o

def findRole(objects, Role):
    for obj in objects:
        if findAnnotation(obj).Role == Role:
            return obj
