import asyncio


# Функция, имитирующая подъем шаров атлетом
async def start_strongman(name, power):
    print(f'Силач {name} начал соревнования.')
    for i in range(1, 6):  # Каждый атлет поднимает 5 шаров
        await asyncio.sleep(1 / power)  # Задержка обратно пропорциональна силе
        print(f'Силач {name} поднял {i} шар')
    print(f'Силач {name} закончил соревнования.')


# Функция, запускающая турнир
async def start_tournament():
    # Создаем задачи для каждого участника
    task1 = asyncio.create_task(start_strongman('Pasha', 3))
    task2 = asyncio.create_task(start_strongman('Denis', 4))
    task3 = asyncio.create_task(start_strongman('Apollon', 5))

    # Ожидаем завершения всех задач
    await task1
    await task2
    await task3


# Запуск асинхронного турнира
asyncio.run(start_tournament())
