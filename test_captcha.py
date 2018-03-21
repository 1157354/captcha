from gen_captcha_ import gen_captcha_text_and_image
from setting import convert2gray
from setting import MAX_CAPTCHA, CHAR_SET_LEN, vec2text, X, keep_prob
from cnn import crack_captcha_cnn
import tensorflow as tf
import numpy as np
import time

model_path = "/Users/tian/Downloads/model/"




def hack_function(sess, predict, captcha_image):

    text_list = sess.run(predict, feed_dict={X: [captcha_image], keep_prob: 1})
    print(text_list)
    text = text_list[0].tolist()
    vector = np.zeros(MAX_CAPTCHA * CHAR_SET_LEN)
    i = 0
    for n in text:
        vector[i * CHAR_SET_LEN + n] = 1
        i += 1
    return vec2text(vector)


def batch_hack_captcha():


    output = crack_captcha_cnn()
    predict = tf.argmax(tf.reshape(output, [-1, MAX_CAPTCHA, CHAR_SET_LEN]), 2)

    saver = tf.train.Saver()
    with tf.Session() as sess:
        # saver = tf.train.import_meta_graph(save_model + ".meta")
        saver.restore(sess, tf.train.latest_checkpoint(model_path))

        stime = time.time()
        task_cnt = 1000
        right_cnt = 0
        for i in range(task_cnt):
            text, image = gen_captcha_text_and_image()
            image = convert2gray(image)
            image = image.flatten() / 255
            predict_text = hack_function(sess, predict, image)
            if text == predict_text:
                right_cnt += 1
            else:
                print("标记: {}  预测: {}".format(text, predict_text))
                pass
                # print("标记: {}  预测: {}".format(text, predict_text))

        print('task:', task_cnt, ' cost time:', (time.time() - stime), 's')
        print('right/total-----', right_cnt, '/', task_cnt)

if __name__ == '__main__':
    batch_hack_captcha()
    print('end...')




