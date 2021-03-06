#!/usr/bin/env bash

# 50000

EPOCHS=500
for network in net_32 alex_32 dense_32
do
    for data in cifar100
    do
        # Siamese
        for loss in  ContrastiveLoss
        do
              python __main__.py siamese --data_name $data  --width 32 --height 32 --channel 3 \
                --network siamese_${network} --embedding 128 --epochs $EPOCHS --loss $loss --negative 1 --positive 0 \
                 --loader_name pair_loaders
        done
        for loss in  CosineEmbeddingLoss
        do
              python __main__.py siamese --data_name $data  --width 32 --height 32 --channel 3 \
                --network siamese_${network} --embedding 128 --epochs $EPOCHS --loss $loss --negative -1 --positive 1 \
                 --loader_name pair_loaders
        done

        # Triplet
        for loss in TripletMarginLoss
        do
              python __main__.py triplet --data_name $data  --width 32 --height 32 --channel 3 \
                --network triplet_${network} --embedding 128 --epochs $EPOCHS --loss $loss  --loader_name triplet_loaders
        done
    done
done