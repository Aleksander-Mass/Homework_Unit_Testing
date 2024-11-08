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

    def __repr__(self):  # Добавляем метод __repr__ для корректного отображения имени участника
        return self.name

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other
        elif isinstance(other, Runner):
            return self.name == other.name


class Tournament:
    def __init__(self, distance, *participants):
        self.full_distance = distance
        self.participants = list(participants)

    def start(self):
        finishers = {}
        place = 1
        while self.participants:
            for participant in self.participants[:]:  # Создаем копию списка участников
                participant.run()
                if participant.distance >= self.full_distance:
                    finishers[place] = participant
                    place += 1
                    self.participants.remove(participant)

        return finishers

# Напишите класс TournamentTest, наследованный от TestCase. В нём реализуйте следующие методы:
#
# setUpClass - метод, где создаётся атрибут класса all_results. Это словарь в который будут сохраняться результаты всех тестов.
# setUp - метод, где создаются 3 объекта:
class TournamentTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.all_results = []  # Словарь для хранения результатов всех тестов

    def setUp(self):
        # Создаем 3 объекта бегунов
        self.runner_usain = Runner("Усэйн", speed=10)
        self.runner_andrei = Runner("Андрей", speed=9)
        self.runner_nik = Runner("Ник", speed=3)

# tearDownClass - метод, где выводятся all_results по очереди в столбец.
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

###   Вывод на консоль:
"""
{1: Андрей, 2: Ник}
{1: Усэйн, 2: Андрей, 3: Ник}
{1: Усэйн, 2: Ник}


Ran 3 tests in 0.004s

OK
"""