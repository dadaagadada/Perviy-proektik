import requests
import urllib.parse
from django.core.management.base import BaseCommand
from main.models import Prompt, Answer, Block, Transaction


class Command(BaseCommand):
    help = 'Отправляет данные в бесплатный Pollinations API (исправлено)'

    def handle(self, *args, **options):
        # 1. Получаем промпт
        prompt_obj = Prompt.objects.first()
        if not prompt_obj:
            self.stdout.write(self.style.ERROR('❌ Нет промптов в таблице Prompt'))
            return

        # 2. Получаем данные блокчейна
        block = Block.objects.first()
        transactions = Transaction.objects.all()

        # 3. Формируем сообщение (логика не меняется)
        block_str = str(block) if block else "Нет данных о блоке"
        transaction_str = ' '.join([str(tx) for tx in transactions])
        task = 'Ответь вопрос: '
        data = ('Тебе сейчас поступят данные в таком формате: сначала идёт информация о блоке в таком поредке: номер время, майнерб комиссия.'
                'В этом же сообщении тебе поступят данные в шестнадцатиричном формате о транзакциях этого блока в формате'
                'строки: блок хеш отправитель получатель сумма. После чего начинаются данные другой транзакции в таком же формате'
                'для ответа используй только полученные данные')
        full_prompt = task + prompt_obj.text + data +' Данные: ' + block_str + ' ' + transaction_str
        self.stdout.write(self.style.ERROR(f'Промпт:: {full_prompt}'))
        # 4. Отправляем POST-запрос к Pollinations API
        url = "https://text.pollinations.ai/"

        # Данные для POST-запроса (тело)
        # Pollinations API ожидает данные в формате JSON или plain text
        payload = {
            "messages": [
                {
                    "role": "user",
                    "content": full_prompt
                }
            ]
        }

        # Заголовки (headers) для POST-запроса
        headers = {
            "Content-Type": "application/json"
        }

        self.stdout.write(f'📨 Отправка POST-запроса к Pollinations API...')

        try:
            # Отправляем POST-запрос с JSON-данными
            response = requests.post(url, headers=headers, json=payload, timeout=60)

            if response.status_code == 200:
                # Проверяем, что ответ не пустой
                if response.text:
                    answer = response.text

                    # Сохраняем ответ
                    Answer.objects.create(
                        prompt=prompt_obj,
                        text=answer
                    )

                    self.stdout.write(self.style.SUCCESS(f'✅ Сохранён ответ для {prompt_obj.name}'))
                else:
                    self.stdout.write(self.style.ERROR(f'❌ API вернул пустой ответ'))

            else:
                self.stdout.write(self.style.ERROR(f'❌ Ошибка API: {response.status_code}'))
                self.stdout.write(f'Ответ сервера: {response.text[:200]}')

        except requests.exceptions.Timeout:
            self.stdout.write(self.style.ERROR('❌ Превышено время ожидания ответа от API'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Ошибка: {e}'))