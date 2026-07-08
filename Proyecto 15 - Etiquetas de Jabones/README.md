# Projeto 15: Etiquetas de Sabonetes Artesanais e Nomes de Velas

Este projeto reúne a automação para geração de etiquetas de sabonetes e nomes de velas no tamanho de **4cm x 2cm** e distribuição em folha A4.

## Funcionalidades

- **Gerador de Etiquetas de Sabonetes (`generate_final.py`):** Cria 12 modelos personalizados de etiquetas com ingredientes e propriedades medicinais de cada sabonete.
- **Gerador de Folhas A4 (`generate_a4_pdfs.py`):** Organiza e replica as etiquetas em folhas A4 individuais prontas para corte (30 etiquetas por página).
- **Gerador de Nomes Otimizado (`generate_names_a4.py`):** Distribui os nomes das velas de forma ordenada em colunas verticais na folha A4, agrupando nomes idênticos seguidos para facilitar o manuseio.

## Como Executar os Scripts

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
2. Para gerar as etiquetas individuais e as folhas A4 de sabonetes:
   ```bash
   python generate_final.py
   python generate_a4_pdfs.py
   ```
3. Para gerar a folha A4 de nomes ordenados em vertical:
   ```bash
   python generate_names_a4.py
   ```
