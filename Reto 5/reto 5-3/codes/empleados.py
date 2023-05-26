from mrjob.job import MRJob


class SalarioSE(MRJob):
    def mapper(self, _, line):
        empleado, sector, salario, anio = line.split(",")
        if empleado != "idemp":
            yield sector, float(salario)

    def reducer(self, sector, salarios):
        salarios = list(salarios)
        yield sector, sum(salarios) / len(salarios)


class SalariosEM(MRJob):
    def mapper(self, _, line):
        empleado, sector, salario, anio = line.split(",")
        if empleado != "idemp":
            yield empleado, float(salario)

    def reducer(self, empleado, salarios):
        salarios = list(salarios)
        yield empleado, sum(salarios) / len(salarios)


class SectorEM(MRJob):
    def mapper(self, _, line):
        empleado, sector, salario, anio = line.split(",")
        if empleado != "idemp":
            yield empleado, sector

    def reducer(self, empleado, sectores):
        yield empleado, len(set(sectores))


if __name__ == "__main__":
    jobs = [
        ("Salarios por sector", SalarioSE),
        ("Salarios por empleado", SalariosEM),
        ("Sectores por empleado", SectorEM)
    ]

    for job_name, job_class in jobs:
        print(f">>>>>>>>>> {job_name}")
        job = job_class()
        with job.make_runner() as runner:
            runner.run()
            for key, value in job.parse_output(runner.cat_output()):
                print(f"{key}: {value}")
