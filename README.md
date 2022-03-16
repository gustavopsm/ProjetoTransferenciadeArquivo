# ProjetoTransferenciadeArquivo
O projeto consiste num servidor web que recebe requisições no formato HTTP 1.1 de um navegador e retorna o pedido caso exista, caso contrário, existem três tipos de erro. Eles são: ‘400 Bad Request’ - ocorre quando a requisição possui um erro de sintaxe e o servidor não compreende a requisição, ‘404 Not Found’ - ocorre caso a página requisitada não exista, ‘505 HTTP Version Not Supported’ - acontece quando a requisição é feita numa versão HTTP diferente da suportada pelo servidor. Caso seja requisitado ‘ / ’ o servidor irá buscar na pasta um arquivo denominado ‘index.HTML’ ou ‘index.HTM’ e abri-lo, caso não exista o servidor irá criar um arquivo HTML para que o usuário consiga acessar os documentos de forma mais intuitiva.  
como usar:
Para rodar o código do servidor web, você precisa seguir os seguintes passos:

⦁	Redigir um arquivo de texto denominado ‘ConfiguracoesServidor.txt’ e colocá-lo no mesmo arquivo do código. 
Seguindo o seguinte padrão => 
LocalPasta-'digitar aqui local do arquivo inspecionado'
LocalErros-'digitar aqui local com as páginas de erro'
No final do arquivo não pode haver uma linha de sobra.
OBS.: O arquivo contendo os erros deve conter três arquivos HTML, denominados: ‘html400.html’, ‘html404.html’ e ‘html505.html’.

⦁	Rodar o código disponibilizado no GITHUB na sua IDE de preferência.

⦁	Realizar requisições utilizando o navegador a partir do endereço ‘localhost:4000’, o número 4000 indica a porta usada.

OBS 1.: O código suporta da forma esperada, os arquivos do tipo: texto (.js , .plain, .HTML, .CSS), Imagem(.jpg, .png, GIF) e áudio(OGG), as demais extensões são transferidas como aplicações(application). 

OBS 2 .: Tomar cuidado e evitar a utilização de caracteres especiais (caracteres non-ascii) como acentos e ‘ç’.
