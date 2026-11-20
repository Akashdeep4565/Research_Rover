import zipfile
import xml.etree.ElementTree as ET

pptx_path = r'C:\Users\AkashDeep\.gemini\antigravity\brain\9cc2b58b-563a-426d-91ff-76790ac91454\.user_uploaded\media_1795086816454_604f38b2.pptx'

with zipfile.ZipFile(pptx_path, 'r') as z:
    root = ET.fromstring(z.read('ppt/slides/slide2.xml'))
    ns = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
          'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}
    
    print("SLIDE 2 CONNECTORS:")
    for cxn in root.iter('{http://schemas.openxmlformats.org/presentationml/2006/main}cxnSp'):
        cNvPr = cxn.find('.//p:cNvPr', ns)
        name = cNvPr.attrib.get('name', '') if cNvPr is not None else ''
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
        
        # Check arrow heads in spPr -> ln -> headEnd / tailEnd
        ln = cxn.find('.//p:spPr/a:ln', ns)
        headEnd = ln.find('a:headEnd', ns) if ln is not None else None
        tailEnd = ln.find('a:tailEnd', ns) if ln is not None else None
        headType = headEnd.attrib.get('type', 'none') if headEnd is not None else 'none'
        tailType = tailEnd.attrib.get('type', 'none') if tailEnd is not None else 'none'
        
        print(f"Cxn [ID:{cid}] '{name}' from ({x1//1000},{y1//1000}) to ({x2//1000},{y2//1000}) | tail:{tailType} -> head:{headType}")
