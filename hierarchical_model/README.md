This folder contains the hierarchical model.
The model is trained jointly on three datasets, each training batch contains 80 examples, the examples in each batch is randomly shuffled from the three datasets.

The code needs python2.7, Theano bleeding edge version, gpu with at least 12G memory, CUDA10.0.
If trained on gpu with less memory, tune down the batch size.