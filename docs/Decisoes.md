# Registro de Decisões Técnicas — Pascom Live Manager

Este documento registra decisões técnicas relevantes e o motivo de cada uma —
não a jornada até chegar nelas. Isso o histórico de commits já guarda.

## 1. Biblioteca de comunicação com o OBS: obsws-python

**Decisão:** usar `obsws-python` para conectar e controlar o OBS Studio.

**Motivo:** desde a versão 28, o OBS inclui nativamente um servidor WebSocket
no protocolo v5. `obsws-python` foi feita especificamente para esse protocolo,
e os nomes dos métodos seguem os comandos oficiais em snake_case
(`SetInputSettings` → `set_input_settings`).

**Alternativa considerada:** `obs-websocket-py`, construída para o protocolo
v4, usado antes da versão 28. Descartada por não ser a via atual.

## 2. Fonte da liturgia: Canção Nova, não a CNBB oficial

**Decisão:** buscar a liturgia diária em `liturgia.cancaonova.com`.

**Motivo:** a página oficial (`cnbb.org.br/liturgia-diaria`) é só uma página
de menu. O conteúdo real está em `liturgiadiaria.edicoescnbb.com.br`, que
renderiza via JavaScript (Next.js) — uma requisição HTTP simples retorna
página vazia, exigindo Selenium ou Playwright pra ler. A Canção Nova publica
o mesmo conteúdo oficial (copyright da CNBB confirmado no rodapé) já
renderizado no servidor, extraível com `requests` + `BeautifulSoup`.

**Risco assumido:** depender da estrutura HTML de terceiros, que pode mudar
sem aviso (a própria CNBB já trocou de plataforma uma vez). Mitigado
isolando busca e extração em funções próprias, pra que uma mudança no site
afete só essas funções.

## 3. Estrutura de dados: dataclass em vez de dict

**Decisão:** representar a liturgia extraída com `LiturgiaDoDia`, uma
dataclass, não um dicionário solto.

**Motivo:** erro de digitação numa chave de dict só aparece em tempo de
execução. Com dataclass, o editor sinaliza antes de rodar, e habilita
autocomplete. `frozen=True` porque o objeto representa um retrato fixo da
liturgia de um dia — nada deveria alterá-lo depois de criado.

## 4. Extração de texto por parágrafo, não pelo container inteiro

**Decisão:** extrair o texto de cada `<p>` separadamente, sem separador entre
eles, em vez de pedir o texto de todo o container de uma vez.

**Motivo:** o método padrão do BeautifulSoup insere quebra de linha em toda
transição de tag, incluindo tags inline (`<strong>` nos números de
versículo), quebrando frases no meio. Por parágrafo, o espaçamento original
do HTML permanece correto.

## 5. Credenciais do OBS fora do controle de versão

**Decisão:** a senha do WebSocket nunca deve ser commitada com valor real;
placeholder no código versionado.

**Motivo:** repositório público — qualquer segredo commitado fica no
histórico do Git permanentemente, mesmo substituído depois. Um valor real
chegou a ser commitado numa etapa inicial; corrigido rotacionando a senha
no OBS.

## 6. Git: branch por etapa a partir da Sprint 2

**Decisão:** cada etapa nova nasce numa branch própria, integrada à `main`
via Pull Request (GitHub Flow).

**Motivo:** o programa roda minutos antes de transmissões reais, toda
semana — `main` precisa continuar íntegra mesmo com trabalho em andamento
em outro lugar. Também prepara o projeto para colaboração futura.

## 7. Integracao da liturgia com o OBS em arquivo proprio

**Decisao:** criar `atualizar_liturgia_no_obs.py` como uma camada de
integracao entre a extracao da liturgia e a atualizacao das fontes no OBS.

**Motivo:** `buscar_liturgia.py` deve continuar responsavel por buscar e
extrair dados da pagina, enquanto `sprint1_titulo.py` continua concentrando o
acesso basico ao OBS. O novo arquivo apenas orquestra as duas partes e mapeia
`titulo`, `leitura1` e `salmo` para `PLM_TITULO`, `PLM_LEITURA1` e
`PLM_SALMO`.

**Alternativas consideradas:** colocar essa logica dentro de
`buscar_liturgia.py` ou dentro de `sprint1_titulo.py`. Descartadas porque
misturariam responsabilidades. Criar uma arquitetura em `src/` tambem foi
adiado para evitar complexidade antes do MVP pedir isso.

**Risco assumido:** a integracao ainda reaproveita `OBS_HOST`, `OBS_PORT` e
`OBS_SENHA` de `sprint1_titulo.py`. No futuro, essas configuracoes devem ir
para variaveis de ambiente ou arquivo local ignorado pelo Git.

## 8. Animated Lower Thirds via arquivo de importacao

**Decisao:** preparar a integracao inicial com o Animated Lower Thirds gerando
um JSON de importacao para o painel `control-panel.html`.

**Motivo:** a investigacao dos arquivos locais mostrou que o sistema usado nao
e o H2R Graphics. O Animated Lower Thirds v1.6 guarda textos e configuracoes no
`localStorage` do navegador do OBS e envia os dados para `browser-source.html`
via `BroadcastChannel`. Nao existe uma API HTTP simples como no H2R.

**Alternativas consideradas:** alterar diretamente os arquivos HTML do pacote
em `Downloads` ou tentar escrever no armazenamento interno do OBS. Descartadas
porque seriam frageis, dependentes da maquina e arriscadas para um projeto open
source. A importacao JSON usa um fluxo que o proprio painel ja oferece.

**Risco assumido:** essa etapa ainda exige que o operador importe o JSON no
painel antes da transmissao. Uma integracao mais automatica podera ser estudada
depois usando recursos especificos do OBS Browser Source, se forem confiaveis.

## 10. Encerrando a automação do Import: limitação confirmada da ferramenta

**Decisão:** aceitar o clique manual de Import no Animated Lower Thirds como
etapa permanente do fluxo. Encerrada a investigação de automação completa.

**Motivo:** quatro mecanismos técnicos foram avaliados e descartados com
evidência concreta: fetch() (bloqueado por CORS, origem file://), emit_event
do obs-browser (Custom Browser Docks não têm suporte confirmado à API JS do
OBS, ao contrário de Browser Sources), escrita direta em localStorage/LevelDB
(decisão 8, formato interno não documentado), e File System Access API (sem
precedente de uso em Custom Browser Docks do OBS). A causa raiz é comum às
quatro tentativas: control-panel.html carrega como Custom Browser Dock, que
tem superfície de API menor que Browser Source dentro do obs-browser —
confirmado por relato direto de mantenedor do projeto.

**Alternativas descartadas:** automação de interface via Playwright/CDP ou
AutoHotkey — tecnicamente viável, mas excluída por decisão de produto: risco
de interferir num processo ao vivo durante transmissão, dependência pesada,
manutenção exige conhecimento avançado.

**Risco assumido:** nenhum novo — o processo mantém a mesma etapa manual que
já existe hoje (um clique de Import), só que agora com o JSON já preparado
automaticamente pelo PLM.