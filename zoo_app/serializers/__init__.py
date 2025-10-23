from . import animalsSerializer
from . import enclosureSerializer
from . import foodsSerializer
from . import feedRecordsSerializer
from . import managersSerializer

__all__ = (
    animalsSerializer.__all__
    + enclosureSerializer.__all__
    + foodsSerializer.__all__
    + feedRecordsSerializer.__all__
    + managersSerializer.__all__
)
