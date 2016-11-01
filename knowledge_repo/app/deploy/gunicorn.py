""" gunicorn.py

    Utilities for running the knowledge app via gunicorn.

    Adapted from example in http://docs.gunicorn.org/en/stable/custom.html.
"""

from __future__ import absolute_import

from gunicorn.app.base import BaseApplication

class GunicornDeployer(BaseApplication):

    def __init__(self,
                 knowledge_flask,
                 host='0.0.0.0',
                 port=7000,
                 workers=4,
                 timeout=60):
        self.knowledge_flask = knowledge_flask
        self.options = {
            'bind': '{}:{}'.format(host, port),
            'workers': workers,
            'timeout': timeout
        }
        BaseApplication.__init__(self)

    def load_config(self):
        for key, value in self.options.items():
            self.cfg.set(key, value)

    def load(self):
        return self.knowledge_flask

# class GunicornKnowledgeApplication(BaseApplication):
#     def __init__(self, repo_uris, db_uri, debug, config, repos, options=None):
#         self.repo_uris = repo_uris
#         self.db_uri = db_uri
#         self.debug = debug
#         self.config = config
#         self.repos = repos
#         self.options = options or {}
#
#         super(GunicornKnowledgeApplication, self).__init__()
#
#     def load_config(self):
#         config = dict([(key, value) for key, value in self.options.iteritems()
#                        if key in self.cfg.settings and value is not None])
#         for key, value in config.iteritems():
#             self.cfg.set(key.lower(), value)
#
#     def load(self):
#         # Create app here as opposed to earlier (e.g., in contructor) so that this process is
#         # done post-fork. Doing it pre-fork seems to cause issues.
#         return knowledge_repo.KnowledgeRepository.for_uri(self.repo_uris).get_app(
#             db_uri=self.db_uri, debug=self.debug, config=self.config, REPOS=self.repos)
#
#     @classmethod
#     def create_app(cls, ip, port, num_workers, timeout, repo_uris, db_uri, debug, config, repos):
#         options = {
#             'bind': '%s:%s' % (ip, port),
#             'workers': num_workers,
#             'timeout': timeout,
#         }
#
#         return cls(repo_uris, db_uri, debug, config, repos, options)
