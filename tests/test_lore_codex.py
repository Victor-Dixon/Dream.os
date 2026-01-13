import unittest
import yaml
import json
import os
from pathlib import Path
import jsonschema

class TestLoreCodex(unittest.TestCase):
    def setUp(self):
        self.lore_root = Path("lore")
        self.schema_root = self.lore_root / "schema"
        
    def load_yaml(self, path):
        with open(path, "r") as f:
            return yaml.safe_load(f)
            
    def load_json(self, path):
        with open(path, "r") as f:
            return json.load(f)

    def test_codex_validates_against_schema(self):
        """Truthkeeper: Codex must validate against schema."""
        codex = self.load_yaml(self.lore_root / "codex.yaml")
        schema = self.load_json(self.schema_root / "lore_schema.json")
        
        try:
            jsonschema.validate(instance=codex['digital_dreamscape_lore_codex'], schema=schema)
        except jsonschema.exceptions.ValidationError as e:
            self.fail(f"Codex validation failed: {e}")

    def test_voice_styleguide_integrity(self):
        """Truthkeeper: All voices in Codex must exist in Styleguide."""
        codex = self.load_yaml(self.lore_root / "codex.yaml")
        styleguide = self.load_yaml(self.lore_root / "voices/styleguide.yaml")
        
        codex_voices = set()
        
        # Collect voices from agents
        agents_data = codex['digital_dreamscape_lore_codex']['agents']
        for group in agents_data.values():
            if isinstance(group, list):
                for agent in group:
                    if 'voice_profile' in agent:
                        codex_voices.add(agent['voice_profile'])
                        
        # Collect voices from portals
        portals_data = codex['digital_dreamscape_lore_codex']['portals']
        for portal in portals_data.values():
            if 'voice_profile' in portal:
                codex_voices.add(portal['voice_profile'])
                
        # Access strictly under 'styleguide' -> 'profiles'
        styleguide_voices = set(styleguide['styleguide']['profiles'].keys())
        
        missing_voices = codex_voices - styleguide_voices
        self.assertEqual(len(missing_voices), 0, f"Voices defined in Codex but missing in Styleguide: {missing_voices}")

if __name__ == "__main__":
    unittest.main()
