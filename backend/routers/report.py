from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional

from backend.auth import get_api_key
from scripts.chart_parser import ChartParser
from scripts.destiny_reasoner import DestinyReasoner
from engine.bazi_engine import BaziEngine
from engine.cross_validator import CrossValidator
from agents.rag_retriever import ClassicsRAGRetriever
from backend.report_generator import ReportGenerator
from backend.quality_gates import QualityGates

router = APIRouter()

class ReportRequest(BaseModel):
    year: int
    month: int
    day: int
    time_branch: str
    gender: str
    format: Optional[str] = "json"

def get_parser():
    return ChartParser()

def get_reasoner():
    return DestinyReasoner()

def get_bazi_engine():
    return BaziEngine()

def get_cross_validator():
    return CrossValidator()

def get_retriever():
    return ClassicsRAGRetriever()

def get_generator():
    return ReportGenerator()

def get_quality_gates(generator: ReportGenerator = Depends(get_generator)):
    return QualityGates(generator.forbidden_words)

@router.post("", dependencies=[Depends(get_api_key)])
async def generate_professional_report(
    req: ReportRequest,
    parser: ChartParser = Depends(get_parser),
    reasoner: DestinyReasoner = Depends(get_reasoner),
    bazi_engine: BaziEngine = Depends(get_bazi_engine),
    cross_validator: CrossValidator = Depends(get_cross_validator),
    retriever: ClassicsRAGRetriever = Depends(get_retriever),
    generator: ReportGenerator = Depends(get_generator),
    quality_gates: QualityGates = Depends(get_quality_gates)
):
    try:
        ziwei_data, bazi_data = parser.generate_chart_payload(
            req.year, req.month, req.day, req.time_branch, req.gender
        )
        bazi_detailed = bazi_engine.calculate_bazi(
            req.year, req.month, req.day, req.time_branch, req.gender
        )
        detected_patterns = reasoner.analyze_ziwei_chart(ziwei_data)
        cross_validation = cross_validator.validate_5d(ziwei_data, bazi_detailed)

        classic_refs = retriever.retrieve_classics("紫微")

        master_data = {
            "ziwei": ziwei_data,
            "bazi": bazi_detailed,
            "patterns": detected_patterns,
            "cross_validation": cross_validation,
            "classic_references": classic_refs
        }

        raw_report = generator.build_json_report(master_data)

        passed, final_report, errors = quality_gates.run_gates(raw_report)

        if req.format == "markdown":
            return {"status": "success", "report": generator.convert_to_markdown(final_report), "qa_logs": errors}

        return {"status": "success", "report": final_report, "qa_logs": errors}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
