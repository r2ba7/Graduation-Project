import argparse, shutil
from glob import glob
from os import path
import xml.etree.ElementTree as ET


parser = argparse.ArgumentParser(description='Convert TF xml to Pytorch, Create Text Files, and Move Files.')
parser.add_argument("--source", type=str)
parser.add_argument("--dist_xml", type=str)
parser.add_argument("--dist_jpg", type=str)
parser.add_argument("--textfile", type=str)

args = parser.parse_args()


def adjust_file(f):
    tree = ET.parse(f)
    root = tree.getroot()
    try:
        root.remove(root.find("path"))
    except:
        pass
    for node in list(root):
        if node.tag == "folder":
            node.text = "gp"
        if node.tag == 'source':
            for node2 in list(node):
                if node2.tag == "database":
                    node2.text = "gp"

    tree.write(f, encoding="utf-8")

def move_file(file, source, dist):
    shutil.move(path.join(source, file), path.join(dist, file))

def create_text(text):
    text = text.split(".")[0]
    if not path.exists(str(args.textfile) + '.txt'):
        with open(str(args.textfile) + '.txt', "w") as f:
            f.write(text + "\n")
    else:
        with open(str(args.textfile) + '.txt', "a") as f:
            f.write(text + "\n")
    
if __name__ == '__main__':
    for f, name_xml_test, name_jpg_test in zip(glob(path.join(args.source, "*.xml")), glob("*.xml"), glob("*.jpg")):
        adjust_file(f)
        create_text(name_jpg_test)
        move_file(name_xml_test, args.source, args.dist_xml)
        move_file(name_jpg_test, args.source, args.dist_jpg)
    print("Done!")
