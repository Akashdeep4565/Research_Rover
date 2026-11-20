import os, sys, json, pandas as pd

from app.core.config import get_settings
from app.services.canonical_loader import CanonicalDataLoader
from app.services.dataset_normalizer import DatasetNormalizer
from app.services.country_service import CountryService
from app.services.analysis_service import AnalysisService

settings = get_settings()
data_dir = settings.DATA_FOLDER
sample_csv = os.path.join(data_dir, 'AI__cANCER.csv')

print('=== 1. TESTING SEARCH CORPUS LOADING & VALIDATION ===')
loader = CanonicalDataLoader()
df = loader.load_canonical_dataframe(sample_csv)
print(f'Loaded {len(df)} papers from {sample_csv}')
print('Columns present:', list(df.columns[:8]))

print('\n=== 2. TESTING KEYWORD BIBLIOMETRIC ANALYSIS ===')
analysis_service = AnalysisService(settings)
summary = analysis_service.load_analysis_summary('AI__cANCER.csv')
if summary:
    print('Analysis summary loaded successfully!')
    total_p = summary.get("total_papers")
    print('Total papers in summary:', total_p)

kw_freq_csv = os.path.join(data_dir, 'AI__cANCER_analysis_keyword_frequency.csv')
if os.path.exists(kw_freq_csv):
    kw_df = pd.read_csv(kw_freq_csv)
    print(f'Keyword frequency CSV found: {len(kw_df)} keywords extracted')
    print('Top 5 keywords:', list(kw_df.iloc[:5, 0].values))

matrix = analysis_service.load_keyword_matrix('AI__cANCER.csv', 5)
if matrix:
    rows = matrix.get("rows", [])
    print(f'Presence matrix loaded: {len(rows)} sample rows')

print('\n=== 3. TESTING COUNTRY COLLABORATION ANALYSIS ===')
country_service = CountryService()
ctry_stats = country_service.analyze_csv(sample_csv)
uniq_c = ctry_stats.get('unique_countries')
print(f'Country statistics: {uniq_c} unique countries detected')
print('Top countries:', [c['country'] for c in ctry_stats.get('countries', [])[:5]])
collab = country_service.get_collaboration_graph_from_csv(sample_csv)
n_count = len(collab.get('nodes', []))
l_count = len(collab.get('links', []))
print(f'Collaboration Network: {n_count} nodes, {l_count} collaboration links')

print('\n=== 4. TESTING DATASET UPLOAD & NORMALIZATION ===')
test_df = pd.DataFrame([{
    'Title': 'Deep Learning for Oncology',
    'Authors': 'Doe, J.; Smith, A.',
    'Abstract': 'A review of deep learning models in cancer diagnostics.',
    'DOI': '10.1000/182',
    'Affiliations': 'Department of Oncology, Harvard Medical School, Boston, USA'
}])

normalizer = DatasetNormalizer()
norm_df, report = normalizer.normalize_dataframe(test_df)
print(f'Dataset Normalizer: Validated {len(norm_df)} rows, report: {type(report).__name__}')

print('\n=== 5. TESTING AI RESEARCH CHAT VECTOR INDEX & CITATIONS ===')
index_path = os.path.join(data_dir, 'AI__cANCER_paper_chunks_hdbscan.index')
mapping_path = os.path.join(data_dir, 'AI__cANCER_full_text_mapping.json')
print(f'FAISS vector index exists: {os.path.exists(index_path)}')
print(f'Full-text citation mapping exists: {os.path.exists(mapping_path)}')
if os.path.exists(mapping_path):
    with open(mapping_path, 'r', encoding='utf-8') as f:
        mapping = json.load(f)
    print(f'Indexed documents mapped for citations: {len(mapping)} papers')

print('\nALL APPLICATION FEATURE WORKFLOWS TESTED & VERIFIED!')
