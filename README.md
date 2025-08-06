🧬 De Genética a Dados: Minha Jornada Analisando a Netflix
Como uma estudante de Biologia e Ciência de Dados descobriu padrões no catálogo da Netflix

Olá! Me chamo Maria Rodrigues. Minha jornada na tecnologia começou nas Ciências Biológicas, com foco em Genética e Bioinformática, e hoje se expande com minha graduação em Ciência de Dados. Este projeto nasceu da intersecção dessas duas paixões, combinando:

🧪 Meu raciocínio analítico da pesquisa científica

📊 Técnicas de modelagem e engenharia de dados

🎬 Minha paixão pessoal por filmes e séries

🌱 Como Tudo Começou
Durante minha iniciação científica em Bioinformática, percebi que as técnicas que usava para analisar sequências genéticas poderiam ser aplicadas para "sequenciar" os gêneros da Netflix. Afinal:

"Analisar gêneros de filmes não é tão diferente de estudar genes, até porque ambos envolvem padrões, combinações e evolução ao longo do tempo."

🔍 O Que Você Vai Encontrar Aqui
Um dashboard interativo que conta histórias através de dados, revelando:

Como os padrões de popularidade se assemelham à expressão gênica

A "filogenia" dos gêneros (quais tendem a aparecer juntos)

Mutações culturais (como gêneros evoluem com o tempo)

📊 Arquitetura do Projeto
O diagrama abaixo resume o fluxo de dados e a arquitetura modular deste projeto. O foco principal é garantir a integridade e consistência dos dados desde a origem até a visualização.

🔄 movies_dataset.py: O coração do pipeline de ETL (Extração, Transformação, Carga). Este script é responsável por ler o CSV bruto, executar uma limpeza rigorosa e consolidação de gêneros para garantir a consistência dos dados, e salvar a versão tratada que alimenta o dashboard.

📊 app.py: Carrega os dados já processados e limpos, executa as análises e envia os resultados ao frontend via Streamlit, garantindo performance com o uso de cache.

🎨 style.css e config.toml: Personalizam o layout e comportamento do aplicativo Streamlit.

🧩 Visualization Engine: Gera os gráficos interativos exibidos ao usuário.

🌐 Client Browser: É onde o usuário interage com o app, visualizando as análises diretamente no navegador.

📚 requirements.txt e demais documentos: Listam as dependências e informações adicionais sobre o projeto.

🚧 Desafios e Evolução do Projeto
Todo projeto de dados apresenta desafios, e este não foi exceção. A principal dificuldade foi garantir a consistência na categorização dos gêneros, um problema que evoluiu em duas etapas:

O Desafio Inicial: Os dados brutos continham múltiplas variações para o mesmo gênero (ex: "Sci-Fi", "Science Fiction", "sci fi"). A primeira versão do tratamento de dados tentou resolver isso diretamente no app do Streamlit, mas a inconsistência persistia visualmente.

O Diagnóstico: Após uma depuração cuidadosa, identifiquei que o problema não estava no app, mas sim no pipeline de dados. O script de pré-processamento (movies_dataset.py) gerava um arquivo CSV com uma limpeza superficial, e o app do Streamlit lia esses dados já "contaminados". Qualquer limpeza feita no app era ineficaz.

A Solução Definitiva: A arquitetura foi refatorada. Toda a lógica de limpeza, padronização e consolidação de gêneros foi centralizada no script movies_dataset.py. Isso garantiu que o arquivo data_tratada.csv fosse a fonte única da verdade (Single Source of Truth), com dados íntegros e consistentes. O app do Streamlit foi então simplificado para apenas carregar e visualizar os dados já tratados.

Essa experiência reforçou a importância de um pipeline de dados robusto e da depuração metódica para garantir a qualidade do produto final.

🚀 Próximos Passos e Aprimoramentos Futuros
Este projeto é uma base sólida, mas a análise de dados é um processo contínuo de descoberta. Os próximos passos planejados incluem:

Implementar um Sistema de Recomendação: Desenvolver um modelo de recomendação baseado em conteúdo (Content-Based Filtering). O usuário poderá selecionar um filme que gostou, e o sistema sugerirá outros títulos com base na similaridade de gêneros e outros atributos.

Análise de Sentimentos: Se os dados permitirem (ou com a adição de um novo dataset de reviews), aplicar técnicas de NLP para analisar o sentimento das críticas e correlacioná-lo com as notas do IMDb.

Visualizações Avançadas: Criar um gráfico de rede para visualizar as conexões entre gêneros, mostrando quais pares aparecem juntos com mais frequência e a força dessa conexão.

Modelo Preditivo: Treinar um modelo de Machine Learning (ex: Regressão) para prever a nota do IMDb de um título com base em seus atributos, como gênero, tipo e ano de lançamento.

🛠️ Para Iniciar a Análise
# Clone este repositório (meu primeiro projeto público!)
git clone [https://github.com/mulinco/analysis-genre-netflix.git](https://github.com/mulinco/analysis-genre-netflix.git)

# Instale as dependências
pip install -r requirements.txt

# Execute o dashboard
streamlit run app.py

Ou então, acesse diretamente pelo link do Streamlit Cloud.

📚 Meu Processo de Aprendizado
Habilidade Biológica

Equivalente em Dados

O Que Aprendi

Análise de sequências

Processamento de texto

Padronizar e consolidar categorias de gêneros como faço com sequências de genes.

Alinhamento múltiplo

Data cleaning

Identificar e tratar "mutações" (inconsistências) nos dados.

Depuração de protocolos

Depuração de pipeline

Isolar a origem de um erro (script de processamento vs. app) e garantir a integridade dos dados desde a fonte.

Árvores filogenéticas

Clusterização

Agrupar gêneros que frequentemente aparecem juntos para entender suas relações.

🤝 Como Você Pode Me Ajudar
Como uma profissional que une as áreas de Biologia e Ciência de Dados, adoraria:

✏️ Feedback sobre minha abordagem analítica

💻 Sugestões para melhorar o código

🔗 Conexões com oportunidades em análise de dados, bioinformática e áreas correlatas.

Vamos conversar! mariarodrigues.ufrj@gmail.com | Meu LinkedIn
