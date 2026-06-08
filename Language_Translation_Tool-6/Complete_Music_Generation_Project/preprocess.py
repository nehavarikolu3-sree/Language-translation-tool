
from music21 import converter, instrument, note, chord
import os,pickle

notes=[]
for file in os.listdir("midi_dataset"):
    if file.endswith(".mid") or file.endswith(".midi"):
        midi=converter.parse(os.path.join("midi_dataset",file))
        for element in midi.flatten().notes:
            if isinstance(element,note.Note):
                notes.append(str(element.pitch))
            elif isinstance(element,chord.Chord):
                notes.append(".".join(str(n) for n in element.normalOrder))

with open("notes.pkl","wb") as f:
    pickle.dump(notes,f)

print("Extracted",len(notes),"notes")
