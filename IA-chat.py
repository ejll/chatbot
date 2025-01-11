import os
import requests
import webbrowser
import unicodedata
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from flask import Flask, request, jsonify

class PapelariaChatbot:
    def __init__(self):
        """
        Inicializa o chatbot com a chave da API e o modelo.
        """
        self.api_key = "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"
        if not self.api_key:
            raise ValueError("A variável de ambiente 'GROQ_API_KEY' não foi definida.")
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "llama-3.3-70b-versatile"
        self.pdf_file_path = "https://papelariacentralparque.com.br/pdf/listaEscolar.pdf"
        self.whatsapp_number = "5515997523463" 

    def gerar_resposta(self, mensagem):
            
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": mensagem}],
            "temperature": 0.7,
            "max_tokens": 8000,
            "top_p": 0.9
        }

        try:
            response = requests.post(self.api_url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()
        except requests.exceptions.RequestException as e:
            return f"Erro ao se comunicar com a API: {e}"

    def gerar_sugestao(self, mensagem):
        """
        Envia uma mensagem para a API Groq e retorna a resposta.

        :param mensagem: Mensagem enviada pelo usuário.
        :return: Resposta gerada pela API.
       """
        sugestao = "Gere uma lista de material escolar para "+ mensagem 
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": sugestao}],
            "temperature": 0.7,
            "max_tokens": 8000,
            "top_p": 0.9
        }

        try:
            response = requests.post(self.api_url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()
        except requests.exceptions.RequestException as e:
            return f"Erro ao se comunicar com a API: {e}"

    def enviar_pdf_email(self, destinatario):
        """
        Envia o PDF por e-mail.

        :param destinatario: Endereço de e-mail do destinatário.
        """
        remetente = "ejllopes@gmail.com"
        senha = "osbsclsejbikblty"
        
        if not senha:
            raise ValueError("A variável de ambiente 'senha' não foi definida.")

         # Baixar o arquivo PDF
        pdf_response = requests.get( "https://papelariacentralparque.com.br/pdf/listaEscolar.pdf")
        pdf_response.raise_for_status()
        pdf_name = "anexo.pdf"
   
        # Salvar o PDF localmente
        with open(pdf_name, 'wb') as pdf_file:
         pdf_file.write(pdf_response.content)

        # Configuração do e-mail
        msg = MIMEMultipart()
        msg["From"] = remetente
        msg["To"] = destinatario
        msg["Subject"] = "Lista de Preços - Papelaria Central Parque"

        # Corpo do e-mail
        corpo = "Segue em anexo a lista de preços dos materiais escolares da Papelaria Central Parque."
        msg.attach(MIMEText(corpo, "plain"))

        # Anexando o PDF
        try:
            with open(pdf_name, "rb") as anexo:
                parte = MIMEBase("application", "octet-stream")
                parte.set_payload(anexo.read())
            encoders.encode_base64(parte)
            parte.add_header("Content-Disposition", f"attachment; filename=listaEscolar.pdf")
            msg.attach(parte)

            # Enviar o e-mail
            with smtplib.SMTP("smtp.gmail.com", 587) as servidor:
                servidor.starttls()
                servidor.login(remetente, senha)
                servidor.send_message(msg)
                return "PDF enviado com sucesso para o e-mail fornecido!"
        except Exception as e:
            return f"Erro ao enviar e-mail: {e}"
     
    def falar_via_whatsapp(self):
      try:
          url = f"https://wa.me/{self.whatsapp_number}"
          webbrowser.open(url)
          return "Clique no link para abrir Whats ==>" + url
      except Exception as e:
           return f"Erro ao abrir site: {e}"

    def irSitePapelaria(self):
          url = f"https://papelariacentralparque.com.br/"
          webbrowser.open(url)
          return "Clique no link para abrir o site da Papelaria Central Parque ==>" + url
    
    def generate_google_maps_link(self,start):
        origemFormatada = ''.join(
              char for char in unicodedata.normalize('NFD', start)
              if unicodedata.category(char) != 'Mn')
        destination_address = "Rua Jose Totora, 1041, Jardim Vera Cruz, Sorocaba, SP"
        base_url = "https://www.google.com/maps/dir/"
        origem = origemFormatada.replace(" ", "+")
        destination = destination_address.replace(" ", "+")
        f"{base_url}{origem}/{destination}"
        # Gera o link
        link = f"{base_url}{origem}/{destination}"
        webbrowser.open(link)
        return f"Acesse sua rota: {link}"
      
    def exibir_menu(self):
        """
        Exibe o menu de opções para o usuário.
        """
        print("\nBem-vindo ao Chatbot da Roxinha!")
        print("\nEscolha uma das opções disponíveis:")
        print("\n1 - Perguntar algo para a Roxinha")
        print("2 - Baixar lista de preços de material escolar (PDF)")
        print("3 - Enviar lista de preços por e-mail")
        print("4 - Falar pelo WhatsApp")
        print("5 - Ir Site da Papelaria Central Parque")
        print("6 - Como chegar na Papelaria Central Parque")
        print("7 - A Roxinha sugere uma lista de material escolar")
        print("0 - Sair")

    def executar_opcao(self, opcao):
        """
        Executa a opção selecionada pelo usuário.

        :param opcao: Número da opção escolhida pelo usuário.
        :return: Resposta ou ação correspondente.
        """
        if opcao == "1":
            pergunta = input("Digite sua pergunta: ")
            return self.gerar_resposta(pergunta)
        elif opcao == "2":
            print("Clique no link abaixo para baixar o PDF:")
            return f"[Baixar PDF](sandbox:{self.pdf_file_path})"
        elif opcao == "3":
            destinatario = input("Digite o e-mail do destinatário: ")
            return self.enviar_pdf_email(destinatario)
        elif opcao == "4":
          return self.falar_via_whatsapp()
        elif opcao == "5":
          return self.irSitePapelaria()
        elif opcao == "6":
            partida = input("Digite o endereço do ponto de partida:")
            return self.generate_google_maps_link(partida)
        elif opcao == "7":
           escola = input("Digite qual a série do aluno ex 1ª grau, pré-escola:")
           return self.gerar_sugestao(escola)
            
        elif opcao == "0":
            return "Obrigado por usar o chatbot da Roxinha. Até logo!"
        else:
            return "Opção inválida. Por favor, escolha uma das opções disponíveis."

    def iniciar(self):
        """
        Inicia o chatbot, permitindo interação com o usuário.
        """
        while True:
            self.exibir_menu()
            opcao = input("\nDigite o número da opção desejada: ")
            resposta = self.executar_opcao(opcao)
            print(f"\n{resposta}")

            if opcao == "0":
                break


# Inicializar e rodar o chatbot
if __name__ == "__main__":
    try:
        chatbot = PapelariaChatbot()
        chatbot.iniciar()
    except ValueError as e:
        print(f"Erro de configuração: {e}")