# 🛡️ Simulador Educativo de Inventário de Rede PRO

Aplicação web educativa interativa desenvolvida em **Python**, **Flask** e **ReportLab** para a simulação didática de inventário e postura de segurança de rede, utilizando exclusivamente dados de demonstração fictícios (mock data).

---

## ✨ Características Principais

- 🧪 **Simulação Didática**: Demonstra conceitos de inventário de ativos de rede através de dados sintéticos estáticos sem interagir com redes físicas.
- 📊 **Painel Interativo**: Visualiza topologias fictícias de teste (routers, servidores NAS, estações de trabalho e impressoras).
- 📄 **Gerador de Relatórios PDF de Amostra**: Exporta relatórios formatados em PDF com base na simulação didática.
- 🛡️ **Segurança Garantida**: Sem ligações por socket, sem envio de pacotes nem pedidos ARP.

---

## 🛠️ Instalação e Utilização

1. Instalar dependências:
   ```bash
   pip install -r requeriments.txt
   ```
2. Executar o servidor web local:
   ```bash
   python app.py
   ```
3. Abrir no navegador:
   ```text
   http://localhost:5005
   ```
