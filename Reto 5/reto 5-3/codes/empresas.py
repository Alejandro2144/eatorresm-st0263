from mrjob.job import MRJob


class DiaMinMax(MRJob):
    def mapper(self, _, line):
        company, price, date = line.split(",")
        if company != "Company":
            yield company, (float(price), date)

    def reducer(self, company, data):
        prices_dates = list(data)
        lowest_price = min(prices_dates, key=lambda x: x[0])[1]
        highest_price = max(prices_dates, key=lambda x: x[0])[1]
        yield company, [lowest_price, highest_price]


class AccionCreciente(MRJob):
    def mapper(self, _, line):
        company, price, date = line.split(",")
        if company != "Company":
            yield company, (float(price), date)

    def reducer(self, company, data):
        prices_dates = list(data)
        sorted_dates = sorted(prices_dates, key=lambda x: x[1])
        initial_price = sorted_dates[0][0]
        new_stonks = [date for price, date in sorted_dates[1:] if price >= initial_price]
        if new_stonks:
            yield company, "Acciones crecientes o estables"


class BlackFriday(MRJob):
    def mapper(self, _, line):
        company, price, date = line.split(",")
        if company != "Company":
            yield None, (float(price), date)

    def reducer(self, _, data):
        sums = {}
        for price, date in data:
            if date not in sums:
                sums[date] = 0
            sums[date] += price
        key, value = min(sums.items(), key=lambda x: x[1])
        yield key, value


if __name__ == "__main__":
    jobs = [
        ("Dia con valor mínimo y máximo para cada empresa", DiaMinMax),
        ("Empresas con acciones iguales o mayores", AccionCreciente),
        ("Dia con precios más bajos", BlackFriday)
    ]

    for job_name, job_class in jobs:
        print(f">>>>>>>>>> {job_name}")
        job = job_class()
        with job.make_runner() as runner:
            runner.run()
            for key, value in job.parse_output(runner.cat_output()):
                print(f"{key}: {value}")
