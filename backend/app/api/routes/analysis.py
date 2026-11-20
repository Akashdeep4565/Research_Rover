"""
Analysis API routes for metadata-driven keyword analytics.
"""

import logging
import os
import time
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query

from app.core.config import get_settings
from app.models.schemas import (
    AnalysisRequest,
    AnalysisSourceInfo,
    AnalysisSummary,
    KeywordMatrixResponse,
    CountryCollaborationGraphResponse,
    CountryFrequencyItem,
    CountryStatisticsResponse,
    SuccessResponse,
)
from app.services.analysis_service import AnalysisService
from app.services.country_service import CountryService
from app.utils.csv_loader import CSVLoadError

router = APIRouter()
logger = logging.getLogger("research_rover")


@router.get("/files", response_model=List[AnalysisSourceInfo])
async def list_analysis_files(settings=Depends(get_settings)):
    """List CSV files that can be used as analysis sources."""
    try:
        service = AnalysisService(settings)
        sources = service.list_analysis_sources()
        return [AnalysisSourceInfo(**source) for source in sources]
    except Exception as e:
        logger.error("Error listing analysis files: %s", e)
        raise HTTPException(status_code=500, detail="Failed to list analysis files")


@router.post("/generate", response_model=AnalysisSummary)
async def generate_analysis(
    request: AnalysisRequest,
    settings=Depends(get_settings),
):
    """Generate phases 1-5 analysis artifacts for a CSV file."""
    try:
        service = AnalysisService(settings)
        result = service.build_analysis_artifacts(
            filename=request.filename,
            top_keywords=request.top_keywords,
            minimum_frequency=request.minimum_frequency,
            refresh=request.refresh,
        )
        return AnalysisSummary(**result)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except (CSVLoadError, UnicodeDecodeError, ValueError) as e:
        logger.error("Invalid CSV file for analysis %s: %s", request.filename, e)
        raise HTTPException(status_code=400, detail=f"Invalid or unreadable CSV file: {e}")
    except Exception as e:
        logger.error("Error generating analysis for %s: %s", request.filename, e)
        raise HTTPException(status_code=500, detail="Failed to generate analysis")


@router.get("/{filename}/summary", response_model=AnalysisSummary)
async def get_analysis_summary(
    filename: str,
    refresh: bool = Query(False, description="Regenerate artifacts if summary is missing"),
    settings=Depends(get_settings),
):
    """Load a cached analysis summary, or generate one if requested."""
    try:
        service = AnalysisService(settings)
        if refresh:
            result = service.build_analysis_artifacts(filename=filename, refresh=True)
        else:
            try:
                result = service.load_analysis_summary(filename)
            except FileNotFoundError:
                result = service.build_analysis_artifacts(filename=filename, refresh=True)
        return AnalysisSummary(**result)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except (CSVLoadError, UnicodeDecodeError, ValueError) as e:
        logger.error("Invalid CSV file for analysis %s: %s", filename, e)
        raise HTTPException(status_code=400, detail=f"Invalid or unreadable CSV file: {e}")
    except Exception as e:
        logger.error("Error loading analysis summary for %s: %s", filename, e)
        raise HTTPException(status_code=500, detail="Failed to load analysis summary")


@router.get("/{filename}/matrix", response_model=KeywordMatrixResponse)
async def get_keyword_matrix(
    filename: str,
    preview_rows: int = Query(25, ge=1, le=100, description="Number of rows to preview"),
    settings=Depends(get_settings),
):
    """Return a preview of the keyword presence matrix."""
    try:
        service = AnalysisService(settings)
        result = service.load_keyword_matrix(filename, preview_rows=preview_rows)
        return KeywordMatrixResponse(**result)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except (CSVLoadError, UnicodeDecodeError, ValueError) as e:
        logger.error("Invalid CSV file for keyword matrix %s: %s", filename, e)
        raise HTTPException(status_code=400, detail=f"Invalid or unreadable CSV file: {e}")
    except Exception as e:
        logger.error("Error loading keyword matrix for %s: %s", filename, e)
        raise HTTPException(status_code=500, detail="Failed to load keyword matrix")


@router.get("/{filename}/country-collaboration", response_model=CountryCollaborationGraphResponse)
async def get_country_collaboration(
    filename: str,
    settings=Depends(get_settings),
):
    """Return country collaboration graph data (nodes and links) for a CSV file."""
    try:
        filename = os.path.basename(filename)
        csv_path = os.path.join(settings.DATA_FOLDER, filename)
        if not os.path.exists(csv_path):
            raise HTTPException(status_code=404, detail=f"CSV file not found: {filename}")

        country_service = CountryService()
        result = country_service.get_collaboration_graph_from_csv(csv_path)
        return CountryCollaborationGraphResponse(**result)
    except HTTPException:
        raise
    except (CSVLoadError, UnicodeDecodeError, ValueError) as e:
        logger.error("Invalid CSV file for country collaboration %s: %s", filename, e)
        raise HTTPException(status_code=400, detail=f"Invalid or unreadable CSV file: {e}")
    except Exception as e:
        logger.error("Error generating country collaboration for %s: %s", filename, e)
        raise HTTPException(status_code=500, detail="Failed to generate country collaboration analysis")


@router.get("/{filename}/countries", response_model=CountryStatisticsResponse)
async def get_country_statistics(
    filename: str,
    settings=Depends(get_settings),
):
    """Return country frequency and publication statistics for a CSV file."""
    try:
        filename = os.path.basename(filename)
        csv_path = os.path.join(settings.DATA_FOLDER, filename)
        if not os.path.exists(csv_path):
            raise HTTPException(status_code=404, detail=f"CSV file not found: {filename}")

        country_service = CountryService()
        raw_result = country_service.analyze_csv(csv_path)

        country_items = [
            CountryFrequencyItem(
                country=item["country"],
                iso_a3=item.get("iso_a3"),
                frequency=item["frequency"],
                percentage=item["percentage"],
            )
            for item in raw_result.get("country_frequency", [])
        ]

        unassigned_items = [
            {
                "paper_id": item["paper_id"],
                "title": item["title"],
                "authors": item.get("authors"),
                "source": item.get("source"),
                "year": item.get("year"),
            }
            for item in raw_result.get("unassigned_papers", [])
        ]

        return CountryStatisticsResponse(
            filename=filename,
            total_papers=raw_result.get("total_papers", 0),
            papers_with_country_data=raw_result.get("papers_with_country_data", 0),
            papers_without_country_data=raw_result.get("papers_without_country_data", 0),
            unique_countries=raw_result.get("unique_countries", 0),
            international_papers=raw_result.get("international_papers", 0),
            country_coverage_percentage=raw_result.get("country_coverage_percentage", 0.0),
            countries=country_items,
            unassigned_papers=unassigned_items,
        )
    except HTTPException:
        raise
    except (CSVLoadError, UnicodeDecodeError, ValueError) as e:
        logger.error("Invalid CSV file for country statistics %s: %s", filename, e)
        raise HTTPException(status_code=400, detail=f"Invalid or unreadable CSV file: {e}")
    except Exception as e:
        logger.error("Error generating country statistics for %s: %s", filename, e)
        raise HTTPException(status_code=500, detail="Failed to generate country statistics")



@router.post("/{filename}/regenerate", response_model=SuccessResponse)
async def regenerate_analysis(
    filename: str,
    top_keywords: int = Query(100, ge=1, le=500),
    minimum_frequency: int = Query(1, ge=1),
    settings=Depends(get_settings),
):
    """Convenience endpoint to rebuild analysis artifacts for a CSV file."""
    try:
        service = AnalysisService(settings)
        service.build_analysis_artifacts(
            filename=filename,
            top_keywords=top_keywords,
            minimum_frequency=minimum_frequency,
            refresh=True,
        )
        return SuccessResponse(
            message=f"Analysis regenerated for {filename}",
            data={
                "filename": filename,
                "generated_at": time.time(),
            },
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except (CSVLoadError, UnicodeDecodeError, ValueError) as e:
        logger.error("Invalid CSV file for analysis %s: %s", filename, e)
        raise HTTPException(status_code=400, detail=f"Invalid or unreadable CSV file: {e}")
    except Exception as e:
        logger.error("Error regenerating analysis for %s: %s", filename, e)
        raise HTTPException(status_code=500, detail="Failed to regenerate analysis")
