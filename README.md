# 📸  Image Watermark Processor (CR2 & Standard)


Este script Python foi desenvolvido para automatizar a aplicação de marcas d'água em grandes volumes de imagens. Ele é ideal para fotógrafos, pois oferece suporte nativo para arquivos RAW da Canon (.CR2), além de formatos comuns como JPG, JPEG e PNG.
TODO
- [ ] Interface grafica
- [ ] Gerar executavel
O script redimensiona a marca d'água proporcionalmente e a aplica de forma centralizada, garantindo que o logo nunca ultrapasse os limites da imagem original.

✨ Funcionalidades
```
    Suporte RAW: Processamento de arquivos .CR2 via biblioteca rawpy.
    Processamento em Lote: Escaneia diretórios inteiros e processa todas as imagens compatíveis de uma só vez.
    ROI Inteligente: Calcula a Região de Interesse (ROI) para evitar erros de dimensões e garantir que o logo esteja sempre centralizado.
    Transparência Ajustável: Controle fino sobre a opacidade da marca d'água.
    Organização Automática: Cria os diretórios necessários (imgs_nao_marcadas e imgs_marcadas) caso não existam.
```
🛠️ Pré-requisitos

Antes de rodar o script, você precisará instalar as dependências Python:
``` Bash
pip install opencv-python numpy rawpy
```
🚀 Como Usar
1. Configuração Inicial:
    Coloque o script em uma pasta no seu computador.

2. Marca d'Água:
    Adicione seu arquivo de logo na mesma pasta com o nome marca_dagua.png.

3. Imagens Originais:
    Execute o script uma vez para criar as pastas ou crie manualmente uma pasta chamada imgs_nao_marcadas/ e coloque suas fotos dentro dela.

4. Execução:
    Rode o script pelo terminal:
    ```Bash

    python nome_do_seu_arquivo.py
    ```
Resultado:
    As imagens processadas serão salvas na pasta imgs_marcadas/ com o sufixo _marcado.png.


📂 Estrutura de Pastas
Plaintext
```
.
├── imgs_nao_marcadas/   # Fotos originais (CR2, PNG, JPG)
├── imgs_marcadas/       # Fotos com marca d'água (Saída)
├── marca_dagua.png      # Sua logo
└── script.py            # O código fonte
```
