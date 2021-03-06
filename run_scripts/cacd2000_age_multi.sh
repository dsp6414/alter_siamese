#!/usr/bin/env bash

# 163446

EPOCHS=500
for network in net_64 alex_64 dense_64
do
    for data in cacd2000_age
    do
        # Siamese
        for loss in  ContrastiveLoss
        do
              python __main__.py siamese --data_name $data  --width 64 --height 64 --channel 3 \
                --network siamese_${network} --embedding 128 --epochs $EPOCHS --loss $loss --negative 1 --positive 0 \
                 --loader_name pair_loaders
        done
        for loss in  CosineEmbeddingLoss
        do
              python __main__.py siamese --data_name $data  --width 64 --height 64 --channel 3 \
                --network siamese_${network} --embedding 128 --epochs $EPOCHS --loss $loss --negative -1 --positive 1 \
                 --loader_name pair_loaders
        done
        # Triplet
        for loss in TripletMarginLoss
        do
              python __main__.py triplet --data_name $data  --width 64 --height 64 --channel 3 \
                --network triplet_${network} --embedding 128 --epochs $EPOCHS --loss $loss  --loader_name triplet_loaders
        done
    done
done