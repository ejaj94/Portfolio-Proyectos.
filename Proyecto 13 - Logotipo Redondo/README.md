# Projeto 13: Gerador de Logotipos Redondos 3x3cm (A4 Completo)

Este projeto automatiza a criação de uma folha de impressão A4 cheia de logotipos circulares de **3cm x 3cm** com margens e marcas de corte precisas. Ideal para criação rápida de etiquetas adesivas de branding.

## Funcionalidades

- **Corte Circular Perfeito:** Recorta e aplica transparência a logotipos quadrados para criar uma apresentação redonda.
- **Moldura Premium:** Aplica um design de borda circular dupla dourada no estilo da identidade da marca.
- **Layout Inteligente A4:** Distribui automaticamente 48 logotipos por folha A4 (6 colunas e 8 filas).
- **Marcas de Corte:** Adiciona guias discretas de corte para facilitar a guilhotina e corte manual.
- **Exportação Direta em PDF:** Gera um arquivo PDF de alta definição (300 DPI) pronto para a gráfica.

## Tecnologias Utilizadas

- **Python 3.11**
- **Pillow (PIL Image Processing Library)**
- **HTML5 / CSS3 (Vanilla)** para apresentação web.

## Como Executar o Script

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
2. Execute o script gerador:
   ```bash
   python generate_round_logos_a4.py
   ```
3. O PDF final será gerado na pasta de destino configurada.
