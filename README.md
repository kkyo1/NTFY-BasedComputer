Automação Remota de Aplicativos com Python
Projeto pessoal desenvolvido para explorar a automação de tarefas locais por meio de comandos enviados remotamente.
A aplicação consulta notificações recebidas pelo ntfy, valida as mensagens e pode abrir aplicativos previamente definidos em um computador Windows.
Status: projeto de aprendizado em desenvolvimento. Esta versão é um protótipo e ainda possui limitações de segurança e de tratamento de mensagens.


Problema
Em alguns cenários, uma pessoa pode precisar iniciar um aplicativo em um computador sem estar fisicamente diante dele. Este projeto explora uma forma simples de automatizar essa ação a partir de mensagens enviadas remotamente.
O cenário é ilustrativo: o projeto não foi implantado nem validado em uma empresa.


Solução
Um script em Python consulta um tópico do ntfy e interpreta as notificações recebidas. Quando encontra as duas mensagens esperadas — uma contendo a senha configurada e outra com o nome de um aplicativo permitido —, tenta iniciar o aplicativo no Windows.


Fluxo de funcionamento
1. O usuário envia uma mensagem com a senha no formato esperado.
2. Em seguida, envia o nome do aplicativo, como calculadora ou paint.
3. O script consulta as notificações do ntfy.
4. As mensagens são verificadas e registradas em um arquivo de texto.
5. Se a validação passar, o aplicativo permitido é iniciado.
6. O programa registra eventos e erros no log e pode enviar uma resposta pelo ntfy.
7. 
Tecnologias utilizadas
- Python — lógica principal da automação.
- Requests — requisições HTTP para o ntfy.
- JSON — interpretação das notificações recebidas.
- Subprocess — inicialização de aplicativos locais.
- Logging — registro de eventos e erros.
- Pathlib — criação e manipulação de caminhos e arquivos.
- Aplicativos disponíveis


A versão atual está configurada para tentar abrir:
- Calculadora do Windows (calculadora)
- Microsoft Paint (paint)
Os caminhos definidos no código são específicos do Windows.


Requisitos
- Windows
- Python 3.10 ou superior (recomendado)
- Acesso à internet
- Um tópico configurado no ntfy


Configuração
No código, configure o tópico do ntfy e a senha utilizados pelo programa. Não publique senhas, tokens ou tópicos privados no repositório.
Para um projeto compartilhado, prefira carregar valores sensíveis de variáveis de ambiente em vez de deixá-los diretamente no código. O .gitignore não protege segredos que já tenham sido enviados ao Git.


Uso
1. Inicie o script:
   python main.py
2. Envie ao tópico configurado uma primeira mensagem contendo a senha, por exemplo:
   senha: SUA_SENHA
3. Envie uma segunda mensagem com um dos comandos permitidos:
   calculadora
   ou
   paint
4. Verifique a abertura do aplicativo e consulte os arquivos de log e de texto configurados no programa.
O script consulta o ntfy em intervalos de 15 minutos. Por isso, a execução do comando pode não ser imediata.
Arquivos gerados


Na configuração padrão do código, os arquivos são gravados em:
- Documents/VSCode/programa.log — eventos e erros.
- Documents/VSCode/Novos_Arquivos/Arquivo_de_Texto.txt — mensagens recebidas.
Esses arquivos são gerados localmente e não precisam ser enviados ao GitHub.


Limitações e segurança
Este projeto é um protótipo educacional, não uma solução pronta para uso empresarial ou para exposição pública.
- O tópico do ntfy não deve ser considerado privado apenas por possuir um identificador difícil de adivinhar.
- Uma senha fixa no código não é um mecanismo robusto de autenticação.
- A versão atual associa as duas últimas notificações encontradas. Mensagens antigas ou fora de ordem podem ser interpretadas incorretamente.
- A consulta periódica e o intervalo de retenção das notificações podem levar ao processamento repetido de comandos.
- O programa foi pensado para abrir apenas os aplicativos explicitamente listados no código.
Antes de utilizar o projeto em um ambiente real, é necessário melhorar a autenticação, a proteção das credenciais, a identificação única dos comandos, o controle contra repetição e a estratégia de recebimento das mensagens.


Próximos passos
- [ ] Refatorar e documentar as funções.
- [ ] Melhorar a configuração de credenciais.
- [ ] Tratar mensagens duplicadas e antigas.
- [ ] Adicionar testes para comandos válidos e inválidos.
- [ ] Melhorar o tratamento de falhas de rede.
- [ ] Gravar uma demonstração do funcionamento.


Objetivo de aprendizado
O objetivo é praticar a organização de um programa Python, comunicação HTTP, processamento de dados, tratamento de exceções, logs e automação de tarefas locais.


Projeto pessoal para fins de aprendizado.
