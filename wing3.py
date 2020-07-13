import math
from mh49 import mh49
from scale import scaleListOfTuple
from fattenTe import fattenTe
#from dumpAttr import dumpAttr
#from verticesAsList import verticesAsList

from pprint import pprint
import cadquery as cq # type: ignore

from typing import List, Sequence, Tuple

chord: float = 50 

# Normalize, Scale, fattenTe
scaleFactor: float = 1/mh49[0][0]
nMh49 = scaleListOfTuple(mh49, scaleFactor)
sMh49: List[Tuple[float, float]] = scaleListOfTuple(nMh49, chord)
fMh49: List[Tuple[float, float]] = fattenTe(sMh49, 0.75, 10)

h = 100
d = 25
dihederal = math.radians(10)
sweep = math.radians(20)
X = 0
Y = 1
Z = 2

# Use "XY" with Jeremey's transformed(rotate) technique
halfWing = (
    cq.Workplane("YZ")
    .spline(fMh49).close()
    .sweep(
        cq.Workplane("YX")
        .spline([(0, 0, 0), (h * math.sin(sweep), h, h * math.sin(-dihederal))])
    )
)
log(f'halfWing.val().isValid()={halfWing.val().isValid()}')
#show_object(halfWing)

fullWing = halfWing.mirror("YZ").union(halfWing)
log(f'fullWing.val().isValid()={fullWing.val().isValid()}')
#show_object(fullWing)

verticalWing = fullWing.rotate((0, 0, 0), (1, 0, 0), -90)
log(f'verticalWing.val().isValid()={verticalWing.val().isValid()}')
#show_object(verticalWing)

wing3 = verticalWing.translate((0, 0, fMh49[-1][X] + (h * math.sin(sweep))))
log(f'wing3.val().isValid()={wing3.val().isValid()}')
show_object(wing3)

##pprint(vars(wing3))
import io
tolerance=0.001;
f = io.open(f'wing3-direct-{tolerance}.stl', 'w+')
cq.exporters.exportShape(wing3, cq.exporters.ExportTypes.STL, f, tolerance)
f.close()

