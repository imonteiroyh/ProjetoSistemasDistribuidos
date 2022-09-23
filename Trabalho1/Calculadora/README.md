# Calculadora Simples Usando Sockets

### Formato da mensagem

Requisição:

``` 
[PRIMEIRO_OPERANDO] [SEGUNDO_OPERANDO] [OPERAÇÃO] [TIPO_DE_DADO]
```

Resposta:

```
SUCCESS [RESULTADO]
``` 

ou 

```
ERROR [MENSAGEM_DE_ERRO]
```

Restrições:
- Operandos devem ser numéricos
- Operação deve ser +, -, * ou /
- Tipo de dado deve ser "INTEGER" ou "FLOAT"
