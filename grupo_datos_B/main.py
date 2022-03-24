from functools import reduce
from typing import Counter
import xml.etree.ElementTree as ET
import re
import os

base = str(os.path.dirname(__file__)) + '/'
print(base)
ef = ET.parse(base + 'posts.xml')