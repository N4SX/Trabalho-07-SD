import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import glob
import numpy as np # Import numpy for calculating mean safely

# --- Configuração ---
# Diretórios contendo os resultados de cada cenário
scenario_dirs = {
    'Cenário A (Leve)': 'cenario_a',
    'Cenário B (Moderado)': 'cenario_b',
    'Cenário C (Pico)': 'cenario_c'
}
# Garante a ordem dos cenários para o gráfico de linha
scenario_order = ['Cenário A (Leve)', 'Cenário B (Moderado)', 'Cenário C (Pico)']

# Métricas a serem extraídas e plotadas
metrics_config = {
    'Tempo Médio de Resposta (ms)': {'csv_col': 'Average Response Time', 'plot_type': 'line'},
    'Tempo Máximo de Resposta (ms)': {'csv_col': 'Max Response Time', 'plot_type': 'line'},
    'Requisições por Segundo (req/s)': {'csv_col': 'Requests/s', 'plot_type': 'line'},
    'Total de Requisições': {'csv_col': 'Request Count', 'plot_type': 'bar'},
    'Total de Erros': {'csv_col': 'Failure Count', 'plot_type': 'bar'},
    'Percentual de Sucesso (%)': {'csv_col': 'Success Percentage', 'plot_type': 'line'} # Será calculado
}

# Colunas que precisamos ler dos CSVs (incluindo as necessárias para cálculo)
required_cols = ['Name', 'Request Count', 'Failure Count',
                 'Average Response Time', 'Max Response Time', 'Requests/s']

# --- Processamento dos Dados ---
results = {}

print("Processando resultados...")

for scenario_name, dir_path in scenario_dirs.items():
    print(f"  Processando {scenario_name} em '{dir_path}'...")
    if not os.path.isdir(dir_path):
        print(f"    AVISO: Diretório '{dir_path}' não encontrado. Pulando cenário.")
        continue

    stat_files = glob.glob(os.path.join(dir_path, 'run*_stats.csv'))

    if not stat_files:
        print(f"    AVISO: Nenhum arquivo 'run*_stats.csv' encontrado em '{dir_path}'.")
        continue

    print(f"    Encontrados {len(stat_files)} arquivos de stats.")

    scenario_metrics_data = {metric: [] for metric in metrics_config}

    for i, file_path in enumerate(stat_files):
        try:
            df = pd.read_csv(file_path)
            agg_row = df[df['Name'] == 'Aggregated']

            if agg_row.empty:
                 agg_row = df.iloc[[-1]]
                 if agg_row.empty or agg_row['Type'].iloc[0] == 'None':
                    print(f"      AVISO: Linha 'Aggregated' não encontrada ou inválida em {os.path.basename(file_path)}. Pulando arquivo.")
                    continue

            request_count = agg_row['Request Count'].iloc[0]
            failure_count = agg_row['Failure Count'].iloc[0]

            # Extrai/Calcula métricas baseado na configuração
            for metric_name, config in metrics_config.items():
                csv_col = config['csv_col']
                if csv_col == 'Success Percentage':
                    if request_count > 0:
                        value = ((request_count - failure_count) / request_count) * 100
                    else:
                        value = 100
                    scenario_metrics_data[metric_name].append(value)
                else:
                    if csv_col in agg_row.columns:
                         scenario_metrics_data[metric_name].append(agg_row[csv_col].iloc[0])
                    else:
                         print(f"      AVISO: Coluna '{csv_col}' não encontrada em {os.path.basename(file_path)} para métrica '{metric_name}'.")
                         scenario_metrics_data[metric_name].append(np.nan) # Adiciona NaN se a coluna não existir


        except Exception as e:
            print(f"      ERRO ao processar arquivo {os.path.basename(file_path)}: {e}")

    # Calcula a média para o cenário
    avg_results = {}
    valid_scenario = False
    for metric, values in scenario_metrics_data.items():
        if values:
            avg_results[metric] = np.mean([v for v in values if not np.isnan(v)]) # Calcula média ignorando NaNs
            if not np.isnan(avg_results[metric]): # Verifica se a média é válida
                 valid_scenario = True
        else:
            avg_results[metric] = np.nan
            print(f"    AVISO: Sem dados válidos para a métrica '{metric}' em {scenario_name}.")

    if valid_scenario:
        results[scenario_name] = avg_results
    else:
        print(f"    AVISO: Nenhum dado válido processado para {scenario_name}. Cenário será omitido nos gráficos.")


if not results:
    print("\nERRO: Nenhum dado de cenário foi processado com sucesso. Verifique os diretórios e arquivos CSV.")
else:
    # Cria um DataFrame do Pandas com os resultados médios e reordena as colunas/linhas
    results_df = pd.DataFrame(results).T # Transpõe para ter cenários nas linhas
    results_df = results_df.reindex(scenario_order) # Garante a ordem correta para gráficos de linha

    print("\nResultados Médios por Cenário:")
    print(results_df)

    # --- Geração dos Gráficos ---
    print("\nGerando gráficos...")
    sns.set_theme(style="whitegrid")

    plot_count = 0
    plt.style.use('seaborn-v0_8-talk') # Um estilo visual um pouco mais moderno

    for plot_title, config in metrics_config.items():
        if plot_title not in results_df.columns:
             print(f"  AVISO: Métrica '{plot_title}' não encontrada nos resultados processados. Pulando gráfico.")
             continue

        if results_df[plot_title].isnull().all():
            print(f"  AVISO: Sem dados válidos para plotar '{plot_title}'. Pulando gráfico.")
            continue

        plt.figure(figsize=(10, 6))
        plot_type = config['plot_type']
        y_label = plot_title.split('(')[0].strip()

        if plot_type == 'line':
            line_plot = sns.lineplot(x=results_df.index, y=results_df[plot_title], marker='o', sort=False, linewidth=2.5) # sort=False para manter a ordem definida
            # Adiciona os valores nos pontos
            for x, y in zip(results_df.index, results_df[plot_title]):
                 if not np.isnan(y): # Só adiciona label se o valor não for NaN
                      plt.text(x, y, f'{y:.2f}', ha='center', va='bottom')
            plt.ylabel(y_label, fontsize=12)


        elif plot_type == 'bar':
            bar_plot = sns.barplot(x=results_df.index, y=results_df[plot_title], palette="viridis")
            # Adiciona os valores nas barras
            for container in bar_plot.containers:
                bar_plot.bar_label(container, fmt='%.2f')
            plt.ylabel(y_label, fontsize=12)

        # Configurações comuns
        plt.title(plot_title, fontsize=16, pad=20)
        plt.xlabel("Cenário de Teste", fontsize=12)
        plt.xticks(rotation=0)
        plt.tight_layout()

        # Salva o gráfico
        filename = f"grafico_{plot_title.split('(')[0].strip().replace(' ', '_').lower()}.png"
        try:
             plt.savefig(filename)
             print(f"  Gráfico '{plot_title}' salvo como '{filename}'")
             plot_count += 1
        except Exception as e:
            print(f"  ERRO ao salvar gráfico '{filename}': {e}")

    if plot_count > 0:
        print(f"\n{plot_count} gráficos gerados com sucesso.")
        plt.show() # Mostra todos os gráficos gerados
    else:
        print("\nNenhum gráfico pôde ser gerado devido à falta de dados.")

print("\nScript finalizado.")