# Disciplina: P8902-IANA-Computação Cognitiva 2 Interface do usuário baseada em voz
# Professor: Rafael Brasileiro de Araujo
# Alunos:
#     1. Fábio Tranzillo Nogueira
#     2. Guilherme Augusto das Chagas Praser
#     3. Marcelo Caldeira Pereira

from threading import Thread
from ibm_watson import TextToSpeechV1
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.websocket import RecognizeCallback, AudioSource
import PySimpleGUI as sg
import simpleaudio as sa
import pyaudio
import sys

try:
    from Queue import Queue, Full
except ImportError:
    from queue import Queue, Full

##################################################################
# Classe com a definição do CALLBACK para o serviço speech-to-text
##################################################################
class MyRecognizeCallback(RecognizeCallback):
    def __init__(self):
        RecognizeCallback.__init__(self)

    # Método executado quando receber o resultado final da sentença
    def on_transcription(self, transcript):
        dicRet = transcript[0]
        print('============================================================')
        print(f'Percentual de confiança da conversão: {dicRet.get("confidence") * 100} %')
        print(f'Texo convertido: {dicRet.get("transcript")}')
        print('============================================================\n')        

    # Método executado quando a conexão for estabelecida
    def on_connected(self):
        print('Conexão bem sucedida. \n')

    # Método executado quando ocorrer qualquer erro
    def on_error(self, error):
        print('Error recebido: {}'.format(error) , '\n')

    # Método executado quando ocorrer timeout por inatividade da conexão
    def on_inactivity_timeout(self, error):
        print('Timeout: {}'.format(error) , '\n')

    # Método executado quando a conexão já tiver escutando
    def on_listening(self):
        print('Iniciando a captura do audio. O serviço está ouvindo! \n')

    # Método executado quando passar a receber resultados intermediários, porém ainda não conclusivos
    def on_hypothesis(self, hypothesis):
        print('Resultado intermediário:' , hypothesis , '\n')

    # Método executado quando passar a receber qualquer tipo de dados do request
    def on_data(self, data):
        return

    # Método executado quando a conexão for finalizada
    def on_close(self):
        print('Conexão de audio finalizada. \n')
        print('>>>>>>>>>>>>>>>>>>>>>>>>> End of Sysout <<<<<<<<<<<<<<<<<<<<<<<< \n')

###########################################################################
# Classe UTILITARIO para a definição dos serviços de conexão IBM Watson e #
# dicionarios contendo as variáveis de configuração.                      #
###########################################################################
class Utilitario:
    def autenticarIbmWatson(self, servico, aut):
        if servico == 'tts':
            authenticator = IAMAuthenticator(aut.strip())
            tts = TextToSpeechV1(authenticator=authenticator)
            return tts
        elif servico == 'stt':
            authenticator = IAMAuthenticator(aut.strip())
            stt = SpeechToTextV1(authenticator=authenticator)
            return stt            
        
    def converterTTS(self, tts, texto='Texto não informado'):
        with open('audio.wav', 'wb') as audio_file:
            content = tts.synthesize(
                texto,
                voice='pt-BR_IsabelaVoice',
                accept='audio/wav'
            ).get_result().content
            audio_file.write(content)

    def playerAudio(self, path):
        wave_obj = sa.WaveObject.from_wave_file(path)
        play_obj = wave_obj.play()
        play_obj.wait_done()
        return 'Audio reproduzido com sucesso! \n'
    
    def initializeQueue(self):
        dicInitializeQueue = dict()
        dicInitializeQueue['CHUNK'] = 1024        
        dicInitializeQueue['BUF_MAX_SIZE'] = dicInitializeQueue.get('CHUNK') * 10
        dicInitializeQueue['q'] = Queue(maxsize=int(round(dicInitializeQueue.get('BUF_MAX_SIZE') / 
                                                          dicInitializeQueue.get('CHUNK'))))
        dicInitializeQueue['audio_source'] = AudioSource(dicInitializeQueue.get('q'), True, True)                                        
        return dicInitializeQueue
    
    def recordingSpeech(self):
        dicRecordingSpeech = dict()
        dicRecordingSpeech['FORMAT'] = pyaudio.paInt16
        dicRecordingSpeech['CHANNELS'] = 1
        dicRecordingSpeech['RATE'] = 44100
        return dicRecordingSpeech

class TelaProjeto:
    THREAD_ATIVA = False
    
    def __init__(self):        
        text_to_speech_layout = [
            [sg.T('Text')],
            [sg.Input(size=(70,0),key='TStextGUI')],
            [sg.T('Authenticator')],
            [sg.Input(size=(70,0),key='TSAuthenticatorGUI')], 
            [sg.Checkbox('Verbose Processing',key='TSverboseGUI') , sg.Checkbox('Play Audio',key='TSplayGUI')],
            [sg.Button('Generate',key='TSgenerateBT')]
        ]
        
        speech_to_text_layout = [
            [sg.T('Authenticator')],
            [sg.Input(size=(70,0),key='STAuthenticatorGUI')],
            [sg.Checkbox('Verbose Processing',key='STverboseGUI')],
            [sg.Button('Start',key='STstartBT') , sg.Button('Stop',key='STstopBT')]
        ]

        player = [
            [sg.Button('Click Here to Identify the File',size=(62,10),key='PLAYgenerateBT')]
        ]
        
        layout = [
            [sg.TabGroup([[sg.Tab('text-to-speech', text_to_speech_layout, key='TabTS'),
                           sg.Tab('speech-to-text', speech_to_text_layout, key='TabST'), 
                           sg.Tab('wav player', player, key='TabPlayer')]])],
            [sg.Text('Sysout')], 
            [sg.Output(size=(70,20),key='sysoutGUI')],
            [sg.Button('Exit',key='exitBT')]             
        ]

        # Janela
        self.janela = sg.Window('Text-to-speech and speech-to-text converter').layout(layout)

    def Iniciar(self):
        # Disponibiliza métodos utilitários para a tela            
        Util = Utilitario()
        
        while True:            
            # Extrair dados da tela
            self.button, self.values = self.janela.Read()
            
            # Efetuar print para processamento verboso ligado
            if ((self.button == 'TSgenerateBT' and self.values['TSverboseGUI'] == True) or
                (self.button == 'STstartBT' and self.values['STverboseGUI'] == True) or
                (self.button == 'STstopBT' and self.values['STverboseGUI'] == True)):
                print(f'Evento: {self.button} \n')
                print(f'Values: {self.values} \n')            
                
            if self.button == 'exitBT' or self.button == sg.WIN_CLOSED:
                self.janela.close()
                break
            elif self.button == 'TSgenerateBT':
                texto = self.values['TStextGUI']
                autenticador = self.values['TSAuthenticatorGUI']
                PLAY = self.values['TSplayGUI']
                
                if autenticador != '':  
                    try:            
                        # Cria objeto com a chave de autenticação
                        tts = Util.autenticarIbmWatson(servico='tts', aut=autenticador)
                                        
                        # Converte texto para fala
                        if texto != '':
                            Util.converterTTS(tts, texto)
                        else:
                            Util.converterTTS(tts)
                            
                        print('Arquivo "audio.wav" gerado com sucesso! \n')
                        
                        if PLAY == True:
                            print('Iniciando reprodução do audio! \n')
                            msg = Util.playerAudio(path='audio.wav')
                            print(msg)
                    except:
                        print('Oops! Ocorreu erro. \n')
                        print('Unexpected error:', sys.exc_info()[0], '\n')
                else:
                    sg.popup('Informar o autenticador IBM watson Text to Speech.')
                    
                    print('Geração de audio não concluída. Autenticador watson IBM não informado. \n')
                print('>>>>>>>>>>>>>>>>>>>>>>>>> End of Sysout <<<<<<<<<<<<<<<<<<<<<<<< \n')
            elif self.button == 'STstartBT':                
                dicInitializeQueue = Util.initializeQueue()
                dicRecordingSpeech = Util.recordingSpeech()

                INTERIM_RESULTS = self.values['STverboseGUI']
                autenticador = self.values['STAuthenticatorGUI']

                if autenticador != '' and self.THREAD_ATIVA == False:  
                    try:            
                        # Cria objeto com a chave de autenticação
                        stt = Util.autenticarIbmWatson(servico='stt', aut=autenticador)
                    except:
                        print('Oops! Ocorreu erro. \n')
                        print('Unexpected error:', sys.exc_info()[0], '\n')

                    # Iniciar o serviço de reconhecimento e passar o AudioSource
                    def recognize_using_weboscket(*args):
                        mycallback = MyRecognizeCallback()
                        stt.recognize_using_websocket(audio=dicInitializeQueue.get('audio_source'),
                                                      content_type='audio/l16; rate=44100',
                                                      recognize_callback=mycallback,
                                                      model='pt-BR_BroadbandModel',
                                                      interim_results=INTERIM_RESULTS)
                        
                    # definir retorno de chamada para pyaudio para armazenar a gravação na fila
                    def pyaudio_callback(in_data, frame_count, time_info, status):
                        try:
                            dicInitializeQueue.get('q').put(in_data)
                        except Full:
                            pass # discard
                        return (None, pyaudio.paContinue)

                    # Instância do pyaudio
                    audio = pyaudio.PyAudio()
                                    
                    # Abrir stream using callback
                    stream = audio.open(
                        format=dicRecordingSpeech.get('FORMAT'),
                        channels=dicRecordingSpeech.get('CHANNELS'),
                        rate=dicRecordingSpeech.get('RATE'),
                        input=True,
                        frames_per_buffer=dicInitializeQueue.get('CHUNK'),
                        stream_callback=pyaudio_callback,
                        start=False
                    )                                    

                    # Iniciar a gravação e Iniciar o serviço para reconhecer o stream                
                    stream.start_stream()
                    
                    try:
                        recognize_thread = Thread(target=recognize_using_weboscket, args=())
                        recognize_thread.start()
                        
                        self.THREAD_ATIVA = True
                    except:
                        print('Oops! Ocorreu erro ao iniciar o serviço de stream. \n')
                        print('Unexpected error:', sys.exc_info()[0], '\n')
                else:
                    if autenticador == '':
                        sg.popup('Informar o autenticador IBM watson Speech to Text.')
                        
                        print('Captura de audio não iniciada. Autenticador watson IBM não informado. \n')
                    else:
                        print('Captura de audio já ativa. START já realizado! \n')
                    print('>>>>>>>>>>>>>>>>>>>>>>>>> End of Sysout <<<<<<<<<<<<<<<<<<<<<<<< \n')
            elif self.button == 'STstopBT':
                if self.THREAD_ATIVA == True:
                    self.THREAD_ATIVA = False
                    try:
                        stream.stop_stream()
                        stream.close()
                        audio.terminate()
                        dicInitializeQueue.get('audio_source').completed_recording()                           
                    except:
                        print('Oops! Ocorreu erro ao finalizar o serviço de stream. \n')
                        print('Unexpected error:', sys.exc_info()[0], '\n')
                else:
                    print('Captura de audio não ativa. STOP já realizado! \n')
                    print('>>>>>>>>>>>>>>>>>>>>>>>>> End of Sysout <<<<<<<<<<<<<<<<<<<<<<<< \n')
            elif self.button == 'PLAYgenerateBT':
                pathAudio = sg.popup_get_file('Escolha um arquivo para reprodução')
                
                if pathAudio != '':
                    if pathAudio != None:
                        print(f'File: {pathAudio} \n')                        
                        print('Iniciando reprodução do audio! \n')
                        msg = Util.playerAudio(path=pathAudio)
                        print(msg)
                    else:
                        print('Reprodução de audio cancelada. \n')
                else:
                    sg.popup('Informar arquivo de audio.')
                    
                    print('Reprodução de audio não realizada. Arquivo de audio não informado. \n')
                print('>>>>>>>>>>>>>>>>>>>>>>>>> End of Sysout <<<<<<<<<<<<<<<<<<<<<<<< \n')

# Controlador
def main():
    Tela = TelaProjeto()
    Tela.Iniciar()

if __name__ == '__main__':
    main()