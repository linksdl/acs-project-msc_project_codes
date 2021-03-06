#!/usr/bin/env python
"""
Train an encoder-decoder network on image/trajectory data.

Loads the synthetic dataset of MNIST-esque digit images and accompanying
trajectories and trains a deep encoder-decoder network to predict DMP parameter
outputs from input images.
"""
from __future__ import print_function

import os
import sys
import argparse
from datetime import datetime
import torch
import numpy as np

from os.path import dirname, realpath
sys.path.append(dirname(dirname(realpath(__file__))))

from imednet.models.encoder_decoder import EncoderDecoderNet, TrainingParameters
from imednet.trainers.encoder_decoder_trainer import Trainer
from imednet.data.smnist_loader import MatLoader

# Save datetime
date = datetime.now()

# Set defaults

default_data_path = os.path.join(dirname(dirname(realpath(__file__))), 'data/s-mnist/40x40-smnist.mat')
default_model_save_path = os.path.join(dirname(dirname(realpath(__file__))),
                                       'models/encoder_decoder',
                                       'imednet-40x40-smnist')

# default_data_path = os.path.join(dirname(dirname(realpath(__file__))), 'data/s-mnist/40x40-smnist-with-awgn.mat')
# default_model_save_path = os.path.join(dirname(dirname(realpath(__file__))),
#                                        'models/encoder_decoder',
#                                        'imednet-40x40-smnist-with-awgn')

# default_data_path = os.path.join(dirname(dirname(realpath(__file__))), 'data/s-mnist/40x40-smnist-with-motion-blur.mat')
# default_model_save_path = os.path.join(dirname(dirname(realpath(__file__))),
#                                        'models/encoder_decoder',
#                                        'imednet-40x40-smnist-with-motion-blur')


# default_data_path = os.path.join(dirname(dirname(realpath(__file__))), 'data/s-mnist/40x40-smnist-with-reduced-contrast-and-awgn.mat')
# default_model_save_path = os.path.join(dirname(dirname(realpath(__file__))),
#                                        'models/encoder_decoder',
#                                        'imednet-40x40-smnist-with-reduced-contrast-and-awgn')

default_model_load_path = None
default_batch_size = 100
default_optimizer = 'adam'
default_learning_rate = 0.001
default_momentum = 0.5
default_lr_decay = None
default_weight_decay = None
default_val_fail = 60
default_hidden_layer_sizes = ['1500', '1300', '1000', '600', '200', '20', '35']

# Parse arguments
description = 'Train an encoder-decoder network on image/trajectory data.'
parser = argparse.ArgumentParser(description=description)
parser.add_argument('--data-path', type=str, default=default_data_path,
                    help='data path (default: "{}")'.format(str(default_data_path)))
parser.add_argument('--model-save-path', type=str, default=default_model_save_path,
                    help='model save path (default: "{}")'.format(str(default_model_save_path)))
parser.add_argument('--model-load-path', type=str, default=None,
                    help='model load path (default: "{}")'.format(str(default_model_load_path)))
parser.add_argument('--launch-tensorboard', action='store_true', default=False,
                    help='launch tensorboard process')
parser.add_argument('--launch-gui', action='store_true', default=False,
                    help='launch GUI control panel')
parser.add_argument('--plot-freq', type=int, default=0,
                    help='set tensorboard plot visualization frequency (default: 0)')
parser.add_argument('--device', type=int, default=0,
                    help='select CUDA device (default: 0)')
parser.add_argument('--batch-size', type=int, default=default_batch_size,
                    help='batch size (default: "{}")'.format(str(default_batch_size)))
parser.add_argument('--optimizer', type=str, default=default_optimizer,
                    help='optimizer (default: "{}")'.format(str(default_optimizer)))
parser.add_argument('--learning-rate', type=float, default=default_learning_rate,
                    help='learning rate (default: "{}")'.format(str(default_learning_rate)))
parser.add_argument('--momentum', type=float, default=default_momentum,
                    help='momentum (default: "{}")'.format(str(default_momentum)))
parser.add_argument('--lr-decay', type=float, default=default_lr_decay,
                    help='learning rate decay (default: "{}")'.format(str(default_lr_decay)))
parser.add_argument('--weight-decay', type=float, default=default_weight_decay,
                    help='weight decay (default: "{}")'.format(str(default_weight_decay)))
parser.add_argument('--val-fail', type=int, default=default_val_fail,
                    help='maximum number of epochs stopping criterion for improving best validation loss (default: "{}")'.format(str(default_val_fail)))
parser.add_argument('--hidden-layer-sizes', nargs='+', default=default_hidden_layer_sizes,
                    help='hidden layer sizes (default: {})'.format(' '.join(default_hidden_layer_sizes)))
args = parser.parse_args()

# Append the current date/time to any user-defined model save path
args.model_save_path = args.model_save_path + ' ' + str(date)

# Set up model save files
os.makedirs(args.model_save_path)
net_description_save_path = os.path.join(args.model_save_path, 'network_description.txt')
net_description_file = open(net_description_save_path, 'w')
net_description_file.write('Network created: ' + str(date))

# Load data and scale it
images, outputs, scale, or_tr = MatLoader.load_data(args.data_path)

# Set up DMP parameters
N = 25
sampling_time = 0.1

# Define layer sizes
input_size = 1600
hidden_layer_sizes = list(map(int, args.hidden_layer_sizes))
output_size = 2*N + 4
conv = None
layer_sizes = [input_size] + hidden_layer_sizes + [output_size]

# Load the model
model = EncoderDecoderNet(layer_sizes, conv, scale)

# Initialize the model
if args.model_load_path:
    net_params_path = os.path.join(args.model_load_path, 'net_parameters')
    model.load_state_dict(torch.load(net_params_path))
    print(' + Loaded parameters from file: ', args.model_load_path)
else:
    for p in list(model.parameters()):
        if p.data.ndimension() == 1:
            torch.nn.init.constant(p, 0)
        else:
            torch.nn.init.xavier_uniform(p, gain=1)
    print(' + Initialized parameters randomly')

# Set up trainer
train_param = TrainingParameters()
device = args.device
train_param.epochs = -1
learning_rate = 0.001
momentum = 0.5
train_param.batch_size = args.batch_size
train_param.training_ratio = 0.7
train_param.validation_ratio = 0.15
train_param.test_ratio = 0.15
train_param.val_fail = 60
trainer = Trainer(launch_tensorboard=args.launch_tensorboard,
                  launch_gui=args.launch_gui,
                  plot_freq=args.plot_freq)

# Save model to file
torch.save(model, (os.path.join(args.model_save_path, 'model.pt')))

# Save model type to file
net_description_file.write('\nModel: imednet.models.encoder_decoder.EncoderDecoderNet')

# Save data path
if args.data_path:
    net_description_file.write('\nData path: ' + args.data_path)

# Save model save path to file
if args.model_save_path:
    net_description_file.write('\nModel save path: ' + args.model_save_path)

# Save model load path to file
if args.model_load_path:
    net_description_file.write('\nModel load path: ' + args.model_load_path)

# Save layer sizes to file
net_description_file.write('\nLayer sizes: ' + str(layer_sizes))
np.save(os.path.join(args.model_save_path, 'layer_sizes'), np.asarray(layer_sizes))

# Save data scaling to file
np.save(os.path.join(args.model_save_path, 'scale_x_min'), scale.x_min)
np.save(os.path.join(args.model_save_path, 'scale_x_max'), scale.x_max)
np.save(os.path.join(args.model_save_path, 'scale_y_min'), scale.y_min)
np.save(os.path.join(args.model_save_path, 'scale_y_max'), scale.y_max)

# Save training parameters to file
net_description_file.write('\nOptimizer: {}'.format(args.optimizer))
net_description_file.write('\nLearning rate: {}'.format(args.learning_rate))
net_description_file.write('\nMomentum: {}'.format(args.momentum))

# Load previously trained model
if args.model_load_path:
    net_indeks_path = os.path.join(args.model_load_path, 'net_indeks.npy')
    trainer.indeks = np.load(net_indeks_path)

# Train
best_nn_parameters = trainer.train(model,
                                   images,
                                   outputs,
                                   args.model_save_path,
                                   train_param,
                                   net_description_file,
                                   optimizer_type=args.optimizer,
                                   learning_rate=args.learning_rate,
                                   momentum=args.momentum,
                                   lr_decay=args.lr_decay,
                                   weight_decay=args.weight_decay)

# Save model
np.save(os.path.join(args.model_save_path, 'net_indeks'), trainer.indeks)
net_params_path = os.path.join(args.model_save_path, 'net_parameters')
torch.save(best_nn_parameters, net_params_path)
net_description_file.close()
