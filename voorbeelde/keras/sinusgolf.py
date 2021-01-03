#%%
# Voorspel sinusgolf een stap in toekoms

# Kombineer twee sinusgolwe om derde golf te vorm.  Voorspel dan die derde golf met die eerste twee as inset.
# sein1 en sein2 is insette en seinsom is die uitset.
# Voorspel seinsom met sein1 en sein2 as insette

# Laai eers alle modules wat gebruik gaan word
import numpy as np
import tensorflow as tf
from tensorflow import keras
from math import pi

import matplotlib.pyplot as plt

#%%
# Druk die weergawe van tensorflow wat gebruik word
tf.__version__

#%%

# Maak die tydvektor van die fiktiewe sein
seinlengte = 10000
tyd = np.linspace(0, 6*pi, seinlengte)

# Maak nou die sein wat twee frekwensies bevat
ω1 = 10 # Frequency in [Hz]
sein1 = np.sin(ω1*tyd)

plt.plot(tyd,sein1)

ω2 = 5 # Frequency in [Hz]
sein2 = np.sin(ω2*tyd)

# Plot die sein
plt.plot(tyd,sein2)

#%%
seinsom = 0.5 + 0.25*(sein1 + sein2)
plt.plot(tyd, seinsom)
print(max(seinsom))

#%%

# Kombineer die tydsein in 'n matriks om aan tensorflow te gee
sein1 = sein1.reshape(sein1.size, 1)
sein2 = sein2.reshape(sein2.size, 1)

x_train = np.append(sein1, sein2, axis = 1)
y_train = seinsom

#%%

print(x_train.shape)
print(y_train.shape)

#%%

venstergrootte = 1000
plt.plot(x_train[1:venstergrootte,0])
plt.plot(x_train[1:venstergrootte,1])

#%%

plt.plot(y_train[1:venstergrootte])

#%%

lengtevansein = 20
monsterfrekwensie = 20
verspreiding = 1
aantaldatasteekproewe = 11

# Opleidingsdata
dataset_train = keras.preprocessing.timeseries_dataset_from_array(
    x_train,
    y_train,
    sequence_length=lengtevansein,
    sequence_stride = verspreiding,
    sampling_rate = monsterfrekwensie,
    batch_size = aantaldatasteekproewe,
)


# Toetsdata
# Neem toetsdata as dieselfde as die opleidingsdata, want hierdie is net 'n eenvoudige toetsmodel
dataset_val = keras.preprocessing.timeseries_dataset_from_array(
    x_train,
    y_train,
    sequence_length=lengtevansein,
    sequence_stride = verspreiding,
    sampling_rate = monsterfrekwensie,
    batch_size = aantaldatasteekproewe,
)

#%%

for batch in dataset_train:
    insette, uitsette = batch
    
    print(insette.shape)
    print(uitsette.shape)

#%%
for x, y in dataset_train.take(1):
    #plt.plot(x[10,:,0])
    #print(x.shape)
    
    print(y.shape)
    plt.plot(y, '+-')
    
    #a = x[1]
    #plt.plot(a[:,1], 'x-')
    #print(a[:,1].shape)
    #print(x[0])
    #plt.plot(model.predict(x)[0])

#%%

inputs = keras.layers.Input(shape=(lengtevansein, x_train.shape[1]))
lstm_out = keras.layers.LSTM(100)(inputs)
outputs = keras.layers.Dense(lengtevansein)(lstm_out)

#%%

model = keras.Model(inputs=inputs, outputs=outputs)
model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.001), loss="mse")
model.summary()

#%%

dot_img_file = 'model_1.png'
tf.keras.utils.plot_model(model, to_file=dot_img_file, show_shapes=True)

#%%

"""
We'll use the `ModelCheckpoint` callback to regularly save checkpoints, and
the `EarlyStopping` callback to interrupt training when the validation loss
is not longer improving.
"""

path_checkpoint = "model_sinewave_checkpoint.h5"
es_callback = keras.callbacks.EarlyStopping(monitor="val_loss", min_delta=0, patience=5)

modelckpt_callback = keras.callbacks.ModelCheckpoint(
    monitor="val_loss",
    filepath=path_checkpoint,
    verbose=1,
    save_weights_only=True,
    save_best_only=True,
)

#%%

history = model.fit(
    dataset_train,
    epochs=10,
    validation_data=dataset_val,
    callbacks=[es_callback, modelckpt_callback],
)

#%%

"""
We can visualize the loss with the function below. After one point, the loss stops
decreasing.
"""


def visualize_loss(history, title):
    loss = history.history["loss"]
    val_loss = history.history["val_loss"]
    epochs = range(len(loss))
    plt.figure()
    plt.plot(epochs, loss, "b", label="Training loss")
    plt.plot(epochs, val_loss, "r", label="Validation loss")
    plt.title(title)
    plt.xlabel("Epochs")
    plt.ylabel("Loss")
    plt.legend()
    plt.show()


visualize_loss(history, "Training and Validation Loss")

#%%

"""
## Voorspelling

The opgeleide model hierbo kan nou gebruik word om 5 voorspellings te maak van die toetsdata
"""


def show_plot(plot_data, delta, title):
    labels = ["History", "True Future", "Model Prediction"]
    marker = [".-", "rx", "go"]
    time_steps = list(range(-(plot_data[0].shape[0]), 0))
    if delta:
        future = delta
    else:
        future = 0

    plt.title(title)
    for i, val in enumerate(plot_data):
        if i:
            plt.plot(future, plot_data[i], marker[i], markersize=10, label=labels[i])
        else:
            plt.plot(time_steps, plot_data[i].flatten(), marker[i], label=labels[i])
    plt.legend()
    plt.xlim([time_steps[0], (future + 5) * 2])
    plt.xlabel("Time-Step")
    plt.show()
    return

def wys_plot(plot_data, delta, titel):
    labels = ["History", "True Future", "Model Prediction"]
    marker = [".-", "rx", "go"]


    plt.title(titel)
    for i, val in enumerate(plot_data):
        if i:
            plt.plot(future, plot_data[i], marker[i], markersize=10, label=labels[i])
        else:
            plt.plot(time_steps, plot_data[i].flatten(), marker[i], label=labels[i])
    plt.legend()
    plt.xlim([time_steps[0], (future + 5) * 2])
    plt.xlabel("Time-Step")
    plt.show()
    return


for x, y in dataset_val.take(1):
    plt.plot(y)
    print(y.shape)
    #print(x[0])
    print(x[0,:].shape)
    #plt.plot(model.predict(x)[0])
    plt.plot(x[0])
    print(model.predict(x)[0].shape)

#%%
