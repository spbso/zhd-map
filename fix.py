from pathlib import Path
from lxml import etree


if __name__ == '__main__':
    frame = Path.cwd() / "src" / "data" / "Frame2.svg"
    root = etree.XML(frame.read_text())
    for element in root.iter('{http://www.w3.org/2000/svg}circle'):
        cx = element.get('cx')
        cy = element.get('cy')
        element.set('cx', str(int(cx)-10))
        element.set('cy', str(int(cy)-10))

    print(etree.tostring(root, pretty_print=True).decode('utf-8'))


