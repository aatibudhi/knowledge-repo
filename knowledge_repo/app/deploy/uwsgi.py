import os
import subprocess
import logging
import shutil

logger = logging.getLogger()

class uWSGIDeployer(object):

    COMMAND = "uwsgi --http {socket} --plugin python --wsgi-file {path} --callable app --master --processes {processes} --threads {threads} --uid --gid"

    def __init__(self,
                 knowledge_flask,
                 host='0.0.0.0',
                 port=7000,
                 workers=4,
                 timeout=60):
        self.knowledge_flask = knowledge_flask
        self.options = {
            'socket': '{}:{}'.format(host, port),
            'processes': workers,
            'threads': 2,
            'timeout': timeout
        }

    def run(self):

        import tempfile
        tmp_dir = tempfile.mkdtemp()
        tmp_path = os.path.join(tmp_dir, 'server.py')

        kr_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

        repo_uri = self.knowledge_flask.repository.uri

        if isinstance(repo_uri, str):
            uris = "'{}'".format(repo_uri.replace("'", "\\'"))
        else:
            uris = str({prefix: repo_uri for prefix, repo in repo_uri.items()})

        db_uri = self.knowledge_flask.config['SQLALCHEMY_DATABASE_URI']

        db_uri = "'{}'".format(db_uri.replace("'", "\\'")) if isinstance(db_uri, str) else str(db_uri)

        config = None
        with open(tmp_path, 'w') as f:
            f.write('''
import sys
sys.path.insert(0, '{}')
import knowledge_repo
app = knowledge_repo.KnowledgeRepository.for_uri({}).get_app(db_uri={}, debug={}, config={})
        '''.format(kr_path, uris, db_uri, str(self.knowledge_flask.config['DEBUG']),
                   '"' + os.path.abspath(config) + '"' if config is not None else "None"))

        config = {}
        config.update(self.options)
        config['path'] = tmp_path
        print(config)
        try:
            # Run gunicorn server
            cmd = "cd {};" + self.COMMAND.format(**config)
            logger.info("Starting server with command:  " + " ".join(cmd))
            subprocess.check_output(cmd, shell=True)
        finally:
            shutil.rmtree(tmp_dir)