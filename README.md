# Keep Alive — WebServices

Monitor leve para verificar de 5 a 10 sites/APIs por meio do GitHub Actions. Não precisa de servidor próprio nem de dependências Python externas.

## Como configurar

1. Crie um repositório no GitHub e envie todos os arquivos desta pasta.
2. No repositório, abra **Settings → Secrets and variables → Actions**.
3. Clique em **New repository secret**.
4. Nome: `KEEPALIVE_URLS`
5. Valor: cole uma URL completa por linha, por exemplo:

   ```text
   https://meu-plano-de-voo.onrender.com/health
   https://meu-webservice-2.onrender.com/
   https://meu-webservice-3.onrender.com/health
   ```

   Use os endereços reais dos seus serviços. Se tiver um endpoint leve como `/health` ou `/healthz`, prefira-o. Caso não tenha, use a URL principal.

6. Abra a aba **Actions** e habilite os workflows, se o GitHub solicitar.
7. Entre em **Actions → Keep Alive WebServices → Run workflow** para testar imediatamente.
8. Depois, o agendamento tentará executar a cada 10 minutos.

### Alternativa sem segredo

Você pode colocar as URLs públicas em `targets.txt`, uma por linha, e deixar o segredo `KEEPALIVE_URLS` vazio. Não coloque tokens, senhas ou URLs privadas em um repositório público.

## Como ler o resultado

- `OK | HTTP 200`: resposta normal.
- `OK | HTTP 3xx`: redirecionamento; o monitor considera a resposta alcançável.
- `FALHA | HTTP 4xx/5xx` ou erro de conexão: a execução será marcada como falha.
- Abra a execução em **Actions** para consultar o log de cada URL.

## Importante

- O GitHub Actions tem intervalo mínimo de agendamento de 5 minutos, mas horários agendados podem atrasar. O arquivo está configurado para 10 minutos.
- Em repositórios públicos, workflows agendados podem ser desativados automaticamente após 60 dias sem atividade no repositório. Confira a aba Actions periodicamente.
- Pings ajudam a reduzir o descanso por inatividade, mas não garantem disponibilidade contínua. O Render pode reiniciar ou suspender serviços por manutenção, limites de uso ou políticas da plataforma.
- Use somente em serviços que você administra ou tem autorização para monitorar. Faça chamadas a endpoints leves e seguros; evite rotas que alterem dados, disparem processos ou consumam recursos elevados.
- Se um serviço exigir autenticação, não coloque credenciais diretamente na URL nem no código. Este exemplo foi pensado para endpoints públicos de saúde/status.
