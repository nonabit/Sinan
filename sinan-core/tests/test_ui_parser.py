# sinan-core/tests/test_ui_parser.py
"""UI 树解析器测试"""
import pytest
from sinan_core.agents.ui_parser import UITreeParser

SAMPLE_ANDROID_XML = '''<?xml version="1.0" encoding="UTF-8"?>
<hierarchy>
  <node text="设置" class="android.widget.TextView" bounds="[0,0][100,50]"/>
  <node text="" class="android.widget.Button" content-desc="返回" bounds="[0,50][50,100]"/>
</hierarchy>
'''


def test_parse_android_ui_tree():
    """测试解析 Android UI 树"""
    parser = UITreeParser()
    result = parser.parse_android(SAMPLE_ANDROID_XML)

    assert len(result) == 2
    assert result[0]["text"] == "设置"
    assert result[1]["content_desc"] == "返回"


def test_fuzzy_match():
    """测试模糊匹配"""
    parser = UITreeParser()
    elements = [
        {"text": "设置", "bounds": [0, 0, 100, 50]},
        {"text": "显示与亮度", "bounds": [0, 50, 200, 100]},
    ]

    matches = parser.fuzzy_match("设置", elements)
    assert len(matches) == 1
    assert matches[0]["text"] == "设置"


def test_parse_harmony_ui_tree():
    """测试解析鸿蒙 UI 树"""
    parser = UITreeParser()
    harmony_json = {
        "type": "Column",
        "text": "主页",
        "id": "main_page",
        "bounds": {"left": 0, "top": 0, "right": 100, "bottom": 50},
        "children": [
            {
                "type": "Button",
                "text": "设置",
                "id": "settings_btn",
                "bounds": {"left": 10, "top": 10, "right": 90, "bottom": 40},
                "children": []
            }
        ]
    }

    result = parser.parse_harmony(harmony_json)
    assert len(result) == 2
    assert result[0]["text"] == "主页"
    assert result[1]["text"] == "设置"
