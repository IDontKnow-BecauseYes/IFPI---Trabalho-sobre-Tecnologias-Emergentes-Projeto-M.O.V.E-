Introdução
No contexto atual de interação homem‑máquina, interfaces naturais baseadas em gestos têm se mostrado uma alternativa intuitiva e eficiente para controlar dispositivos eletrônicos. Este projeto, batizado de Drusa Control, une reconhecimento de gestos de mão, síntese de voz e comunicação serial com um microcontrolador Arduino. O sistema principal captura o fluxo de vídeo da câmera, identifica números de dedos erguidos e, de acordo com gestos previamente definidos, executa ações como verificar a conexão com o Arduino, alternar modos de controle por gestos ou encerrar o programa. Em modo avançado, o submódulo de gestos detalhados dispara comandos para acionar LEDs de diferentes cores, ligar ou desligar todos os dispositivos e permite um tutorial falado para guiar o usuário.

Justificativa
A escolha de uma interface gestual justifica‑se pela crescente demanda por soluções livres do uso de periféricos convencionais (mouse, teclado e telas sensíveis ao toque), sobretudo em aplicações de automação residencial, ambientes industriais ou para pessoas com mobilidade reduzida. O projeto Drusa Control busca oferecer:

Acessibilidade – Ao dispensar controles físicos, facilita o uso por pessoas com limitações motoras finas.

Rapidez e naturalidade – Reconhecer gestos de forma estável elimina a necessidade de navegar por menus ou botões, tornando a operação mais direta.

Feedback multimodal – A síntese de voz informa o usuário sobre o status do sistema e confirmações de comando, reduzindo incertezas.

Modularidade e portabilidade – A comunicação por porta serial padrão (USB‑Serial) garante compatibilidade com diversas placas Arduino e microcontroladores, permitindo futuras expansões.

Metodologia de Desenvolvimento
O desenvolvimento seguiu as seguintes etapas:

Pesquisa e configuração inicial

Estudo das bibliotecas MediaPipe (para detecção de mãos e contagem de dedos), OpenCV (captação e visualização de vídeo) e pyttsx3 (TTS em Python).

Definição de um protocolo de comunicação serial simples, com comandos textuais padronizados (ALL_ON, RED_ON, etc.) e resposta via \n.

Implementação do módulo principal

Criação do loop de captura de vídeo, conversão de cores e processamento de frames.

Contagem dinâmica de dedos, utilizando limiares relativos à altura da palma para maior robustez em diferentes distâncias da câmera.

Lógica de “hold time” para evitar gatilhos acidentais, além de cooldown para dar tempo de reposicionamento após cada ação.

Integração com síntese de voz para mensagem de boas‑vindas, status do Arduino e transições de modo.

Desenvolvimento do submódulo de gestos avançados

Definição de gestos especiais (rock para tutorial, punho para sair, contagem de dedos para comandos específicos).

Uso de comparação parcial de estados de dedos para tolerar pequenas imprecisões de detecção.

Tutorial falado detalhando cada gesto, seguido de execução de comandos via send_command() ao Arduino.

Teste e refinamento

Ajuste dos thresholds de detecção (polegar versus demais dedos) para minimizar falsos positivos.

Tratamento de exceções e uso de context managers (with serial.Serial) para garantir fechamento seguro da porta.

Substituição de time.sleep() por controle de timestamps, evitando travamentos do loop de vídeo.

Validação manual em diferentes cenários de iluminação e ângulos de câmera, visando tornar o sistema tolerante a variações reais.

Documentação e exemplos de uso

Inclusão de trechos de código comentados e funções de exemplo em __main__ para demonstrar a inicialização, verificação de conexão e envio de comandos.

Redação de um relatório técnico (este documento) para guiar usuários e desenvolvedores interessados em estender ou integrar o Drusa Control em suas aplicações.

Com essa arquitetura, o Drusa Control torna‑se uma plataforma versátil para experimentação de interfaces gestuais, com potencial aplicação em domótica, prototipagem educativa e acessibilidade.
