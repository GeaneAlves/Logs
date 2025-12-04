import subprocess
import os

print("--- 1. Buscando logs do sistema ---")

# CORREÇÃO AQUI: Mudamos de -Comand para -Command
comando_ps = 'powershell -Command "Get-EventLog -LogName System -Newest 200 | Format-List"'

nome_arquivo = "logs_sistema.txt"

try:
    # check=True faz o Python avisar se o PowerShell der erro
    resultado = subprocess.run(comando_ps, capture_output=True, text=True, shell=True, check=True)

    # Se chegou aqui, o comando funcionou. Vamos salvar o conteúdo.
    conteudo_logs = resultado.stdout

    with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
        arquivo.write(conteudo_logs)
        
    print(f"   Sucesso! Arquivo '{nome_arquivo}' gerado nesta pasta.")
    
except subprocess.CalledProcessError as e:
    # Se o PowerShell reclamar, mostramos o erro exato
    print(f"   Erro ao executar PowerShell: {e.stderr}")
except Exception as e:
    print(f"   Erro crítico: {e}")

print("\n--- 2. Analisando o arquivo ---")

erros_encontrados = []
termos_suspeitos = ["erro", "falha", "critico", "aviso", "warn", "fail", "error"]

# Só tentamos analisar se o arquivo realmente foi criado no passo 1
if os.path.exists(nome_arquivo):
    try:
        with open(nome_arquivo, "r", encoding="utf-8") as f:
            for linha in f:
                if any(termo in linha.lower() for termo in termos_suspeitos):
                    erros_encontrados.append(linha.strip())

        if erros_encontrados:
            print(f"Encontrados {len(erros_encontrados)} indícios de problemas:")
            print("-" * 40)
            
            # Mostra os primeiros 10
            for erro in erros_encontrados[:10]:
                print(f" -> {erro}")
            
            if len(erros_encontrados) > 10:
                print(f" ... e mais {len(erros_encontrados) - 10} ocorrências.")
        else:
            print("Nenhum erro grave encontrado nos últimos 200 eventos.")

    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
else:
    print("O arquivo de log não foi encontrado. A etapa 1 falhou?")