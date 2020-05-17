import xml.etree.ElementTree as ET


def xml_parsing(tree):
    root = tree.getroot()
    bounding_boxes = []
    for child in root.iter('object'):
        for name, box in zip(child.findall("name"), child.findall("bndbox")):
            x1, y1, x2, y2 = int(box.find("xmin").text), int(box.find("ymin").text), int(box.find("xmax").text), \
                             int(box.find("ymax").text)
            bounding_boxes.append([name.text, x1, y1, x2, y2])
    return bounding_boxes


def get_row_wise_boxes(bboxes):
    i = 0  # for looping over all the bounding boxes present
    j = 1  # for checking the next box is in same row as the previous box
    box = []  # temp variable for storing the collected boxes of the same row
    row_list = []  # list of list for row wise boxes
    # sorting with x2 and y2 coordinates because we can consider the corner point of bounding box as base
    # line for a row.
    bboxes = sorted(bboxes, key=lambda k: [k[4], k[3]])  # sorting based on ymin coordinate
    while i < len(bboxes) and j < len(bboxes):  # boundary condition for the loop
        # approximating error distance in Y-AXIS direction for boxes
        # this threshold for considering a box in same row I have considered some approximation around 15
        if abs(bboxes[j][4] - bboxes[i][4]) <= 15:
            # present in a row.
            # we go on adding the boxes which are in same row to this lis
            box.append(bboxes[j - 1])
            j += 1
        else:  # if the box is not present in the same row.
            # we append the last box which stored in the box
            box.append(bboxes[j - 1])
            row_list.append(box)  # append to all the row boxes to another list
            # the pointer should go to the box which will come in the next row.
            i += len(box)
            j = j + 1  # increasing the pointer counter of the box
            box = []  # emptying the temporary variable box list.
    # at the end the of loop after exiting every page last combined list will be there in the list
    if j - 1 < len(bboxes):
        box.append(bboxes[j - 1])  # append that last box to the list
    if box:  # checking for if box is not empty then only appending the whole row boxes to row_list variable
        row_list.append(box)
    return row_list


def main():
    tree = ET.parse('./AP04V5222-6.xml')
    bounding_boxes = xml_parsing(tree)
    row_wise_boxes = get_row_wise_boxes(bounding_boxes)
    final_sorted_list = []
    for row in row_wise_boxes:
        print(row)
        final_sorted_list.extend(sorted(row, key=lambda x: x[1]))  # sort each individual row based xmin coordinate
    print(final_sorted_list)


if __name__ == '__main__':
    main()
