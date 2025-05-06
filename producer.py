import pika
from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)
class MQProducer(models.Model):
    _name = 'mq.producer'
    _description = 'MQ Producer'

    name = fields.Char("Message")

    def send_to_queue(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='odoo_queue', durable=True)

        for record in self:
            message = record.name
            channel.basic_publish(
                exchange='',
                routing_key='odoo_queue',
                body=message,
                properties=pika.BasicProperties(
                    delivery_mode=2,  # make message persistent
                ))
            _logger.info(f"Sent: {message}")

        connection.close()
