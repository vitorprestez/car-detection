# pip install urllib
# pip install m3u8
# pip install streamlink
from datetime import datetime, timedelta, timezone
import urllib
import m3u8
import streamlink
import cv2  # openCV
import time


def pegarStream(url):
    """
    Recebe como parâmetro uma URL de transmissão ao vivo do youtube e retorna um segmento m3u8
    """

    tentativas = 10
    for i in range(tentativas):
        try:
            streams = streamlink.streams(url)
        except:
            if i < tentativas - 1:
                print(f"Tentativa {i+1} de {tentativas}")
                # Pausa por 1 segundo
                time.sleep(1)
                continue
            else:
                raise
        break

    # Seleciona a melhor qualidade
    stream_url = streams["best"]

    # Cria um objeto M3U8
    m3u8_obj = m3u8.load(stream_url.args['url'])
    return m3u8_obj.segments[0]


def dl_stream(url, filename, chunks):
    """
    Baixa cada segmento do m3u8 e salva em um arquivo
    Recebe a url da strem, o nome do arquivo e o número de segmentos
    """
    pre_time_stamp = datetime(1, 1, 1, 0, 0, tzinfo=timezone.utc)
    
    i = 1
    while i <= chunks:

        # Abre a stream
        stream_segment = pegarStream(url)

        # Pega o tempo atual do video
        cur_time_stamp = stream_segment.program_date_time

        # Pega somente o proximo tempo do video, espera se ele ainda nao for novo
        if cur_time_stamp <= pre_time_stamp:

            # Não incrementa o contador até que tenha um novo segmento
            print("NO   pre: ", pre_time_stamp, "curr:", cur_time_stamp)
            time.sleep(1)
            pass
        else:
            print("YES: pre: ", pre_time_stamp, "curr:", cur_time_stamp)
            print(f'#{i} at time {cur_time_stamp}')

            # Abre o arquivo
            file = open(filename, 'ab+')

            # Escreve a stream no arquivo
            with urllib.request.urlopen(stream_segment.uri) as response:
                html = response.read()
                file.write(html)

            # Atualiza o tempo
            pre_time_stamp = cur_time_stamp
            time.sleep(stream_segment.duration)

            # Somente incrementa se tiver um novo segmento
            i += 1

    return None


def processarVideo(arquivo):
    # Carregar o vídeo
    video = cv2.VideoCapture(arquivo)

    # Importar classificadores treinados para detectar alguns recursos de algum objeto que queremos detectar
    classificador = cv2.CascadeClassifier('./carros.xml')

    # Loop infinito enquanto o vídeo estiver aberto
    while True:
        # Lê os frames do vídeo
        ret, frames = video.read()

        # Converte o frame para escala de cinza
        cinza = cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY)

        # Detectar carros de diferentes tamanhos no frame de entrada
        carros, niveisRejeicao, niveisConfianca = classificador.detectMultiScale3(cinza, 1.1, 1, outputRejectLevels=True)

        # Contador de objetos detectados
        i = 0
        # Desenhar um retângulo em cada carro
        for (x, y, w, h) in carros:
            # Se o nivel de confiaça for maior que 90, então considera como um carro
            if niveisConfianca[i] > 0.9:
                cv2.rectangle(frames, (x, y), (x+w, y+h), (0, 0, 255), 2)

            i += 1

        # Exibe os frames do vídeo
        cv2.imshow('Resultado', frames)

        # Se apertar ESC, interrompe o loop
        if cv2.waitKey(1) & 0XFF == 27:
            break

        # Fecha todas as janelas abertas
    cv2.destroyAllWindows()


arquivoTemporario = "temp.ts"  # files are format ts, open cv can view them
urlTransmissao = "https://www.youtube.com/watch?v=5_XSYlAfJZM&ab_channel=BradPhillips"
# urlTransmissao = "https://www.youtube.com/watch?v=jI6ELKQ9q5E&ab_channel=RustyBryant"

dl_stream(urlTransmissao, arquivoTemporario, 3)
processarVideo(arquivoTemporario)
# processarVideo("./modelo.mp4")
# processarVideo("./video.avi")
