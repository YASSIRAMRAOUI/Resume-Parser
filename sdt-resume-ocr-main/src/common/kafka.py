import logging
from typing import Callable

from confluent_kafka import Consumer, Producer

from src.common.config import KafkaConfig

logger = logging.getLogger(__name__)


class Kafka:
    def __init__(self, kafka_config: KafkaConfig):
        self._consumer = Consumer({
            'bootstrap.servers': kafka_config.bootstrap_servers,
            'group.id': kafka_config.group_id,
            'auto.offset.reset': 'earliest',
        })

        self._producer = Producer({
            'bootstrap.servers': kafka_config.bootstrap_servers,
        })

    def send(self, topic: str, message: str) -> None:
        logger.info('Sending message %s to topic: %s', message, topic)
        self._producer.produce(topic, message)

    def listen(self, topic: str, callback: Callable[[str], None]) -> None:
        logger.info(f'Listening to topic {topic}')

        self._consumer.subscribe([topic])

        self._consume(callback)

    def _consume(self, callback: Callable[[str], None]) -> None:
        while True:
            message = self._consumer.poll(1.0)

            if message is None:
                continue

            if message.error() is not None:
                logger.error('Consumer error: %s', message.error())

            message = message.value().decode('utf-8')
            logger.info('Message received: %s', message)

            callback(message)

    def close(self) -> None:
        self._consumer.close()
        self._producer.flush()
