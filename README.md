<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>README: De Genética a Dados</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Inter', sans-serif;
        }
        .prose h1, .prose h2, .prose h3 {
            color: #f3f4f6; /* gray-100 */
        }
        .prose a {
            color: #93c5fd; /* blue-300 */
            text-decoration: none;
            transition: color 0.2s;
        }
        .prose a:hover {
            color: #60a5fa; /* blue-400 */
            text-decoration: underline;
        }
        .prose blockquote {
            border-left-color: #0ea5e9; /* sky-500 */
            background-color: rgba(14, 165, 233, 0.05);
            color: #d1d5db; /* gray-300 */
            padding-top: 0.5rem;
            padding-bottom: 0.5rem;
        }
        .prose code {
            background-color: #374151; /* gray-700 */
            color: #f3f4f6; /* gray-100 */
            padding: 0.2em 0.4em;
            border-radius: 6px;
        }
        .prose pre {
            background-color: #111827; /* gray-900 */
            border: 1px solid #374151; /* gray-700 */
            padding: 1.25em;
            border-radius: 8px;
        }
        .prose table {
            width: 100%;
            border-collapse: collapse;
        }
        .prose th, .prose td {
            border: 1px solid #4b5563; /* gray-600 */
            padding: 0.75em 1em;
        }
        .prose th {
            background-color: #374151; /* gray-700 */
            font-weight: 600;
        }
        .prose tbody tr:hover {
            background-color: rgba(55, 65, 81, 0.5);
        }
        .section-icon {
            display: inline-block;
            margin-right: 0.75rem;
            vertical-align: middle;
            width: 1.5rem;
            height: 1.5rem;
        }
    </style>
</head>
<body class="bg-gray-900 text-gray-300 antialiased">

    <main class="prose prose-invert max-w-4xl mx-auto p-6 sm:p-8">
        <h1 class="text-4xl font-bold mb-4">🧬 De Genética a Dados: Minha Jornada Analisando a Netflix</h1>
        <p class="text-xl text-gray-400"><strong>Como uma estudante de Biologia e Ciência de Dados descobriu padrões no catálogo da Netflix</strong></p>
        
        <p class="mt-6">Olá! Me chamo Maria Rodrigues. Minha jornada na tecnologia começou nas Ciências Biológicas, com foco em Genética e Bioinformática, e hoje se expande com minha graduação em <strong>Ciência de Dados</strong>. Este projeto nasceu da intersecção dessas duas paixões, combinando:</p>
        <ul class="mt-4 space-y-2">
            <li>🧪 Meu raciocínio analítico da pesquisa científica</li>
            <li>📊 Técnicas de modelagem e engenharia de dados</li>
            <li>🎬 Minha paixão pessoal por filmes e séries</li>
        </ul>

        <hr class="my-12 border-gray-700">

        <h2><svg class="section-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M12 6.042A8.967 8.967 0 006 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 016 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 016-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0018 18a8.967 8.967 0 00-6 2.292m0-14.25v14.25" /></svg>Como Tudo Começou</h2>
        <p>Durante minha iniciação científica em Bioinformática, percebi que as técnicas que usava para analisar sequências genéticas poderiam ser aplicadas para "sequenciar" os gêneros da Netflix. Afinal:</p>
        <blockquote class="italic">
            <p>"Analisar gêneros de filmes não é tão diferente de estudar genes, até porque ambos envolvem padrões, combinações e evolução ao longo do tempo."</p>
        </blockquote>

        <h2 class="mt-12"><svg class="section-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" /></svg>O Que Você Vai Encontrar Aqui</h2>
        <p>Um dashboard interativo que conta histórias através de dados, revelando:</p>
        <ul class="mt-4 space-y-2">
            <li>Como os <strong>padrões de popularidade</strong> se assemelham à expressão gênica</li>
            <li>A <strong>"filogenia" dos gêneros</strong> (quais tendem a aparecer juntos)</li>
            <li><strong>Mutações culturais</strong> (como gêneros evoluem com o tempo)</li>
        </ul>

        <h3 class="mt-8">📊 Arquitetura do Projeto</h3>
        <p>O diagrama abaixo resume o fluxo de dados e a arquitetura modular deste projeto. O foco principal é garantir a <strong>integridade e consistência dos dados</strong> desde a origem até a visualização.</p>
        <ul class="mt-4 list-disc list-inside space-y-2">
            <li>🔄 <strong>movies_dataset.py</strong>: O coração do pipeline de ETL. Este script executa uma <strong>limpeza rigorosa e consolidação de gêneros</strong>, salvando uma versão tratada que alimenta o dashboard.</li>
            <li>📊 <strong>app.py</strong>: Carrega os dados já processados e limpos e envia os resultados ao frontend via Streamlit, garantindo performance com o uso de cache.</li>
            <li>🎨 <strong>style.css</strong> e <strong>config.toml</strong>: Personalizam o layout e comportamento do aplicativo Streamlit.</li>
        </ul>

        <hr class="my-12 border-gray-700">

        <h2><svg class="section-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z" /></svg>Desafios e Evolução do Projeto</h2>
        <p>Todo projeto de dados apresenta desafios. A principal dificuldade foi garantir a <strong>consistência na categorização dos gêneros</strong>, um problema que evoluiu em três etapas:</p>
        <ol class="mt-4 space-y-2 list-decimal list-inside">
            <li><strong>O Desafio Inicial:</strong> Os dados brutos continham múltiplas variações para o mesmo gênero (ex: "Sci-Fi", "Science Fiction", "sci fi").</li>
            <li><strong>O Diagnóstico:</strong> Após uma depuração cuidadosa, identifiquei que o problema estava no <strong>pipeline de dados</strong>. O script de pré-processamento gerava um arquivo CSV com uma limpeza superficial.</li>
            <li><strong>A Solução Definitiva:</strong> A arquitetura foi refatorada. Toda a lógica de limpeza foi centralizada no script <code>movies_dataset.py</code>, garantindo que o arquivo <code>data_tratada.csv</code> se tornasse a <strong>fonte única da verdade (Single Source of Truth)</strong>.</li>
        </ol>
        <p class="mt-4">Essa experiência reforçou a importância de um pipeline de dados robusto e da depuração metódica para garantir a qualidade do produto final.</p>

        <h2 class="mt-12"><svg class="section-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" /></svg>Próximos Passos e Aprimoramentos Futuros</h2>
        <p>Este projeto é uma base sólida, mas a análise de dados é um processo contínuo. Os próximos passos planejados incluem:</p>
        <ol class="mt-4 space-y-2 list-decimal list-inside">
            <li><strong>Implementar um Sistema de Recomendação:</strong> Desenvolver um modelo de recomendação baseado em conteúdo (Content-Based Filtering).</li>
            <li><strong>Análise de Sentimentos:</strong> Aplicar técnicas de NLP para analisar o sentimento das críticas e correlacioná-lo com as notas do IMDb.</li>
            <li><strong>Visualizações Avançadas:</strong> Criar um gráfico de rede para visualizar as conexões entre gêneros.</li>
            <li><strong>Modelo Preditivo:</strong> Treinar um modelo de Machine Learning para prever a nota do IMDb de um título.</li>
        </ol>

        <hr class="my-12 border-gray-700">

        <h2><svg class="section-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M17.25 6.75L22.5 12l-5.25 5.25m-10.5 0L1.5 12l5.25-5.25m7.5-3l-4.5 16.5" /></svg>Para Iniciar a Análise</h2>
        <pre><code># Clone este repositório
git clone https://github.com/mulinco/analysis-genre-netflix.git

# Instale as dependências
pip install -r requirements.txt

# Execute o dashboard
streamlit run app.py
</code></pre>
        <p class="mt-4">Ou então, acesse diretamente pelo link do <a href="https://analysis-genre-netflix.streamlit.app/" target="_blank" class="font-semibold"><strong>Streamlit Cloud</strong></a>.</p>

        <h2 class="mt-12"><svg class="section-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" /></svg>Meu Processo de Aprendizado</h2>
        <div class="overflow-x-auto mt-4">
            <table>
                <thead>
                    <tr>
                        <th>Habilidade Biológica</th>
                        <th>Equivalente em Dados</th>
                        <th>O Que Aprendi</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Análise de sequências</td>
                        <td>Processamento de texto</td>
                        <td>Padronizar e consolidar categorias de gêneros como faço com sequências de genes.</td>
                    </tr>
                    <tr>
                        <td>Alinhamento múltiplo</td>
                        <td>Data cleaning</td>
                        <td>Identificar e tratar "mutações" (inconsistências) nos dados.</td>
                    </tr>
                    <tr>
                        <td>Depuração de protocolos</td>
                        <td>Depuração de pipeline</td>
                        <td><strong>Isolar a origem de um erro e garantir a integridade dos dados desde a fonte.</strong></td>
                    </tr>
                    <tr>
                        <td>Árvores filogenéticas</td>
                        <td>Clusterização</td>
                        <td>Agrupar gêneros que frequentemente aparecem juntos para entender suas relações.</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <hr class="my-12 border-gray-700">

        <h2><svg class="section-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M7.5 8.25h9m-9 3H12m-9.75 1.51c0 1.6 1.123 2.994 2.707 3.227 1.129.166 2.27.293 3.423.379.35.026.67.21.865.501L12 21l2.755-4.133a1.14 1.14 0 01.865-.501 48.172 48.172 0 003.423-.379c1.584-.233 2.707-1.626 2.707-3.228V6.741c0-1.602-1.123-2.995-2.707-3.228A48.394 48.394 0 0012 3c-2.392 0-4.744.175-7.043.513C3.373 3.746 2.25 5.14 2.25 6.741v6.018z" /></svg>Como Você Pode Me Ajudar</h2>
        <p class="mt-4">Como uma profissional que une as áreas de Biologia e Ciência de Dados, adoraria:</p>
        <ul class="mt-4 space-y-2">
            <li>✏️ Feedback sobre minha abordagem analítica</li>
            <li>💻 Sugestões para melhorar o código</li>
            <li>🔗 Conexões com oportunidades em análise de dados, bioinformática e áreas correlatas.</li>
        </ul>
        <p class="mt-6 text-center text-lg">
            Vamos conversar! <a href="mailto:mariarodrigues.ufrj@gmail.com" class="font-semibold">mariarodrigues.ufrj@gmail.com</a> | <a href="https://linkedin.com/in/mariaclararodrigues3113" target="_blank" class="font-semibold">Meu LinkedIn</a>
        </p>

    </main>

</body>
</html>
