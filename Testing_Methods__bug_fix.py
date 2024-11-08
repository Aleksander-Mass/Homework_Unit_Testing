import unittest

class Runner:
    def __init__(self, name, speed=5):
        self.name = name
        self.distance = 0
        self.speed = speed

    def run(self):
        self.distance += self.speed * 2

    def walk(self):
        self.distance += self.speed

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other
        elif isinstance(other, Runner):
            return self.name == other.name

"""
class Tournament:
    def __init__(self, distance, *participants):
        self.full_distance = distance
        self.participants = list(participants)

    def start(self):
        finishers = {}
        place = 1
        while self.participants:
            for participant in self.participants:
                participant.run()
                if participant.distance >= self.full_distance:
                    finishers[place] = participant
                    place += 1
                    self.participants.remove(participant)

        return finishers
"""

#
###   Исправление ошибки в классе Tournament
# Чтобы исправить ошибку, когда бегун с меньшей скоростью может завершить дистанцию раньше,
# чем бегун с большей скоростью, можно пересчитать результаты после каждого круга,
# чтобы учесть разницу в скорости. Например, можно отсортировать участников по оставшейся дистанции после каждого "шага":
#
class Tournament:
    def __init__(self, distance, *participants):
        self.full_distance = distance
        self.participants = list(participants)

    def start(self):
        finishers = {}
        place = 1
        while self.participants:
            # Участники совершают шаг (бегут с текущей скоростью)
            for participant in self.participants:
                participant.run()

            # Проверка, если кто-то финишировал, добавляем его в финишеры
            for participant in self.participants[:]:  # копия списка, чтобы безопасно удалять
                if participant.distance >= self.full_distance:
                    finishers[place] = participant
                    place += 1
                    self.participants.remove(participant)

            # Сортируем участников по оставшейся дистанции
            self.participants.sort(key=lambda p: self.full_distance - p.distance, reverse=True)

        return finishers

    # Этот подход гарантирует, что участники с большей скоростью быстрее завершат дистанцию,
    # даже если достигнут финиша в одном и том же шаге.


class TournamentTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.all_results = []  # Словарь для хранения результатов всех тестов

    def setUp(self):
        # Создаем 3 объекта бегунов
        self.runner_usain = Runner("Усэйн", speed=10)
        self.runner_andrei = Runner("Андрей", speed=9)
        self.runner_nik = Runner("Ник", speed=3)

    @classmethod
    def tearDownClass(cls):
        # Выводим результаты всех тестов
        for result in cls.all_results:
            print(result)

    def test_race_usain_nik(self):
        # Забег с участием Усэйна и Ника
        tournament = Tournament(90, self.runner_usain, self.runner_nik)
        results = tournament.start()
        self.__class__.all_results.append(results)
        # Проверяем, что последним пришел Ник
        self.assertTrue(results[max(results)].name == "Ник")

    def test_race_andrei_nik(self):
        # Забег с участием Андрея и Ника
        tournament = Tournament(90, self.runner_andrei, self.runner_nik)
        results = tournament.start()
        self.__class__.all_results.append(results)
        # Проверяем, что последним пришел Ник
        self.assertTrue(results[max(results)].name == "Ник")

    def test_race_usain_andrei_nik(self):
        # Забег с участием Усэйна, Андрея и Ника
        tournament = Tournament(90, self.runner_usain, self.runner_andrei, self.runner_nik)
        results = tournament.start()
        self.__class__.all_results.append(results)
        # Проверяем, что последним пришел Ник
        self.assertTrue(results[max(results)].name == "Ник")


if __name__ == "__main__":
    unittest.main()

"""
Объяснение кода
setUpClass - метод, который вызывается перед запуском всех тестов. Здесь создается атрибут all_results, 
куда будут сохраняться результаты всех тестов.

setUp - метод, создающий объекты бегунов перед каждым тестом:

Усэйн со скоростью 10,
Андрей со скоростью 9,
Ник со скоростью 3.
tearDownClass - метод, вызываемый после выполнения всех тестов. Здесь выводятся результаты всех тестов.

Методы тестирования забегов:

test_race_usain_nik — забег с участием Усэйна и Ника.
test_race_andrei_nik — забег с участием Андрея и Ника.
test_race_usain_andrei_nik — забег с участием Усэйна, Андрея и Ника.
Каждый из тестов создает объект Tournament, запускает его метод start и сохраняет результат в all_results. 
Проверка последнего участника идет через assertTrue, где ожидается, что на последнем месте будет Ник.
"""

#########   Вывод на консоль:
#
"""
Testing started at 20:18 ...

{1: <Testing_Methods__bug_fix.Runner object at 0x000002182BC38800>, 
 2: <Testing_Methods__bug_fix.Runner object at 0x000002182BC38740>}
{1: <Testing_Methods__bug_fix.Runner object at 0x000002182BC38A70>, 
 2: <Testing_Methods__bug_fix.Runner object at 0x000002182BC387D0>, 
 3: <Testing_Methods__bug_fix.Runner object at 0x000002182BC387A0>}
{1: <Testing_Methods__bug_fix.Runner object at 0x000002182BC38A40>, 
2: <Testing_Methods__bug_fix.Runner object at 0x000002182BC38560>}


Ran 3 tests in 0.004s

OK
"""