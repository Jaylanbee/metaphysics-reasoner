import pytest
from backend.quality_gates import QualityGates

def test_quality_gates_auto_repair():
    forbidden_words = ["一定", "絕對"]
    gates = QualityGates(forbidden_words)

    mock_report = {
        "modules": {
            "module_1": {"title": "Test", "content": "這是一定會發生的事情。"} # Too short, contains forbidden word
        }
    }

    passed, repaired_report, errors = gates.run_gates(mock_report)

    # It auto-repairs so it passes
    assert passed is True
    assert len(errors) > 0 # But it should log the errors it found

    repaired_content = repaired_report["modules"]["module_1"]["content"]
    assert "一定" not in repaired_content
    assert "有較大機率" in repaired_content
    assert len(repaired_content) >= 50 # Length auto-repaired
