from django.core.management.base import BaseCommand

import logging
import pymongo


class Command(BaseCommand):
    help = 'Store Log'
    
    def add_arguments(self, parser):
        parser.add_argument('ip', type=str, help='Indicates the IP')
        parser.add_argument('date', type=str, help='Indicates the date')
        parser.add_argument('user', type=str, help='Indicates the user')

    def handle(self, *args, **kwargs):
        ip = kwargs['ip']
        date = kwargs['date']
        user = kwargs['user']
        logger = logging.getLogger(__name__)
        LOG_MSG = {
            'IP': ip,
            'Date': date,
            'User': user,
        }
        logger.info(LOG_MSG)