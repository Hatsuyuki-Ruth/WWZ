import fastText
Train_Txt_withlabel__File='data/train_with_videos_with_label.txt'
Test_Txt_withlabel__File='data/test_with_videos_with_label.txt'
classifier = fastText.train_supervised(Train_Txt_withlabel__File, epoch=20, ws=2, lr=0.5, wordNgrams=2, dim=1000,
                                       label=u"__label__", loss=u'softmax')
classifier.save_model("model/classify_with_videos3.model")
train_res=classifier.test(Train_Txt_withlabel__File)
test_res=classifier.test(Test_Txt_withlabel__File)
print(train_res)
print(test_res)
