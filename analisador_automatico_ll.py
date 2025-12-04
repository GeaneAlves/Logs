import subprocess
import os

nome_arquivo = "logs_sistema.txt"

if os.path.exists(nome_arquivo):
    os.remove(nome_arquivo)

print("--- 1. Buscando  logs do sistema (Final)---")


# AQUI ESTÁ O TRUQUE: Usamos aspas simples ' ' dentro do comando.
# Isso evita a confusão com barras invertidas (\)
comando_ps = """powershell -Command "[Console]:: OutputEncoding = [System.Text.Encoding]:: UTF8; Get-EventLog -LogName System -Newest 200 | ForEach-Object { $_.TimeGenerated.ToString() + ' | ' + $_.EntryType + ' | ' + $_.Message }" """

try:
    # check=True avisa se houver erro
    resultado = subprocess.run(comando_ps, capture_output=True, text=True, shell=True, check=True)
    # Se chegou aqui, funcionou! Vamos salvar.
    with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
        arquivo.write(resultado.stdout)
        
    print(f" Sucesso! Novo arquivo '{nome_arquivo}' gerado.")
    
except subprocess.CalledProcessError as e:
    print(f" Erro no PowerShell: {e.stderr}")
except Exception as e:
    print(f" Erro crítico: {e}")

#\n quebra de linha para separar as etapas.
print("\n--- 2. Analisando o arquivo ---")


erros_encontrados = []
# os erros em duas línguas para facilitar a detecção
termos_suspeitos = ["erro", "falha", "critico", "aviso", "warn", "fail", "error"]

# Só tentamos analisar se o arquivo realmente foi criado no passo 1
if os.path.exists(nome_arquivo):
    try:
        with open(nome_arquivo, "r", encoding="utf-8") as f:
            for linha in f:

                if any(termo in linha.lower() for termo in termos_suspeitos) and len(linha.strip()) >5:
                    erros_encontrados.append(linha.strip())

        if erros_encontrados:
            print(f"Encontrados {len(erros_encontrados)} eventos:")
            print("-" * 60)
            
            # Mostra os primeiros 10
            for erro in erros_encontrados[:10]:
                print(f" -> {erro}")
            
            if len(erros_encontrados) > 10:
                print(f" ... e mais {len(erros_encontrados) - 10} ocultos.")
        else:
            print("Sistema limpo! Nenhum erro grave encontrado.")

    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
else:
    print("Arquivo não encontrado.")


    # Fim do script

    # Conceito de Log:
    # Logs são registros automáticos que sistemas e aplicativos criam para documentar eventos, erros e atividades.
    # Eles ajudam na solução de problemas e monitoramento do sistema.
    # Exemplos incluem logs de erros do sistema operacional, registros de acesso a sites e logs de atividades de aplicativos.
    # Analisar logs é crucial para identificar e resolver problemas rapidamente.
    # Logs geralmente contêm informações como data, hora, tipo de evento e detalhes do evento.
    # Ferramentas de análise de logs automatizam a leitura e interpretação desses registros, facilitando a detecção de padrões e problemas.
    # Em resumo, logs são essenciais para manter a saúde e segurança de sistemas e aplicativos.
    # Eles fornecem insights valiosos para administradores e desenvolvedores.
    # Automação na análise de logs economiza tempo e melhora a eficiência na resolução de problemas.
    # troubleshooting é o processo de identificar, diagnosticar e resolver problemas técnicos em sistemas ou dispositivos.
    # Envolve etapas como coleta de informações, análise de logs, testes e implementação de soluções.
    # O objetivo do troubleshooting é restaurar o funcionamento normal do sistema de forma eficiente.
    # É uma habilidade essencial para profissionais de TI e suporte técnico.
    # Rastreabilidade refere-se à capacidade de acompanhar e documentar o histórico, localização ou uso de um item ou informação ao longo do tempo.
    # Em tecnologia, isso pode incluir o rastreamento de mudanças em software, histórico de transações ou movimentação de dados.
    # A rastreabilidade é importante para auditoria, conformidade e solução de problemas.
