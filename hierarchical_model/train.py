import os

generate_training = 'python convert-text2dict.py ./raw_data/train.all --cutoff 15000 ./training_data/Training'
os.system(generate_training)
generate_dev = 'python convert-text2dict.py ./raw_data/dev.all --dict=./training_data/Training.dict.pkl ./training_data/Validation'
os.system(generate_dev)
generate_test = 'python convert-text2dict.py ./raw_data/test.all --dict=./training_data/Training.dict.pkl ./training_data/Test'
os.system(generate_test)

training_command = 'THEANO_FLAGS=mode=FAST_RUN,device=cuda0,floatX=float32 python define_model.py --prototype prototype_twitter_HRED'
os.system(training_command)