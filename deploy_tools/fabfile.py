from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

REPO_URL = 'https://github.com/mstibbard/golf-club-manager.git'


def deploy():
    site_folder = f'/home/{env.user}/sites/{env.host}'
    log_folder = f'/home/{env.user}/logs'
    source_folder = site_folder + '/source'
    _create_directory_structure_if_necessary(site_folder, log_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)
    print(f'''
        Fabfile complete.
        Repo: {REPO_URL}
        Environment: {site_folder}
    ''')


def deploy_test():
    source_folder = f'/home/{env.user}/sites/{env.host}/source'
    check_test_env = str(env.host)
    print(f'\nDEPLOYING FIXTURES TO: {env.host}')

    # Validate this is being done against a test environment
    if check_test_env.find('test') == -1:
        print('''\n
            *** OPERATION CANCELLED ***
            Attempting to deploy to env
            which is not test.
            ***************************\n
        ''')
    else:
        print("Proceeding. Environment includes 'test' in name\n")

        run(
            f'cd {source_folder} && '
            'rm ../database/db.sqlite3 && '
            '../virtualenv/bin/python manage.py migrate --noinput && '
            '../virtualenv/bin/python manage.py loaddata test_games.json '
            'test_gametypes.json test_grade.json test_players.json test_user.json'
        )


def _create_directory_structure_if_necessary(site_folder, log_folder):
    run(f'mkdir -p {log_folder}')
    for subfolder in (
        'database', 'virtualenv', 'source', 'static'
    ):
        run(f'mkdir -p {site_folder}/{subfolder}')


def _get_latest_source(source_folder):
    if exists(source_folder + '/.git'):
        run(f'cd {source_folder} && git fetch')
    else:
        run(f'git clone {REPO_URL} {source_folder}')
    current_commit = local(
        "git log -n 1 --format=%H", capture=True)
    run(f'cd {source_folder} && git reset --hard {current_commit}')


def _update_settings(source_folder, site_name):
    settings_path = source_folder + '/golf_club_manager/settings.py'
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    sed(
        settings_path,
        'ALLOWED_HOSTS =.+$',
        f'ALLOWED_HOSTS = ["{site_name}"]'
    )
    secret_key_file = source_folder + '/golf_club_manager/secret_key.py'
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, f'SECRET_KEY = "{key}"')
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')

def _update_virtualenv(source_folder):
    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder + '/bin/pip'):
        run(f'python3.6 -m venv {virtualenv_folder}')
    run(
        f'{virtualenv_folder}/bin/pip install -r '
        f'{source_folder}/requirements.txt'
    )


def _update_static_files(source_folder):
    run(
        f'cd {source_folder} && '
        '../virtualenv/bin/python manage.py collectstatic --noinput'
    )


def _update_database(source_folder):
    run(
        f'cd {source_folder} && '
        '../virtualenv/bin/python manage.py migrate --noinput'
    )
