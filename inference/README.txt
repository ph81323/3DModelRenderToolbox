1. �쥻���g�k 
    new_saver = tf.train.import_meta_graph('itrichess_new.ckpt.meta')    
    new_saver.restore(session, './itrichess_new.ckpt')


2. �ڧאּ
    new_saver = tf.train.Saver()
    new_saver.restore(session, './itrichess_new.ckpt')

   ���L�o�˴N�S��Ū����itrichess_new.ckpt.meta�F @@

   