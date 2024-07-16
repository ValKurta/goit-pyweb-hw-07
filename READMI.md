Docker:
    docker-compose up -d
it was modified for the reason that was impossible to connect by default with login 'postgres'

Alembic steps:
    alembic init alembic  
    alembic revision --autogenerate -m "Initial migration"
    alembic upgrade head
As alternative main.py doing the same in comparison with alembic migrations

The scripts:
    seed.py - the data population in the BD
    my_select.py - the all queries as functions. they will be processed from the one script
    cli.py - the extra task. I am not sure if everything works fine
    database.py - has sync and async sessions(tried to cover more variants)
