from pathlib import Path
from lxml import etree
from datauri import DataURI


if __name__ == '__main__':
    frame = Path.cwd() / "src" / "data" / "Frame 1.svg"
    root = etree.XML(frame.read_text())
    for element in root.iter('{http://www.w3.org/2000/svg}image'):
        file_id = element.get('id')
        width = element.get('width')
        height = element.get('height')
        data = element.get('{http://www.w3.org/1999/xlink}href')
        uri = DataURI(data)
        extension = "jpg" if uri.mimetype == "image/jpeg" else "png"
        filename = f"{file_id}-{width}-{height}.{extension}"
        with open(filename, 'rb') as f:
            data = f.read()
            new_uri = DataURI.make(uri.mimetype, charset=None, base64=True, data=data)
            element.set('{http://www.w3.org/1999/xlink}href', str(new_uri))

    print(etree.tostring(root, pretty_print=True).decode('utf-8'))


