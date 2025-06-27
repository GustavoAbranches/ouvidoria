#!/bin/bash

echo "=== criar usuario ==="
curl -X POST http://localhost:5000/usuarios \
  -H "Content-Type: application/json" \
  -d '{"tipo": "aluno", "email": "teste@email.com", "senha": "123456"}'
echo -e "\n"

echo "=== listar usuarios ==="
curl http://localhost:5000/usuarios
echo -e "\n"

echo "=== atualizando usuario ==="
curl -X PUT http://localhost:5000/usuarios/1 \
  -H "Content-Type: application/json" \
  -d '{"tipo": "professor", "email": "prof@email.com", "senha": "nova_senha"}'
echo -e "\n"

echo "=== criando comentario ==="
curl -X POST http://localhost:5000/comentarios \
  -H "Content-Type: application/json" \
  -d '{"texto": "Esse sistema é excelente!", "usuario_id": 1}'
echo -e "\n"

echo "=== listar comentarios ==="
curl http://localhost:5000/comentarios
echo -e "\n"

echo "=== analisando sentimento ==="
curl -X POST http://localhost:5000/analisar_sentimento \
  -H "Content-Type: application/json" \
  -d '{"texto": "Esse produto é horrível"}'
echo -e "\n"

echo "=== deletar comentario ID 1 ==="
curl -X DELETE http://localhost:5000/comentarios/1
echo -e "\n"

echo "=== deletando usuario ID 1 ==="
curl -X DELETE http://localhost:5000/usuarios/1
echo -e "\n"
