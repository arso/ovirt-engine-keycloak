
# ovirt-engine-setup -- ovirt engine setup
#
# Copyright oVirt Authors
# SPDX-License-Identifier: Apache-2.0
#
#

"""Keycloak db schema plugin"""

import datetime
import gettext
import os

from otopi import plugin
from otopi import util

from ovirt_engine_setup import constants as osetupcons
from ovirt_engine_setup import util as osetuputil
from ovirt_engine_setup.engine import constants as oenginecons
from ovirt_engine_setup.engine_common import constants as oengcommcons
from ovirt_engine_setup.engine_common import database
from ovirt_engine_setup.keycloak import constants as okkcons


def _(m):
    return gettext.dgettext(message=m, domain='ovirt-engine-keycloak')


@util.export
class Plugin(plugin.PluginBase):
    """Keycloak db schema plugin"""

    def __init__(self, context):
        super(Plugin, self).__init__(context=context)

    @plugin.event(
        stage=plugin.Stages.STAGE_MISC,
        name=okkcons.Stages.KEYCLOAK_DB_SCHEMA_AVAILABLE,
        after=(
            okkcons.Stages.ENGINE_DB_CONNECTION_AVAILABLE,
        ),
        condition=lambda self: (
            self.environment[oenginecons.EngineDBEnv.NEW_DATABASE] and
            not self.environment[osetupcons.CoreEnv.DEVELOPER_MODE]
        )
    )
    def _misc(self):
        statement = database.Statement(
            dbenvkeys=oenginecons.Const.ENGINE_DB_ENV_KEYS,
            environment=self.environment,
        )

        statement.execute(
            statement="CREATE SCHEMA IF NOT EXISTS {KEYCLOAK_DB_SCHEMA} "\
                      "AUTHORIZATION {KEYCLOAK_DB_USER};".format(
                KEYCLOAK_DB_USER=self.environment[oenginecons.EngineDBEnv.USER],
                KEYCLOAK_DB_SCHEMA=okkcons.Const.KEYCLOAK_DB_SCHEMA
            ),
            ownConnection=True,
            transaction=False,
        )


# vim: expandtab tabstop=4 shiftwidth=4