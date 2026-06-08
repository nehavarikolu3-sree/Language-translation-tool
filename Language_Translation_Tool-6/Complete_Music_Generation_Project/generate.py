
import pickle, numpy as np
from music21 import stream, note
from tensorflow.keras.models import load_model

with open("notes.pkl","rb") as f:
    notes=pickle.load(f)

pitchnames=sorted(set(notes))
int_to_note=dict(enumerate(pitchnames))

model=load_model("model/music_model.keras")

pattern=np.random.randint(0,len(pitchnames),20).tolist()
prediction_output=[]

for _ in range(50):
    inp=np.reshape(pattern,(1,len(pattern),1))/float(len(pitchnames))
    pred=model.predict(inp,verbose=0)
    idx=np.argmax(pred)
    prediction_output.append(int_to_note[idx])
    pattern.append(idx)
    pattern=pattern[1:]

output_notes=[]
offset=0
for p in prediction_output:
    n=note.Note(p if "." not in p else "C4")
    n.offset=offset
    output_notes.append(n)
    offset+=0.5

midi_stream=stream.Stream(output_notes)
midi_stream.write("midi",fp="generated_music/generated.mid")
print("generated_music/generated.mid created")
