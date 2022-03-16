from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from email.utils import formatdate
import os

prefixo = {'js': 'text', 'html': 'text', 'plain': 'text', 'css': 'text',
           'png': 'image', 'jpeg': 'image', 'ex-icon': 'image', 'gif': 'image',
           'ogg': 'audio'}


class Especificacoes:
    def __init__(self, comando, pedido, contenttype, versao):
        self.comando = comando
        self.pedido = pedido
        self.versao = versao
        self.contenttype = None
        if contenttype:
            try:
                self.contenttype = prefixo[contenttype] + '/' + contenttype
            except KeyError:
                self.contenttype = 'application' + '/' + contenttype


class ServidorWeb:

    def __init__(self, documentos, erros):
        self.servidor_WEB = socket(AF_INET, SOCK_STREAM)
        self.endereco = 'localhost'
        self.servidor_WEB.bind((self.endereco, 4000))
        self.servidor_WEB.listen()
        self.pasta_inspecionada = documentos
        self.pasta_erros = erros

        try:
            os.mkdir(self.pasta_inspecionada)
        except FileExistsError:
            pass

        self.lista_de_documentos = os.listdir(self.pasta_inspecionada)

    def formar_erro(self, sk_cliente, tipo_erro):
        primeira_linha = f'HTTP/1.1 {tipo_erro} '
        if tipo_erro == '400':
            primeira_linha += 'Bad Request\r\n'
        elif tipo_erro == '404':
            primeira_linha += 'Not Found\r\n'
        elif tipo_erro == '505':
            primeira_linha += 'HTTP Version Not Supported\r\n'
        arquivo = f'{self.pasta_erros}/html{tipo_erro}.html'
        resposta = ''
        resposta += primeira_linha
        resposta += f'Date: {formatdate(localtime=False, usegmt=True)}\r\n'
        resposta += f'Server: {self.endereco} (Windows)\r\n'
        resposta += f'Content-Length: {os.path.getsize(arquivo)}'
        resposta += 'Content-Type: text/html\r\n'
        resposta += '\r\n'
        arq = open(arquivo, 'r')
        conteudo = arq.read()
        resposta += conteudo
        sk_cliente.send(resposta.encode())

    def formar_200(self, esp, sk_cliente):
        arquivo = self.pasta_inspecionada + esp.pedido
        if esp.contenttype is not None:
            resposta = ''
            resposta += 'HTTP/1.1 200 OK\r\n'
            resposta += f'Date: {formatdate(localtime=False, usegmt=True)}\r\n'
            resposta += f'Server: {self.endereco} (Windows)\r\n'
            resposta += f'Content-Length: {os.path.getsize(arquivo)}\r\n'
            resposta += f'Content-Type: {esp.contenttype}\r\n'
            resposta += '\r\n'
            sk_cliente.send(resposta.encode())
            print(resposta)
        try:
            arq = open(arquivo, 'rb')
            while True:
                parte = arq.read(1024)
                if len(parte) == 0:
                    break
                sk_cliente.send(parte)
        except PermissionError:
            caminho = arquivo
            if self.pasta_inspecionada in caminho:
                caminho = caminho.split(self.pasta_inspecionada + '/')[1]
                caminho += '/'
            if ' ' in caminho:
                caminho = caminho.split(' ')
                caminho = '%20'.join(caminho)
            self.formar_index(sk_cliente, os.listdir(f'{arquivo}'), caminho)

    def formar_index(self, sk_cliente, lista, arquivo):
        resposta = ''
        resposta += 'HTTP/1.1 200 OK\r\n'
        resposta += f'Date: {formatdate(localtime=False, usegmt=True)}\r\n'
        resposta += f'Server: {self.endereco} (Windows)\r\n'
        resposta += 'Content-Type: text/html\r\n'
        resposta += '\r\n'
        sk_cliente.send(resposta.encode())
        index_criado = '<!DOCTYPE html>\r\n'
        index_criado += '<html>\r\n'
        index_criado += '<head>\r\n'
        index_criado += '<title> Index ServidorWEB </title>\r\n'
        index_criado += '</head>\r\n'
        index_criado += '\r\n'
        index_criado += '<body>\r\n'
        index_criado += '<h1>Documentos disponiveis <h1>\r\n'
        if lista:
            index_criado += '<ul>\r\n'
            for documento in lista:
                if documento.split(".")[0] != 'favicon':
                    index_criado += f' <li><a href="http://localhost:4000/{arquivo}{documento}"' \
                                    f'>{documento.split(".")[0]}</a></li>\r\n'
            index_criado += '<ul>\r\n'
        index_criado += '</body>\r\n'
        index_criado += '</html>\r\n'
        print(resposta, index_criado)
        sk_cliente.send(index_criado.encode())

    def tratar_mensagem(self, msg_http):
        msg_http_tratada = msg_http.split('\r\n')[0].split(' ')
        if msg_http_tratada[1] == '/' and 'index.html' in self.lista_de_documentos:
            msg_http_tratada[1] = 'index.html'
        cttp = msg_http_tratada[1].split('.')[-1]
        if cttp[0] == '/':
            cttp = None
        if cttp == 'htm':
            cttp = 'html'
        elif cttp == 'jpg':
            cttp = 'jpeg'
        elif cttp == 'ico':
            cttp = 'ex-icon'
        elif cttp == 'txt':
            cttp = 'plain'
        if '%20' in msg_http_tratada[1]:
            msg_http_tratada[1] = msg_http_tratada[1].split('%20')
            msg_http_tratada[1] = ' '.join(msg_http_tratada[1])
        return Especificacoes(msg_http_tratada[0], msg_http_tratada[1], cttp, msg_http_tratada[2])

    def receber_mensagens(self, sk_cliente):
        while True:
            msg_http = sk_cliente.recv(2048).decode()
            if msg_http:
                print(msg_http)
                try:
                    especificacoes = self.tratar_mensagem(msg_http)

                    if especificacoes.pedido == '/':
                        self.formar_index(sk_cliente, self.lista_de_documentos, '')

                    elif especificacoes.pedido[1:].split('/')[0] not in self.lista_de_documentos:
                        self.formar_erro(sk_cliente, 404)
                        print('erro 404\n')

                    elif especificacoes.versao.split('/')[1] != '1.1':
                        self.formar_erro(sk_cliente, 505)
                        print('erro 505\n')

                    else:
                        self.formar_200(especificacoes, sk_cliente)
                        print('200 ok\n')
                except:
                    print('erro 400\n')
                    self.formar_erro(sk_cliente, 400)

    def iniciar_servidor(self):
        while True:
            (sock_cliente, endereco_cliente) = self.servidor_WEB.accept()

            Thread(target=self.receber_mensagens, args=(sock_cliente, )).start()


def configurar(arq):
    docs = arq.readline().split('-')[1][:-1]
    erros = arq.readline().split('-')[1]
    return docs, erros


doc, err = configurar(open('ConfiguracoesServidor.txt', 'r'))
serv_WEB = ServidorWeb(doc, err)
serv_WEB.iniciar_servidor()
