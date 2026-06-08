
import pickle, numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.utils import to_categorical

with open("notes.pkl","rb") as f:
    notes=pickle.load(f)

pitchnames=sorted(set(notes))
n_vocab=len(pitchnames)

sequence_length=20
network_input=[]
network_output=[]

note_to_int={n:i for i,n in enumerate(pitchnames)}

for i in range(len(notes)-sequence_length):
    seq_in=notes[i:i+sequence_length]
    seq_out=notes[i+sequence_length]
    network_input.append([note_to_int[c] for c in seq_in])
    network_output.append(note_to_int[seq_out])

n_patterns=len(network_input)
network_input=np.reshape(network_input,(n_patterns,sequence_length,1))
network_input=network_input/float(max(n_vocab,1))
network_output=to_categorical(network_output,num_classes=n_vocab)

model=Sequential()
model.add(LSTM(256,input_shape=(network_input.shape[1],network_input.shape[2])))
model.add(Dropout(0.2))
model.add(Dense(n_vocab,activation="softmax"))
model.compile(loss="categorical_crossentropy",optimizer="adam")

model.fit(network_input,network_output,epochs=5,batch_size=64)
model.save("model/music_model.keras")
print("Model saved")
