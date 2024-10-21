## RFs (Requisitos Funcionais)

- [x] Deve ser possível cadastrar um usuário.
- [x] Deve ser possível autenticar um usuário.
- [x] Deve ser possível criar uma task com título, descrição (opcional), data de vencimento (opcional), categoria (opcional) e prioridade (opcional).
- [x] Deve ser possível listar todas as tasks de um usuário autenticado.
- [x] Deve ser possível filtrar tasks por título, descrição, prioridade ou categoria.
- [x] Deve ser possível visualizar os detalhes de uma task específica pelo seu ID.
- [x] Deve ser possível atualizar uma task existente, incluindo o título, descrição, data de vencimento, categoria e prioridade.
- [x] Deve ser possível excluir uma task pelo ID.
- [x] Deve ser possível marcar uma task como concluída ou pendente.
- [x] Deve ser possível adicionar subtasks a uma task.
- [x] Deve ser possível listar, atualizar e remover subtasks associadas a uma task.
- [x] Deve ser possível anexar arquivos a uma task.
- [x] Deve ser possível listar e remover arquivos anexados a uma task.
- [x] Deve ser possível adicionar, listar e remover comentários em uma task.
- [x] Deve ser possível listar todas as categorias de tasks e criar novas categorias.
- [x] Deve ser possível listar todas as tasks que estão próximas da data de vencimento (menos de 24 horas).


## RNs (Regras de Negócio)

- [x] A data de vencimento de uma task deve ser igual ou maior que a data atual. 
- [x] Não deve ser permitido cadastrar ou atualizar uma task com data de vencimento no passado.
- [x] O título da task é obrigatório e deve ter um limite de 100 caracteres.
- [x] Apenas o usuário que criou a task pode visualizá-la, editá-la ou excluí-la.
- [x] Somente um usuário autenticado pode criar, atualizar ou deletar suas tasks.
- [x] Não deve ser permitido cadastrar um usuário com um e-mail já existente.
- [x] Apenas administradores podem criar e gerenciar categorias de tasks.
- [x] Uma task deve ter uma das seguintes prioridades: baixa, média ou alta.
- [x] Ao marcar uma task como concluída, todas as subtasks associadas também devem ser marcadas como concluídas.
- [x] O tamanho máximo dos arquivos anexados a uma task deve ser de 5MB.

---

## RNFs (Requisitos Não-Funcionais)

- [x] A API deve seguir o padrão REST, com endpoints intuitivos e organizados.
- [x] A aplicação deve responder em um tempo aceitável para operações básicas de criação, leitura, atualização e exclusão.
- [x] Deve ser validado que os dados de entrada estejam no formato correto, retornando mensagens de erro apropriadas em caso de valores inválidos.
- [x] A aplicação deve ser modular e seguir boas práticas de arquitetura, como Clean Architecture e os princípios SOLID.
- [x] A aplicação deve estar documentada com Swagger para que os endpoints e suas funcionalidades sejam facilmente compreendidos.
- [x] Deve ser possível realizar testes unitários e de integração nos principais componentes da aplicação.
- [x] A aplicação deve armazenar as tasks e usuários em um banco de dados relacional, como PostgreSQL ou SQLite.
- [x] A senha do usuário deve ser armazenada de forma segura, utilizando hashing.
- [x] O usuário deve ser identificado por um JWT (JSON Web Token);
- [x] A aplicação deve ser escalável para suportar um número crescente de usuários e tasks.
- [x] Os arquivos anexados devem ser armazenados de maneira segura, preferencialmente usando um serviço como Amazon S3 ou sistema de arquivos local com controle de acesso.