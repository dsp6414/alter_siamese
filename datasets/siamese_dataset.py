import random

import PIL.ImageOps
import numpy as np
import torch
from PIL import Image
from torch.utils.data import Dataset

random.seed(1137)
np.random.seed(1137)


class SiameseNetworkDataset(Dataset):
    def __init__(self, image_folder_dataset, transform=None, should_invert=True, channel=1, negative=0, positive=1,
                 train=True):
        self.train = train
        self.image_folder_dataset = image_folder_dataset
        self.transform = transform
        self.should_invert = should_invert
        self.channel = channel
        self.counter = 0
        self.negative = negative
        self.positive = positive
        self.num_inputs = 2
        self.num_targets = 1

    def get_eval_items(self, index):
        img0_tuple = self.image_folder_dataset.imgs[self.counter]
        # we need to make sure approx 50% of images are in the same class
        self.counter += 1
        img0 = Image.open(img0_tuple[0])
        if self.channel == 1:
            img0 = img0.convert("L")
        elif self.channel == 3:
            img0 = img0.convert("RGB")

        if self.should_invert:
            img0 = PIL.ImageOps.invert(img0)

        if self.transform is not None:
            img0 = self.transform(img0)
        return (img0, img0), img0_tuple[1]

    def get_train_items(self, index):
        img0_tuple = random.choice(self.image_folder_dataset.imgs)
        # we need to make sure approx 50% of images are in the same class
        should_get_same_class = random.randint(0, 1)
        if not should_get_same_class:
            while True:
                # keep looping till the same class image is found
                img1_tuple = random.choice(self.image_folder_dataset.imgs)
                if img0_tuple[1] == img1_tuple[1]:
                    break
        else:
            img1_tuple = random.choice(self.image_folder_dataset.imgs)

        img0 = Image.open(img0_tuple[0])
        img1 = Image.open(img1_tuple[0])
        if self.channel == 1:
            img0 = img0.convert("L")
            img1 = img1.convert("L")
        elif self.channel == 3:
            img0 = img0.convert("RGB")
            img1 = img1.convert("RGB")

        if self.should_invert:
            img0 = PIL.ImageOps.invert(img0)
            img1 = PIL.ImageOps.invert(img1)

        if self.transform is not None:
            img0 = self.transform(img0)
            img1 = self.transform(img1)
        if img1_tuple[1] == img0_tuple[1]:
            label = torch.FloatTensor([float(self.positive)])
        else:
            label = torch.FloatTensor([float(self.negative)])
        return (img0, img1), label

    def __getitem__(self, index):
        if self.train:
            return self.get_eval_items(index)
        return self.get_eval_items(index)

    def __len__(self):
        if self.train:
            return len(self.image_folder_dataset.imgs)
        return len(self.image_folder_dataset.imgs)
