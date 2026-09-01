import pytest
from backend.report_generator import ReportGenerator

def test_report_generator_structure():
    generator = ReportGenerator()

    mock_data = {
        "ziwei": {},
        "bazi": {"day_master": "戊", "dominant_shishen": "正印"},
        "patterns": [{"patternName": "紫府同宮"}],
        "cross_validation": {"aligned_count": 5, "total_dimensions": 5, "confidence_score": "HIGH", "dimensions": {}},
        "classic_references": [{"source": "《骨髓賦》", "chapter": "星曜篇", "quote": "紫微辰戌遇破軍"}]
    }

    report = generator.build_json_report(mock_data)

    assert "metadata" in report
    assert "modules" in report
    assert len(report["modules"]) == 9
    assert "module_1" in report["modules"]

def test_forbidden_words():
    generator = ReportGenerator()
    # "保證" is a forbidden word configured to be replaced with "預期"
    # "必定" is replaced with "有較大機率"
    text = "我保證你必定會發財。"
    clean_text = generator.filter_forbidden_words(text)

    assert "保證" not in clean_text
    assert "必定" not in clean_text
    assert "預期" in clean_text
    assert "有較大機率" in clean_text
