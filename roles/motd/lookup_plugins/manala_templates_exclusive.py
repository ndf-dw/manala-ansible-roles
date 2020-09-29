from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.plugins.lookup import LookupBase
from ansible.errors import AnsibleError
from ansible.module_utils._text import to_text

import os


class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):

        results = []

        wantstate = kwargs.pop('wantstate', None)

        if wantstate and wantstate not in ['present', 'absent']:
            raise AnsibleError('Expect a wanstate of "present" or "absent" but was "%s"' % to_text(wantstate))

        templates = self._flatten(terms[0])
        exclusives = self._flatten(terms[1])
        dir = terms[2]
        template = terms[3]

        itemDefault = {
            'state': 'present',
            'template': template
        }

        # Mark exclusive templates as absent
        for template in exclusives:
            item = itemDefault.copy()
            item.update({
                'file': template['path'],
                'state': 'absent'
            })
            results.append(item)

        for template in templates:

            items = []

            # Must be a dict
            if not isinstance(template, dict):
                raise AnsibleError('Expect a dict but was a %s' % type(template))

            # Check file key
            if 'file' not in template:
                raise AnsibleError('Expect a "file" key')

            item = itemDefault.copy()
            item.update(template)

            if item['state'] not in ['present', 'absent', 'ignore']:
                raise AnsibleError('Expect a state of "present", "absent" or "ignore" but was "%s"' % to_text(item['state']))

            if item['state'] == 'ignore':
                continue

            item.update({
                'file': os.path.join(dir, item['file'])
            })

            items.append(item)

            # Merge by file key
            for item in items:
                itemFound = False
                for i, result in enumerate(results):
                    if result['file'] == item['file']:
                        results[i] = item
                        itemFound = True
                        break

                if not itemFound:
                    results.append(item)

        # Filter by state
        if wantstate:
            results = [result for result in results if result.get('state') == wantstate]

        return results
