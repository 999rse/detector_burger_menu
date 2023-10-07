import json
import os

import torch
from torch.utils.data import Dataset
from torchvision.io import read_image
from torchvision.transforms import ToPILImage

from PIL import Image

class BurgerMenu_Dataset(Dataset):
    def __init__(self, path2dataset, transform=None) -> None:
        self.data = self.load_data_from_json(path2dataset)
        self.transform = transform
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, index) -> tuple:
        image_path = self.data[index]['image_path']
        image = read_image(image_path)

        annotation = self.data[index]['annotation']

        if self.transform:
            tpi = ToPILImage()
            image = self.transform(tpi(image))
        
        return image, annotation

    def load_data_from_json(self, path2dataset):
        try:
            data_json_path = os.path.join(path2dataset, [x for x in os.listdir(path2dataset) if x.endswith('.json')][0])
        except:
             FileNotFoundError
        with open(data_json_path, 'r')  as file:
            data_json = json.load(file)

        data = []

        for img_filename, img_data in data_json['_via_img_metadata'].items():
            img_path = os.path.join(path2dataset, img_data['filename'])
            regions = img_data['regions']

            for region in regions:
                shape_attributes = region['shape_attributes']
                annotation = {
                    'image_path': img_path,
                    'annotation': {
                        'x': shape_attributes['x'],
                        'y': shape_attributes['y'],
                        'width': shape_attributes['width'],
                        'height': shape_attributes['height']
                    }
                }   
                data.append(annotation)
        
        return data    

    def load_image(self, image_path):
        return Image.open(image_path)
    