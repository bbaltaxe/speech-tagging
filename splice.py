#import all the things
from pathlib import Path 
import librosa
import os
import argparse

#get all the arguments
parser = argparse.ArgumentParser(description='Split conversational audio files into utterances')
parser.add_argument('file', help='the path to the file that you would like to split')
parser.add_argument('--db', help='decibles below which silence is considered silence. Defaults to 25.', default = 25)
parser.add_argument('-t','--mintime', help='the minimum length of an utterance in milliseconds. Default is 363', default = 363)
parser.add_argument('-o','--output_path', help='the path to the folder the utterance files should be placed in. Default is "clips"', default = 'clips')
args = parser.parse_args()



'''
Takes in a waveform array and splits it on silence. 
Returns an array of waveform arrays
args: 
y: waveform array
db: decibles below which to consider silence
mintime: boots short snippets which are shorter than mintime
'''
def chunkify(y,sr,db,mintime):
    stamps = librosa.effects.split(y,top_db=db)
    output = []
    for entry in stamps:
        start = entry[0]
        end = entry[1]
        
        if end - start > ms_to_samples(mintime,sr): 
            chunk = y[start:end]
            output.append(chunk)

    return output

def chunks_to_wavs(yarray,inpath,outpath): 
    #check that outpath exists, if not create it 
    Path(outpath).mkdir(parents=True, exist_ok=True)

    #create wav files
    for i,entry in enumerate(yarray): 
        filename = os.path.split(inpath)[1]
        title, extension = os.path.splitext(filename)
        name = title + "_utterance_" + str(i) + ".wav"
        path = outpath + "/" + name
        librosa.output.write_wav(path, entry, sr)
        print("created " + path)

def ms_to_samples(time,sr): 
    return sr * (time/1000)

if __name__ == "__main__":
    y,sr = librosa.load(args.file)
    chunks = chunkify(y,sr,args.db,args.mintime)
    chunks_to_wavs(chunks,args.file,args.output_path)
