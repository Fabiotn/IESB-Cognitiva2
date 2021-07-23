# IESB-Cognitiva2
## Disciplina: P8902-IANA-Computação Cognitiva 2 Interface do usuário baseada em voz
### Professor: Rafael Brasileiro de Araujo
### Alunos:
    1. Fábio Tranzillo Nogueira
    2. Guilherme Augusto das Chagas Praser
    3. Marcelo Caldeira Pereira
    
### Sobre o aplicativo (Text-to-speech and speech-to-text converter):
    Foi desenvolvido um aplcativo contendo 03 funções básicas, conforme seguem:
    
    1. Conversão de texto para fala: Nesse caso é necessário informar o autenticador IBM watson para realizar a geração do audio. Caso não seja informado um TEXTO, será gerado um aúdio com o texto padrão (Texto não informado). Todo audio gerado posuirá o nome "audio.wav" e será gravado na pasta de instalação da aplicação. O PLAY do audio gerado será iniciado no momento da sua geração, caso seja assinalado o "check: Play Audio". O "check: Play Audio" é opcional.
    
    2. Conversão de fala para texto: Nesse caso é necessário informar o autenticador IBM watson para START de captura de voz. É opcional o assinalamento do "check: Verbose Processing", caso o mesmo seja assinalado o processamento irá apresentar resultados itermediários, caso contrário, somete apresentará o resultado final. Enquanto não for realizado STOP o canal para captura de voz estará aberto, sendo possível a utilização de qualquer outra funcionalidade em paralelo.
    
    3. Tocador de audio (wav): Nesse caso será solicitado a identificação do arquivo de audio, por meio de navegador(BROWSE) apresentado na própria aplicação. Após a identificação, sua reprodução será executada após o click no botão OK.
    
    OBS: Em toda aplicação é apresentada uma SYSOUT demonstrando toda execução que vislubramos como importante nesse momento de apredizado. 

### Dicas para instalação do aplicativo:
    1. Criar uma pasta com o nome que desejar;
    2. Baixar o projeto "Projeto_Cognitiva_2.py" na pasta criada;
    3. Baixar o "requirements.txt" na pasta criada;
    4. Executar a instalação dos requisitos do projeto:
        pip install -r requirements.txt
    5. Executar o projeto:
        python Projeto_Cognitiva_2.py
