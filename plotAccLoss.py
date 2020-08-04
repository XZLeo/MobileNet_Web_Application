import matplotlib.pyplot as plt

def plotLossAcc(history):
    acc = history.history['acc']
    val_acc = history.history['val_acc']
    loss = history.history['loss']
    val_loss = history.history['val_loss']

    epochs = range(1, len(acc)+1)

    plt.plot(epochs, acc, 'b', label='Trainning Accuracy')
    plt.plot(epochs, val_acc, 'r', label='Validation Accuracy')
    plt.title('Accuracy')
    plt.legend() #给图加上图例

    plt.figure()

    plt.plot(epochs, loss, 'b', label='Trainning Loss')
    plt.plot(epochs, val_loss, 'r', label='Validation Loss')
    plt.title('Loss')
    plt.legend() 

    plt.show()
    return
    

