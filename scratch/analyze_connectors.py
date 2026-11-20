import zipfile
import xml.etree.ElementTree as ET

pptx_path = r'C:\Users\AkashDeep\.gemini\antigravity\brain\9cc2b58b-563a-426d-91ff-76790ac91454\.user_uploaded\media_1795086816454_604f38b2.pptx'

def analyze_connectors_and_boxes(slide_xml_bytes, slide_num):
    root = ET.fromstring(slide_xml_bytes)
    ns = {
        'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'
    }
    
    print('='*80)
    print(f'SLIDE {slide_num} CONNECTOR AND BOX MATCHING')
    print('='*80)
    
    shapes = {}
    connectors = []
    
    for elem in root.iter('{http://schemas.openxmlformats.org/presentationml/2006/main}sp'):
        cNvPr = elem.find('.//p:cNvPr', ns)
        sid = cNvPr.attrib.get('id') if cNvPr is not None else None
        name = cNvPr.attrib.get('name') if cNvPr is not None else ''
        
        xfrm = elem.find('.//a:xfrm', ns)
        if xfrm is not None:
            off = xfrm.find('a:off', ns)
            ext = xfrm.find('a:ext', ns)
            if off is not None and ext is not None:
                x = int(off.attrib['x'])
                y = int(off.attrib['y'])
                cx = int(ext.attrib['cx'])
                cy = int(ext.attrib['cy'])
                
                text_runs = []
                for p in elem.findall('.//a:p', ns):
                    p_text = ' '.join([t.text for t in p.findall('.//a:t', ns) if t.text]).strip()
                    if p_text:
                        text_runs.append(p_text)
                text = ' | '.join(text_runs)
                shapes[sid] = {'name': name, 'rect': (x, y, cx, cy), 'text': text}
                
    for elem in root.iter('{http://schemas.openxmlformats.org/presentationml/2006/main}cxnSp'):
        cNvPr = elem.find('.//p:cNvPr', ns)
        cid = cNvPr.attrib.get('id') if cNvPr is not None else None
        name = cNvPr.attrib.get('name') if cNvPr is not None else ''
        
        xfrm = elem.find('.//a:xfrm', ns)
        flipH = xfrm.attrib.get('flipH', '0') if xfrm is not None else '0'
        flipV = xfrm.attrib.get('flipV', '0') if xfrm is not None else '0'
        off = xfrm.find('a:off', ns) if xfrm is not None else None
        ext = xfrm.find('a:ext', ns) if xfrm is not None else None
        x = int(off.attrib['x']) if off is not None else 0
        y = int(off.attrib['y']) if off is not None else 0
        cx = int(ext.attrib['cx']) if ext is not None else 0
        cy = int(ext.attrib['cy']) if ext is not None else 0
        
        # Calculate start and end coordinates of connector
        # Default: from (x, y) to (x+cx, y+cy), adjusted for flips
        x1 = x + cx if flipH == '1' else x
        x2 = x if flipH == '1' else x + cx
        y1 = y + cy if flipV == '1' else y
        y2 = y if flipV == '1' else y + cy
        
        connectors.append({'id': cid, 'name': name, 'start': (x1, y1), 'end': (x2, y2), 'rect': (x, y, cx, cy)})

    print(f'Total shapes: {len(shapes)}, Total connectors: {len(connectors)}')
    
    # Match connectors to nearest shapes
    for c in connectors:
        x1, y1 = c['start']
        x2, y2 = c['end']
        
        # find closest shape to start
        closest_start = None
        min_d1 = float('inf')
        for sid, s in shapes.items():
            sx, sy, scx, scy = s['rect']
            # center of shape
            scx_c = sx + scx / 2
            scy_c = sy + scy / 2
            d = ((x1 - scx_c)**2 + (y1 - scy_c)**2)**0.5
            if d < min_d1:
                min_d1 = d
                closest_start = sid
                
        # find closest shape to end
        closest_end = None
        min_d2 = float('inf')
        for sid, s in shapes.items():
            sx, sy, scx, scy = s['rect']
            scx_c = sx + scx / 2
            scy_c = sy + scy / 2
            d = ((x2 - scx_c)**2 + (y2 - scy_c)**2)**0.5
            if d < min_d2:
                min_d2 = d
                closest_end = sid
                
        s_text = shapes[closest_start]['text'][:30] if closest_start else 'None'
        e_text = shapes[closest_end]['text'][:30] if closest_end else 'None'
        print(f"Connector {c['id']}: [{s_text}] ---> [{e_text}] (start: {c['start']}, end: {c['end']})")

with zipfile.ZipFile(pptx_path, 'r') as z:
    for i in (1, 2):
        analyze_connectors_and_boxes(z.read(f'ppt/slides/slide{i}.xml'), i)
