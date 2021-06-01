from query.bm32234 import BM32234
from query.bm32312 import BM32312
from query.bm35115 import BM35115
from query.bm41222 import BM41222
from query.bm76738 import BM76738


def get_tablet_class(tablet: str):
    if tablet == "bm32312":
        return BM32312
    if tablet == "bm41222":
        return BM41222
    if tablet == "bm76738":
        return BM76738
    if tablet == "bm35115":
        return BM35115
    if tablet == "bm32234":
        return BM32234
    raise ValueError("Unknown tablet name")
