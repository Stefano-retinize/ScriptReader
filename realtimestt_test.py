from RealtimeSTT import AudioToTextRecorder
from colorama import Fore, Back, Style
import colorama
import os
from IPython.display import clear_output
import sounddevice as sd
import soundfile as sf
from Utils import process_script_file, generate_audio

if __name__ == '__main__':

    print("Initializing RealtimeSTT test...")

    colorama.init()

    full_sentences = []
    displayed_text = ""
    
    User_character = 'Donkey'
    Script, start = process_script_file(r'C:\Users\jack\Desktop\IA\scriptreader\RealtimeSTT\tests\Script_sample.txt', User_character)
    global_sentence_idx = 0
    user_sentence = 0
    
    key_wrd_1, key_wrd_2 = None, None
    
    

    def clear_console():
        #os.system('clear' if os.name == 'posix' else 'cls')
        clear_output(wait=True)
        
        
    def quit_loop():
        global Break
        Break = True
        
    def update_key_word():
        global user_sentence, key_wrd_1, key_wrd_2
        if len(Script) >= user_sentence:
            sentence = Script[user_sentence].split()
            if len(sentence)>1:
                key_wrd_1 = sentence[-2]
                if key_wrd_1[-1] in '?!.$-':
                    key_wrd_1 = key_wrd_1[:-1] 
            else:
                key_wrd_1 = "sjaslkfjsalfww"   #In case the sentence is one word length word becomes inexisting word
            key_wrd_2 = sentence[-1]
            if key_wrd_2[-1] in '?!.$-':
                key_wrd_2 = key_wrd_2[:-1]
            user_sentence+=1
        else:
            print ("Finished detection")
            
    def reproduce(idx):
        global global_sentence_idx
        data, samplerate = sf.read(os.path.join(r'C:\Users\jack\Desktop\IA\scriptreader\RealtimeSTT\tests', f'output_{idx}.mp3'))
        print ("reproducing", idx)
        sd.play(data, samplerate)
        sd.wait()
        global_sentence_idx+=1
        recorder.start()

    def text_detected(text):
        global displayed_text, user_sentence, global_sentence_idx
        displayed_text = []
        #sentences_with_style = [
        #    f"{Fore.YELLOW + sentence + Style.RESET_ALL if i % 2 == 0 else Fore.CYAN + sentence + Style.RESET_ALL} "
        #    for i, sentence in enumerate(full_sentences)
        #]
        #new_text = "".join(sentences_with_style).strip() + " " + text if len(sentences_with_style) > 0 else text

        #if new_text != displayed_text:
        #    displayed_text = new_text
        #    clear_console()
        #    print(displayed_text, end="", flush=True)
        clear_console()
        print (f'{text} {user_sentence} {key_wrd_1} {key_wrd_2}')
            # Trigger something based on a keyword
        if "quit" in text.lower():
             quit_loop()
        
        elif key_wrd_1.lower() in text.lower() or key_wrd_2.lower() in text.lower():
            print(f'Keyword detected! Triggering reproduce...{global_sentence_idx}')
            global_sentence_idx+=1
            reproduce(global_sentence_idx)
            update_key_word()
        
        
            
    def process_text(text):
        global recorder
        #full_sentences.append(text)
        text_detected("")
        text.lower()
        #recorder.start()
        
    

    recorder_config = {
        'spinner': False,
        'model': 'large-v2',
        'language': 'en',
        'silero_sensitivity': 0.1,
        'webrtc_sensitivity': 2,
        'post_speech_silence_duration': 20,
        'min_length_of_recording': 0,
        'min_gap_between_recordings': 0,
        'enable_realtime_transcription': True,
        'realtime_processing_pause': 0.1,
        'realtime_model_type': 'tiny.en',
        'on_realtime_transcription_update': text_detected, 
        #'on_realtime_transcription_stabilized': text_detected,
    }

    recorder = AudioToTextRecorder(**recorder_config)
    print ("recorder initialized")
    
    clear_console()
    
    Break = False
    update_key_word()
    print (start, User_character)
    if start != User_character:
        print ("different character start reproducing")
        reproduce(global_sentence_idx)
        
    print("Say something...", end="", flush=True)
    while True:
        recorder.text(process_text)
        if Break:
            break