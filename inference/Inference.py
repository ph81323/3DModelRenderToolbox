import numpy as np
import h5py
import tensorflow as tf
import math

def get_accuracy(predictions, labels):
  gt = tf.argmax(labels,1)
  prediction = tf.argmax(predictions,1)
  singleacc = tf.reduce_sum(tf.cast(tf.equal(prediction, gt), tf.float32))
  accuracy = 100 * tf.reduce_mean(tf.cast(tf.equal(prediction, gt), tf.float32))
  return  gt,prediction, singleacc, accuracy


batch_size = 64
num_labels = 6
graph = tf.Graph()
with graph.as_default():
    predict = tf.Variable(False)
    # Input data.
    with tf.name_scope('data') as scope:
        tf_train_dataset = tf.placeholder(tf.float32, shape=(None, 50, 50, 100, 1), name="train_dataset")
        tf_train_labels = tf.placeholder(tf.float32, shape=(None, num_labels), name="train_labels")
    # Variables.
    with tf.name_scope('conv1') as scope:
        # conv1
        stdv = 1 / math.sqrt(5 * 5 * 5 * 1)
        # tf.random_uniform
        layer1_weights = tf.Variable(tf.random_uniform([5, 5, 5, 1, 32], -stdv, stdv), name="conv1_w")
        layer1_biases = tf.Variable(tf.random_uniform([32], -stdv, stdv), name="conv1_bias")
    # layer1_biases = tf.Variable(tf.constant(1.0, shape=[32]))#tf.zeros([32])
    with tf.name_scope('conv2') as scope:
        # conv2
        stdv = 1 / math.sqrt(3 * 3 * 3 * 32)
        layer2_weights = tf.Variable(tf.random_uniform([3, 3, 3, 32, 32], -stdv, stdv), name="conv2_w")
        layer2_biases = tf.Variable(tf.random_uniform([32], -stdv, stdv), name="conv2_bias")
    # layer2_biases = tf.Variable(tf.constant(1.0, shape=[32]))
    with tf.name_scope('fc1') as scope:
        # fc1
        stdv = 1 / math.sqrt(11 * 11 * 23 * 32)
        layer3_weights = tf.Variable(tf.random_uniform([11 * 11 * 23 * 32, 128], -stdv, stdv), name="fc1_w")
        # layer3_weights = tf.Variable(tf.random_normal([11*11*23*32, 128]), name = "fc1_w")
        layer3_biases = tf.Variable(tf.random_uniform([128]), name="fc1_bias")
        # layer3_biases = tf.Variable(tf.constant(1.0, shape=[128]))
    with tf.name_scope('fc2') as scope:
        # fc2
        stdv = 1 / math.sqrt(128)
        layer4_weights = tf.Variable(tf.random_uniform([128, num_labels], -stdv, stdv), name="fc2_w")
        layer4_biases = tf.Variable(tf.random_uniform([num_labels]), name="fc2_bias")

    # MODEL
    def model(data):
        # Conv1
        padding = [[0, 0], [1, 1], [1, 1], [1, 1], [0, 0]]
        padded_input = tf.pad(data, padding, "CONSTANT")
        conv1 = tf.nn.conv3d(padded_input, layer1_weights, [1, 2, 2, 2, 1], padding='VALID')
        hidden1 = tf.nn.relu(tf.nn.bias_add(conv1, layer1_biases))
        dropout1 = tf.nn.dropout(hidden1, 0.2)
        # Conv2
        conv2 = tf.nn.conv3d(dropout1, layer2_weights, [1, 1, 1, 1, 1], padding='VALID')
        hidden2 = tf.nn.relu(tf.nn.bias_add(conv2, layer2_biases))
        # Pool1
        pool1 = tf.nn.max_pool3d(hidden2, ksize=[1, 2, 2, 2, 1], strides=[1, 2, 2, 2, 1], padding='VALID')
        dropout2 = tf.nn.dropout(pool1, 0.3)
        normalize3_flat = tf.reshape(dropout2, [-1, 11 * 11 * 23 * 32])
        # FC1
        fc1 = tf.add(tf.matmul(normalize3_flat, layer3_weights), layer3_biases)
        hidden3 = tf.nn.relu(fc1)

        dropout3 = tf.nn.dropout(hidden3, 0.4)
        # FC2
        res = tf.add(tf.matmul(dropout3, layer4_weights), layer4_biases)
        return res

    local_res = model(tf_train_dataset)

    with tf.name_scope("accuracy") as scope:
        gt, prediction, singleacc, accuracy = get_accuracy(local_res, tf_train_labels)



with tf.Session(graph=graph) as session:
    new_saver = tf.train.Saver()
    new_saver.restore(session, './itrichess_new.ckpt')


    f = h5py.File('2_group10.mat')
    pointCloud = np.array(f['answer'])
    f.close()
    pointCloud = pointCloud[None, :, :, :, None].astype('float32')

    fake_label = np.zeros((1, 6))
    fake_label[0][2] = 1

    val_prediction, val_label, val_acc = session.run([prediction, gt, singleacc],
                                                     feed_dict={tf_train_dataset: pointCloud,
                                                                tf_train_labels: fake_label})

    print ("Your model prediction it is :" , val_prediction[0])
    print ("The label is : ",val_label[0])
