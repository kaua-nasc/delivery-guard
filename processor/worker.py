import aio_pika
import asyncio
import json

from .config import RABBIT_URL
from .processor import process_transaction

async def main():
    connection = await aio_pika.connect_robust(RABBIT_URL)
    channel = await connection.channel()
    
    queue = await channel.declare_queue("transaction_analise", durable=True)

    async def on_message(message: aio_pika.IncomingMessage):
        async with message.process():  # faz ack automático ao fim
            try:
                payload = json.loads(message.body.decode())
                if not isinstance(payload, dict):
                    raise ValueError("Invalid message format")
                
                await process_transaction(payload)
            except Exception as e:
                print(f"[ERRO] Falha ao processar mensagem: {e}")

    await queue.consume(on_message)

    print(" [*] Aguardando mensagens. Para sair pressione CTRL+C")
    await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
