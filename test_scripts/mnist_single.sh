#!/usr/bin/env bash

for network in net_28 alex_28 dense_28 mynet_28
do
    for data in mnist
    do
        for loss in CrossEntropyLoss MultiMarginLoss  FocalLoss SoftmaxLoss CenterLoss CenterLoss2  MultiClassHingeLoss HistogramLoss
        do
               timeout 1200s python  evaluate/svm.py --data_path results/${data}/${network}/${loss}
        done
    done
done