# Projeto 14: Etiquetas de Segurança e Instruções para Velas Aromáticas

Este projeto automatiza a criação de rótulos de segurança e instruções de queima circulares para velas artesanais. Ele gera três estilos visuais distintos (Clássico Branco, Kraft Rústico, e Rosa Suave) mantendo a conformidade com as normas de rotulagem de segurança.

## Estilos Gerados

1. **Classic White (etiqueta_original_3.jpg):** Fundo branco limpo, texto preto e borda dourada elegante.
2. **Kraft Rustic (etiqueta_original_4.jpg):** Fundo bege simulando papel kraft ecológico, borda e texto marrom carvão.
3. **Blush Pink (etiqueta_original_5.jpg):** Fundo rosa claro romântico, borda branca e texto marrom escuro suave.

## Conteúdo da Etiqueta

- **Título Principal:** VELA AROMÁTICA
- **Alertas de Segurança:** Regras cruciais (não queimar sem supervisão, longe de inflamáveis, crianças e pets).
- **Instruções de Queima:** Cuidados com o pavio e tempo de queima máximo (2 horas).
- **Composição:** Cera vegetal de soja, pavio de algodão e essência.
- **Rodapé Técnico:** Espaço para data de fabricação, validade de 2 anos e peso do produto.

## Como Executar o Script

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
2. Execute o script:
   ```bash
   python make_labels.py
   ```
3. Os arquivos de imagem das etiquetas serão salvos diretamente na pasta `assets`.
