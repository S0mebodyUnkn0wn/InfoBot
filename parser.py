"""Parses pages.xml into Units to be displayed by the bot"""
import pathlib
import re
from xml.dom.minidom import parseString, Element
from page import *
from callbacks import *


def make_unit_from_element(element: Element)-> Unit:
    title = element.getAttribute("title")
    unit:Unit
    match element.tagName:
        case "page":
            content = ""
            children = []
            for el in element.childNodes:
                el: Element
                if el.nodeType != Element.ELEMENT_NODE:
                    continue
                match el.nodeName:
                    case "content":
                        text:str = [node for node in el.childNodes if node.nodeType == Element.TEXT_NODE][0].nodeValue
                        content = text
                    case "button":
                        children.append(make_unit_from_element(el))
                    case "page":
                        children.append(make_unit_from_element(el))
            unit = Page(title, content, children)
        case "button":
            text:str = [node for node in element.childNodes if node.nodeType == Element.TEXT_NODE][0].nodeValue
            callback = globals()[text.strip()]
            unit = Button(title, callback)
        case _:
            raise ValueError(f"Could not parse element {element.tagName}")

    return unit


def make_dict_from_element(root: Unit) -> dict[int,Unit]:
    lookup_table = {}
    for i in root.flatten():
        lookup_table[i.id]=i
    return lookup_table


def build_pages_from_file(filepath: pathlib.Path) -> (Unit,dict[int,Unit]):
    doc = parseString(
        re.sub(r"<!--[\s\S]*?-->","",filepath.read_text()) #Purge comments
    )
    root: Element = doc.documentElement
    root_unit = make_unit_from_element(root)
    return root_unit, make_dict_from_element(root_unit)


if __name__ == '__main__':
    print(build_pages_from_file(pathlib.Path("pages.xml")))
