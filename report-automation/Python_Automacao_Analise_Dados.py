import pyautogui
import pyperclip
import time
import pandas

import pyautogui
import time

pyautogui.PAUSE = 0.5

# Passo a passo do desafio
# Passo 1: Entrar no sistema da empresa (link do drive)
# abrir o Chrome
pyautogui.press("win")
time.sleep(2)
pyautogui.write("chrome")
time.sleep(2)
pyautogui.press("enter")

time.sleep(2)

# digitei o link do sistema
link = "https://drive.google.com/drive/folders/149xknr9JvrlEnhNWO49zPcw0PW5icxga" 
pyautogui.write(link)
# apertei enter e esperei
pyautogui.press("enter")
time.sleep(3)



# Passo 2: Navegar no sistema para encontrar a base de dados
pyautogui.click(x=492, y=417, clicks=2)
time.sleep(1)

# Passo 3: Exportar a base de dados (baixar o arquivo)
# pyautogui.click(x=401, y=510) # seleciona o arquivo
# pyautogui.click(x=1810, y=518) # clica nos 3 pontos
pyautogui.click(x=1660, y=421) # baixa o arquivo
time.sleep(3)



# Passo 4: Calcular os indicadores (faturamento e quantidade de produtos vendidos)
# abrir a base de dados
caminho = r"C:\Users\user\Downloads\Vendas - Dez.xlsx"
tabela = pandas.read_excel(caminho)



# somar o faturamento de todos os produtos = somar a coluna de Valor Final
faturamento = tabela["Valor Final"].sum()
# somar a quantidade de produtos = somar a coluna de quantidade
qtde_produtos = tabela["Quantidade"].sum()

print(faturamento)
print(qtde_produtos)



# Passo 5: Enviar as informações por e-mail
# abrir uma nova aba
pyautogui.hotkey("ctrl", "t")
time.sleep(3)
# entrar no email
pyautogui.write("http://mail.google.com/")
pyautogui.press("enter")
time.sleep(8)

# clicar no botão escrever
pyautogui.click(x=188, y=222)
time.sleep(6)

# para quem enviar o email
pyautogui.write("pythonimpressionador@gmail.com")
time.sleep(2)
pyautogui.press("tab") # seleciona o email
time.sleep(2)
pyautogui.press("tab") # passar para o campo do assunto

# qual o assunto
pyperclip.copy("Relatório de Vendas")
time.sleep(2)
pyautogui.hotkey("ctrl", "v")
time.sleep(2)
pyautogui.press("tab")

# qual o corpo do email
texto = f"""
Prezados,

Segue o relatório de vendas de hoje.

Faturamento: R${faturamento:,.2f}
Quantidade de produtos vendidos: {qtde_produtos:,}

Qualquer dúvida estou à disposição.
Abs,
Lira Python
"""
pyperclip.copy(texto)
pyautogui.hotkey("ctrl", "v")

# enviar o email
pyautogui.click(x=1222, y=956)