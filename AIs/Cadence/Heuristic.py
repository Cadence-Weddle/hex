import numpy as np
import tensorflow as tf

def weight_var(shape):return tf.Variable(tf.truncated_normal(shape, std=0.1))

def bias_var(shape):return tf.Variable(tf.truncated_normal(shape))

