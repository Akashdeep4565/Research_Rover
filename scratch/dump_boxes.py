import zipfile
import xml.etree.ElementTree as ET

pptx_path = r'C:\Users\AkashDeep\.gemini\antigravity\brain\9cc2b58b-563a-426d-91ff-76790ac91454\.user_uploaded\media_1795086816454_604f38b2.pptx'

with zipfile.ZipFile(pptx_path, 'r') as z:
    for slide_idx in [1, 2]:
        root = ET.fromstring(z.read(f'ppt/slides/slide{slide_idx}.xml'))
        ns = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
              'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}
        print(f"\n{'='*40} SLIDE {slide_idx} {'='*40}")
        
        shapes = []
        for sp in root.iter('{http://schemas.openxmlformats.org/presentationml/2006/main}sp'):
            cNvPr = sp.find('.//p:cNvPr', ns)
            name = cNvPr.attrib.get('name', '') if cNvPr is not None else ''
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
            text = ' \n '.join(paragraphs).strip()
            
            # fill color
            fill = 'none'
            solidFill = sp.find('.//a:solidFill', ns)
            if solidFill is not None:
                srgb = solidFill.find('a:srgbClr', ns)
                scheme = solidFill.find('a:schemeClr', ns)
                if srgb is not None:
                    fill = srgb.attrib.get('val', '')
                elif scheme is not None:
                    fill = scheme.attrib.get('val', '')
                    
            shapes.append({'id': sid, 'name': name, 'x': x, 'y': y, 'cx': cx, 'cy': cy, 'text': text, 'fill': fill})
            
        # Sort by y then x
        shapes.sort(key=lambda s: (s['y'], s['x']))
        for s in shapes:
            if s['text']:
                print(f"[ID:{s['id']}] (x:{s['x']//1000}, y:{s['y']//1000}, w:{s['cx']//1000}, h:{s['cy']//1000}) fill:{s['fill']}")
                print(f"   \"{s['text']}\"")
