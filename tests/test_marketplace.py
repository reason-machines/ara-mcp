"""Exercise the published package through the actual Codex installer."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class MarketplaceInstallation(unittest.TestCase):
    def test_clean_install(self):
        self.install(with_legacy=False)

    def test_install_alongside_retired_marketplace(self):
        self.install(with_legacy=True)

    def install(self, with_legacy):
        if not shutil.which('codex'):
            self.fail('The Codex CLI is required for installation tests')
        with tempfile.TemporaryDirectory(prefix='reason-plugin-test-') as directory:
            temp = Path(directory)
            client = temp / 'client'
            client.mkdir()
            env = dict(os.environ, CODEX_HOME=str(client))

            def codex(*args):
                result = subprocess.run(['codex', 'plugin', *args], env=env,
                                        text=True, capture_output=True, timeout=60)
                self.assertEqual(result.returncode, 0, result.stderr)
                return result.stdout

            if with_legacy:
                legacy = temp / 'legacy' / '.agents' / 'plugins'
                legacy.mkdir(parents=True)
                (legacy / 'marketplace.json').write_text(json.dumps({
                    'name': 'ara', 'plugins': []
                }))
                codex('marketplace', 'add', str(temp / 'legacy'))
            codex('marketplace', 'add', str(ROOT))
            codex('add', 'reason@reason')
            listing = codex('list')
            self.assertIn('reason@reason', listing)
            self.assertIn('installed, enabled', listing)
            cached = list((client / 'plugins' / 'cache').rglob('.mcp.json'))
            self.assertEqual(len(cached), 1)
            self.assertEqual(json.loads(cached[0].read_text()), {
                'mcpServers': {'reason': {
                    'type': 'http', 'url': 'https://mcp.reasonmachines.com/mcp'
                }}
            })
            self.assertTrue((cached[0].parent / 'skills/reason/SKILL.md').is_file())
            plugin = json.loads((cached[0].parent / '.codex-plugin/plugin.json').read_text())
            portable = json.loads((cached[0].parent / 'plugin.json').read_text())
            self.assertEqual(portable['$schema'],
                             'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json')
            self.assertEqual(portable['name'], 'reason')
            self.assertEqual(portable['version'], '1.1.1')
            self.assertEqual(portable['version'], plugin['version'])
            interface = portable['extensions']['com.openai']['interface']
            self.assertEqual(interface, plugin['interface'])
            self.assertEqual(interface['displayName'], 'Reason')
            self.assertEqual(interface['shortDescription'], 'Cloud coding across machines')
            self.assertLessEqual(len(interface['shortDescription']), 30)
            for key in ['websiteURL', 'supportURL', 'privacyPolicyURL', 'termsOfServiceURL']:
                self.assertTrue(interface[key].startswith('https://'), key)
            self.assertEqual(json.loads((cached[0].parent / 'mcp.json').read_text()), {
                '$schema': 'https://agent-plugins.org/schemas/1.0.0/mcp.schema.json',
                'mcpServers': {'reason': {
                    'type': 'streamable-http', 'url': 'https://mcp.reasonmachines.com/mcp'
                }}
            })
            for key in ['composerIcon', 'logo', 'logoDark']:
                icon = cached[0].parent / plugin['interface'][key]
                self.assertEqual(icon.read_bytes()[:8], b'\x89PNG\r\n\x1a\n')
            self.assertTrue((cached[0].parent / 'skills/reason/agents/openai.yaml').is_file())

            for path in ['.agents/plugins/marketplace.json', '.claude-plugin/marketplace.json']:
                manifest = json.loads((ROOT / path).read_text())
                self.assertEqual(manifest['name'], 'reason')
                self.assertEqual([p['name'] for p in manifest['plugins']], ['reason'])
            self.assertEqual(sorted(p.name for p in (ROOT / 'plugins').iterdir()), ['reason'])


if __name__ == '__main__':
    unittest.main()
