"""
File management API routes
"""

from fastapi import APIRouter, HTTPException, Depends, Query, UploadFile, File
from fastapi.responses import FileResponse, StreamingResponse
from typing import List, Optional, Tuple
import os
import re
import socket
import ipaddress
import urllib.parse
import requests
import logging

from app.models.schemas import (
    PaginatedResponse, FileInfo, ErrorResponse, SuccessResponse,
    ExtendedFileUploadResponse, DatasetQualityReport,
)
from app.core.config import get_settings
from app.services.canonical_loader import CanonicalDataLoader
from app.utils.csv_loader import detect_csv_encoding, CSVLoadError

router = APIRouter()
logger = logging.getLogger("research_rover")

@router.post("/upload", response_model=ExtendedFileUploadResponse)
async def upload_file(
    file: UploadFile = File(...),
    settings=Depends(get_settings)
):
    """
    Upload a CSV file to the data folder with automatic canonical schema normalization,
    quality scoring, duplicate tracking, and feature readiness assessment.
    Preserves original uploaded CSV untouched.
    """
    try:
        if not file.filename or not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="Only CSV files are allowed")

        os.makedirs(settings.DATA_FOLDER, exist_ok=True)
        safe_name = os.path.basename(file.filename)
        file_path = os.path.join(settings.DATA_FOLDER, safe_name)

        if hasattr(file, "file") and hasattr(file.file, "read"):
            content = file.file.read()
        else:
            content = await file.read()
        if len(content) > settings.MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail=f"File exceeds maximum allowed size of {settings.MAX_FILE_SIZE} bytes")

        with open(file_path, 'wb') as f:
            f.write(content)

        detected_enc = detect_csv_encoding(file_path)
        logger.info(f"Uploaded file: {safe_name} ({len(content)} bytes), encoding: {detected_enc}")

        if len(content) == 0:
            return ExtendedFileUploadResponse(
                message=f"File {safe_name} uploaded successfully, but the file is 0 bytes.",
                filename=safe_name,
                encoding=detected_enc or "utf-8",
                total_records=0,
                valid_records=0,
                duplicate_records=0,
                overall_quality_score=0.0,
                quality_grade="Critical",
                warnings=["Uploaded file is 0 bytes and contains no records."],
                recommendations=["Please upload a CSV file containing research paper records and column headers."],
                index_status="not_indexed",
            )

        # Normalize and assess with canonical loader
        records, quality_report = CanonicalDataLoader.process_and_save_canonical(file_path)
        index_exists, index_status = CanonicalDataLoader.check_index_files_exist(file_path, data_folder=settings.DATA_FOLDER)
        # Apply shared runtime index overlay to ensure 100% consistency with GET /{filename}/quality
        quality_report = CanonicalDataLoader.apply_index_status_overlay(quality_report, index_exists)

        # Collect mapped and unmapped column details
        norm_rep = quality_report.normalization_report
        canonical_detected = []
        col_mappings = {}
        conflicts = []

        if norm_rep:
            canonical_detected = [
                m.canonical_field for m in norm_rep.mappings.values() if m.canonical_field
            ]
            col_mappings = norm_rep.mappings
            conflicts = norm_rep.conflicts

        # Collect feature warnings
        warnings = []
        for fid, fr in quality_report.feature_readiness.items():
            if fr.warnings:
                warnings.extend(fr.warnings)

        return ExtendedFileUploadResponse(
            message=f"File {safe_name} uploaded and normalized successfully",
            filename=safe_name,
            encoding=detected_enc or "utf-8",
            total_records=quality_report.total_records,
            valid_records=quality_report.valid_records,
            duplicate_records=quality_report.duplicate_records,
            overall_quality_score=quality_report.overall_quality_score,
            quality_grade=quality_report.quality_grade,
            canonical_fields_detected=canonical_detected,
            column_mappings=col_mappings,
            unmapped_columns=quality_report.unmapped_columns,
            conflicting_mappings=conflicts,
            feature_readiness=quality_report.feature_readiness,
            warnings=warnings,
            recommendations=quality_report.recommendations,
            index_status=index_status,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading file: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to upload and normalize file: {e}")


@router.get("/{filename}/quality", response_model=DatasetQualityReport)
async def get_file_quality(
    filename: str,
    settings = Depends(get_settings)
):
    """
    Get the dataset quality assessment and feature readiness report for any existing CSV file.
    Overlays runtime vector index availability onto feature readiness.
    """
    try:
        csv_path = os.path.join(settings.DATA_FOLDER, os.path.basename(filename))
        if not os.path.exists(csv_path):
            raise HTTPException(status_code=404, detail="File not found")

        report = CanonicalDataLoader.get_quality_report(csv_path, data_folder=settings.DATA_FOLDER)
        return report

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error evaluating quality for {filename}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to assess file quality: {e}")


@router.get("/download/{filename}")
async def download_file(
    filename: str,
    settings = Depends(get_settings)
):
    """Download a file from the data folder"""
    try:
        # Sanitize filename
        filename = "_".join(filename.split("%20"))
        file_path = os.path.join(settings.DATA_FOLDER, filename)
        
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")
        
        return FileResponse(
            path=file_path,
            filename=filename,
            media_type='application/octet-stream'
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error downloading file {filename}: {e}")
        raise HTTPException(status_code=500, detail="Failed to download file")


def validate_safe_url(target_url: str) -> None:
    """
    Validate that target_url uses http/https and does not resolve to private,
    loopback, link-local, multicast, or reserved networks (SSRF prevention).
    """
    if not target_url or not isinstance(target_url, str):
        raise HTTPException(status_code=400, detail="A valid 'url' parameter is required.")

    target_url = target_url.strip()
    try:
        parsed = urllib.parse.urlparse(target_url)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Malformed URL: {e}")

    scheme = parsed.scheme.lower()
    if scheme not in ("http", "https"):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid URL scheme '{parsed.scheme}'. Only http and https protocols are permitted."
        )

    hostname = parsed.hostname
    if not hostname:
        raise HTTPException(status_code=400, detail="Invalid URL: missing hostname.")

    hostname_lower = hostname.lower()
    blocked_hostnames = {
        "localhost", "127.0.0.1", "0.0.0.0", "::1", "metadata.google.internal", "instance-data"
    }
    if hostname_lower in blocked_hostnames or any(
        hostname_lower.endswith(sfx) for sfx in (".local", ".internal", ".lan", ".localhost", ".home.arpa")
    ):
        raise HTTPException(
            status_code=400,
            detail="Access to internal, local, or private network hostnames is forbidden."
        )

    # 1. Fast check for IP literals (avoids slow DNS/NetBIOS timeouts on private IPs)
    try:
        direct_ip = ipaddress.ip_address(hostname)
        if (
            direct_ip.is_private
            or direct_ip.is_loopback
            or direct_ip.is_link_local
            or direct_ip.is_multicast
            or direct_ip.is_reserved
            or direct_ip.is_unspecified
        ):
            raise HTTPException(
                status_code=400,
                detail=f"Access to private or local network address ({hostname}) is forbidden."
            )
        return
    except ValueError:
        # Not an IP literal, proceed to hostname resolution
        pass

    try:
        port = parsed.port or (443 if scheme == "https" else 80)
        addr_info = socket.getaddrinfo(hostname, port, proto=socket.IPPROTO_TCP)
    except socket.gaierror as e:
        raise HTTPException(status_code=400, detail=f"Could not resolve hostname '{hostname}': {e}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Hostname resolution failed: {e}")

    if not addr_info:
        raise HTTPException(status_code=400, detail=f"No IP addresses resolved for hostname '{hostname}'.")

    for item in addr_info:
        sockaddr = item[4]
        ip_str = sockaddr[0]
        try:
            ip_obj = ipaddress.ip_address(ip_str)
        except ValueError:
            continue

        if (
            ip_obj.is_private
            or ip_obj.is_loopback
            or ip_obj.is_link_local
            or ip_obj.is_multicast
            or ip_obj.is_reserved
            or ip_obj.is_unspecified
        ):
            raise HTTPException(
                status_code=400,
                detail=f"Access to private or local network address ({ip_str}) is forbidden."
            )


def fetch_pdf_stream_safely(initial_url: str, max_redirects: int = 5) -> Tuple[requests.Response, str]:
    """
    Fetch a remote PDF stream while strictly validating every redirect against SSRF rules.
    """
    current_url = initial_url
    session = requests.Session()
    session.headers.update({
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/131.0.0.0 Safari/537.36 ResearchRover/2.0"
        ),
        "Accept": "application/pdf,application/octet-stream,*/*;q=0.8",
    })

    for _ in range(max_redirects + 1):
        validate_safe_url(current_url)
        try:
            resp = session.get(current_url, stream=True, timeout=25, allow_redirects=False)
        except requests.exceptions.Timeout:
            raise HTTPException(status_code=504, detail="Connection timed out while fetching PDF from publisher.")
        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=502, detail=f"Network error while connecting to publisher: {e}")

        if resp.status_code in (301, 302, 303, 307, 308):
            location = resp.headers.get("Location")
            if not location:
                raise HTTPException(status_code=502, detail="Publisher returned redirect without Location header.")
            current_url = urllib.parse.urljoin(current_url, location)
            continue

        return resp, current_url

    raise HTTPException(status_code=508, detail="Too many redirects encountered while resolving PDF URL.")


@router.get("/download-pdf")
async def download_pdf(
    url: str = Query(..., description="Target PDF URL to download"),
    title: Optional[str] = Query(None, description="Paper title for naming the downloaded file"),
    doi: Optional[str] = Query(None, description="Paper DOI as fallback naming"),
    pmid: Optional[str] = Query(None, description="Paper PMID as fallback naming"),
    settings=Depends(get_settings),
):
    """
    Download a research paper PDF by streaming it from a verified open-access provider.
    Includes comprehensive SSRF prevention, private IP protection, safe redirects,
    paywall detection, and automatic filename construction.
    """
    resp, final_url = fetch_pdf_stream_safely(url)

    if resp.status_code in (401, 403):
        raise HTTPException(
            status_code=403,
            detail="Access restricted: This PDF requires publisher credentials, authentication, or subscription paywall. A free direct PDF is not available."
        )
    if resp.status_code == 404:
        raise HTTPException(
            status_code=404,
            detail="PDF not found at the remote destination (404)."
        )
    if resp.status_code >= 500:
        raise HTTPException(
            status_code=502,
            detail=f"Publisher server error ({resp.status_code}) while downloading PDF."
        )
    if resp.status_code != 200:
        raise HTTPException(
            status_code=resp.status_code,
            detail=f"Remote server responded with HTTP status {resp.status_code}."
        )

    # Read initial chunk to verify PDF header / magic bytes
    chunk_iter = resp.iter_content(chunk_size=4096)
    try:
        first_chunk = next(chunk_iter)
    except StopIteration:
        first_chunk = b""

    content_type = resp.headers.get("Content-Type", "").lower()
    is_pdf_content = (
        b"%PDF-" in first_chunk[:1024]
        or "application/pdf" in content_type
        or "application/x-pdf" in content_type
    )

    if not is_pdf_content:
        # Check if remote server served an HTML landing page
        if b"<html" in first_chunk.lower() or b"<!doctype" in first_chunk.lower():
            if "pmc.ncbi.nlm.nih.gov" in final_url or "ncbi.nlm.nih.gov/pmc" in final_url:
                raise HTTPException(
                    status_code=422,
                    detail="PMC direct download requires interactive browser verification. Please open the official PMC link directly."
                )
            raise HTTPException(
                status_code=422,
                detail="The remote server returned an HTML webpage instead of a direct PDF. This article may require publisher login or paywall access."
            )
        raise HTTPException(
            status_code=422,
            detail="The destination content is not a valid PDF document."
        )

    # Construct clean, meaningful filename
    clean_name = ""
    if title and title.strip() and title.strip().lower() != "unknown":
        clean_name = re.sub(r'[^a-zA-Z0-9_\- ]', '', title.strip())
        clean_name = re.sub(r'\s+', '_', clean_name)[:80]
    elif doi and doi.strip():
        clean_name = re.sub(r'[^a-zA-Z0-9_\-]', '_', doi.strip())
    elif pmid and pmid.strip():
        clean_name = f"PMID_{pmid.strip()}"
    else:
        clean_name = "research_paper"

    filename = f"{clean_name}.pdf"

    def iter_stream():
        yield first_chunk
        for chunk in chunk_iter:
            if chunk:
                yield chunk

    return StreamingResponse(
        iter_stream(),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Access-Control-Expose-Headers": "Content-Disposition",
        }
    )


@router.get("/csv/{filename}/data", response_model=List[dict])
async def get_csv_data(
    filename: str,
    settings = Depends(get_settings)
):
    """Get CSV data as JSON"""
    try:
        csv_path = os.path.join(settings.DATA_FOLDER, filename)
        
        if not os.path.exists(csv_path):
            raise HTTPException(status_code=404, detail="CSV file not found")
        
        from app.services.search_service import SearchService
        search_service = SearchService(settings)
        papers = await search_service.load_papers_from_csv(csv_path)
        
        # Convert to dict format for response
        return [paper.dict() for paper in papers]
        
    except HTTPException:
        raise
    except (CSVLoadError, UnicodeDecodeError, ValueError) as e:
        logger.error(f"Error reading CSV {filename}: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid or unreadable CSV file: {e}")
    except Exception as e:
        logger.error(f"Error reading CSV {filename}: {e}")
        raise HTTPException(status_code=500, detail="Error processing CSV file")

@router.get("/csv/{filename}/paginated", response_model=PaginatedResponse)
async def get_paginated_csv_data(
    filename: str,
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(10, ge=1, le=100, description="Results per page"),
    settings = Depends(get_settings)
):
    """Get paginated CSV data"""
    try:
        csv_path = os.path.join(settings.DATA_FOLDER, filename)
        
        if not os.path.exists(csv_path):
            raise HTTPException(status_code=404, detail="CSV file not found")
        
        # Check if file is empty
        if os.path.getsize(csv_path) == 0:
            raise HTTPException(status_code=404, detail="CSV file is empty")
        
        from app.services.search_service import SearchService
        search_service = SearchService(settings)
        papers = await search_service.load_papers_from_csv(csv_path)
        
        if not papers:
            raise HTTPException(status_code=404, detail="No valid data found in CSV")
        
        # Calculate pagination
        total_results = len(papers)
        total_pages = max(1, (total_results + per_page - 1) // per_page)
        start_idx = min((page - 1) * per_page, total_results)
        end_idx = min(start_idx + per_page, total_results)
        
        return PaginatedResponse(
            results=papers[start_idx:end_idx],
            total_results=total_results,
            current_page=page,
            total_pages=total_pages,
            per_page=per_page
        )
        
    except HTTPException:
        raise
    except (CSVLoadError, UnicodeDecodeError, ValueError) as e:
        logger.error(f"Error getting paginated CSV data for {filename}: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid or unreadable CSV file: {e}")
    except Exception as e:
        logger.error(f"Error getting paginated CSV data: {e}")
        raise HTTPException(status_code=500, detail="Error processing CSV file")

@router.get("/list", response_model=List[FileInfo])
async def list_files(
    settings = Depends(get_settings)
):
    """List all files in the data folder"""
    try:
        files = []
        
        if os.path.exists(settings.DATA_FOLDER):
            for filename in os.listdir(settings.DATA_FOLDER):
                file_path = os.path.join(settings.DATA_FOLDER, filename)
                if os.path.isfile(file_path):
                    stat = os.stat(file_path)
                    file_info = FileInfo(
                        filename=filename,
                        size=stat.st_size,
                        created_at=stat.st_ctime,
                        file_type=os.path.splitext(filename)[1] or 'unknown'
                    )
                    files.append(file_info)
        
        return files
        
    except Exception as e:
        logger.error(f"Error listing files: {e}")
        raise HTTPException(status_code=500, detail="Error listing files")

@router.delete("/{filename}", response_model=SuccessResponse)
async def delete_file(
    filename: str,
    settings = Depends(get_settings)
):
    """Delete a file from the data folder"""
    try:
        file_path = os.path.join(settings.DATA_FOLDER, filename)
        
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")
        
        os.remove(file_path)
        
        return SuccessResponse(
            message=f"File {filename} deleted successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting file {filename}: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete file")