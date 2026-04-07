import requests
import json
from django.core.management.base import BaseCommand
from main.models import *


class Command(BaseCommand):
    Block.objects.all().delete()
    def handle(self, *args, **options):
        API_KEY = '8J3Q4NHCADWBNV18HYHMU7GYZRXV8QGYYK'

        # Используем V2 API (без /api в конце)
        base_url = "https://api.etherscan.io/v2/api"

        # 1. Получаем номер блока (V2 формат)
        params = {
            "chainid": 1,  # 1 = Ethereum mainnet
            "module": "proxy",
            "action": "eth_blockNumber",
            "apikey": API_KEY
        }

        self.stdout.write("Запрос номера блока...")
        response = requests.get(base_url, params=params)

        try:
            data = response.json()
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR(f"Ошибка: {response.text}"))
            return

        if 'result' not in data or data['result'] is None:
            self.stdout.write(self.style.ERROR(f"Ошибка API: {data}"))
            return

        block_id = data['result']
        self.stdout.write(f"Получен блок: {block_id}")

        # 2. Получаем блок (V2 формат)
        params = {
            "chainid": 1,
            "module": "proxy",
            "action": "eth_getBlockByNumber",
            "tag": block_id,
            "boolean": "true",
            "apikey": API_KEY
        }

        self.stdout.write("Запрос данных блока...")
        response = requests.get(base_url, params=params)

        try:
            response_data = response.json()
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR(f"Ошибка получения блока: {response.text}"))
            return

        if 'result' not in response_data or response_data['result'] is None:
            self.stdout.write(self.style.ERROR(f"Ошибка: {response_data}"))
            return

        block_result = response_data['result']

        # Если result — строка, парсим её как JSON
        if isinstance(block_result, str):
            try:
                block_data = json.loads(block_result)
            except json.JSONDecodeError:
                # Если не парсится, значит это уже готовый объект
                self.stdout.write(self.style.ERROR(f"Ошибка парсинга: {block_result[:200]}"))
                return
        else:
            block_data = block_result

        # 4. Сохраняем блок
        block_obj, created = Block.objects.get_or_create(
            number=block_data['number'],
            defaults={
                'time_stamp': block_data['timestamp'],
                'miner': block_data['miner'],
                'gase_used': block_data['gasUsed']
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f"Блок {block_data['number']} сохранен"))
        else:
            self.stdout.write(f"Блок {block_data['number']} уже существует")

        # 5. Сохраняем транзакции
        transactions = block_data.get('transactions', [])
        saved_count = 0

        for tx in transactions:
            tx_obj, created = Transaction.objects.get_or_create(
                hash=tx['hash'],
                defaults={
                    'block': block_obj,
                    'from_address': tx['from'],
                    'to_address': tx['to'],
                    'value': tx['value']
                }
            )
            if created:
                saved_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"Сохранено транзакций: {saved_count} из {len(transactions)}"
        ))