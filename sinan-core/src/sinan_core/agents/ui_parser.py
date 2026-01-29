# sinan-core/src/sinan_core/agents/ui_parser.py
"""UI 树解析器"""
import re
import xml.etree.ElementTree as ET
from typing import Optional


class UITreeParser:
    """UI 树解析和元素匹配"""

    def parse_android(self, xml_content: str) -> list[dict]:
        """解析 Android uiautomator dump 输出"""
        elements = []
        try:
            root = ET.fromstring(xml_content)
            self._traverse_android(root, elements)
        except ET.ParseError:
            pass
        return elements

    def _traverse_android(self, node: ET.Element, elements: list):
        """递归遍历 Android UI 树"""
        bounds_str = node.get("bounds", "[0,0][0,0]")
        bounds = self._parse_bounds(bounds_str)

        element = {
            "text": node.get("text", ""),
            "class": node.get("class", ""),
            "content_desc": node.get("content-desc", ""),
            "resource_id": node.get("resource-id", ""),
            "bounds": bounds,
            "center": [(bounds[0] + bounds[2]) // 2, (bounds[1] + bounds[3]) // 2],
        }

        if element["text"] or element["content_desc"] or element["resource_id"]:
            elements.append(element)

        for child in node:
            self._traverse_android(child, elements)

    def _parse_bounds(self, bounds_str: str) -> list[int]:
        """解析 bounds 字符串 [x1,y1][x2,y2]"""
        match = re.findall(r'\d+', bounds_str)
        if len(match) == 4:
            return [int(x) for x in match]
        return [0, 0, 0, 0]

    def parse_harmony(self, json_content: dict) -> list[dict]:
        """解析鸿蒙 uitest dumpLayout 输出"""
        elements = []
        if isinstance(json_content, dict):
            self._traverse_harmony(json_content, elements)
        return elements

    def _traverse_harmony(self, node: dict, elements: list):
        """递归遍历鸿蒙 UI 树"""
        bounds = node.get("bounds", {})
        element = {
            "text": node.get("text", ""),
            "type": node.get("type", ""),
            "id": node.get("id", ""),
            "bounds": [
                bounds.get("left", 0),
                bounds.get("top", 0),
                bounds.get("right", 0),
                bounds.get("bottom", 0),
            ],
        }

        if element["text"] or element["id"]:
            element["center"] = [
                (element["bounds"][0] + element["bounds"][2]) // 2,
                (element["bounds"][1] + element["bounds"][3]) // 2,
            ]
            elements.append(element)

        for child in node.get("children", []):
            self._traverse_harmony(child, elements)

    def fuzzy_match(self, query: str, elements: list[dict]) -> list[dict]:
        """模糊匹配元素"""
        matches = []
        query_lower = query.lower()

        for elem in elements:
            text = elem.get("text", "").lower()
            desc = elem.get("content_desc", "").lower()
            res_id = elem.get("resource_id", "").lower()

            if query_lower in text or query_lower in desc or query_lower in res_id:
                matches.append(elem)

        return matches
