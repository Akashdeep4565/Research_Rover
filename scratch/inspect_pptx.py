import zipfile
import xml.etree.ElementTree as ET

pptx_path = r'C:\Users\AkashDeep\.gemini\antigravity\brain\9cc2b58b-563a-426d-91ff-76790ac91454\.user_uploaded\media_1795086816454_604f38b2.pptx'

def dump_slide_structure(slide_xml_bytes, slide_num):
    root = ET.fromstring(slide_xml_bytes)
    ns = {
        'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'
    }
    
    print('='*80)
    print(f'SLIDE {slide_num} DETAILED SHAPE & CONNECTOR DUMP')
    print('='*80)
    
    spTree = root.find('.//p:spTree', ns)
    if spTree is None:
        print('No spTree found')
        return

    # Recursive function for groups and shapes
    def process_container(container, indent=''):
        for elem in container:
            tag = elem.tag.split('}')[-1]
            
            if tag == 'sp':
                cNvPr = elem.find('.//p:cNvPr', ns)
                name = cNvPr.attrib.get('name', '') if cNvPr is not None else ''
                shape_id = cNvPr.attrib.get('id', '') if cNvPr is not None else ''
                
                xfrm = elem.find('.//a:xfrm', ns)
                off = xfrm.find('a:off', ns) if xfrm is not None else None
                ext = xfrm.find('a:ext', ns) if xfrm is not None else None
                pos_str = f"pos:({off.attrib.get('x')},{off.attrib.get('y')}) size:({ext.attrib.get('cx')},{ext.attrib.get('cy')})" if off is not None and ext is not None else ''
                
                text_runs = []
                for p in elem.findall('.//a:p', ns):
                    p_text = ' '.join([t.text for t in p.findall('.//a:t', ns) if t.text]).strip()
                    if p_text:
                        text_runs.append(p_text)
                full_text = ' | '.join(text_runs).strip()
                
                prstGeom = elem.find('.//a:prstGeom', ns)
                geom = prstGeom.attrib.get('prst', '') if prstGeom is not None else 'custom'
                
                print(f'{indent}[Shape {shape_id}] "{name}" ({geom}) {pos_str}')
                if full_text:
                    print(f'{indent}     Text: "{full_text}"')
                    
            elif tag == 'grpSp':
                cNvPr = elem.find('.//p:cNvPr', ns)
                name = cNvPr.attrib.get('name', '') if cNvPr is not None else ''
                shape_id = cNvPr.attrib.get('id', '') if cNvPr is not None else ''
                print(f'{indent}[GroupShape {shape_id}] "{name}"')
                process_container(elem, indent + '  ')
                
            elif tag == 'cxnSp':
                cNvPr = elem.find('.//p:cNvPr', ns)
                name = cNvPr.attrib.get('name', '') if cNvPr is not None else ''
                shape_id = cNvPr.attrib.get('id', '') if cNvPr is not None else ''
                
                cNvCxnPr = elem.find('.//p:cNvCxnPr', ns)
                stCxn = cNvCxnPr.find('a:stCxn', ns) if cNvCxnPr is not None else None
                endCxn = cNvCxnPr.find('a:endCxn', ns) if cNvCxnPr is not None else None
                st_id = stCxn.attrib.get('id', 'None') if stCxn is not None else 'None'
                st_idx = stCxn.attrib.get('idx', '') if stCxn is not None else ''
                end_id = endCxn.attrib.get('id', 'None') if endCxn is not None else 'None'
                end_idx = endCxn.attrib.get('idx', '') if endCxn is not None else ''
                
                print(f'{indent}[Connector {shape_id}] "{name}": from Shape {st_id} (idx:{st_idx}) -> Shape {end_id} (idx:{end_idx})')

    process_container(spTree)

with zipfile.ZipFile(pptx_path, 'r') as z:
    for i in (1, 2):
        dump_slide_structure(z.read(f'ppt/slides/slide{i}.xml'), i)
