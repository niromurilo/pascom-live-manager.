import requests

resposta = requests.get("https://liturgia.cancaonova.com/pb/", timeout=10)

with open("pagina_liturgia.html", "w", encoding="utf-8") as arquivo:
    arquivo.write(resposta.text)

print("Salvo em pagina_liturgia.html")