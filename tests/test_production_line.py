from console_mvc.models.production import ProductionJob, ProductionLine


def test_job_create_computes_quantity_and_time():
    job = ProductionJob.create(
        order_id=1, sample_id="S1", shortfall=10, yield_rate=0.4, avg_production_time=2.0
    )

    assert job.quantity_to_produce == 25  # ceil(10 / 0.4)
    assert job.total_time == 50.0  # 2.0 * 25
    assert job.remaining_time == 50.0


def test_current_job_and_waiting_jobs():
    line = ProductionLine()
    job1 = ProductionJob.create(1, "S1", 10, 1.0, 5.0)
    job2 = ProductionJob.create(2, "S2", 4, 1.0, 3.0)
    line.enqueue(job1)
    line.enqueue(job2)

    assert line.current_job() is job1
    assert line.waiting_jobs() == [job2]


def test_tick_progresses_current_job_without_completing():
    line = ProductionLine()
    job = ProductionJob.create(1, "S1", 10, 1.0, 5.0)  # total_time = 50
    line.enqueue(job)

    completed = line.tick(20)

    assert completed == []
    assert job.remaining_time == 30
    assert line.current_job() is job


def test_tick_completes_job_exactly():
    line = ProductionLine()
    job = ProductionJob.create(1, "S1", 10, 1.0, 5.0)  # total_time = 50
    line.enqueue(job)

    completed = line.tick(50)

    assert completed == [job]
    assert job.remaining_time == 0
    assert line.current_job() is None


def test_tick_spills_over_to_next_fifo_job():
    line = ProductionLine()
    job1 = ProductionJob.create(1, "S1", 4, 1.0, 3.0)  # total_time = 12
    job2 = ProductionJob.create(2, "S2", 4, 1.0, 2.0)  # total_time = 8
    line.enqueue(job1)
    line.enqueue(job2)

    completed = line.tick(20)

    assert completed == [job1, job2]
    assert line.current_job() is None


def test_tick_does_not_start_next_job_before_current_completes():
    line = ProductionLine()
    job1 = ProductionJob.create(1, "S1", 4, 1.0, 3.0)  # total_time = 12
    job2 = ProductionJob.create(2, "S2", 4, 1.0, 2.0)  # total_time = 8
    line.enqueue(job1)
    line.enqueue(job2)

    completed = line.tick(10)

    assert completed == []
    assert job1.remaining_time == 2
    assert job2.remaining_time == 8
    assert line.current_job() is job1
