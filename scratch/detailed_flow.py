import zipfile
import xml.etree.ElementTree as ET

pptx_path = r'C:\Users\AkashDeep\.gemini\antigravity\brain\9cc2b58b-563a-426d-91ff-76790ac91454\.user_uploaded\media_1795086816454_604f38b2.pptx'

def detailed_flow(slide_num):
    with zipfile.ZipFile(pptx_path, 'r') as z:
        root = ET.fromstring(z.read(f'ppt/slides/slide{slide_num}.xml'))
    ns = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
          'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}
    
    shapes = {}
    for sp in root.iter('{http://schemas.openxmlformats.org/presentationml/2006/main}sp'):
        cNvPr = sp.find('.//p:cNvPr', ns)
        sid = cNvPr.attrib.get('id', '') if cNvPr is not None else ''
        xfrm = sp.find('.//a:xfrm', ns)
        if xfrm is not None:
            off = xfrm.find('a:off', ns)
            ext = xfrm.find('a:ext', ns)
            x = int(off.attrib['x']) if off is not None else 0
            y = int(off.attrib['y']) if off is not None else 0
            cx = int(ext.attrib['cx']) if ext is not None else 0
            cy = int(ext.attrib['cy']) if ext is not None else 0
        else:
            x, y, cx, cy = 0, 0, 0, 0
        paragraphs = []
        for p in sp.findall('.//a:p', ns):
            t_list = [t.text for t in p.findall('.//a:t', ns) if t.text]
            if t_list:
                paragraphs.append(''.join(t_list))
        text = ' / '.join(paragraphs).strip()
        if text:
            shapes[sid] = {'text': text, 'box': (x, y, cx, cy)}
            
    print(f"=== SLIDE {slide_num} BOXES ===")
    for sid, s in shapes.items():
        print(f"[{sid}] (x:{s['box'][0]//1000}, y:{s['box'][1]//1000}, w:{s['box'][2]//1000}, h:{s['box'][3]//1000}): {s['text']}")

    print(f"\n=== SLIDE {slide_num} CONNECTORS ===")
    for cxn in root.iter('{http://schemas.openxmlformats.org/presentationml/2006/main}cxnSp'):
        cNvPr = cxn.find('.//p:cNvPr', ns)
        cid = cNvPr.attrib.get('id', '') if cNvPr is not None else ''
        xfrm = cxn.find('.//a:xfrm', ns)
        flipH = xfrm.attrib.get('flipH', '0') if xfrm is not None else '0'
        flipV = xfrm.attrib.get('flipV', '0') if xfrm is not None else '0'
        off = xfrm.find('a:off', ns)
        ext = xfrm.find('a:ext', ns)
        x = int(off.attrib['x']) if off is not None else 0
        y = int(off.attrib['y']) if off is not None else 0
        cx = int(ext.attrib['cx']) if ext is not None else 0
        cy = int(ext.attrib['cy']) if ext is not None else 0
        
        x1 = x + cx if flipH == '1' else x
        x2 = x if flipH == '1' else x + cx
        y1 = y + cy if flipV == '1' else y
        y2 = y if flipV == '1' else y + cy
        
        ln = cxn.find('.//p:spPr/a:ln', ns)
        headEnd = ln.find('a:headEnd', ns) if ln is not None else None
        tailEnd = ln.find('a:tailEnd', ns) if ln is not None else None
        headType = headEnd.attrib.get('type', 'none') if headEnd is not None else 'none'
        tailType = tailEnd.attrib.get('type', 'none') if tailEnd is not None else 'none'
        
        # Determine actual from/to based on arrow heads
        # If tailType == 'triangle', arrow points to start (x1, y1), or if headType == 'triangle' points to (x2, y2)
        # Find which shape is near (x1, y1) and (x2, y2)
        def find_near(px, py):
            best = None
            min_dist = float('inf')
            for sid, s in shapes.items():
                bx, by, bcx, bcy = s['box']
                # distance to box
                dx = max(bx - px, 0, px - (bx + bcx))
                dy = max(by - py, 0, py - (by + bcy))
                dist = (dx*dx + dy*dy)**0.5
                if dist < min_dist:
                    min_dist = dist
                    best = sid
            return best, min_dist
            
        near1, d1 = find_near(x1, y1)
        near2, d2 = find_near(x2, y2)
        
        t1 = shapes[near1]['text'] if near1 else '?'
        t2 = shapes[near2]['text'] if near2 else '?'
        
        print(f"Cxn [{cid}] from ({x1//1000},{y1//1000}) near [{near1}:{t1[:25]}] (d={d1//1000}) -> to ({x2//1000},{y2//1000}) near [{near2}:{t2[:25]}] (d={d2//1000}) | tail={tailType}, head={headType}")

detailed_flow(1)
detailed_flow(2)
