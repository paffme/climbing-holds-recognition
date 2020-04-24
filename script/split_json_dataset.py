import json
from argparse import Namespace

if __name__ == '__main__':
    import argparse

    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='Split coco dataset with train conf and val conf.')
    parser.add_argument("--coco-file",
                        metavar="/path/and/file/name",
                        help="Enter valid coco file with train and val as subdir")
    args = parser.parse_args()

    with open(args.coco_file, "r") as read_file:
        coco_file = json.load(read_file)

        coco_train_files = []
        train_img_id = []
        coco_val_files = []
        val_img_id = []

        for img in coco_file['images']:
            if str(img['path']).find("/train/") != -1:
                coco_train_files.append(img)
                train_img_id.append(img["id"])

            if str(img['path']).find("/val/") != -1:
                coco_val_files.append(img)
                val_img_id.append(img["id"])

        coco_train_anns = []
        coco_val_anns = []

        for ann in coco_file['annotations']:
            if ann['image_id'] in train_img_id:
                coco_train_anns.append(ann)
            elif ann['image_id'] in val_img_id:
                coco_val_anns.append(ann)

        # print(coco_train_files)

        coco_train = json.dumps({'images': coco_train_files,
                                 'categories': coco_file['categories'],
                                 'annotations': coco_train_anns},
                                indent=4
                                )
        coco_val = json.dumps({'images': coco_val_files,
                               'categories': coco_file['categories'],
                               'annotations': coco_val_anns},
                              indent=4
                              )

        indexStart = str(args.coco_file).rindex("/")
        indexEnd = str(args.coco_file).rindex(".json")

        path = args.coco_file[0: indexStart]

        with open(path + "/train" + args.coco_file[indexStart: indexEnd] + "_train.json", 'w') as outfile:
            outfile.write(coco_train)
        with open(path + "/val" + args.coco_file[indexStart: indexEnd] + "_val.json", 'w') as outfile:
            outfile.write(coco_val)
