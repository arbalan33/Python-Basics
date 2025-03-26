import xml.etree.ElementTree as ET

def data_to_xml():
    root = ET.Element('main')
    ET.tostring(root, 'unicode')






