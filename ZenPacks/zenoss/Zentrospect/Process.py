#######################################################################
#
# Copyright (C) 2013, Chet Luther <chet.luther@gmail.com>
#
# Licensed under GNU General Public License 3.0 or later.
# Some rights reserved. See COPYING, AUTHORS.
#
#######################################################################

from zope.component import adapts
from zope.interface import implements

from Products.ZenRelations.RelSchema import ToOne, ToManyCont
from Products.Zuul.decorators import info
from Products.Zuul.form import schema
from Products.Zuul.infos import ProxyProperty
from Products.Zuul.infos.component import ComponentInfo
from Products.Zuul.interfaces.component import IComponentInfo
from Products.Zuul.utils import ZuulMessageFactory as _t

from ZenPacks.zenoss.Zentrospect import MODULE_NAME
from ZenPacks.zenoss.Zentrospect.Component import Component


class Process(Component):
    '''
    Model class for Process.
    '''

    meta_type = portal_type = 'ZentrospectProcess'

    process_name = None

    _properties = Component._properties + (
        {'id': 'process_name', 'type': 'string', 'mode': 'w'},
        )

    _relations = Component._relations + (
        ('system', ToOne(ToManyCont, MODULE_NAME['System'], 'processes')),
        ('metrics', ToManyCont(ToOne, MODULE_NAME['Metric'], 'process')),
        )


class IProcessInfo(IComponentInfo):
    '''
    API Info interface for Process.
    '''

    title = schema.TextLine(title=_t(u'Title'))
    process_name = schema.TextLine(title=_t(u'Process Name'))
    system = schema.Entity(title=_t(u'System'))
    metric_count = schema.Int(title=_t(u'Number of Metrics'))


class ProcessInfo(ComponentInfo):
    '''
    API Info adapter factory for Process.
    '''

    implements(IProcessInfo)
    adapts(Process)

    title = ProxyProperty('title')
    process_name = ProxyProperty('process_name')

    @property
    @info
    def system(self):
        return self._object.system()

    @property
    @info
    def metric_count(self):
        return self._object.metrics.countObjects()
