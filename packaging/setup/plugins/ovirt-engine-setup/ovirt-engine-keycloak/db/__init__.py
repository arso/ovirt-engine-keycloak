#
# ovirt-engine-setup -- ovirt engine setup
#
# Copyright oVirt Authors
# SPDX-License-Identifier: Apache-2.0
#
#

from otopi import util


from . import schema


@util.export
def createPlugins(context):
    schema.Plugin(context=context)


# vim: expandtab tabstop=4 shiftwidth=4
