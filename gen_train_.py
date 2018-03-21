__author__ = 'tian'
from gen_captcha_ import gen_captcha_text_and_image

from setting import IMAGE_HEIGHT,IMAGE_WIDTH,MAX_CAPTCHA,char_set,CHAR_SET_LEN,X,Y,keep_prob,convert2gray,text2vec,vec2text
from cnn import crack_captcha_cnn

import numpy as np
import tensorflow as tf

text, image = gen_captcha_text_and_image()

model_path = "/Users/tian/Downloads/model/"






# 生成一个训练batch
def get_next_batch(batch_size=128):
    batch_x = np.zeros([batch_size, IMAGE_HEIGHT * IMAGE_WIDTH])
    batch_y = np.zeros([batch_size, MAX_CAPTCHA * CHAR_SET_LEN])


    # def wrap_gen_captcha_text_and_image():
    #     while True:
    #         text, image = gen_captcha_text_and_image()
    #         if image.shape == (60, 160, 3):
    #             return text, image

    for i in range(batch_size):
        text, image = gen_captcha_text_and_image()
        image = convert2gray(image)

        batch_x[i, :] = image.flatten() / 255  # (image.flatten()-128)/128  mean为0
        batch_y[i, :] = text2vec(text)

    return batch_x, batch_y




# 训练
def train_crack_captcha_cnn():
    output = crack_captcha_cnn()
    # loss
    # loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(output, Y))
    loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=output, labels=Y))

    optimizer = tf.train.AdamOptimizer(learning_rate=0.001).minimize(loss)

    predict = tf.reshape(output, [-1, MAX_CAPTCHA, CHAR_SET_LEN])
    max_idx_p = tf.argmax(predict, 2)
    max_idx_l = tf.argmax(tf.reshape(Y, [-1, MAX_CAPTCHA, CHAR_SET_LEN]), 2)
    correct_pred = tf.equal(max_idx_p, max_idx_l)
    accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

    saver = tf.train.Saver(max_to_keep=1)
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())

        step = 0
        while True:
            batch_x, batch_y = get_next_batch(64)
            _, loss_ = sess.run([optimizer, loss], feed_dict={X: batch_x, Y: batch_y, keep_prob: 0.75})
            print(step, loss_)

            if step % 100 == 0:
                batch_x_test, batch_y_test = get_next_batch(100)
                acc = sess.run(accuracy, feed_dict={X: batch_x_test, Y: batch_y_test, keep_prob: 1.})
                print(step, acc)

                if acc >= 0.98:
                    save_path = saver.save(sess, model_path+"crack_captcha.model",global_step=step)
                    print("Save to path: ", save_path)
                    break

            step += 1


def crack_captcha(captcha_image):
    output = crack_captcha_cnn()
    saver = tf.train.Saver()

    with tf.Session() as sess:

        saver.restore(sess, model_path)

        predict = tf.argmax(tf.reshape(output, [-1, MAX_CAPTCHA, CHAR_SET_LEN]), 2)
        text_list = sess.run(predict, feed_dict={X: [captcha_image], keep_prob: 1})

        text = text_list[0].tolist()
        vector = np.zeros(MAX_CAPTCHA * CHAR_SET_LEN)
        i = 0
        for n in text:
            vector[i * CHAR_SET_LEN + n] = 1
            i += 1
        return vec2text(vector)


if __name__ == '__main__':
    train_crack_captcha_cnn()



