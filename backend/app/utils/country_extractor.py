"""
Country extraction and normalization utility for Research Rover.

Provides robust, alias-aware country recognition from author affiliation text,
author records, and CSV datasets without false positives on arbitrary words.
"""

import ast
import re
from typing import Any, Dict, List, Optional, Set, Tuple


# Comprehensive mapping of country aliases, variants, ISO codes, and major sub-regions
# to canonical country names.
COUNTRY_ALIASES: Dict[str, str] = {
    # United States
    "united states": "United States",
    "united states of america": "United States",
    "usa": "United States",
    "u.s.a.": "United States",
    "u.s.": "United States",
    "us": "United States",
    "america": "United States",
    "us of a": "United States",
    
    # United Kingdom
    "united kingdom": "United Kingdom",
    "uk": "United Kingdom",
    "u.k.": "United Kingdom",
    "great britain": "United Kingdom",
    "britain": "United Kingdom",
    "england": "United Kingdom",
    "scotland": "United Kingdom",
    "wales": "United Kingdom",
    "northern ireland": "United Kingdom",
    
    # China
    "china": "China",
    "p.r. china": "China",
    "pr china": "China",
    "peoples republic of china": "China",
    "people's republic of china": "China",
    "mainland china": "China",
    "p.r.c.": "China",
    "prc": "China",
    
    # Korea
    "south korea": "South Korea",
    "republic of korea": "South Korea",
    "korea, republic of": "South Korea",
    "korea": "South Korea",
    "r.o.k.": "South Korea",
    "rok": "South Korea",
    "north korea": "North Korea",
    "democratic people's republic of korea": "North Korea",
    
    # Germany
    "germany": "Germany",
    "deutschland": "Germany",
    "frg": "Germany",
    "federal republic of germany": "Germany",
    
    # France
    "france": "France",
    "french republic": "France",
    "republique francaise": "France",
    
    # Japan
    "japan": "Japan",
    "nippon": "Japan",
    
    # India
    "india": "India",
    "bharat": "India",
    
    # Canada
    "canada": "Canada",
    
    # Australia
    "australia": "Australia",
    
    # Italy
    "italy": "Italy",
    "italia": "Italy",
    "italian republic": "Italy",
    
    # Spain
    "spain": "Spain",
    "españa": "Spain",
    "espana": "Spain",
    "kingdom of spain": "Spain",
    
    # Brazil
    "brazil": "Brazil",
    "brasil": "Brazil",
    
    # Netherlands
    "netherlands": "Netherlands",
    "the netherlands": "Netherlands",
    "holland": "Netherlands",
    
    # Switzerland
    "switzerland": "Switzerland",
    "schweiz": "Switzerland",
    "suisse": "Switzerland",
    "svizzera": "Switzerland",
    "swiss": "Switzerland",
    
    # Sweden
    "sweden": "Sweden",
    "sverige": "Sweden",
    
    # Belgium
    "belgium": "Belgium",
    "belgique": "Belgium",
    "belgië": "Belgium",
    "belgie": "Belgium",
    
    # Austria
    "austria": "Austria",
    "österreich": "Austria",
    "oesterreich": "Austria",
    
    # Poland
    "poland": "Poland",
    "polska": "Poland",
    
    # Russia
    "russia": "Russia",
    "russian federation": "Russia",
    "u.s.s.r.": "Russia",
    "ussr": "Russia",
    
    # Taiwan
    "taiwan": "Taiwan",
    "republic of china": "Taiwan",
    "taiwan, r.o.c.": "Taiwan",
    "roc": "Taiwan",
    
    # Hong Kong
    "hong kong": "Hong Kong",
    "hong kong sar": "Hong Kong",
    "hk": "Hong Kong",
    
    # Singapore
    "singapore": "Singapore",
    
    # Israel
    "israel": "Israel",
    
    # Iran
    "iran": "Iran",
    "islamic republic of iran": "Iran",
    
    # Saudi Arabia
    "saudi arabia": "Saudi Arabia",
    "kingdom of saudi arabia": "Saudi Arabia",
    "ksa": "Saudi Arabia",
    
    # Turkey
    "turkey": "Turkey",
    "türkiye": "Turkey",
    "turkiye": "Turkey",
    
    # Denmark
    "denmark": "Denmark",
    "danmark": "Denmark",
    
    # Norway
    "norway": "Norway",
    "norge": "Norway",
    
    # Finland
    "finland": "Finland",
    "suomi": "Finland",
    
    # Ireland
    "ireland": "Ireland",
    "republic of ireland": "Ireland",
    "eire": "Ireland",
    
    # Portugal
    "portugal": "Portugal",
    
    # Greece
    "greece": "Greece",
    "hellas": "Greece",
    
    # Czech Republic
    "czech republic": "Czech Republic",
    "czechia": "Czech Republic",
    
    # Hungary
    "hungary": "Hungary",
    "magyarország": "Hungary",
    "magyarorszag": "Hungary",
    
    # Mexico
    "mexico": "Mexico",
    "méxico": "Mexico",
    
    # Argentina
    "argentina": "Argentina",
    
    # Chile
    "chile": "Chile",
    
    # Colombia
    "colombia": "Colombia",
    
    # Egypt
    "egypt": "Egypt",
    
    # South Africa
    "south africa": "South Africa",
    
    # New Zealand
    "new zealand": "New Zealand",
    
    # Pakistan
    "pakistan": "Pakistan",
    
    # Nigeria
    "nigeria": "Nigeria",
    
    # Malaysia
    "malaysia": "Malaysia",
    
    # Thailand
    "thailand": "Thailand",
    
    # Vietnam
    "vietnam": "Vietnam",
    "viet nam": "Vietnam",
    
    # Indonesia
    "indonesia": "Indonesia",
    
    # United Arab Emirates
    "united arab emirates": "United Arab Emirates",
    "uae": "United Arab Emirates",
    "u.a.e.": "United Arab Emirates",
    
    # Philippines
    "philippines": "Philippines",
    
    # Ukraine
    "ukraine": "Ukraine",
    
    # Romania
    "romania": "Romania",
    
    # Croatia
    "croatia": "Croatia",
    
    # Slovenia
    "slovenia": "Slovenia",
    
    # Slovakia
    "slovakia": "Slovakia",
    
    # Serbia
    "serbia": "Serbia",
    
    # Bulgaria
    "bulgaria": "Bulgaria",
    
    # Estonia
    "estonia": "Estonia",
    
    # Latvia
    "latvia": "Latvia",
    
    # Lithuania
    "lithuania": "Lithuania",
    
    # Luxembourg
    "luxembourg": "Luxembourg",
    
    # Iceland
    "iceland": "Iceland",
    
    # Cyprus
    "cyprus": "Cyprus",
    
    # Malta
    "malta": "Malta",
    
    # Qatar
    "qatar": "Qatar",
    
    # Kuwait
    "kuwait": "Kuwait",
    
    # Oman
    "oman": "Oman",
    
    # Jordan
    "jordan": "Jordan",
    
    # Lebanon
    "lebanon": "Lebanon",
    
    # Iraq
    "iraq": "Iraq",
    
    # Bangladesh
    "bangladesh": "Bangladesh",
    
    # Sri Lanka
    "sri lanka": "Sri Lanka",
    
    # Nepal
    "nepal": "Nepal",
    
    # Kenya
    "kenya": "Kenya",
    
    # Ethiopia
    "ethiopia": "Ethiopia",
    
    # Ghana
    "ghana": "Ghana",
    
    # Morocco
    "morocco": "Morocco",
    
    # Tunisia
    "tunisia": "Tunisia",
    
    # Algeria
    "algeria": "Algeria",
    "dza": "Algeria",
    
    # Peru
    "peru": "Peru",
    "perú": "Peru",
    "per": "Peru",
    
    # Uruguay
    "uruguay": "Uruguay",
    "ury": "Uruguay",
    
    # Venezuela
    "venezuela": "Venezuela",
    "ven": "Venezuela",
    
    # Ecuador
    "ecuador": "Ecuador",
    "ecu": "Ecuador",
    
    # Additional ISO-3 Codes & Aliases
    "ind": "India",
    "gbr": "United Kingdom",
    "chn": "China",
    "jpn": "Japan",
    "deu": "Germany",
    "fra": "France",
    "can": "Canada",
    "aus": "Australia",
    "ita": "Italy",
    "esp": "Spain",
    "bra": "Brazil",
    "kor": "South Korea",
    "prk": "North Korea",
    "nld": "Netherlands",
    "che": "Switzerland",
    "swe": "Sweden",
    "bel": "Belgium",
    "aut": "Austria",
    "pol": "Poland",
    "rus": "Russia",
    "twn": "Taiwan",
    "hkg": "Hong Kong",
    "sgp": "Singapore",
    "isr": "Israel",
    "irn": "Iran",
    "sau": "Saudi Arabia",
    "tur": "Turkey",
    "dnk": "Denmark",
    "nor": "Norway",
    "fin": "Finland",
    "irl": "Ireland",
    "prt": "Portugal",
    "grc": "Greece",
    "cze": "Czech Republic",
    "hun": "Hungary",
    "mex": "Mexico",
    "arg": "Argentina",
    "chl": "Chile",
    "col": "Colombia",
    "egy": "Egypt",
    "zaf": "South Africa",
    "nzl": "New Zealand",
    "pak": "Pakistan",
    "nga": "Nigeria",
    "mys": "Malaysia",
    "tha": "Thailand",
    "vnm": "Vietnam",
    "idn": "Indonesia",
    "are": "United Arab Emirates",
    "phl": "Philippines",
    "ukr": "Ukraine",
    "rou": "Romania",
    "hrv": "Croatia",
    "svn": "Slovenia",
    "svk": "Slovakia",
    "srb": "Serbia",
    "bgr": "Bulgaria",
    "est": "Estonia",
    "lva": "Latvia",
    "ltu": "Lithuania",
    "lux": "Luxembourg",
    "isl": "Iceland",
    "cyp": "Cyprus",
    "mlt": "Malta",
    "qat": "Qatar",
    "kwt": "Kuwait",
    "omn": "Oman",
    "jor": "Jordan",
    "lbn": "Lebanon",
    "irq": "Iraq",
    "bgd": "Bangladesh",
    "lka": "Sri Lanka",
    "npl": "Nepal",
    "ken": "Kenya",
    "eth": "Ethiopia",
    "gha": "Ghana",
    "mar": "Morocco",
    "tun": "Tunisia",

    # Full US State Names
    "california": "United States",
    "massachusetts": "United States",
    "new york": "United States",
    "texas": "United States",
    "illinois": "United States",
    "washington": "United States",
    "pennsylvania": "United States",
    "ohio": "United States",
    "michigan": "United States",
    "north carolina": "United States",
    "virginia": "United States",
    "georgia": "United States",
    "colorado": "United States",
    "minnesota": "United States",
    "florida": "United States",
    "maryland": "United States",
    "new jersey": "United States",
    "connecticut": "United States",
    "wisconsin": "United States",
    "indiana": "United States",
    "missouri": "United States",
    "tennessee": "United States",
    "alabama": "United States",
    "arizona": "United States",
    "oregon": "United States",
    "kentucky": "United States",
    "louisiana": "United States",
    "oklahoma": "United States",
    "south carolina": "United States",
    "iowa": "United States",
    "kansas": "United States",
    "utah": "United States",
    "nevada": "United States",
    "new mexico": "United States",
    "nebraska": "United States",
    "idaho": "United States",
    "west virginia": "United States",
    "hawaii": "United States",
    "new hampshire": "United States",
    "maine": "United States",
    "rhode island": "United States",
    "montana": "United States",
    "delaware": "United States",
    "south dakota": "United States",
    "north dakota": "United States",
    "alaska": "United States",
    "vermont": "United States",
    "wyoming": "United States",
}

# Short aliases that require strict uppercase or word boundary matching to avoid
# false positives (e.g., "us" in "virus", "in" in "insulin", "it" in "unit").
CASE_SENSITIVE_ALIASES: Set[str] = {
    "US", "U.S.", "USA", "U.S.A.", "UK", "U.K.", "PRC", "P.R.C.", "KSA", "UAE", "U.A.E.", "HK", "ROC",
    "IND", "GBR", "CHN", "JPN", "DEU", "FRA", "CAN", "AUS", "ITA", "ESP", "BRA", "KOR", "PRK", "NLD", "CHE",
    "SWE", "BEL", "AUT", "POL", "RUS", "TWN", "HKG", "SGP", "ISR", "IRN", "SAU", "TUR", "DNK", "NOR", "FIN",
    "IRL", "PRT", "GRC", "CZE", "HUN", "MEX", "ARG", "CHL", "COL", "EGY", "ZAF", "NZL", "PAK", "NGA", "MYS",
    "THA", "VNM", "IDN", "ARE", "PHL", "UKR", "ROU", "HRV", "SVN", "SVK", "SRB", "BGR", "EST", "LVA", "LTU",
    "LUX", "ISL", "CYP", "MLT", "QAT", "KWT", "OMN", "JOR", "LBN", "IRQ", "BGD", "LKA", "NPL", "KEN", "ETH",
    "GHA", "MAR", "TUN", "DZA", "PER", "URY", "VEN", "ECU"
}

# Pre-compiled regex for US State 2-letter postal code in address context (e.g., ", MA," or ", CA 94305")
US_STATE_ADDRESS_PAT = re.compile(
    r'(?<=,\s)\b(AL|AK|AZ|AR|CA|CO|CT|DE|FL|GA|HI|ID|IL|IN|IA|KS|KY|LA|ME|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|OH|OK|OR|PA|RI|SC|SD|TN|TX|UT|VT|VA|WA|WV|WI|WY|DC)\b(?=\s*\d{5}|\s*[,;\.]|$)',
    re.IGNORECASE
)


def normalize_country_name(name: str) -> Optional[str]:
    """
    Normalize a raw country string or variant to its canonical country name.
    Returns None if the input is not recognized as a valid country.
    """
    if not name or not isinstance(name, str):
        return None
    
    cleaned = name.strip().strip("\t\n\r,;:()[]{}'\"")
    if not cleaned:
        return None
    
    lowered = cleaned.lower()
    res = COUNTRY_ALIASES.get(lowered)
    if res:
        return res
    if lowered.endswith('.'):
        res = COUNTRY_ALIASES.get(lowered.rstrip('.'))
        if res:
            return res
    return None


import functools

# Pre-compiled regex patterns for all aliases sorted by length descending for maximum performance
COMPILED_ALIASES: List[Tuple[re.Pattern, str]] = []
for _alias in sorted(COUNTRY_ALIASES.keys(), key=len, reverse=True):
    _canonical = COUNTRY_ALIASES[_alias]
    _upper_alias = _alias.upper()
    if _upper_alias in CASE_SENSITIVE_ALIASES:
        _pat = re.compile(r'(?<![a-zA-Z0-9])' + re.escape(_upper_alias) + r'(?![a-zA-Z0-9])')
    else:
        _pat = re.compile(r'(?<![a-zA-Z0-9])' + re.escape(_alias) + r'(?![a-zA-Z0-9])', re.IGNORECASE)
    COMPILED_ALIASES.append((_pat, _canonical))


@functools.lru_cache(maxsize=32768)
def _cached_extract_countries_tuple(cleaned_text: str) -> Tuple[str, ...]:
    """LRU-cached extraction worker returning immutable tuples for fast lookups."""
    found_countries: List[str] = []
    seen: Set[str] = set()

    for pattern, canonical in COMPILED_ALIASES:
        if pattern.search(cleaned_text):
            if canonical not in seen:
                seen.add(canonical)
                found_countries.append(canonical)

    if "United States" not in seen and US_STATE_ADDRESS_PAT.search(cleaned_text):
        seen.add("United States")
        found_countries.append("United States")

    return tuple(found_countries)


def extract_countries_from_text(text: str) -> List[str]:
    """
    Extract all unique canonical country names from a single affiliation text string.
    Uses pre-compiled regexes and LRU caching for ultra-fast extraction across large datasets.
    """
    if not text or not isinstance(text, str):
        return []
        
    cleaned_text = text.strip()
    if not cleaned_text or cleaned_text.lower() in {"nan", "none", "null"}:
        return []

    return list(_cached_extract_countries_tuple(cleaned_text))



def extract_countries_from_affiliations(affiliations: Any) -> List[str]:
    """
    Extract unique canonical country names from arbitrary affiliation input types:
    - String (e.g., single affiliation string or semicolon/comma-separated)
    - List of strings (e.g., ["Harvard, USA", "Oxford, UK"])
    - List of dictionaries (e.g., [{"affiliation": "Harvard, USA"}, ...])
    - JSON-encoded string representation
    - Missing / NaN / None values
    
    Returns a deduplicated list of canonical country names for the paper.
    """
    if affiliations is None:
        return []
        
    # Handle pandas NaN
    if isinstance(affiliations, float):
        return []

    lines_to_process: List[str] = []

    if isinstance(affiliations, list):
        for item in affiliations:
            if isinstance(item, str):
                lines_to_process.append(item)
            elif isinstance(item, dict):
                aff_val = item.get("affiliation") or item.get("affiliations") or item.get("address")
                if isinstance(aff_val, str):
                    lines_to_process.append(aff_val)
                elif isinstance(aff_val, list):
                    lines_to_process.extend([str(sub) for sub in aff_val if sub])
    elif isinstance(affiliations, dict):
        aff_val = affiliations.get("affiliation") or affiliations.get("affiliations") or affiliations.get("address")
        if isinstance(aff_val, str):
            lines_to_process.append(aff_val)
        elif isinstance(aff_val, list):
            lines_to_process.extend([str(sub) for sub in aff_val if sub])
    elif isinstance(affiliations, str):
        text = affiliations.strip()
        if not text or text.lower() in {"nan", "none", "null", "[]", "{}"}:
            return []
            
        # Try parsing JSON or Python literal if formatted as list string
        if (text.startswith("[") and text.endswith("]")) or (text.startswith("{") and text.endswith("}")):
            try:
                parsed = ast.literal_eval(text)
                return extract_countries_from_affiliations(parsed)
            except Exception:
                pass
        
        # Split on semicolons or newlines if multiple affiliations are merged into one string
        if ";" in text:
            lines_to_process.extend([part.strip() for part in text.split(";") if part.strip()])
        else:
            lines_to_process.append(text)

    # Extract countries across all gathered lines
    paper_countries: List[str] = []
    seen: Set[str] = set()

    for line in lines_to_process:
        extracted = extract_countries_from_text(line)
        for country in extracted:
            if country not in seen:
                seen.add(country)
                paper_countries.append(country)

    return paper_countries


# ISO 3166-1 alpha-3 code mapping for canonical country names
COUNTRY_ISO3_MAP: Dict[str, str] = {
    "United States": "USA",
    "United Kingdom": "GBR",
    "China": "CHN",
    "India": "IND",
    "Japan": "JPN",
    "Germany": "DEU",
    "France": "FRA",
    "Canada": "CAN",
    "Australia": "AUS",
    "Italy": "ITA",
    "Spain": "ESP",
    "Brazil": "BRA",
    "South Korea": "KOR",
    "North Korea": "PRK",
    "Netherlands": "NLD",
    "Switzerland": "CHE",
    "Sweden": "SWE",
    "Belgium": "BEL",
    "Austria": "AUT",
    "Poland": "POL",
    "Russia": "RUS",
    "Taiwan": "TWN",
    "Hong Kong": "HKG",
    "Singapore": "SGP",
    "Israel": "ISR",
    "Iran": "IRN",
    "Saudi Arabia": "SAU",
    "Turkey": "TUR",
    "Denmark": "DNK",
    "Norway": "NOR",
    "Finland": "FIN",
    "Ireland": "IRL",
    "Portugal": "PRT",
    "Greece": "GRC",
    "Czech Republic": "CZE",
    "Hungary": "HUN",
    "Mexico": "MEX",
    "Argentina": "ARG",
    "Chile": "CHL",
    "Colombia": "COL",
    "Egypt": "EGY",
    "South Africa": "ZAF",
    "New Zealand": "NZL",
    "Pakistan": "PAK",
    "Nigeria": "NGA",
    "Malaysia": "MYS",
    "Thailand": "THA",
    "Vietnam": "VNM",
    "Indonesia": "IDN",
    "United Arab Emirates": "ARE",
    "Philippines": "PHL",
    "Ukraine": "UKR",
    "Romania": "ROU",
    "Croatia": "HRV",
    "Slovenia": "SVN",
    "Slovakia": "SVK",
    "Serbia": "SRB",
    "Bulgaria": "BGR",
    "Estonia": "EST",
    "Latvia": "LVA",
    "Lithuania": "LTU",
    "Luxembourg": "LUX",
    "Iceland": "ISL",
    "Cyprus": "CYP",
    "Malta": "MLT",
    "Qatar": "QAT",
    "Kuwait": "KWT",
    "Oman": "OMN",
    "Jordan": "JOR",
    "Lebanon": "LBN",
    "Iraq": "IRQ",
    "Bangladesh": "BGD",
    "Sri Lanka": "LKA",
    "Nepal": "NPL",
    "Kenya": "KEN",
    "Ethiopia": "ETH",
    "Ghana": "GHA",
    "Morocco": "MAR",
    "Tunisia": "TUN",
    "Algeria": "DZA",
    "Peru": "PER",
    "Uruguay": "URY",
    "Venezuela": "VEN",
    "Ecuador": "ECU",
}


def get_country_iso3(country_name: str) -> Optional[str]:
    """
    Get ISO 3166-1 alpha-3 code for a canonical country name.
    Returns None if the country is unmapped.
    """
    if not country_name or not isinstance(country_name, str):
        return None
    canonical = normalize_country_name(country_name) or country_name.strip()
    return COUNTRY_ISO3_MAP.get(canonical)

