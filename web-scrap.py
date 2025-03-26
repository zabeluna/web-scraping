import requests
from bs4 import BeautifulSoup
import os
import shutil

link = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
request = requests.get(link)
site = BeautifulSoup(request.text, "html.parser")
print(site.title)

anexos = []
for a in site.find_all("a"):
    titulo_anexo = a.text.strip()
    link = a.get("href")
    
    if titulo_anexo.startswith("Anexo") and link and link.endswith(".pdf"):
        anexos.append((titulo_anexo, link))

if anexos:
    print("Anexos encontrados:")
    for titulo, link in anexos:
        print(titulo + ":" + link)
else:
    print("Erro!")

os.makedirs("anexos", exist_ok=True)

for titulo, link in anexos:
    nome = "anexos/" + titulo.replace(" ", "_") + ".pdf" 
    print("Baixando:", titulo)
    
    response = requests.get(link)
    if response.status_code == 200:
        with open(nome, "wb") as arquivo:
            arquivo.write(response.content)
        print("OK!")
    else:
        print("Erro!")

shutil.make_archive("anexos_compactados", "zip", "anexos")
print("Compactado!")
